#!make

all: restart logs

clean:
	@echo "===== Docker up ====="
	docker rm -fv $(docker ps -aq -f "status=exited")

up: .env
	@echo "===== Docker up ====="
	docker-compose -f ./docker-compose.yml up -d

down: .env
	@echo "===== Docker down ====="
	docker-compose down --remove-orphans

downv: .env
	@echo "===== Docker down -v  ====="
	docker-compose down -v --remove-orphans


start: .env
	@echo "===== Docker start ====="
	docker-compose -f ./docker-compose.yml up -d 

stop: .env
	@echo "===== Docker stop ====="
	docker-compose -f ./docker-compose.yml stop

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
	docker-compose run --rm airflow bash

exec: .env
	@echo "===== Docker exec container ====="
	docker-compose exec airflow bash

stats:
	@echo "===== Docker stats ====="
	docker stats

ps:
	@echo "===== Print state of containers ====="
	docker-compose -f ./docker-compose-apache.yml ps
