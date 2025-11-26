.PHONY: sync check test build clean

sync:
	uv sync --no-editable

check:
	uv run --no-editable basedpyright

test:
	uv run --no-editable pytest

lint:
	uv run --no-editable ruff check

build:
	uv build

clean:
	rm -rf dist/
