#################################################
#  Export OS environment variables
#################################################

export APP_CORS_DOMAINS=localhost:3000
export DB_CONNECTION=sqlite


requirements.txt:
	poetry export -f requirements.txt --output requirements.txt

env:
	! test -s ./.env && cp ./.env.local.sample ./.env

install:
	pip install -r requirements.txt

start:
	uvicorn pyfolio.main:app --reload

start-sqlite:
	rm .env && cp .env.sqlite .env
	uvicorn pyfolio.main:app --reload

start-mysql:
	rm .env && cp .env.mysql .env
	uvicorn pyfolio.main:app --reload

lint:
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

test: lint
	pytest

test-feature: lint
	pytest pyfolio/tests/feature

test-unit: lint
	pytest pyfolio/tests/unit

test-mailer: lint
	pytest pyfolio/tests/unit/apps/mailer pyfolio/tests/unit/services/test_mail_service.py


## Production
start-prod:
	gunicorn -k uvicorn.workers.UvicornWorker pyfolio.main:app

start-prod-multiple-workers:
	gunicorn -k uvicorn.workers.UvicornWorker pyfolio.main:app --workers 4

