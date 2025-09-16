# Use: `make venv` -> creates .venv
#      `make dev`  -> install package in editable mode with dev deps
#      `make lint` -> check code style
#      `make fmt`  -> apply formatting
#      `make fix`  -> auto-fix lint issues where possible
#      `make typecheck` -> run mypy
#      `make test` -> run pytest
#      `make clean` -> remove caches

# Detect platform-specific venv bin directory
BIN = .venv/bin
ifeq ($(OS),Windows_NT)
	BIN = .venv/Scripts
endif

PYTHON = $(BIN)/python
PIP    = $(BIN)/pip
RUFF   = $(BIN)/ruff
MYPY   = $(BIN)/mypy
PYTEST = $(BIN)/pytest

.PHONY: prepare venv dev lint fmt fix typecheck test clean

venv:
	@if [ ! -d ".venv" ]; then python3 -m venv .venv; fi
	@echo "Created/using virtualenv at .venv"

dev:
	$(PIP) install --upgrade pip
	$(PIP) install -e .[dev]
	@echo "Installed package in editable mode with dev tools."

prepare: venv dev
	@echo "Virtual Environment ready! Run 'source .venv/bin/activate' (Linux/Mac)"

lint:
	$(RUFF) check src tests

fmt:
	$(RUFF) format src tests

fix:
	$(RUFF) check --fix src tests
	$(RUFF) format src tests

typecheck:
	$(MYPY) src

test:
	$(PYTEST)

clean:
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache .mypy_cache .ruff_cache dist build *.egg-info
	@echo "Cleaned build/test caches."
