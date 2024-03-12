
build:
	docker-compose build

build-macos:
	docker buildx build --platform linux/amd64 -t demoinsights-app:latest --load .

run:
	docker-compose up

app-shell:
	docker-compose run app /bin/bash

test:
	docker-compose run app pytest --cov=/app
