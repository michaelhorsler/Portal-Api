FROM python:buster AS base

# Upgrade base pip & setuptools to avoid vulnerable preinstalled versions
RUN pip install --upgrade pip setuptools

# Install Poetry and the export plugin
RUN pip install poetry \
 && poetry self add poetry-plugin-export

WORKDIR /app

# Copy and install project dependencies
COPY poetry.toml ./   
COPY pyproject.toml poetry.lock ./
ADD portalapi portalapi
RUN poetry install

ENV WEBSITES_PORT=5000
EXPOSE ${WEBSITES_PORT}

COPY . .

FROM base AS test
COPY .env.test .env
ENTRYPOINT ["poetry", "run", "pytest"]

FROM base AS production
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]

FROM base AS development
ENV FLASK_ENV=development
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]