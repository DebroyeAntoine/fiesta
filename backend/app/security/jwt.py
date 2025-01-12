# security/jwt.py
from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt
from dataclasses import dataclass
from app.config.config import SecurityConfig
from app.exceptions import AuthenticationError

@dataclass
class TokenPair:
    access_token: str
    refresh_token: str
    access_expires: datetime
    refresh_expires: datetime

class JWTManager:
    def __init__(self, config: SecurityConfig):
        self.config = config
        if not config.jwt_secret:
            raise ValueError("JWT secret key is not configured")

    def create_token_pair(self, user_id: int, additional_claims: Optional[Dict] = None) -> TokenPair:
        """Create token access + refresh"""
        now = datetime.utcnow()
        
        claims = additional_claims or {}
        access_expires = now + timedelta(seconds=self.config.jwt_access_expires)
        refresh_expires = now + timedelta(seconds=self.config.jwt_refresh_expires)

        access_token = jwt.encode(
            {
                **claims,
                'sub': str(user_id),
                'exp': access_expires,
                'iat': now,
                'type': 'access'
            },
            self.config.jwt_secret,
            algorithm='HS256'
        )

        refresh_token = jwt.encode(
            {
                'sub': str(user_id),
                'exp': refresh_expires,
                'iat': now,
                'type': 'refresh'
            },
            self.config.jwt_secret,
            algorithm='HS256'
        )

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            access_expires=access_expires,
            refresh_expires=refresh_expires
        )

    def verify_token(self, token: str) -> Dict:
        """Verify and decode token"""
        try:
            payload = jwt.decode(
                token,
                self.config.jwt_secret,
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise AuthenticationError(f"Invalid token: {str(e)}")
