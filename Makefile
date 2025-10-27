PYTHON?=python3
VENV?=.venv
PIP?=$(VENV)/bin/python -m pip

# Default target
.PHONY: help install venv clean-venv

help:
	@echo "Available targets:"
	@echo "  install      Create a venv (default .venv) and install dependencies"
	@echo "  venv         Create the virtualenv only"
	@echo "  clean-venv   Remove the virtualenv directory"

venv:
	@echo "Ensuring virtualenv $(VENV) exists..."
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
		echo "Created virtualenv at $(VENV)"; \
	else \
		echo "Virtualenv $(VENV) already exists"; \
	fi

install: venv
	@echo "Installing from requirements.in into $(VENV)..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.in

clean-venv:
	@echo "Removing virtualenv directory $(VENV)..."
	@rm -rf $(VENV)
