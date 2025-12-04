#!/bin/bash
ruff check --fix-only ./src
ruff format ./src
ruff check ./src
mypy --strict ./src