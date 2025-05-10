import jwt
import datetime
from sqlalchemy.exc import SQLAlchemyError
from ..models.modelsBase import Usuario
import logging
log = logging.getLogger(__name__)

SECRET_KEY = "your_secret_key"  # Cambia esto por una clave segura

class AuthService:
    def __init__(self, dbsession):
        self.dbsession = dbsession

    def autenticar_usuario(self, email, password):
        usuario = self.dbsession.query(Usuario).filter(Usuario.email == email).first()
        if usuario and usuario.password == password: 
            return usuario
        return None

    def generar_token(self, usuario):
        payload = {
            "id": usuario.id,
            "email": usuario.email,
            "es_admin": usuario.es_admin,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        # En el middleware
        log.debug(f"Payload del token: {payload}")
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    def verificar_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("El token ha expirado")
        except jwt.InvalidTokenError:
            raise Exception("Token inválido")