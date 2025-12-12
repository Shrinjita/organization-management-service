.PHONY: help install test run clean docker-up docker-down docker-build lint format

help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  test       Run tests"
	@echo "  run        Run the application"
	@echo "  clean      Clean up temporary files"
	@echo "  docker-up  Start Docker containers"
	@echo "  docker-down Stop Docker containers"
	@echo "  docker-build Build Docker image"
	@echo "  lint       Run code linting"
	@echo "  format     Format code with black"

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=src --cov-report=html

run:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/ .pytest_cache/ .coverage

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-build:
	docker-compose build

docker-logs:
	docker-compose logs -f

lint:
	flake8 src/ tests/ --max-line-length=88
	mypy src/

format:
	black src/ tests/ main.py