# type: ignore
from pathlib import Path

from invoke import task
from logzero import logger

# Note that type definitions don't work well with `invoke` library yet so we exclude this file from
# mypy. See https://github.com/pyinvoke/invoke/issues/357


@task
def isort(ctx):
    logger.info("running isort - automatic imports ordering")
    ctx.run("isort --apply")


@task
def black(ctx):
    logger.info("running black - automatic code reformatting")
    ctx.run("black .")


@task
def pytest(ctx):
    logger.info("running pytest - unit testing")
    ctx.run("pytest")


@task
def mypy(ctx):
    logger.info("running mypy - type checking")
    ctx.run("mypy")


@task
def safety(ctx):
    logger.info("running safety - dependencies vulnerability check")
    ctx.run("safety check --full-report")


@task
def bandit(ctx):
    logger.info("running bandit - code security check")
    ctx.run("bandit --recursive --ini .bandit")


@task
def flake8(ctx):
    logger.info("running flake8 - linting")
    ctx.run("flake8 --benchmark")


@task
def detect_secrets(ctx):
    # See https://github.com/Yelp/detect-secrets for documentation
    logger.info("running detect-secrets - code check for hardcoded secrets")
    ctx.run("detect-secrets-hook --baseline .secrets.baseline $(git ls-files)")


@task(
    pre=[isort, black, safety, bandit, detect_secrets, flake8, mypy, pytest]
)  # noqa: WPS125 can use `all` name
def all(ctx):
    logger.info("running all validation tasks")


@task
def dependency_check(ctx):
    logger.info("running dependency-check - OWASP dependency checker")
    ctx.run("dependency-check --disableAssembly --enableExperimental --out build --scan .")
    report_file = Path("build/dependency-check-report.html")
    logger.info(f"Report file should be at {report_file}. Trying to open it in the browser.")
    ctx.run(f"start {report_file} || open {report_file} || xdg-open {report_file}")
