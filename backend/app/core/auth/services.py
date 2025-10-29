from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.core.users.models import User # Para o payload

# --- PEGUE ISSO DO SEU .env ---
SECRET_KEY = "SUA_SECRET_KEY_MUITO_SECRETA_AQUI" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # Token expira em 1 hora

def create_access_token(data: dict):
    '''Cria um novo token JWT'''
    to_encode = data.copy()
    
    # Define o tempo de expiração
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Cria o token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict | None:
    '''Decodifica um token, retornando o payload (os dados) se for válido'''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None