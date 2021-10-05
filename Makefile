ENV_FILE	?=	.env

.PHONY: build

build: $(ENV_FILE)
	@docker build -t erin .
