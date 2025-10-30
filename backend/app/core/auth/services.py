from jose import jwt, JWTError
from datetime import datetime, timedelta
# Remova a importação de User se não for usada diretamente aqui
# from app.core.users.models import User

# --- Importe a configuração ---
from app import config as app_config

# --- Use as variáveis importadas ---
SECRET_KEY = app_config.SECRET_KEY
ALGORITHM = app_config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = app_config.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    '''Cria um novo token JWT'''
    to_encode = data.copy()

    # Define o tempo de expiração
    # Use ACCESS_TOKEN_EXPIRE_MINUTES importado
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Cria o token
    # Use SECRET_KEY e ALGORITHM importados
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict | None:
    '''Decodifica um token, retornando o payload (os dados) se for válido'''
    try:
        # Use SECRET_KEY e ALGORITHM importados
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None