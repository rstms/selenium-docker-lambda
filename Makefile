# selenium-docker-lambda makefile

PROJECT=nfatools

build:
	docker-compose build

rebuild:
	docker-compose build --no-cache

start: build
	docker-compose up -d

stop:
	docker-compose down --remove-orphans

restart: stop start

shell:
	docker-compose run ${PROJECT} bash -l

exec:
	docker-compose exec ${PROJECT} bash -l

tail:
	docker-compose logs -f ${PROJECT}

ps:
	docker-compose ps

dev:
	$(if $(shell docker-compose ps -q ${PROJECT}),,$(error The ${PROJECT} service must be running!))
	docker-compose stop ${PROJECT}
	docker-compose -f docker-compose.yaml -f dev.yaml run ${PROJECT}-dev $(if ${CMD},bash -l -c '${CMD}',bash -l)
	docker-compose start ${PROJECT}

dev-old: 
	$(if $(shell docker-compose ps -q ${PROJECT}),,$(error The ${PROJECT} service must be running!))
	mkdir -p tmp
	docker-compose stop ${PROJECT}
	docker-compose run \
      --no-deps \
	  --rm \
	  --name ${PROJECT}_dev \
      -v $${HOME}/.vimrc:/home/${PROJECT}/.vimrc \
	  -v $$(pwd)/${PROJECT}/src/nfatools:/home/${PROJECT}/nfatools \
	  ${PROJECT} $(if ${CMD},bash -l -c '${CMD}',bash -l)
	docker-compose start ${PROJECT}

#	  -v $$(pwd)/dev/dot-profile:/home/${USER}/.profile \
#	  -v $$(pwd)/tmp:/tmp \

install-aws-cli:
	sudo pip3 install --upgrade pip && sudo pip3 install --upgrade awscli

# Remove temporary and development files
clean:
	rm -f .fmt
	find . -type f -name *.pyc -exec rm -f \{\} \;
	find . -type d -name __pycache__ -exec rm -rf \{\} \;
	find . -name *.egg-info -exec rm -rf \{\} \;
	rm -rf tmp
	rm -f notes

# Reformat all changed python sources 
fmt: $(shell find nfatools/home/src -type f -name *.py $$([ -e ".fmt" ] && echo ' -newer .fmt'))
	@for S in $?; do yapf --in-place --verbose $$S || exit; done
	@touch .fmt
