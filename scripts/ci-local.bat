@echo off
REM CI/CD Local - Executa testes sem GitHub Actions (Windows)

echo 🚀 Iniciando CI/CD Local...

REM Backend Tests
echo 📦 Backend: Instalando dependências...
cd backend
pip install -r requirements.txt

echo 🧪 Backend: Executando testes...
python manage.py test

echo 🔒 Backend: Verificando segurança...
bandit -r apps/ -f json -o bandit-report.json
safety check --json

REM Frontend Tests
echo 📦 Frontend: Instalando dependências...
cd ..\frontend
call npm install

echo 🧪 Frontend: Executando testes...
call npm test

echo 🔒 Frontend: Auditoria de segurança...
call npm audit --json

REM Docker Build
echo 🐳 Docker: Build das imagens...
cd ..
docker-compose build

echo ✅ CI/CD Local concluído!
pause
