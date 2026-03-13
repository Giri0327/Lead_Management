from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import Depends
from app.core.security import decode_token
import jwt
from fastapi import HTTPException,status

security = HTTPBearer()
def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):

    actual_token = token.credentials
    user = decode_token(actual_token)
    try:
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid token33"
            ) 
        return user
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
def role_required(allowed_roles: list):

    def checker(user=Depends(get_current_user)):

        if user["role"] not in allowed_roles:
            raise HTTPException(status_code=403,
                detail="You are not authorized to perform this action"
            )

        return user

    return checker  