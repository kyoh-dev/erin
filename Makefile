ENV_FILE ?= .env

.PHONY: start clean deploy

start: $(ENV_FILE)
	@docker-compose up

clean: $(ENV_FILE)
	@docker-compose down --volumes --rmi all

server:
	@python -m uvicorn main:app --reload

$(ENV_FILE):
	@cp -v $(ENV_FILE).example $(ENV_FILE)
