import os

APP_ENV = os.getenv('APP_ENV', 'devlopment')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'postgres')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'ecomerce')
TEST_DATABASE_NAME = os.getenv('DATABASE_NAME', 'ecomerce_test')

# ---- JWT Config (CORRIGIDO) ----

# Lê a SECRET_KEY do ambiente, ou usa a padrão (insegura)
SECRET_KEY = os.getenv('SECRET_KEY', 'sua_chave_secreta_padrao_aqui')

# Lê o ALGORITHM do ambiente, ou usa "HS256" como padrão
ALGORITHM = os.getenv('ALGORITHM', 'HS256')

# Lê o tempo de expiração do ambiente, ou usa 30 minutos como padrão
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))

# --- Configurações do Redis (Adicionadas) ---
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))