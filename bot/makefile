ifeq ($(OS),Windows_NT)
    SET_ENV_DEV = set "ENVIRONMENT=development" &&
    SET_ENV_PROD = set "ENVIRONMENT=production" &&
else
    SET_ENV_DEV = ENVIRONMENT=development
    SET_ENV_PROD = ENVIRONMENT=production
endif

dev:
	$(SET_ENV_DEV) uv run aiogram_run.py

prod:
	$(SET_ENV_PROD) uv run aiogram_run.py