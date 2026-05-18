from setuptools import setup, find_packages

setup(
    name="calculadora_cesta_basica",
    version="1.1.0",
    description=(
        "Calculadora de Cesta Básica vs. Salário Mínimo com integração à API "
        "do Banco Central do Brasil"
    ),
    author="Victor Prata",
    author_email="seu.email@exemplo.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31",
    ],
)
