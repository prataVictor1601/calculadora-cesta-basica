"""Testes unitários da calculadora (Etapa 1 — preservados)."""
import pytest
from src.calculadora import (
    calcular_percentual,
    classificar_risco,
    gerar_sugestoes,
)


# === Testes de calcular_percentual ===

def test_calculo_correto():
    """Caminho feliz: cesta de R$ 450, salário de R$ 1412."""
    assert calcular_percentual(450, 1412) == 31.87


def test_calculo_dentro_do_limite():
    """Cesta de 30% do salário (limite)."""
    assert calcular_percentual(300, 1000) == 30.0


def test_calculo_acima_do_limite():
    """Cesta acima de 30%."""
    assert calcular_percentual(500, 1412) == 35.41


def test_salario_zero_deve_retornar_erro():
    """Caso limite: divisão por zero."""
    with pytest.raises(ValueError, match="salário mínimo deve ser maior"):
        calcular_percentual(500, 0)


def test_salario_negativo_deve_retornar_erro():
    with pytest.raises(ValueError, match="salário mínimo deve ser maior"):
        calcular_percentual(500, -100)


def test_valor_negativo_deve_retornar_erro():
    """Valor de cesta negativo é inválido."""
    with pytest.raises(ValueError, match="valor da cesta não pode ser negativo"):
        calcular_percentual(-10, 1412)


# === Testes de classificar_risco ===

def test_classifica_como_ok_quando_baixo():
    emoji, status, _ = classificar_risco(15)
    assert emoji == "🟢"
    assert status == "OK"


def test_classifica_como_atencao_no_limite():
    emoji, status, _ = classificar_risco(28)
    assert emoji == "🟡"
    assert status == "ATENÇÃO"


def test_classifica_como_critico_quando_alto():
    emoji, status, _ = classificar_risco(45)
    assert emoji == "🔴"
    assert status == "CRÍTICO"


# === Testes de gerar_sugestoes ===

def test_sugestoes_quando_acima_do_limite():
    """Deve gerar sugestões quando percentual ultrapassa 30%."""
    itens = {"Carne bovina (1kg)": 200, "Arroz (5kg)": 150, "Feijão (1kg)": 100}
    sugestoes = gerar_sugestoes(itens, 1412, limite_percentual=30)
    assert len(sugestoes) > 0


def test_sem_sugestoes_quando_dentro_do_limite():
    """Não deve gerar sugestões quando percentual está ok."""
    itens = {"Arroz (5kg)": 30, "Feijão (1kg)": 10}
    sugestoes = gerar_sugestoes(itens, 1412, limite_percentual=30)
    assert sugestoes == []
