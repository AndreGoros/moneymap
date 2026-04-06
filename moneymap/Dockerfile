# ── Dockerfile — MoneyMap ────────────────────────────────────────────────────
#
# Imagen que instala MoneyMap desde PyPI y ejecuta el demo completo.
#
# Build:
#   docker build -t moneymap .
#
# Ejecutar demo:
#   docker run --rm moneymap
#
# Ejecutar tests:
#   docker run --rm moneymap pytest
#
# Shell interactivo:
#   docker run --rm -it moneymap bash
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.12-slim

# Metadatos
LABEL maintainer="MoneyMap Contributors"
LABEL description="MoneyMap — conversión de divisas e impuestos con precisión decimal"

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo los archivos necesarios
COPY requirements-docker.txt .

# Instalar MoneyMap desde PyPI con todos los extras
RUN pip install --no-cache-dir -r requirements-docker.txt

# Copiar código fuente y archivos de soporte
COPY demo_moneymap.py .
COPY tests/ ./tests/
COPY moneymap/ ./moneymap/

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Comando por defecto: ejecutar el demo
CMD ["python", "demo_moneymap.py"]
