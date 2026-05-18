"""
Módulo de integração com a API pública do Banco Central do Brasil (BCB).

Documentação: https://dadosabertos.bcb.gov.br/

APIs utilizadas (ambas gratuitas, sem necessidade de chave):

  - Série 1619: Salário mínimo (R$) — valor mensal vigente
    https://api.bcb.gov.br/dados/serie/bcdata.sgs.1619/dados/ultimos/1?formato=json

  - Série 433: IPCA mensal (%) — índice oficial de inflação
    https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/12?formato=json

Funcionalidade adicionada nesta Etapa Intermediária:
  Antes, o usuário precisava digitar o salário mínimo manualmente. Agora a
  aplicação busca o valor oficial atualizado direto do Banco Central, e exibe
  também a inflação acumulada nos últimos 12 meses para contextualizar o
  poder de compra da cesta.
"""
import requests

URL_SALARIO_MINIMO = (
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1619/dados/ultimos/1"
    "?formato=json"
)
URL_IPCA_12_MESES = (
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/12"
    "?formato=json"
)

TIMEOUT = 10  # segundos


class ApiBcbError(Exception):
    """Lançada quando a API do Banco Central falha ou retorna dados inválidos."""


def buscar_salario_minimo_atual():
    """
    Consulta a API do BCB e retorna o salário mínimo vigente em reais.

    Retorna:
        dict com as chaves:
          - valor (float): valor do salário mínimo em R$
          - data (str): data de referência (formato dd/mm/aaaa)

    Lança:
        ApiBcbError: se a API falhar, demorar muito ou retornar dados inválidos.
    """
    try:
        resp = requests.get(URL_SALARIO_MINIMO, timeout=TIMEOUT)
    except requests.Timeout as e:
        raise ApiBcbError("Tempo de resposta do BCB excedido.") from e
    except requests.RequestException as e:
        raise ApiBcbError(f"Falha de conexão com o BCB: {e}") from e

    if resp.status_code != 200:
        raise ApiBcbError(
            f"BCB retornou status HTTP {resp.status_code}."
        )

    try:
        dados = resp.json()
    except ValueError as e:
        raise ApiBcbError("Resposta do BCB não é um JSON válido.") from e

    if not dados or not isinstance(dados, list):
        raise ApiBcbError("Resposta do BCB está vazia ou em formato inesperado.")

    registro = dados[-1]  # último valor publicado

    try:
        valor = float(registro["valor"])
        data = registro["data"]
    except (KeyError, TypeError, ValueError) as e:
        raise ApiBcbError("Resposta do BCB não contém os campos esperados.") from e

    return {"valor": valor, "data": data}


def buscar_inflacao_12_meses():
    """
    Consulta a API do BCB e retorna a inflação acumulada nos últimos 12 meses.

    A série 433 do BCB retorna o IPCA mensal. Somamos os 12 últimos meses
    para obter o acumulado (aproximação simples; o cálculo oficial usa
    composição multiplicativa, que também é fornecida aqui).

    Retorna:
        dict com as chaves:
          - acumulado_pct (float): inflação acumulada nos últimos 12 meses (%)
          - meses (int): quantos meses foram considerados
          - mes_mais_recente (str): mês de referência mais recente

    Lança:
        ApiBcbError: se a API falhar.
    """
    try:
        resp = requests.get(URL_IPCA_12_MESES, timeout=TIMEOUT)
    except requests.Timeout as e:
        raise ApiBcbError("Tempo de resposta do BCB excedido.") from e
    except requests.RequestException as e:
        raise ApiBcbError(f"Falha de conexão com o BCB: {e}") from e

    if resp.status_code != 200:
        raise ApiBcbError(f"BCB retornou status HTTP {resp.status_code}.")

    try:
        dados = resp.json()
    except ValueError as e:
        raise ApiBcbError("Resposta do BCB não é um JSON válido.") from e

    if not dados or not isinstance(dados, list):
        raise ApiBcbError("Resposta do BCB está vazia ou em formato inesperado.")

    # Cálculo composto: (1+i1)*(1+i2)*...*(1+i12) - 1
    fator = 1.0
    for registro in dados:
        try:
            ipca_mes = float(registro["valor"]) / 100.0
        except (KeyError, TypeError, ValueError) as e:
            raise ApiBcbError("Registro de IPCA inválido na resposta.") from e
        fator *= (1.0 + ipca_mes)

    acumulado_pct = round((fator - 1.0) * 100.0, 2)

    return {
        "acumulado_pct": acumulado_pct,
        "meses": len(dados),
        "mes_mais_recente": dados[-1].get("data", ""),
    }


def formatar_dados_bcb(salario, inflacao):
    """
    Formata para exibição na CLI as informações trazidas do BCB.

    Recebe os dicts retornados por buscar_salario_minimo_atual() e
    buscar_inflacao_12_meses() e devolve uma string pronta para print.
    """
    linhas = [
        "=======================================================",
        "  DADOS OFICIAIS — Banco Central do Brasil",
        "=======================================================",
        f"  Salário mínimo vigente:   R$ {salario['valor']:.2f}",
        f"  Data de referência:       {salario['data']}",
        f"  IPCA acumulado (12 m):    {inflacao['acumulado_pct']}%",
        f"  Mês mais recente do IPCA: {inflacao['mes_mais_recente']}",
        "-------------------------------------------------------",
    ]
    return "\n".join(linhas)
