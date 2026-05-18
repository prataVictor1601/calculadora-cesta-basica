"""
Testes de INTEGRAÇÃO com a API pública do Banco Central do Brasil.

Diferente dos testes unitários (que validam funções isoladas), os testes
de integração validam o fluxo completo de comunicação com o serviço externo:
montagem da requisição HTTP → recebimento da resposta → parsing do JSON →
retorno no formato esperado pela aplicação.

Usamos a biblioteca `responses` para INTERCEPTAR as chamadas HTTP reais e
simular as respostas do BCB. Isso garante que os testes sejam:
  - Reprodutíveis (não dependem da disponibilidade real do BCB)
  - Rápidos (rodam em milissegundos)
  - Determinísticos (mesma resposta a cada execução)
  - Capazes de testar cenários de erro que seriam difíceis de reproduzir
    com chamadas reais (ex.: API fora do ar, JSON malformado, timeout)
"""
import pytest
import requests
import responses

from src.api_bcb import (
    buscar_salario_minimo_atual,
    buscar_inflacao_12_meses,
    formatar_dados_bcb,
    ApiBcbError,
    URL_SALARIO_MINIMO,
    URL_IPCA_12_MESES,
)


# =====================================================================
# Integração: salário mínimo (série 1619 do BCB)
# =====================================================================

class TestIntegracaoSalarioMinimo:

    @responses.activate
    def test_busca_salario_minimo_caminho_feliz(self):
        """Fluxo feliz: BCB retorna 200 com o valor — função devolve dict."""
        responses.add(
            responses.GET,
            URL_SALARIO_MINIMO,
            json=[{"data": "01/05/2025", "valor": "1518.00"}],
            status=200,
        )

        resultado = buscar_salario_minimo_atual()

        assert resultado["valor"] == 1518.00
        assert resultado["data"] == "01/05/2025"

    @responses.activate
    def test_bcb_retorna_500_lanca_erro_tratado(self):
        """Se o BCB cair, a aplicação lança ApiBcbError em vez de quebrar."""
        responses.add(
            responses.GET,
            URL_SALARIO_MINIMO,
            status=500,
        )

        with pytest.raises(ApiBcbError, match="status HTTP 500"):
            buscar_salario_minimo_atual()

    @responses.activate
    def test_bcb_retorna_json_invalido(self):
        """Resposta não-JSON deve lançar ApiBcbError."""
        responses.add(
            responses.GET,
            URL_SALARIO_MINIMO,
            body="isto não é json",
            status=200,
            content_type="text/html",
        )

        with pytest.raises(ApiBcbError, match="JSON válido"):
            buscar_salario_minimo_atual()

    @responses.activate
    def test_bcb_retorna_lista_vazia(self):
        """Lista vazia da API deve lançar ApiBcbError."""
        responses.add(
            responses.GET,
            URL_SALARIO_MINIMO,
            json=[],
            status=200,
        )

        with pytest.raises(ApiBcbError, match="vazia ou em formato inesperado"):
            buscar_salario_minimo_atual()

    @responses.activate
    def test_bcb_retorna_estrutura_inesperada(self):
        """Resposta sem o campo 'valor' deve lançar ApiBcbError."""
        responses.add(
            responses.GET,
            URL_SALARIO_MINIMO,
            json=[{"campo_errado": "abc"}],
            status=200,
        )

        with pytest.raises(ApiBcbError, match="campos esperados"):
            buscar_salario_minimo_atual()

    @responses.activate
    def test_falha_de_conexao_lanca_erro(self):
        """Erros de rede (ConnectionError) viram ApiBcbError."""
        responses.add(
            responses.GET,
            URL_SALARIO_MINIMO,
            body=requests.ConnectionError("rede offline"),
        )

        with pytest.raises(ApiBcbError, match="conexão"):
            buscar_salario_minimo_atual()


# =====================================================================
# Integração: IPCA acumulado 12 meses (série 433 do BCB)
# =====================================================================

class TestIntegracaoIpca:

    @responses.activate
    def test_busca_ipca_caminho_feliz(self):
        """Soma composta de 12 meses de IPCA -> acumulado."""
        # 12 meses de 0,4% -> aprox 4,907%
        registros = [
            {"data": f"{m:02d}/01/2025", "valor": "0.40"} for m in range(1, 13)
        ]
        responses.add(
            responses.GET,
            URL_IPCA_12_MESES,
            json=registros,
            status=200,
        )

        resultado = buscar_inflacao_12_meses()

        assert resultado["meses"] == 12
        # (1.004)^12 - 1 = 0.04907... ou seja, 4.91%
        assert resultado["acumulado_pct"] == pytest.approx(4.91, abs=0.05)
        assert resultado["mes_mais_recente"] == "12/01/2025"

    @responses.activate
    def test_ipca_com_meses_negativos(self):
        """IPCA pode ter deflação (valores negativos). Deve calcular OK."""
        registros = [
            {"data": "01/01/2025", "valor": "0.50"},
            {"data": "02/01/2025", "valor": "-0.30"},
            {"data": "03/01/2025", "valor": "0.20"},
        ]
        responses.add(
            responses.GET,
            URL_IPCA_12_MESES,
            json=registros,
            status=200,
        )

        resultado = buscar_inflacao_12_meses()

        assert resultado["meses"] == 3
        # (1.005)(0.997)(1.002) - 1 ≈ 0.00399 -> 0.40%
        assert resultado["acumulado_pct"] == pytest.approx(0.40, abs=0.05)

    @responses.activate
    def test_ipca_servidor_indisponivel(self):
        responses.add(
            responses.GET,
            URL_IPCA_12_MESES,
            status=503,
        )

        with pytest.raises(ApiBcbError):
            buscar_inflacao_12_meses()


# =====================================================================
# Integração: formatação dos dados (fluxo completo)
# =====================================================================

class TestFluxoCompleto:

    @responses.activate
    def test_dados_formatados_para_exibir_na_cli(self):
        """
        Teste de integração completo: simula as duas chamadas (salário + IPCA)
        e valida que o output final formatado contém as informações esperadas.
        """
        responses.add(
            responses.GET,
            URL_SALARIO_MINIMO,
            json=[{"data": "01/05/2025", "valor": "1518.00"}],
            status=200,
        )
        responses.add(
            responses.GET,
            URL_IPCA_12_MESES,
            json=[{"data": f"{m:02d}/01/2025", "valor": "0.40"} for m in range(1, 13)],
            status=200,
        )

        salario = buscar_salario_minimo_atual()
        ipca = buscar_inflacao_12_meses()
        texto = formatar_dados_bcb(salario, ipca)

        assert "1518.00" in texto
        assert "01/05/2025" in texto
        assert "Banco Central" in texto
        # acumulado de 12 meses ~4.91%
        assert "4.9" in texto or "4.91" in texto
