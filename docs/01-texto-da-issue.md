# 📌 Texto pronto para abrir a Issue no GitHub

Vá em **https://github.com/prataVictor1601/calculadora-cesta-basica/issues** →
clique em **New issue** → cole o conteúdo abaixo.

---

## Título da Issue

```
Integrar API pública do Banco Central para buscar salário mínimo e inflação
```

## Corpo da Issue

```markdown
## 🎯 Objetivo
Evoluir a calculadora de cesta básica integrando-a com a API pública do
**Banco Central do Brasil**, atendendo aos requisitos da Etapa Intermediária
do BootCamp.

## 📋 Funcionalidade proposta
Atualmente o usuário precisa digitar o salário mínimo manualmente, o que é
trabalhoso e pode levar a erros (valores desatualizados). A integração com
a API do BCB resolve isso buscando automaticamente:

1. **Salário mínimo vigente** (Série SGS 1619)
2. **Inflação (IPCA) acumulada nos últimos 12 meses** (Série SGS 433)

Esses dados são apresentados ao usuário no início da execução como contexto
econômico e oferecidos como valor padrão para o cálculo do percentual.

## 💡 Valor que essa integração agrega
- **Dados oficiais e sempre atualizados** — o usuário não precisa decorar
  qual é o salário mínimo atual.
- **Contexto econômico** — ao ver a inflação dos últimos 12 meses, o usuário
  entende por que o gasto com cesta pode estar mais alto.
- **Robustez** — se o BCB estiver fora do ar, a aplicação continua funcionando
  com entrada manual (graceful degradation).
- **Coerência com o tema do projeto** — usar dados do Banco Central numa
  calculadora de orçamento familiar é o caso de uso perfeito.

## 🛠️ Tarefas
- [ ] Criar branch `entrega-intermediaria`
- [ ] Criar módulo `src/api_bcb.py` com as funções de integração
- [ ] Integrar o novo módulo em `src/calculadora.py`
- [ ] Adicionar `requests` e `responses` ao `requirements.txt`
- [ ] Escrever testes de integração com mock HTTP (`tests/test_integracao_bcb.py`)
- [ ] Atualizar o CI para rodar na branch nova
- [ ] Criar `Dockerfile` para o deploy
- [ ] Publicar Release v1.1.0 no GitHub (deploy da CLI)
- [ ] Atualizar README e CHANGELOG
- [ ] Abrir Pull Request fechando esta Issue (`closes #1`)

## 🔗 Referências
- API pública do BCB: https://dadosabertos.bcb.gov.br/
- Série 1619 (salário mínimo): https://www3.bcb.gov.br/sgspub/consultarvalores/consultarValoresSeries.do?method=consultarValores&hdSeries=1619
- Série 433 (IPCA): https://www3.bcb.gov.br/sgspub/consultarvalores/consultarValoresSeries.do?method=consultarValores&hdSeries=433
```
