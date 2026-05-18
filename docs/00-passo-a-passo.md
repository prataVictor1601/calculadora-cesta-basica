# 🚀 Passo a passo completo — Entrega da Etapa Intermediária

Este guia explica **cada passo** que você precisa dar, com os comandos exatos.
Siga **na ordem**.

> **Pré-requisitos:** Git instalado, Python 3.10+, conta no GitHub e seu
> repositório `prataVictor1601/calculadora-cesta-basica` já existente (da Etapa 1).

---

## Passo 1 — Abrir a Issue no GitHub

1. Acesse https://github.com/prataVictor1601/calculadora-cesta-basica/issues
2. Clique em **New issue**
3. Abra o arquivo `docs/01-texto-da-issue.md` desta entrega e **copie e cole**
   o título e o corpo na Issue
4. Clique em **Submit new issue**
5. **Anote o número da Issue** (provavelmente `#1`)

---

## Passo 2 — Clonar o repositório e criar a branch

No terminal, dentro de uma pasta de trabalho:

```bash
# Clona o repo (pule se já tem ele baixado)
git clone https://github.com/prataVictor1601/calculadora-cesta-basica.git
cd calculadora-cesta-basica

# Garanta que está atualizado
git checkout main
git pull

# Cria a branch da entrega (nome OBRIGATÓRIO conforme barema)
git checkout -b entrega-intermediaria
```

---

## Passo 3 — Substituir os arquivos do projeto

**ATENÇÃO:** os arquivos da Etapa 1 serão substituídos. Faça backup se quiser
guardar a versão antiga (a v1.0.0 já está no histórico do git, então não tem
problema sobrescrever).

Copie todos os arquivos desta entrega **para dentro da pasta do repositório**,
substituindo os existentes. A estrutura final tem que ficar assim:

```
calculadora-cesta-basica/
├── src/
│   ├── __init__.py
│   ├── calculadora.py        # MODIFICADO
│   └── api_bcb.py            # NOVO
├── tests/
│   ├── __init__.py
│   ├── test_calculadora.py   # MODIFICADO (mais testes)
│   └── test_integracao_bcb.py # NOVO
├── .github/workflows/ci.yml  # MODIFICADO
├── Dockerfile                # NOVO
├── requirements.txt          # MODIFICADO
├── setup.py                  # versão 1.1.0
├── .gitignore
├── README.md                 # MODIFICADO
├── LICENSE
└── CHANGELOG.md              # MODIFICADO
```

**Não copie a pasta `docs/`** para o repositório — ela é só guia para você.

---

## Passo 4 — Testar tudo localmente

```bash
# Cria/ativa o ambiente virtual
python -m venv venv
source venv/bin/activate    # Linux/Mac
# venv\Scripts\activate     # Windows

# Instala as novas dependências
pip install -r requirements.txt

# Roda os testes (devem dar 21 passed)
PYTHONPATH=. pytest -v

# Roda a aplicação
PYTHONPATH=. python -m src.calculadora
```

Você deve ver o bloco do Banco Central aparecendo logo no início.

> Se algum teste falhar ou der erro de import, confirme que as pastas
> `src/` e `tests/` têm o arquivo `__init__.py`.

---

## Passo 5 — Commit e push

```bash
git add .
git status   # confira que vai subir os arquivos esperados
git commit -m "feat: integrar API do Banco Central (closes #1)"
git push -u origin entrega-intermediaria
```

> O `closes #1` no commit faz o GitHub **fechar a Issue automaticamente**
> quando o PR for mergeado. **Use o número exato da sua Issue.** Se for `#2`,
> use `closes #2`, e assim por diante.

---

## Passo 6 — Verificar o CI

1. Acesse a aba **Actions** do seu repositório
2. Confirme que o workflow disparou na branch `entrega-intermediaria`
3. Aguarde de 1 a 2 minutos
4. O check tem que ficar **verde** (✅)

Se der erro de lint ou teste, leia a saída do log no GitHub e corrija
localmente, depois faça novo commit e push.

---

## Passo 7 — Publicar o Deploy (Release no GitHub)

Como é uma **CLI**, o deploy aceito pelo enunciado é via **container** ou
**documentação no README de como executá-la**. Vamos usar **GitHub Release**,
que gera um link público com o pacote para download — é a forma profissional
de "publicar" uma CLI.

1. No GitHub, vá em **Releases** → **Create a new release**
2. **Tag:** digite `v1.1.0` (vai aparecer "Create new tag: v1.1.0 on publish")
3. **Target:** `entrega-intermediaria` (pode trocar depois)
4. **Release title:** `v1.1.0 — Integração com API do Banco Central`
5. **Description:** copie e cole o conteúdo de `docs/03-release-notes.md`
6. Marque **Set as the latest release**
7. Clique em **Publish release**

O GitHub vai gerar automaticamente o link público:

```
https://github.com/prataVictor1601/calculadora-cesta-basica/releases/tag/v1.1.0
```

**Esse é o seu link de deploy** — anote para colocar no PDF.

---

## Passo 8 — Confirmar o link no README

Abra o `README.md` e verifique que o link no topo aponta para o release que
você acabou de criar. Se já estiver correto, pule. Se precisar ajustar:

```bash
# Edite o README, depois:
git add README.md
git commit -m "docs: confirmar link do release no README"
git push
```

---

## Passo 9 — Abrir o Pull Request

1. No GitHub, acesse o repositório → aba **Pull requests** → **New pull request**
2. **base:** `main` ← **compare:** `entrega-intermediaria`
3. Clique em **Create pull request**
4. **Título:**
   ```
   Etapa Intermediária: integração com API do Banco Central
   ```
5. **Descrição:** copie e cole o conteúdo de `docs/02-texto-do-pr.md`
6. Clique em **Create pull request**
7. Aguarde o CI rodar e ficar **verde**
8. Clique em **Merge pull request** → **Confirm merge**

✅ Quando o merge acontecer, a Issue será **fechada automaticamente** por causa
do `closes #1` no commit.

---

## Passo 10 — Gerar e enviar o PDF de entrega

1. Abra o arquivo `docs/gerar_pdf.py`
2. Edite as primeiras linhas com seu **nome completo** e a **matrícula/email**
3. Confira que os links do **repositório** e do **release** estão corretos
4. Rode:
   ```bash
   pip install reportlab
   python docs/gerar_pdf.py
   ```
5. Será gerado o arquivo `entrega-intermediaria.pdf`
6. Envie esse PDF na plataforma do BootCamp ✅

---

## ✅ Checklist final

Antes de considerar entregue, confirme:

- [ ] Issue criada com texto descritivo
- [ ] Branch `entrega-intermediaria` (nome exato) criada
- [ ] Todos os arquivos copiados e funcionando
- [ ] Testes passando localmente (`pytest -v` → 21 passed)
- [ ] CI verde no GitHub Actions
- [ ] Release v1.1.0 publicado no GitHub
- [ ] README com o link do release no topo
- [ ] Pull Request mergeado na main
- [ ] Issue fechada (automático via `closes #1`)
- [ ] PDF gerado e enviado na plataforma

---

## 🆘 Problemas comuns

**"O CI deu erro de lint"**
Rode `flake8 src tests --max-line-length=120` localmente. Corrija o que
ele apontar, faça commit e push.

**"Os testes passam local mas falham no CI"**
Confira que o `ci.yml` tem `env: PYTHONPATH: .` no step de testes — já está
configurado, mas vale a pena olhar.

**"Esqueci de pôr `closes #1` no commit"**
Sem problema. Você pode adicionar essa frase **na descrição do PR** que dá
no mesmo. O GitHub procura `closes #N` no commit *ou* no corpo do PR.

**"O Render não aceita meu projeto"**
Não use Render para essa entrega — como é uma CLI, o deploy aceito é via
Docker + GitHub Release (já configurados).
