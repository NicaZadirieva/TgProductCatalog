dev:
	uv run --env-file .env.dev fastapi dev app/main.py --host 0.0.0.0 --port 8000 --reload-dir app
prod:
	uv run --env-file .env.prod fastapi dev app/main.py --host 0.0.0.0 --port 8000 --reload-dir app
.PHONY: test
test:
	uv run pytest