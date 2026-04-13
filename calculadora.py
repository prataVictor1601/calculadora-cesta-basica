"""
Calculadora de Cesta Básica vs. Salário Mínimo.

Permite ao usuário calcular quanto da renda é comprometido
com a cesta básica e receber sugestões de ajuste.
"""

ITENS_CESTA = [
    "Arroz (5kg)",
    "Feijão (1kg)",
    "Óleo de soja (900ml)",
    "Açúcar (5kg)",
    "Leite (1L)",
    "Café (500g)",
    "Farinha de trigo (1kg)",
    "Macarrão (500g)",
    "Pão francês (1kg)",
    "Carne bovina (1kg)",
    "Frango (1kg)",
    "Ovos (dúzia)",
    "Banana (dúzia)",
    "Tomate (1kg)",
    "Manteiga (200g)",
]


def calcular_percentual(valor_cesta, salario_minimo):
    """Calcula o percentual do salário consumido pela cesta."""
    if salario_minimo <= 0:
        raise ValueError("O salário mínimo deve ser maior que zero.")
    if valor_cesta < 0:
        raise ValueError("O valor da cesta não pode ser negativo.")

    percentual = (valor_cesta / salario_minimo) * 100
    return round(percentual, 2)


def gerar_sugestoes(itens_precos, salario_minimo, limite_percentual=30):
    """Gera sugestões de corte caso a cesta ultrapasse o limite."""
    valor_total = sum(itens_precos.values())
    percentual = calcular_percentual(valor_total, salario_minimo)

    if percentual <= limite_percentual:
        return []

    valor_limite = salario_minimo * (limite_percentual / 100)
    excesso = valor_total - valor_limite

    ordenados = sorted(itens_precos.items(), key=lambda x: x[1], reverse=True)

    sugestoes = []
    acumulado = 0
    for item, preco in ordenados:
        if acumulado >= excesso:
            break
        sugestoes.append(
            f"  - Considere economizar em '{item}' (R$ {preco:.2f})"
        )
        acumulado += preco * 0.3  # supondo economia de 30% por item

    return sugestoes


def ler_float(mensagem):
    """Lê um valor float do usuário com tratamento de erro."""
    while True:
        try:
            valor = float(input(mensagem))
            if valor < 0:
                print("  ⚠  O valor não pode ser negativo. Tente novamente.")
                continue
            return valor
        except ValueError:
            print("  ⚠  Entrada inválida. Digite um número válido.")


def main():
    """Função principal da interface CLI."""
    print("=" * 55)
    print("  CALCULADORA DE CESTA BÁSICA vs. SALÁRIO MÍNIMO")
    print("=" * 55)
    print()

    salario = ler_float("Digite o valor do salário mínimo atual (R$): ")
    if salario <= 0:
        print("Erro: O salário mínimo deve ser maior que zero.")
        return

    print()
    print("Agora, insira o preço de cada item da cesta básica.")
    print("(Digite 0 para itens que não deseja incluir)")
    print("-" * 55)

    itens_precos = {}
    for item in ITENS_CESTA:
        preco = ler_float(f"  {item}: R$ ")
        if preco > 0:
            itens_precos[item] = preco

    if not itens_precos:
        print("\nNenhum item foi adicionado à cesta.")
        return

    valor_total = sum(itens_precos.values())
    percentual = calcular_percentual(valor_total, salario)

    print()
    print("=" * 55)
    print("  RESULTADO")
    print("=" * 55)
    print(f"  Valor total da cesta:  R$ {valor_total:.2f}")
    print(f"  Salário mínimo:        R$ {salario:.2f}")
    print(f"  Comprometimento:       {percentual}%")
    print("-" * 55)

    if percentual > 50:
        print("  🔴 CRÍTICO: A cesta consome mais da metade do salário!")
    elif percentual > 30:
        print("  🟡 ALERTA: O custo está acima do recomendado (30%).")
    else:
        print("  🟢 OK: O custo está dentro de uma margem segura.")

    sugestoes = gerar_sugestoes(itens_precos, salario)
    if sugestoes:
        print()
        print("  💡 Sugestões para reduzir gastos:")
        for s in sugestoes:
            print(s)

    print()
    print("=" * 55)


if __name__ == "__main__":
    main()
