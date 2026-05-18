# 📝 Texto do Pull Request

## Título sugerido

```
Etapa Intermediária: integração com API do Banco Central
```

## Corpo (copie e cole na descrição do PR)

```markdown
## 📋 O que este PR entrega
Implementação da **Etapa Intermediária do BootCamp**: integração com API
pública, testes de integração, CI/CD e empacotamento para deploy.

closes #1

## ✨ Funcionalidades adicionadas
- **Integração com a API pública do Banco Central do Brasil** (sem chave):
  - Busca automática do salário mínimo vigente (Série SGS 1619)
  - Busca da inflação acumulada nos últimos 12 meses (Série SGS 433)
- Bloco informativo "Banco Central" no início da CLI
- Tratamento robusto de erros: fallback para entrada manual se o BCB falhar
- Dockerfile para empacotar a aplicação

## 🧪 Testes
**21 testes no total** (era 11 na Etapa 1):

- 11 testes unitários (preservados)
- **10 testes de integração novos** com mock HTTP (biblioteca `responses`)
  validando:
  - Fluxo feliz das duas chamadas ao BCB
  - Cenários de erro: HTTP 500, 503, JSON inválido, lista vazia, falta de
    campos, falha de conexão
  - Fluxo ponta a ponta (salário + IPCA + formatação)

```
$ pytest -v
========== 21 passed in 0.27s ==========
```

## 🚀 Deploy
A aplicação foi empacotada e publicada como **GitHub Release v1.1.0**:
https://github.com/prataVictor1601/calculadora-cesta-basica/releases/tag/v1.1.0

Pode ser executada via Python ou Docker (instruções no README).

## ✅ Checklist do barema
- [x] Issue #1 criada e descritiva
- [x] Branch `entrega-intermediaria` (nome exato)
- [x] Integração com API pública (BCB)
- [x] Teste de integração implementado
- [x] CI verde (lint + 21 testes)
- [x] Deploy publicado em link público (GitHub Release)
- [x] README atualizado com o link do deploy
```
