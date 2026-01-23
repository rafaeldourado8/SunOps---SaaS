.PHONY: up down logs build clean seed

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

build:
	docker-compose build

clean:
	docker-compose down -v

seed:
	docker-compose exec api python seed_premissas.py

users:
	docker-compose exec api python seed_users.py

restart:
	docker-compose restart

ps:
	docker-compose ps

rabbitmq-restart:
	docker-compose restart rabbitmq

rabbitmq-logs:
	docker-compose logs -f rabbitmq
