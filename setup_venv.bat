@echo off

REM Cleaning .venv folder and recreate it
if exist .venv call RMDIR /S /Q .venv
call mkdir .venv

REM Create virtual environment in .venv folder using
REM dependencies defined in pyproject.toml and poetry.lock
call poetry config virtualenvs.in-project true
call poetry install

REM Activate pre-commit hook
call poetry run pre-commit install -t pre-commit
call poetry run pre-commit install -t pre-push
call poetry run pre-commit install -t commit-msg

REM Leave cmd window open for debugging when exit is not successful
if %ERRORLEVEL% NEQ 0 (
	echo [31m Error occured![0m
	pause
)
