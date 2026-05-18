# 📦 Release Notes — v1.1.0

Cole o texto abaixo no campo "Description" do GitHub Release ao publicar.

---

## v1.1.0 — Integração com API do Banco Central

**Entrega da Etapa Intermediária do BootCamp.**

### 🆕 Novidades

- **Integração com a API pública do Banco Central do Brasil** (sem necessidade de chave):
  - 💰 Busca automática do salário mínimo vigente (Série SGS 1619)
  - 📈 Inflação acumulada nos últimos 12 meses (Série SGS 433 — IPCA)
- Bloco informativo "Banco Central" exibido no início da execução
- Tratamento robusto de erros: a aplicação continua funcionando com entrada
  manual se o BCB estiver indisponível
- **Dockerfile** para rodar a aplicação em container

### 🧪 Qualidade

- 21 testes automatizados (eram 11 na v1.0.0)
- 10 novos testes de integração com mock HTTP
- Pipeline de CI passando no GitHub Actions

### 📦 Como usar

```bash
# Opção 1: Python
pip install -r requirements.txt
python -m src.calculadora

# Opção 2: Docker
docker build -t calculadora-cesta .
docker run -it --rm calculadora-cesta
```

### 📚 Documentação

Veja o [README](../README.md) e o [CHANGELOG](../CHANGELOG.md) para detalhes.
