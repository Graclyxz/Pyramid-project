from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPOk

from .options_view import create_response

from ..views.utils.auth_middleware import requiere_autenticacion, requiere_admin
from .utils.utils import serialize_sqlalchemy_object
from ..services.user_service import UserService

@view_config(route_name='listar_usuarios', renderer='json', request_method='GET')
@requiere_autenticacion
@requiere_admin
def listar_usuarios(context, request):  # Agrega el argumento 'context'
    service = UserService(request.dbsession)
    usuarios = service.listar_usuarios()
    
    # Usa la función auxiliar para serializar cada usuario
    usuarios_dict = [serialize_sqlalchemy_object(usuario) for usuario in usuarios]
    return create_response(usuarios_dict, 200)

@view_config(route_name='obtener_usuario', renderer='json', request_method='GET')
@requiere_autenticacion
@requiere_admin
def obtener_usuario(context, request):
    usuario_id = request.matchdict.get('id')
    service = UserService(request.dbsession)
    usuario = service.obtener_usuario(usuario_id)
    if not usuario:
        return create_response({'error': 'Usuario no encontrado'}, 404)

    # Usa la función auxiliar para serializar cada pedido
    usuarios_dict = serialize_sqlalchemy_object(usuario)
    return create_response(usuarios_dict, 200)

@view_config(route_name='crear_usuario', renderer='json', request_method='POST')
def crear_usuario(context, request):
    try:
        data = request.json_body
        service = UserService(request.dbsession)
        usuario = service.crear_usuario(data)        
        # Usa la función auxiliar para serializar cada pedido
        usuarios_dict = serialize_sqlalchemy_object(usuario)
        return create_response(usuarios_dict, 200)
    except Exception as e:
        return create_response({'error': str(e)}, 404)

@view_config(route_name='actualizar_usuario', renderer='json', request_method='PUT')
@requiere_autenticacion
def actualizar_usuario(context, request):
    usuario_id = request.matchdict.get('id')
    try:
        data = request.json_body
        service = UserService(request.dbsession)
        usuario = service.actualizar_usuario(usuario_id, data)
        if not usuario:
            return create_response({'error': 'Usuario no encontrado'}, 404)
        # Usa la función auxiliar para serializar cada pedido
        usuarios_dict = serialize_sqlalchemy_object(usuario)
        return create_response(usuarios_dict, 200)
    except Exception as e:
        return create_response({'error': str(e)}, 404)

@view_config(route_name='eliminar_usuario', renderer='json', request_method='DELETE')
@requiere_autenticacion
@requiere_admin
def eliminar_usuario(context, request):
    usuario_id = request.matchdict.get('id')
    service = UserService(request.dbsession)
    usuario = service.eliminar_usuario(usuario_id)
    if not usuario:
        return create_response({'error': 'Usuario no encontrado'}, 404)
    # Usa la función auxiliar para serializar el pedido
    usuarios_dict = serialize_sqlalchemy_object(usuario)
    return create_response({'message': 'Usuario eliminado', 'usuario': usuarios_dict}, 200)