ENV_FILE	?=	.env

.PHONY: build start clean

build: $(ENV_FILE)
	@docker build -t erin .
