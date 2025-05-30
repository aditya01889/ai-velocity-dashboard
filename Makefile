.PHONY: help install format lint test test-cov clean build run docker-build docker-run docker-down docker-logs

# Default target
help:
	@echo "Available targets:"
	@echo "  install     Install development dependencies"
	@echo "  format      Format code with black and isort"
	@echo "  lint        Check code style with flake8 and mypy"
	@echo "  test        Run tests"
	@echo "  test-cov    Run tests with coverage"
	@echo "  clean       Remove Python file artifacts"
	@echo "  build       Build the Docker image"
	@echo "  run         Run the application locally"
	@echo "  docker-run  Run the application in Docker"
	@echo "  docker-down Stop the Docker containers"
	@echo "  docker-logs Show Docker container logs"

# Install dependencies
install:
	pip install -e .[dev]

# Format code
format:
	black .
	isort .


# Lint code
lint:
	flake8 app tests
	mypy app tests

# Run tests
test:
	pytest tests/

# Run tests with coverage
test-cov:
	pytest --cov=app --cov-report=term-missing --cov-report=html tests/

# Clean up
clean:
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/ build/ dist/ *.egg-info/

# Build Docker image
build:
	docker-compose build

# Run locally
run:
	streamlit run app/main.py

# Run in Docker
docker-run:
	docker-compose up -d

# Stop Docker containers
docker-down:
	docker-compose down

# Show Docker logs
docker-logs:
	docker-compose logs -f
