ENV_FILE	?=	.env

.PHONY: build start clean

build: $(ENV_FILE)
	@docker build -t erin .

start: $(ENV_FILE)
	@docker-compose -f docker-compose.dev.yml up

clean: $(ENV_FILE)
	@docker-compose -f docker-compose.dev.yml down --volumes --rmi all

$(ENV_FILE):
	@cp -v $(ENV_FILE).example $(ENV_FILE)