from datetime import datetime, timedelta
from tokenize import Token

from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import Depends
from app.core.security import decode_token
import jwt
from fastapi import HTTPException,status
from app.db import get_db,session
from app.models import Token

INACTIVITY_LIMIT = timedelta(hours=1)
#INACTIVITY_LIMIT = timedelta(minutes=1)

security = HTTPBearer()
def get_current_user(token: HTTPAuthorizationCredentials = Depends(security),db:session=Depends(get_db)):

    actual_token = token.credentials
    
    try:
        user = decode_token(actual_token)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        
        sessionn = db.query(Token).filter(
            Token.Token == actual_token,
            Token.update_At == None).first()
        
        if not sessionn:
            raise HTTPException(
                status_code=401,
                detail="Session not found"
            )
        
        if datetime.now() - sessionn.Token_Expiry > INACTIVITY_LIMIT:

            sessionn.update_At = datetime.now()
            db.commit()

            raise HTTPException(
                status_code=401,
                detail="Session expired due to inactivity"
            )
        sessionn.Token_Expiry = datetime.now()
        db.commit()

        return user
    
    except jwt.ExpiredSignatureError:

    # token expired → update logout_time
        sessionn = db.query(Token).filter(
            Token.Token == actual_token).first()

        if sessionn and not sessionn.update_At:
            sessionn.update_At = datetime.now()
            db.commit()
        

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )    

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