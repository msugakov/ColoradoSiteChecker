# Colorad Site Checker

Q: What is this?
A: A secrecy project for now.

## Prerequisites

* pyenv for python version management - <https://github.com/pyenv/pyenv#installation>.
* poetry for dependencies management - <https://python-poetry.org/docs/#installation>.

## Development

### First run

* Clone repository.
* Run `poetry install`.

### Using python and command line tools

* Either prefix commands with `poetry run` like `poetry run python ...`, `poetry run pytest`
* or enter virtual environment shell with `poetry shell` and run any commands there without
prefixing, e.g. just `python ...`, `pytest`.

The following assumes you use either of two options to run the suggested commands.

### Testing

Simply run all tests with

```bash
pytest
```

Run tests in continuous watch mode with

```bash
ptw
```

### Testing, linting, type checks, code formatting

This repository comes with tools for all of that.
Use the following command to run them all at once:

```bash
inv all
```

The definitions of tasks come from `tasks.py` file in the root of this repository. You can also
list available tasks with `inv --list`.
