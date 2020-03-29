# Colorado Site Checker

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

### Running the application

To run the first part which checks sites and pushes messages to Kafka queue:

```bash
./sitechecker/sitechecker.py
```

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

## Security

Besides Python-based security checkers (included in `inv all`) this project comes with integration
for [dependency-check](https://pypi.org/project/dependency-check/) dependencies vulnerability
scanning tool.

`dependency-check` is not precise enough to work in unattended mode. You need to manually and
regularly run it, review its output and take actions. Therefore `dependency-check` is not included
in `inv all` task.

Prerequisite:

* Java - <https://adoptopenjdk.net/>.

Running:

```bash
inv dependency-check
```
