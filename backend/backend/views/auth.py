from pyramid.view import view_config
from pyramid.httpexceptions import HTTPUnauthorized, HTTPBadRequest, HTTPOk
from ..services.auth_service import AuthService
from .utils.token_blacklist import agregar_token_a_blacklist
from datetime import datetime
import logging
log = logging.getLogger(__name__)

@view_config(route_name='login', renderer='json', request_method='POST')
def login(request):
    try:
        data = request.json_body
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return HTTPBadRequest(json_body={"error": "Email y contraseña son requeridos"})

        auth_service = AuthService(request.dbsession)
        usuario = auth_service.autenticar_usuario(email, password)

        if not usuario:
            return HTTPUnauthorized(json_body={"error": "Credenciales inválidas"})

        token = auth_service.generar_token(usuario)
        return {"token": token, "es_admin": usuario.es_admin}
    except Exception as e:
        return HTTPBadRequest(json_body={"error": str(e)})


@view_config(route_name='logout', renderer='json', request_method='POST')
def logout(request):
    token = request.headers.get("Authorization")
    if not token:
        return HTTPUnauthorized(json_body={"error": "Token no proporcionado"})

    try:
        auth_service = AuthService(request.dbsession)
        payload = auth_service.verificar_token(token)

        # Agregar el token a la lista negra
        exp = datetime.utcfromtimestamp(payload["exp"])
        agregar_token_a_blacklist(token, exp)

        return HTTPOk(json_body={"message": "Sesión cerrada exitosamente"})
    except Exception as e:
        return HTTPUnauthorized(json_body={"error": str(e)})