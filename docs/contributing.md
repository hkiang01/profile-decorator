# Contributing

## Dev environment

Use poetry

1. Install [Poetry](https://python-poetry.org/docs/):
    ```zsh
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py > get-poetry.py
    python get-poetry.py --version=1.1.8
    ```

1. Install dependencies
    ```zsh
    poetry install
    ```

1. Start a shell
    ```zsh
    poetry shell
    ```

## Run test app

Attime of writing, the test app is a FastAPI app

```zsh
docker-compose up --build
```
