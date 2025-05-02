# -------- Base Image --------
    FROM python:3.13-slim AS base

    # Set the shell with pipefail for safer script execution (DL4006)
    SHELL ["/bin/bash", "-o", "pipefail", "-c"]
    
    # Set working directory early (DL3045)
    WORKDIR /app
    
    # Upgrade base pip & setuptools to avoid vulnerable preinstalled versions (DL3013, DL3042)
    RUN pip install --no-cache-dir --upgrade pip setuptools
    
    # Copy and install Python dependencies with pinned versions (DL3013, DL3042)
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # hadolint ignore=DL3008
    RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        && apt-get clean && rm -rf /var/lib/apt/lists/*
    
    # Re-pin pip/setuptools explicitly (DL3013, DL3042)
    RUN pip install --no-cache-dir pip==24.0 setuptools==70.0.0
    
    # Install the latest version of Poetry
    RUN curl -sSL https://install.python-poetry.org | python3 -
    ENV PATH="/root/.local/bin:$PATH"
    
    # Copy Poetry project files first to leverage Docker caching
    COPY pyproject.toml poetry.lock poetry.toml ./
    
    # Install project dependencies (production-only)
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
    