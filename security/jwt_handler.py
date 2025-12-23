   # crear/validar tokens JWT
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 30  # minutos
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"

def create_acess_token(username: str) -> str:
    """#funcion para crear un token de acceso JWT"""
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
    payload = {"exp": expire, "sub": username}
    encoded_jwt = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> str | None:
    """#funcion para decodificar un token de acceso JWT"""
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None