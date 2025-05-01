# -------- Base Image --------
FROM python:3.13-slim AS base

# Upgrade base pip & setuptools to avoid vulnerable preinstalled versions
RUN pip install --upgrade pip setuptools

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install dependencies for Poetry and system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
 
# Upgrade pip and setuptools to secure versions
RUN pip install --no-cache-dir pip==24.0 setuptools==70.0.0

# Install the latest version of Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set working directory early for caching
WORKDIR /app
    
# Copy Poetry project files first to leverage Docker caching
COPY pyproject.toml poetry.lock poetry.toml ./
    
# Install project dependencies (no-root mode, production deps only)
RUN poetry install --no-root --no-interaction --no-ansi
    
# Copy source code
COPY portalapi portalapi
COPY . .
    
# Set environment variable for Flask
ENV WEBSITES_PORT=5000
EXPOSE ${WEBSITES_PORT}
    
# -------- Test Image --------
FROM base AS test
COPY .env.test .env
ENTRYPOINT ["poetry", "run", "pytest"]
    
# -------- Production Image --------
FROM base AS production
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
   
# -------- Development Image --------
FROM base AS development
ENV FLASK_ENV=development
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
    
    