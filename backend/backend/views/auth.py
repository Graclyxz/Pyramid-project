from pyramid.view import view_config
from pyramid.httpexceptions import HTTPUnauthorized, HTTPBadRequest, HTTPOk, HTTPNotFound

from .options_view import create_response
from ..services.auth_service import AuthService
from ..services.user_service import UserService
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
            return create_response(HTTPBadRequest(json_body={"error": "Email y contraseña son requeridos"}), 404)

        auth_service = AuthService(request.dbsession)
        usuario = auth_service.autenticar_usuario(email, password)

        if not usuario:
            return create_response(HTTPUnauthorized(json_body={"error": "Credenciales inválidas"}), 404)

        token = auth_service.generar_token(usuario)
        return create_response({"token": token, "es_admin": usuario.es_admin}, 200)
    except Exception as e:
        return create_response(HTTPBadRequest(json_body={"error": str(e)}), 400)


@view_config(route_name='logout', renderer='json', request_method='POST')
def logout(request):
    token = request.headers.get("Authorization")
    if not token:
        return create_response({"error": "Token no proporcionado"}, 404)

    try:
        auth_service = AuthService(request.dbsession)
        payload = auth_service.verificar_token(token)

        # Agregar el token a la lista negra
        exp = datetime.utcfromtimestamp(payload["exp"])
        agregar_token_a_blacklist(token, exp)

        return create_response({"message": "Sesión cerrada exitosamente"}, 200)
    except Exception as e:
        return create_response({"error": str(e)}, 404)


@view_config(route_name='me', renderer='json', request_method='GET')
def obtener_usuario_actual(request):
    # Obtén el token del encabezado Authorization
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return create_response({'error': 'Token no proporcionado o inválido'}, 401)

    token = auth_header.split(' ')[1]

    try:
        # Usa AuthService para verificar y decodificar el token
        auth_service = AuthService(request.dbsession)
        payload = auth_service.verificar_token(token)
        user_id = payload.get('id')

        # Obtén los datos del usuario desde la base de datos
        user_service = UserService(request.dbsession)
        user = user_service.obtener_usuario(user_id)

        if not user:
            return create_response({'error': 'Usuario no encontrado'}, 404)

        # Devuelve los datos del usuario
        return create_response({
            'id': user.id,
            'nombre': user.nombre,
            'email': user.email,
            'telefono': user.telefono,
            'direccion': user.direccion,
            'es_admin': user.es_admin,
        }, 200)
    except Exception as e:
        return create_response({'error': 'Token inválido o expirado'}, 401)