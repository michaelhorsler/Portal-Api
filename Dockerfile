FROM python:buster AS base

# Perform common operations, dependency installation etc...
# Install Poetry and the export plugin
RUN pip install poetry \
 && poetry self add poetry-plugin-export

WORKDIR /app
COPY poetry.toml ./
COPY pyproject.toml poetry.lock ./
ADD portalapi portalapi
RUN poetry install
ENV WEBSITES_PORT=5000
EXPOSE ${WEBSITES_PORT}
COPY . .

FROM base AS test
#Configure for test
COPY .env.test .
ENTRYPOINT ["poetry", "run", "pytest"]

FROM base AS production
# Configure for production
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]

FROM base AS development
# Configure for local development
ENV FLASK_ENV=development
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]