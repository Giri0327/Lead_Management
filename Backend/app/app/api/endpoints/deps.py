from fastapi.security import HTTPBearer
from fastapi import Depends
from app.core.security import decode_token
import jwt
from fastapi import HTTPException

security = HTTPBearer()

def get_current_user(token=Depends(security)):

    try:
        actual_token = token.credentials
        user = decode_token(actual_token)

        return user

    except jwt.PyJWTError:

        raise HTTPException(status_code=401 , detail="invalid token")
