# Folosim o imagine oficială de Python stabilă și ușoară
FROM python:3.12-slim

# Setăm directorul de lucru în container
WORKDIR /workspace

# Setăm variabile de mediu pentru a preveni fișierele .pyc și buffers I/O
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalăm dependențele de sistem necesare pentru compilarea pachetelor python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalăm managerul de pachete ultra-rapid 'uv' global în container
RUN pip install --no-cache-dir uv

# Copiem fișierele de dependențe pentru a folosi cache-ul Docker eficient
COPY pyproject.toml uv.lock ./

# Instalăm dependențele sincronizat direct în sistemul containerului utilizând lockfile-ul deterministic
RUN uv pip install --system -r pyproject.toml

# Copiem restul codului sursă al aplicației în container
COPY . .

# Expunem porturile pentru toate cele 3 servicii (FastAPI, Admin ERP, E-Shop)
EXPOSE 8000 8520 8599

# Comanda implicită va fi suprascrisă de docker-compose
CMD ["python", "main.py"]
