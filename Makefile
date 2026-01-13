.PHONY: test-vendas test-suporte test-suporte-frontend test-whatsapp test-whatsapp-frontend test-all up down logs

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

test-vendas:
	docker-compose --profile test run --rm test-vendas

test-suporte:
	docker-compose --profile test run --rm test-suporte

test-suporte-frontend:
	docker-compose --profile test run --rm test-suporte-frontend

test-whatsapp:
	docker-compose --profile test run --rm test-whatsapp

test-whatsapp-frontend:
	docker-compose --profile test run --rm test-whatsapp-frontend

test-all: test-vendas test-suporte test-suporte-frontend test-whatsapp test-whatsapp-frontend
	@echo "✅ Todos os testes executados"
