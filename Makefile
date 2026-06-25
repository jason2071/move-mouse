PYTHON := .venv/bin/python
PIP := uv pip

.PHONY: help setup run gui clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

setup: ## Create venv and install dependencies
	uv venv
	$(PIP) install pyautogui pynput

run: ## Run the CLI mouse mover (use ARGS="--distance 300")
	$(PYTHON) move-mouse.py $(ARGS)

gui: ## Run the GUI
	$(PYTHON) gui.py

clean: ## Remove venv and caches
	rm -rf .venv __pycache__
