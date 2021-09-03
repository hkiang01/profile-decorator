# profile-decorator

## Problem/Motivation

Find memory leaks in Python code quickly without significant code changes in a quickly digestible manner such that the root cause can be easily diagnosed.

Until open-telemetry [Adds metrics API](https://github.com/open-telemetry/opentelemetry-python/pull/1887), I want a quick and dirty decorator that will give me the  memory usage of the process in scope before and after a function is run.

## Usage

```python
# example.py
from profile_decorator import profile_decorator

profile_decorator.init()


@profile_decorator.profile_memory
def my_func():
    print("hello, world")


if __name__ == "__main__":
    my_func()
```

```zsh
$ poetry run python example.py
hello, world
{
  "id": "eac7b07c-0c48-4ffe-923d-00ba426a146c",
  "function": "my_func",
  "file": "/home/harry/projects/GitHub/hkiang01/profile-decorator/example.py",
  "filename": "example.py",
  "start_time": "2021-08-31T23:06:04.873367",
  "uss_memory_before": 7110656,
  "end_time": "2021-08-31T23:06:04.874252",
  "uss_memory_after": 7258112,
  "lines": [
    {
      "filename": "/home/harry/projects/GitHub/hkiang01/profile-decorator/example.py",
      "lineno": 7,
      "size": 752,
      "size_diff": 0
    },
    {
      "filename": "/home/harry/projects/GitHub/hkiang01/profile-decorator/example.py",
      "lineno": 12,
      "size": 560,
      "size_diff": 0
    }
  ]
}
```

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
