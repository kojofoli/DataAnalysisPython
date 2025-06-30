.PHONY: help install test lint format type-check clean setup-dev run-demo

# Default target
help:
	@echo "Temperature Toolkit - Available commands:"
	@echo ""
	@echo "  setup-dev    - Set up development environment"
	@echo "  install      - Install dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with Black"
	@echo "  type-check   - Run type checking with MyPy"
	@echo "  clean        - Clean up generated files"
	@echo "  run-demo     - Run the main demo"
	@echo "  all          - Run format, lint, type-check, and test"

# Set up development environment
setup-dev:
	@echo "Setting up development environment..."
	python setup_dev.py

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Run tests
test:
	@echo "Running tests..."
	python -m pytest test_temperature_toolkit.py -v

# Run linting
lint:
	@echo "Running linting checks..."
	flake8 .

# Format code
format:
	@echo "Formatting code with Black..."
	black .

# Run type checking
type-check:
	@echo "Running type checking with MyPy..."
	mypy temperature_toolkit/

# Clean up generated files
clean:
	@echo "Cleaning up generated files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

# Run the main demo
run-demo:
	@echo "Running Temperature Toolkit demo..."
	python main.py

# Run all quality checks
all: format lint type-check test
	@echo "All quality checks completed!"

# Install pre-commit hooks
install-hooks:
	@echo "Installing pre-commit hooks..."
	pre-commit install

# Run pre-commit on all files
pre-commit-all:
	@echo "Running pre-commit on all files..."
	pre-commit run --all-files 