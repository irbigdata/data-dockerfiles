#!make

all: restart logs

up: .env
	@echo "===== Docker up ====="
	docker-compose up -d

down: .env
	@echo "===== Docker down ====="
	docker-compose down --remove-orphans

downv: .env
	@echo "===== Docker down ====="
	docker-compose down -v --remove-orphans


clean: .env
	@echo "===== Docker down ====="
	docker rm -fv $(docker ps -aq -f "status=exited")

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
	docker-compose run --rm broker bash

exec: .env
	@echo "===== Docker exec container ====="
	docker-compose exec broker bash

stats:
	@echo "===== Docker stats ====="
	docker stats

ps:
	@echo "===== Print state of containers ====="
	docker-compose ps 
