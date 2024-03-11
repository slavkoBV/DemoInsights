
build:
	docker-compose build

run:
	docker-compose up

app-shell:
	docker-compose run app /bin/bash

test:
	docker-compose run app pytest --cov=/app
