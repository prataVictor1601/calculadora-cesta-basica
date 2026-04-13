# 🛒 Calculadora de Cesta Básica vs. Salário Mínimo

![Python CI](https://github.com/prataVictor1601/calculadora-cesta-basica/actions/workflows/ci.yml/badge.svg)

## 📌 Descrição do Problema

Em tempos de inflação, famílias de baixa renda enfrentam dificuldades crescentes para planejar a compra do mês sem ultrapassar o orçamento. Muitas vezes, o custo da cesta básica consome uma parcela desproporcional do salário mínimo, comprometendo outros gastos essenciais como moradia, transporte e saúde.

## 💡 Proposta da Solução

Esta aplicação CLI permite ao usuário inserir os preços dos itens essenciais da cesta básica (arroz, feijão, óleo, carne, etc.) e calcula automaticamente:

- O **valor total** da cesta básica
- A **porcentagem do salário mínimo** que aquela cesta consome
- **Sugestões de ajuste** para não estourar o limite recomendado de 30%

## 👥 Público-Alvo

- Famílias de baixa renda que precisam planejar gastos alimentares
- Estudantes de economia e ciências sociais
- Assistentes sociais e agentes comunitários
- Qualquer pessoa interessada em controle financeiro alimentar

## ⚙️ Funcionalidades Principais

- Entrada de preços para 15 itens da cesta básica
- Cálculo do percentual do salário comprometido
- Classificação por faixas de risco (🟢 OK, 🟡 Alerta, 🔴 Crítico)
- Sugestões automáticas de economia quando acima do limite
- Validação de entradas (valores negativos, texto inválido, divisão por zero)

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Testes:** pytest 8.3.4
- **Linting:** flake8 7.1.1
- **CI/CD:** GitHub Actions

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/prataVictor1601/calculadora-cesta-basica.git
cd calculadora-cesta-basica
```

2. (Opcional) Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ▶️ Como Executar

```bash
python -m src.calculadora
```

### Exemplo de Uso

```
=======================================================
  CALCULADORA DE CESTA BÁSICA vs. SALÁRIO MÍNIMO
=======================================================

Digite o valor do salário mínimo atual (R$): 1412

Agora, insira o preço de cada item da cesta básica.
(Digite 0 para itens que não deseja incluir)
-------------------------------------------------------
  Arroz (5kg): R$ 28.90
  Feijão (1kg): R$ 8.50
  Óleo de soja (900ml): R$ 7.80
  ...

=======================================================
  RESULTADO
=======================================================
  Valor total da cesta:  R$ 485.30
  Salário mínimo:        R$ 1412.00
  Comprometimento:       34.37%
-------------------------------------------------------
  🟡 ALERTA: O custo está acima do recomendado (30%).

  💡 Sugestões para reduzir gastos:
  - Considere economizar em 'Carne bovina (1kg)' (R$ 45.00)
  - Considere economizar em 'Frango (1kg)' (R$ 18.90)

=======================================================
```

## 🧪 Como Rodar os Testes

```bash
pytest -v
```

Os testes cobrem:
- ✅ Cálculo correto (caminho feliz)
- ✅ Cesta com valor zero
- ✅ Cesta igual ao salário (100%)
- ✅ Salário zero (erro esperado)
- ✅ Salário negativo (erro esperado)
- ✅ Valor de cesta negativo (erro esperado)
- ✅ Geração de sugestões quando acima do limite
- ✅ Ausência de sugestões quando dentro do limite

## 🔍 Como Rodar o Lint

```bash
flake8 src tests --count --show-source --statistics
```

## 📋 Versão Atual

**v1.0.0** — Primeira versão funcional com CLI, testes e CI.

## ✍️ Autor

**Victor Rezende de Melo Prata**

## 🔗 Repositório

[https://github.com/prataVictor1601/calculadora-cesta-basica](https://github.com/prataVictor1601/calculadora-cesta-basica)

## 📄 Licença

Este projeto está licenciado sob a licença MIT — veja o arquivo [LICENSE](LICENSE) para detalhes.
