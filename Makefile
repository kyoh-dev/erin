ENV_FILE ?= .env

.PHONY: start clean deploy

start: $(ENV_FILE)
	@docker-compose up

clean: $(ENV_FILE)
	@docker-compose down --volumes --rmi all

$(ENV_FILE):
	@cp -v $(ENV_FILE).example $(ENV_FILE)
