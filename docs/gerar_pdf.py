"""
Gera o PDF de entrega da Etapa Intermediária do BootCamp.

Como usar:
  1. Preencha os campos NOME_ALUNO, MATRICULA e DISCIPLINA abaixo.
  2. Confira que LINK_REPOSITORIO e LINK_DEPLOY estão corretos.
  3. Rode:  python docs/gerar_pdf.py
  4. O arquivo "entrega-intermediaria.pdf" será gerado na raiz do projeto.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ============================================================
# >>>>>>>>>>>>>>>  PREENCHA SEUS DADOS  <<<<<<<<<<<<<<<<<<<<<<
# ============================================================
NOME_ALUNO = "Victor Prata"
MATRICULA = "SUA MATRÍCULA / E-MAIL AQUI"
DISCIPLINA = "BootCamp II"

LINK_REPOSITORIO = "https://github.com/prataVictor1601/calculadora-cesta-basica"
LINK_DEPLOY = "https://github.com/prataVictor1601/calculadora-cesta-basica/releases/tag/v1.1.0"
# ============================================================

# Caminho do PDF (vai para a raiz do projeto, um nível acima de docs/)
PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "entrega-intermediaria.pdf")
PDF_PATH = os.path.abspath(PDF_PATH)


def gerar():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "Titulo", parent=styles["Title"], fontSize=22,
        textColor=HexColor("#0f1419"), spaceAfter=6, alignment=TA_CENTER,
    )
    estilo_subtitulo = ParagraphStyle(
        "Subtitulo", parent=styles["Normal"], fontSize=11,
        textColor=HexColor("#6b7280"), alignment=TA_CENTER, spaceAfter=24,
    )
    estilo_secao = ParagraphStyle(
        "Secao", parent=styles["Heading2"], fontSize=14,
        textColor=HexColor("#16a34a"), spaceBefore=18, spaceAfter=10,
    )
    estilo_corpo = ParagraphStyle(
        "Corpo", parent=styles["Normal"], fontSize=10.5,
        leading=15, textColor=black, alignment=TA_LEFT, spaceAfter=8,
    )
    estilo_link = ParagraphStyle(
        "Link", parent=estilo_corpo, fontName="Courier",
        fontSize=10, textColor=HexColor("#2563eb"),
    )

    story = []

    # Cabeçalho
    story.append(Paragraph("Entrega Intermediária", estilo_titulo))
    story.append(Paragraph(
        "BootCamp — Etapa 2: Issues, API Pública, Testes e Deploy",
        estilo_subtitulo
    ))

    # 1. Identificação
    story.append(Paragraph("1. Identificação", estilo_secao))
    dados_aluno = [
        ["Aluno(a):", NOME_ALUNO],
        ["Matrícula / E-mail:", MATRICULA],
        ["Disciplina:", DISCIPLINA],
        ["Projeto:", "Calculadora de Cesta Básica vs. Salário Mínimo"],
        ["Versão:", "1.1.0"],
        ["Stack:", "Python · pytest · responses · Docker · GitHub Actions"],
    ]
    tabela = Table(dados_aluno, colWidths=[4.5 * cm, 11 * cm])
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), HexColor("#f3f4f6")),
        ("TEXTCOLOR", (0, 0), (0, -1), HexColor("#374151")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#d1d5db")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, HexColor("#e5e7eb")),
    ]))
    story.append(tabela)

    # 2. Links
    story.append(Paragraph("2. Links da Entrega", estilo_secao))
    story.append(Paragraph("<b>Repositório no GitHub:</b>", estilo_corpo))
    story.append(Paragraph(
        f'<link href="{LINK_REPOSITORIO}">{LINK_REPOSITORIO}</link>',
        estilo_link
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Aplicação publicada (Deploy via GitHub Release):</b>",
        estilo_corpo
    ))
    story.append(Paragraph(
        f'<link href="{LINK_DEPLOY}">{LINK_DEPLOY}</link>',
        estilo_link
    ))

    # 3. Resumo
    story.append(Paragraph("3. Resumo da Entrega", estilo_secao))
    story.append(Paragraph(
        "Esta entrega evolui o projeto Calculadora de Cesta Básica da Etapa 1 "
        "integrando-o com a <b>API pública do Banco Central do Brasil</b>. "
        "Agora a aplicação busca automaticamente o salário mínimo vigente "
        "(Série SGS 1619) e a inflação acumulada nos últimos 12 meses "
        "(Série SGS 433 — IPCA), oferecendo um quadro econômico completo "
        "ao usuário no início da execução. Foram adicionados 10 testes de "
        "integração com mocks HTTP, totalizando 21 testes automatizados.",
        estilo_corpo
    ))

    # 4. Itens do barema
    story.append(Paragraph("4. Itens do Barema Atendidos", estilo_secao))
    itens = [
        ["Critério", "Como foi atendido", "Peso"],
        [
            "Integração com API Pública",
            "API do Banco Central (séries 1619 e 433): salário mínimo + IPCA.",
            "25%",
        ],
        [
            "Issue e Branch",
            "Issue #1 descritiva, branch entrega-intermediaria, PR com closes #1.",
            "20%",
        ],
        [
            "Teste de Integração",
            "10 testes de integração com mock HTTP (biblioteca responses).",
            "20%",
        ],
        [
            "Deploy",
            "GitHub Release v1.1.0 + Dockerfile (link público acessível).",
            "20%",
        ],
        [
            "CI/CD e README",
            "GitHub Actions verde (lint + 21 testes); README com link do release.",
            "10%",
        ],
        [
            "PDF de Entrega",
            "Este documento.",
            "5%",
        ],
    ]
    tabela_barema = Table(itens, colWidths=[4 * cm, 9.5 * cm, 2 * cm])
    tabela_barema.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#0f1419")),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#16a34a")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (-1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#d1d5db")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, HexColor("#e5e7eb")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [HexColor("#ffffff"), HexColor("#f9fafb")]),
    ]))
    story.append(tabela_barema)

    # 5. Como rodar
    story.append(Paragraph("5. Como Executar Localmente", estilo_secao))
    codigo = (
        "git clone " + LINK_REPOSITORIO + "<br/>"
        "cd calculadora-cesta-basica<br/>"
        "python -m venv venv &amp;&amp; source venv/bin/activate<br/>"
        "pip install -r requirements.txt<br/>"
        "PYTHONPATH=. pytest -v   <i># 21 testes</i><br/>"
        "PYTHONPATH=. python -m src.calculadora"
    )
    story.append(Paragraph(
        codigo,
        ParagraphStyle(
            "Codigo", parent=estilo_corpo, fontName="Courier",
            fontSize=9.5, textColor=HexColor("#374151"),
            backColor=HexColor("#f3f4f6"),
            borderColor=HexColor("#d1d5db"),
            borderWidth=0.5, borderPadding=8, leading=14,
        ),
    ))

    doc.build(story)
    print(f"✓ PDF gerado: {PDF_PATH}")


if __name__ == "__main__":
    gerar()
