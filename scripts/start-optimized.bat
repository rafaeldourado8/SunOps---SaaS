@echo off
echo ========================================
echo   CRM Solar - Start Otimizado
echo ========================================
echo.

echo [1/4] Parando containers antigos...
docker-compose down

echo.
echo [2/4] Limpando cache Docker...
docker system prune -f

echo.
echo [3/4] Iniciando servicos otimizados...
docker-compose up -d --build

echo.
echo [4/4] Aguardando inicializacao...
timeout /t 10 /nobreak > nul

echo.
echo ========================================
echo   Status dos Servicos
echo ========================================
docker-compose ps

echo.
echo ========================================
echo   URLs Disponiveis
echo ========================================
echo Frontend:  http://localhost:5173
echo Backend:   http://localhost:8000
echo RabbitMQ:  http://localhost:15672 (guest/guest)
echo.
echo ========================================
echo   Comandos Uteis
echo ========================================
echo Ver logs backend:       docker-compose logs -f backend
echo Ver logs celery:        docker-compose logs -f celery_worker
echo Ver logs rabbitmq:      docker-compose logs -f rabbitmq
echo Reiniciar tudo:         docker-compose restart
echo.
pause
