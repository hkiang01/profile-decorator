# memory-profiler-viz

## Problem/Motivation

Find memory leaks in Python code quickly without significant code changes in a quickly digestible manner such that the root cause can be easily diagnosed.

Until open-telemetry [Adds metrics API](https://github.com/open-telemetry/opentelemetry-python/pull/1887), I want a quick and dirty decorator that will give me the  memory usage of the process in scope before and after a function is run.

## Design

The decorator will collect the following information:
- name of function
- filepath
- line number
- memory usage before function is run
- timestamp when function is called
- timestamp when function is finished
- memory usage after function is run

It will expose this in json or other easily digestble format for reporting purposes.

## Contributing
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
