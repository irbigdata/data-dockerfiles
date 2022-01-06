#!make

all: restart logs

up: .env
	@echo "===== Docker up ====="
	docker-compose up

down: .env
	@echo "===== Docker down ====="
	docker-compose down --remove-orphans

start: .env
	@echo "===== Docker start ====="
	docker-compose up -d

stop: .env
	@echo "===== Docker stop ====="
	docker-compose stop

restart: .env
	@echo "===== Docker restart ====="
	make down
	make start

remove: stop
	@echo "===== Remove containers ====="
	docker-compose rm -f

logs: .env
	@echo "===== Docker logs ====="
	docker-compose logs -f

run: .env
	@echo "===== Docker run container ====="
	docker-compose run --rm redis bash

exec: .env
	@echo "===== Docker exec container ====="
	docker-compose exec redis sh

execit: .env
	@echo "===== Docker exec container ====="
	docker-compose exec -it redis sh

stats:
	@echo "===== Docker stats ====="
	docker stats

ps:
	@echo "===== Print state of containers ====="
	docker-compose ps
