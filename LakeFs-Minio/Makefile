salt = $(shell cat /dev/urandom | base64 | tr -dc A-Za-z0-9 | head -c 16)
bearer_token = $(shell docker-compose run mc admin prometheus generate myminio)
files = .env.local
files += prometheus/prometheus.yml
minio_root_user = admin
minio_root_password = admin123
minio_console_user = console
minio_console_password = console123

up: $(files)
	MINIO_ROOT_USER=$(minio_root_user) \
	MINIO_ROOT_PASSWORD=$(minio_root_password) \
	docker-compose -f ./docker-compose-minio.yml up -d minio prometheus console
	docker-compose --env-file .lakefs-env  -f docker-compose-lakefs.yml up 
	sleep 20
	open http://localhost:8080
	open http://localhost:9000
	open http://localhost:9090

.env.local:
	echo CONSOLE_PBKDF_PASSPHRASE=$(salt) > .env.local
	echo CONSOLE_PBKDF_SALT=$(salt) >> .env.local

init: .env.local
	docker-compose -f ./docker-compose-minio.yml  up -d minio
	docker-compose run mc alias set myminio http://minio:9000 $(minio_root_user) $(minio_root_password)
	docker-compose run mc admin policy add myminio consoleAdmin policy/admin.json
	docker-compose run mc admin user add myminio $(minio_console_user) $(minio_console_password)
	docker-compose run mc admin policy set myminio consoleAdmin user=$(minio_console_user)

clean:
	docker-compose -f ./docker-compose-minio.yml  down -v
	docker-compose --env-file .lakefs-env  -f docker-compose-lakefs.yml down -v 

	rm $(files)

prometheus/prometheus.yml:
	@echo "global:" > $@
	@echo "  scrape_interval:     10s" >> $@
	@echo "  evaluation_interval: 30s" >> $@
	@echo "" >> $@
	@docker-compose -f ./docker-compose-minio.yml run mc admin prometheus generate myminio --no-color >> $@
