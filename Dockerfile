# Imagem oficial enxuta do Python
FROM python:3.10-slim

WORKDIR /app

# Copia e instala dependências primeiro (cache de camada)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY src/ ./src/
COPY setup.py .
COPY README.md .

# Ajusta PYTHONPATH para que `python -m src.calculadora` funcione
ENV PYTHONPATH=/app

# Comando padrão: roda a CLI
CMD ["python", "-m", "src.calculadora"]
