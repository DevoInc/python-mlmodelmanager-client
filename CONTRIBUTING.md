# Contributing

If someone is contributing to any Devo open source repository (internal or external), a Contributor License Agreement should be signed: https://cla-assistant.io/DevoInc/

## Development

This package is built and managed using Poetry. It can be downloaded and installed following the guides here [Python-Poetry.org](https://python-poetry.org/).

Once installed git clone this repository and run `poetry install` in the project root. This will install dependencies and devdependencies and you will then be ready to work on the project.

## Testing/Linting

- Type linting: `poetry run mypy <packages>`, `poetry run mypy devo_ml` `poetry run mypy --namespace-packages tests`

- Style linting: `poetry run flake8 <packages>`, `poetry run flake8 devo_ml`

- Testing: `poetry run pytest`

### Built package testing with tox

Install tox with pip.

Run `tox` to run all tests
Run `tox -e lint` to run all linting
