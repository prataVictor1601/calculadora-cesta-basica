"""
Calculadora de Cesta Básica vs. Salário Mínimo.

Etapa Intermediária do BootCamp:
  - Mantém toda a lógica original da Etapa 1 (entrada de 15 itens,
    cálculo de percentual, faixas de risco e sugestões de economia).
  - ADICIONA integração com a API pública do Banco Central do Brasil:
      * busca automática do salário mínimo vigente (série 1619)
      * busca da inflação acumulada nos últimos 12 meses (série 433)
  - O usuário pode optar por usar o salário oficial (vindo da API) ou
    digitar um valor personalizado, mantendo a aplicação funcional
    mesmo se a API estiver fora do ar.
"""
from src.api_bcb import (
    buscar_salario_minimo_atual,
    buscar_inflacao_12_meses,
    formatar_dados_bcb,
    ApiBcbError,
)


# Itens da cesta básica (preços de referência apenas como sugestão)
ITENS_CESTA = [
    "Arroz (5kg)",
    "Feijão (1kg)",
    "Óleo de soja (900ml)",
    "Açúcar (1kg)",
    "Sal (1kg)",
    "Café (500g)",
    "Leite (1L)",
    "Pão francês (1kg)",
    "Manteiga (200g)",
    "Carne bovina (1kg)",
    "Frango (1kg)",
    "Ovos (1 dúzia)",
    "Banana (1kg)",
    "Tomate (1kg)",
    "Batata (1kg)",
]


def calcular_percentual(valor_cesta, salario_minimo):
    """Calcula a porcentagem do salário comprometida pela cesta básica."""
    if salario_minimo <= 0:
        raise ValueError("O salário mínimo deve ser maior que zero.")
    if valor_cesta < 0:
        raise ValueError("O valor da cesta não pode ser negativo.")

    percentual = (valor_cesta / salario_minimo) * 100
    return round(percentual, 2)


def classificar_risco(percentual):
    """Classifica o percentual em faixas de risco."""
    if percentual <= 20:
        return ("🟢", "OK", "Excelente! O custo está bem controlado.")
    if percentual <= 30:
        return ("🟡", "ATENÇÃO", "O custo está no limite recomendado de 30%.")
    return ("🔴", "CRÍTICO", "O custo ultrapassou 30% do salário — risco alto.")


def gerar_sugestoes(itens, salario_minimo, limite_percentual=30):
    """Gera sugestões dos itens mais caros para reduzir."""
    valor_total = sum(itens.values())
    if calcular_percentual(valor_total, salario_minimo) <= limite_percentual:
        return []

    # Ordena os itens do mais caro para o mais barato
    ordenados = sorted(itens.items(), key=lambda x: x[1], reverse=True)
    sugestoes = []
    for nome, preco in ordenados[:3]:
        if preco > 0:
            sugestoes.append(
                f"Considere reduzir o gasto com '{nome}' (R$ {preco:.2f}). "
                "Procure marcas mais baratas ou compre em maior quantidade."
            )
    return sugestoes


def coletar_precos():
    """Solicita ao usuário os preços de cada item da cesta."""
    print("\nInsira o preço de cada item da cesta básica.")
    print("(Digite 0 para itens que não deseja incluir)")
    print("-" * 55)

    itens = {}
    for nome in ITENS_CESTA:
        while True:
            try:
                entrada = input(f"  {nome}: R$ ").strip().replace(",", ".")
                preco = float(entrada)
                if preco < 0:
                    print("  ⚠ Valor não pode ser negativo. Tente novamente.")
                    continue
                itens[nome] = preco
                break
            except ValueError:
                print("  ⚠ Valor inválido. Digite um número.")
    return itens


def obter_salario(usar_api=True):
    """
    Obtém o salário mínimo. Tenta primeiro a API do BCB; se falhar
    (ou se o usuário recusar), pede o valor manualmente.

    Retorna uma tupla: (salario_float, fonte_str).
    """
    if usar_api:
        try:
            print("\n🌐 Consultando salário mínimo oficial no Banco Central...")
            dados = buscar_salario_minimo_atual()
            print(
                f"✓ Salário mínimo vigente: R$ {dados['valor']:.2f} "
                f"(referência: {dados['data']})"
            )
            usar = input("Usar este valor? [S/n] ").strip().lower()
            if usar in ("", "s", "sim", "y", "yes"):
                return dados["valor"], f"BCB ({dados['data']})"
        except ApiBcbError as e:
            print(f"⚠ Não foi possível consultar o BCB: {e}")
            print("  Você pode informar o salário manualmente.")

    # Fallback: usuário digita
    while True:
        try:
            entrada = input(
                "Digite o valor do salário mínimo (R$): "
            ).strip().replace(",", ".")
            valor = float(entrada)
            if valor <= 0:
                print("  ⚠ O salário deve ser maior que zero.")
                continue
            return valor, "informado pelo usuário"
        except ValueError:
            print("  ⚠ Valor inválido. Digite um número.")


def main():
    """Ponto de entrada da CLI."""
    print("=" * 55)
    print("  CALCULADORA DE CESTA BÁSICA vs. SALÁRIO MÍNIMO")
    print("=" * 55)

    # Tenta exibir o "boletim" do BCB no início (informativo)
    try:
        salario_info = buscar_salario_minimo_atual()
        ipca_info = buscar_inflacao_12_meses()
        print()
        print(formatar_dados_bcb(salario_info, ipca_info))
    except ApiBcbError as e:
        print(f"\n⚠ Não foi possível buscar dados do BCB: {e}")
        print("  A aplicação continuará funcionando normalmente.")

    # 1) Salário
    salario, fonte = obter_salario(usar_api=True)

    # 2) Preços dos itens
    itens = coletar_precos()
    valor_total = sum(itens.values())

    # 3) Cálculo e exibição
    percentual = calcular_percentual(valor_total, salario)
    emoji, status, mensagem = classificar_risco(percentual)

    print("\n" + "=" * 55)
    print("  RESULTADO")
    print("=" * 55)
    print(f"  Valor total da cesta:   R$ {valor_total:.2f}")
    print(f"  Salário mínimo:         R$ {salario:.2f}  ({fonte})")
    print(f"  Comprometimento:        {percentual}%")
    print("-" * 55)
    print(f"  {emoji} {status}: {mensagem}")

    # 4) Sugestões
    sugestoes = gerar_sugestoes(itens, salario)
    if sugestoes:
        print("\n  💡 Sugestões para reduzir o gasto:")
        for s in sugestoes:
            print(f"     • {s}")

    print("=" * 55)


if __name__ == "__main__":
    main()
