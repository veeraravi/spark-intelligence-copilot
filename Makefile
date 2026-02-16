"""Makefile for common development tasks"""

.PHONY: help install dev test coverage lint format clean docker-build docker-up docker-down deploy

help:
	@echo "Spark Intelligence Copilot - Development Commands"
	@echo "=================================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install        Install dependencies"
	@echo "  make dev            Install development dependencies"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test           Run tests"
	@echo "  make coverage       Generate coverage report"
	@echo "  make lint           Run linters (flake8, mypy)"
	@echo "  make format         Format code with black"
	@echo ""
	@echo "Local Development:"
	@echo "  make run            Run application locally"
	@echo "  make docker-build   Build Docker image"
	@echo "  make docker-up      Start Docker containers"
	@echo "  make docker-down    Stop Docker containers"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          Clean build artifacts and cache"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install pytest pytest-asyncio pytest-cov black flake8 mypy

test:
	pytest tests/ -v

coverage:
	pytest tests/ --cov=app --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	flake8 . --max-line-length=100 --exclude=__pycache__,venv,.git
	mypy . --ignore-missing-imports

format:
	black . --line-length=100

run:
	python run.py

docker-build:
	docker build -f infra/docker/Dockerfile -t spark-intelligence-copilot:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache

.DEFAULT_GOAL := help
