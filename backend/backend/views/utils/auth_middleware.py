from pyramid.httpexceptions import HTTPUnauthorized, HTTPForbidden
from ...services.auth_service import AuthService
from ..utils.token_blacklist import es_token_revocado

def requiere_autenticacion(func):
    def wrapper(context, request):
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPUnauthorized(json_body={"error": "Token no proporcionado"})

        # Verificar si el token está revocado
        if es_token_revocado(token):
            raise HTTPUnauthorized(json_body={"error": "Token revocado. Inicia sesión nuevamente."})

        auth_service = AuthService(request.dbsession)
        try:
            payload = auth_service.verificar_token(token)
            request.usuario = payload
        except Exception as e:
            raise HTTPUnauthorized(json_body={"error": str(e)})

        return func(context, request)
    return wrapper

def requiere_admin(func):
    def wrapper(context, request):
        if not getattr(request, "usuario", {}).get("es_admin", False):
            raise HTTPForbidden(json_body={"error": "Acceso denegado"})
        return func(context, request)
    return wrapper