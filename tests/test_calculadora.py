"""Testes automatizados para a calculadora de cesta basica."""

import pytest
from src.calculadora import calcular_percentual, gerar_sugestoes


def test_calculo_correto():
    """Caminho feliz: cesta de R$450 com salario de R$1412."""
    assert calcular_percentual(450, 1412) == 31.87


def test_calculo_cesta_zero():
    """Cesta com valor zero deve retornar 0 porcento."""
    assert calcular_percentual(0, 1412) == 0.0


def test_calculo_cesta_igual_salario():
    """Cesta igual ao salario deve retornar 100 porcento."""
    assert calcular_percentual(1412, 1412) == 100.0


def test_salario_zero_deve_retornar_erro():
    """Caso limite: divisao por zero."""
    with pytest.raises(ValueError, match="salario minimo"):
        calcular_percentual(500, 0)


def test_salario_negativo_deve_retornar_erro():
    """Salario negativo e invalido."""
    with pytest.raises(ValueError, match="salario minimo"):
        calcular_percentual(500, -100)


def test_valor_negativo_deve_retornar_erro():
    """Valor de cesta negativo e invalido."""
    with pytest.raises(ValueError, match="valor da cesta"):
        calcular_percentual(-10, 1412)


def test_sugestoes_quando_acima_do_limite():
    """Deve gerar sugestoes quando acima de 30 porcento."""
    itens = {
        "Carne bovina (1kg)": 200,
        "Arroz (5kg)": 150,
        "Feijao (1kg)": 100,
    }
    sugestoes = gerar_sugestoes(itens, 1412, 30)
    assert len(sugestoes) > 0


def test_sem_sugestoes_quando_dentro_do_limite():
    """Nao deve gerar sugestoes quando esta ok."""
    itens = {"Arroz (5kg)": 30, "Feijao (1kg)": 10}
    sugestoes = gerar_sugestoes(itens, 1412, 30)
    assert sugestoes == []
