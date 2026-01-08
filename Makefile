.PHONY: run check

run:
	uv run python -m gradio app.py

check:
	uv run python -m unittest discover tests
