init:
	# If you don't have alreaduy serverless installed, uncomment the following line
	# sudo npm install -g serverless
	npm i
	sls plugin install -n serverless-python-requirements --stage dev
	make reset

start:
	python -m local_server.app

reset:
	docker-compose down -v
	docker-compose up -d
	sleep 5
	make migrate

flush:
	python manage.py flush

flush-live:
	python manage.py flush live

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

migrate-live:
	python manage.py migrate live

deploy-dev:
	pipenv run pip freeze > requirements.txt
	sls deploy --stage dev

deploy-prod:
	pipenv run pip freeze > requirements.txt
	sls deploy --stage prod

