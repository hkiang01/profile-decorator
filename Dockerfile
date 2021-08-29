# https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi
FROM tiangolo/uvicorn-gunicorn:python3.8 as uvicorn-gunicorn
FROM python:3.9
WORKDIR /app
COPY --from=uvicorn-gunicorn /start.sh /gunicorn_conf.py /start-reload.sh /
RUN chmod +x /start.sh && \
    chmod +x /start-reload.sh

# install app dependencies via poetry
ARG POETRY_VERSION=1.1.8
COPY scripts/get-poetry.py ${WORKDIR}/scripts/get-poetry.py
RUN python "${WORKDIR}"/scripts/get-poetry.py --version=${POETRY_VERSION}
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
COPY ./profile-decorator /app/profile-decorator/
RUN poetry install --no-dev --no-ansi

# app files
COPY ./app ./app

EXPOSE 80

CMD ["python", "-m", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "./app/gunicorn_conf.py", "app.main:app"]
