FROM python:3.9

# https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi
WORKDIR /app
RUN pip install --no-cache-dir "uvicorn[standard]>=0.15.0,<0.16.0" "gunicorn>=20.1.0,<20.2.0" "fastapi>=0.68.1,<0.69.0"

# hadolint ignore=DL3022
COPY --from=tiangolo/uvicorn-gunicorn:python3.8 /start.sh /start.sh
# hadolint ignore=DL3022
COPY --from=tiangolo/uvicorn-gunicorn:python3.8 /gunicorn_conf.py /gunicorn_conf.py
# hadolint ignore=DL3022
COPY --from=tiangolo/uvicorn-gunicorn:python3.8 /start-reload.sh /start-reload.sh
RUN chmod +x /start.sh && \
    chmod +x /start-reload.sh

# install app dependencies via poetry
ARG POETRY_VERSION=1.1.8
COPY scripts/get-poetry.py ${WORKDIR}/scripts/get-poetry.py
RUN python "${WORKDIR}"/scripts/get-poetry.py --version=${POETRY_VERSION}
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-ansi

# app files
COPY ./app ./app

EXPOSE 80

CMD ["/start.sh"]
