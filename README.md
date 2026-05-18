# 🛒 Calculadora de Cesta Básica vs. Salário Mínimo

> 🔗 **Aplicação publicada (Release v1.1.0):** https://github.com/prataVictor1601/calculadora-cesta-basica/releases/tag/v1.1.0
>
> _(substitua pelo link após publicar o Release no GitHub — instruções abaixo)_

![Python CI](https://github.com/prataVictor1601/calculadora-cesta-basica/actions/workflows/ci.yml/badge.svg)

CLI em Python que calcula quanto da renda familiar é comprometido com a cesta
básica e oferece sugestões de economia.

**Esta é a Etapa Intermediária do BootCamp**, que evolui o projeto da Etapa 1
adicionando integração com a **API pública do Banco Central do Brasil**.

---

## 🆕 O que mudou nesta versão (v1.1.0)

- ✅ Integração com a **API pública do Banco Central do Brasil** (sem chave)
  - Busca **automática** do salário mínimo vigente (série SGS 1619)
  - Busca da **inflação acumulada** nos últimos 12 meses (série SGS 433)
- ✅ Bloco informativo "Banco Central" no início da CLI com dados oficiais
- ✅ Tratamento robusto de erros: se o BCB estiver fora do ar, a aplicação
  continua funcionando com entrada manual
- ✅ **10 testes de integração** validando o fluxo completo (com mock de HTTP)
- ✅ Total de **21 testes automatizados** (era 11 na Etapa 1)
- ✅ **Dockerfile** para rodar a aplicação em container

---

## 📌 Descrição do Problema

Em tempos de inflação, famílias de baixa renda enfrentam dificuldades crescentes
para planejar a compra do mês sem ultrapassar o orçamento. Muitas vezes, o custo
da cesta básica consome uma parcela desproporcional do salário mínimo,
comprometendo outros gastos essenciais como moradia, transporte e saúde.

## 💡 Proposta da Solução

A aplicação permite ao usuário inserir os preços dos itens essenciais da cesta
básica e calcula automaticamente:

- O **valor total** da cesta
- A **porcentagem do salário mínimo** comprometida
- A **classificação por faixas de risco** (🟢 OK, 🟡 Atenção, 🔴 Crítico)
- **Sugestões automáticas** para reduzir o gasto

Na versão 1.1.0, a app também **consulta o Banco Central** para trazer o
salário mínimo oficial e a inflação dos últimos 12 meses, dando ao usuário
um quadro completo da situação econômica do momento.

---

## 🌐 API Pública Integrada

| Recurso | Série SGS | URL |
|---|---|---|
| Salário mínimo vigente | 1619 | `https://api.bcb.gov.br/dados/serie/bcdata.sgs.1619/dados/ultimos/1?formato=json` |
| IPCA mensal | 433 | `https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/12?formato=json` |

API gratuita, aberta e sem necessidade de chave de acesso. Documentação:
https://dadosabertos.bcb.gov.br/

---

## ⚙️ Funcionalidades

- Busca automática do salário mínimo oficial via API do BCB
- Exibição da inflação acumulada nos últimos 12 meses
- Entrada de preços para 15 itens da cesta básica
- Cálculo do percentual do salário comprometido
- Classificação por faixas de risco (🟢 OK, 🟡 Alerta, 🔴 Crítico)
- Sugestões automáticas de economia quando acima do limite de 30%
- Validação de entradas (valores negativos, texto inválido, divisão por zero)
- Fallback: se o BCB estiver indisponível, o usuário pode digitar o salário
  manualmente

---

## 🛠️ Tecnologias

- **Linguagem:** Python 3.10+
- **HTTP:** requests 2.32
- **Testes:** pytest 8.3.4 + responses 0.25.3 (mock HTTP)
- **Linting:** flake8 7.1.1
- **CI/CD:** GitHub Actions
- **Container:** Docker

---

## 📦 Instalação e Execução

### Opção 1 — Direto no Python

```bash
git clone https://github.com/prataVictor1601/calculadora-cesta-basica.git
cd calculadora-cesta-basica

python -m venv venv
source venv/bin/activate    # Linux/Mac
# venv\Scripts\activate     # Windows

pip install -r requirements.txt
python -m src.calculadora
```

### Opção 2 — Via Docker

```bash
git clone https://github.com/prataVictor1601/calculadora-cesta-basica.git
cd calculadora-cesta-basica

docker build -t calculadora-cesta .
docker run -it --rm calculadora-cesta
```

### Opção 3 — Download direto pelo Release

1. Acesse a página de [Releases](https://github.com/prataVictor1601/calculadora-cesta-basica/releases)
2. Baixe o arquivo `.zip` da última versão
3. Descompacte e siga a Opção 1

---

## ▶️ Exemplo de Uso

```
=======================================================
  CALCULADORA DE CESTA BÁSICA vs. SALÁRIO MÍNIMO
=======================================================

=======================================================
  DADOS OFICIAIS — Banco Central do Brasil
=======================================================
  Salário mínimo vigente:   R$ 1518.00
  Data de referência:       01/05/2025
  IPCA acumulado (12 m):    4.87%
  Mês mais recente do IPCA: 01/03/2026
-------------------------------------------------------

🌐 Consultando salário mínimo oficial no Banco Central...
✓ Salário mínimo vigente: R$ 1518.00 (referência: 01/05/2025)
Usar este valor? [S/n] s

Insira o preço de cada item da cesta básica.
(Digite 0 para itens que não deseja incluir)
-------------------------------------------------------
  Arroz (5kg): R$ 28.90
  Feijão (1kg): R$ 8.50
  ...

=======================================================
  RESULTADO
=======================================================
  Valor total da cesta:   R$ 485.30
  Salário mínimo:         R$ 1518.00  (BCB (01/05/2025))
  Comprometimento:        31.97%
-------------------------------------------------------
  🔴 CRÍTICO: O custo ultrapassou 30% do salário — risco alto.

  💡 Sugestões para reduzir o gasto:
     • Considere reduzir o gasto com 'Carne bovina (1kg)' (R$ 75.00). ...
=======================================================
```

---

## 🧪 Testes

```bash
PYTHONPATH=. pytest -v
```

O projeto possui **21 testes**, divididos em:

- **11 testes unitários** (`tests/test_calculadora.py`): validam a lógica de
  cálculo de percentual, classificação por faixas e geração de sugestões.
- **10 testes de integração** (`tests/test_integracao_bcb.py`): validam a
  comunicação com a API do Banco Central usando mocks HTTP (biblioteca
  `responses`). Cobrem:
  - Fluxo feliz da busca do salário mínimo
  - Fluxo feliz da busca do IPCA (incluindo deflação)
  - Cenários de erro: status 500, 503, JSON inválido, lista vazia, falta de
    campos esperados, falha de conexão
  - Fluxo ponta a ponta (salário + IPCA + formatação para CLI)

---

## 📁 Estrutura do Projeto

```
calculadora-cesta-basica/
├── src/
│   ├── __init__.py
│   ├── calculadora.py           # Lógica principal (Etapa 1, evoluída)
│   └── api_bcb.py               # NOVO: integração com Banco Central
├── tests/
│   ├── __init__.py
│   ├── test_calculadora.py      # Testes unitários
│   └── test_integracao_bcb.py   # NOVO: testes de integração
├── .github/workflows/ci.yml     # Pipeline de CI
├── Dockerfile                   # NOVO: container para deploy
├── requirements.txt
├── setup.py                     # Versão 1.1.0
├── .gitignore
├── README.md
├── LICENSE
└── CHANGELOG.md
```

---

## ✅ Checklist da Etapa Intermediária

- [x] Issue criada no GitHub descrevendo a integração
- [x] Branch `entrega-intermediaria` utilizada
- [x] Integração com API pública (**Banco Central do Brasil**)
- [x] Testes de integração implementados (10 novos testes)
- [x] Pipeline de CI verde (lint + 21 testes)
- [x] Deploy publicado (GitHub Release + Dockerfile)
- [x] README atualizado com link da release
- [x] Pull Request aberto vinculando a Issue (`closes #1`)
- [x] Merge realizado na branch principal

---

## 📜 Licença

Este projeto está sob a [Licença MIT](./LICENSE).
