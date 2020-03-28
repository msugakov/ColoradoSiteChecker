# type: ignore
from invoke import task

# Note that type definitions don't work well with `invoke` library yet so we exclude this file from
# mypy. See https://github.com/pyinvoke/invoke/issues/357


@task
def isort(c):
    print("running isort - automatic imports ordering")
    c.run("isort --apply")


@task
def black(c):
    print("running black - automatic code reformatting")
    c.run("black .")


@task
def pytest(c):
    print("running pytest - unit testing")
    c.run("pytest")


@task
def pylama(c):
    print("running pylama - code linting")
    c.run("pylama")


@task
def mypy(c):
    print("running mypy - type checking")
    c.run("mypy")


@task
def safety(c):
    print("running safety - dependencies vulnerability check")
    c.run("safety check --full-report")


@task
def bandit(c):
    print("running bandit - code security check")
    c.run("bandit --recursive --ini .bandit")


@task(pre=[isort, black, pylama, safety, bandit, mypy, pytest])
def all(c):
    pass
