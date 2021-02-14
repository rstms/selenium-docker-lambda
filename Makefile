# selenium-docker-lambda makefile

PROJECT=moonbat

build:
	docker-compose build

rebuild:
	docker-compose build --no-cache

start:
	docker-compose up -d

stop:
	docker-compose down

shell:
	docker-compose run ${PROJECT} bash -l

exec:
	docker-compose exec selenium bash -l

tail:
	docker-compose logs -f selenium

ps:
	docker-compose ps

dev: 
	$(if $(shell docker-compose ps -q ${PROJECT}),,$(error The ${PROJECT} service must be running!))
	mkdir -p tmp
	@docker-compose stop ${PROJECT}
	@docker-compose run \
	  --no-deps \
	  --rm \
	  --name ${PROJECT}_dev \
	  -v $$(pwd)/src:/home/${USER}/src
	  ${PROJECT} $(if ${CMD},bash -l -c '${CMD}',bash -l)
	@docker-compose start ${PROJECT}

#	  -v $${HOME}/.vimrc:/home/${USER}/.vimrc \
#	  -v $$(pwd)/dev/dot-profile:/home/${USER}/.profile \
#	  -v $$(pwd)/tmp:/tmp \

install-aws-cli:
	sudo pip3 install --upgrade pip && sudo pip3 install --upgrade awscli
