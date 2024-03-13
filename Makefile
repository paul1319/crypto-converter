.DEFAULT_GOAL := help

DC=docker compose -f tests/docker/docker-compose.tests.yml

export WAIT_IT_TIMEOUT ?= 150

.PHONY: tests
tests:
	@$(DC) up --build --force-recreate -V -d
	@$(DC) logs -ft tests
	@$(DC) down --remove-orphans -v -t0
