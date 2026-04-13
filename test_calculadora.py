"""Testes automatizados para a calculadora de cesta básica."""

import pytest
from src.calculadora import calcular_percentual, gerar_sugestoes


# === Testes de calcular_percentual ===

def test_calculo_correto():
    """Caminho feliz: cesta de R$450 com salário de R$1412."""
    assert calcular_percentual(450, 1412) == 31.87


def test_calculo_cesta_zero():
    """Cesta com valor zero deve retornar 0%."""
    assert calcular_percentual(0, 1412) == 0.0


def test_calculo_cesta_igual_salario():
    """Cesta igual ao salário deve retornar 100%."""
    assert calcular_percentual(1412, 1412) == 100.0


def test_salario_zero_deve_retornar_erro():
    """Caso limite: divisão por zero."""
    with pytest.raises(ValueError, match="salário mínimo deve ser maior"):
        calcular_percentual(500, 0)


def test_salario_negativo_deve_retornar_erro():
    """Salário negativo é inválido."""
    with pytest.raises(ValueError, match="salário mínimo deve ser maior"):
        calcular_percentual(500, -100)


def test_valor_negativo_deve_retornar_erro():
    """Valor de cesta negativo é inválido."""
    with pytest.raises(ValueError, match="valor da cesta não pode ser negativo"):
        calcular_percentual(-10, 1412)


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
