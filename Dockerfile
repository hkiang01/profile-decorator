# https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi
FROM tiangolo/uvicorn-gunicorn:python3.8 as uvicorn-gunicorn
FROM python:3.9
WORKDIR /app
COPY --from=uvicorn-gunicorn /start.sh /gunicorn_conf.py /start-reload.sh /
RUN chmod +x /start.sh && \
    chmod +x /start-reload.sh

# install app dependencies via poetry
ARG POETRY_VERSION=1.1.8
COPY test_app/scripts/get-poetry.py ${WORKDIR}/scripts/get-poetry.py
RUN python "${WORKDIR}"/scripts/get-poetry.py --version=${POETRY_VERSION}
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry config virtualenvs.create false

# install package
COPY poetry.lock pyproject.toml README.md ./
COPY ./profile_decorator ./profile_decorator
RUN poetry install --no-dev

# set up test app
COPY ./test_app /app/test_app
WORKDIR /app/test_app
RUN poetry install --no-dev --no-root
WORKDIR /app

EXPOSE 80

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "./test_app/gunicorn_conf.py", "test_app.main:app"]
