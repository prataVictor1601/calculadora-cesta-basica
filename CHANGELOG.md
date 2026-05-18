# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/),
e o projeto adere ao [Versionamento Semântico](https://semver.org/).

## [1.1.0] - 2026-05-17 — Etapa Intermediária do BootCamp

### Adicionado
- Módulo `src/api_bcb.py` com integração à API pública do Banco Central do Brasil:
  - Busca do salário mínimo vigente (série SGS 1619)
  - Busca da inflação acumulada nos últimos 12 meses (série SGS 433)
- Bloco informativo "Banco Central" no início da execução da CLI
- Opção de usar o salário oficial vindo da API ou digitar manualmente
- 10 testes de integração em `tests/test_integracao_bcb.py` usando mocks HTTP
  com a biblioteca `responses`
- `Dockerfile` para empacotar a aplicação em container
- Dependências `requests` e `responses` em `requirements.txt`

### Modificado
- `src/calculadora.py` agora orquestra a chamada ao módulo de API e mantém
  todo o comportamento da v1.0.0 quando o BCB está indisponível (fallback)
- Pipeline de CI agora roda nas branches `main`, `master` e `entrega-intermediaria`
- README atualizado com a documentação da nova versão

## [1.0.0] - 2026-04-12 — Entrega Inicial do BootCamp

### Adicionado
- Interface CLI para entrada de preços da cesta básica (15 itens)
- Cálculo do percentual do salário comprometido
- Classificação por faixas de risco (OK, Alerta, Crítico)
- Sugestões automáticas de economia
- Validação de entradas (valores negativos, zero, texto inválido)
- 11 testes automatizados com pytest
- Linting com flake8
- Pipeline de CI com GitHub Actions
- README completo com instruções de uso
- Licença MIT
