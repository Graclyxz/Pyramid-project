from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPOk
from ..services.user_service import UserService

@view_config(route_name='listar_usuarios', renderer='json', request_method='GET')
def listar_usuarios(request):
    service = UserService(request.dbsession)
    usuarios = service.listar_usuarios()
    
    # Convierte cada objeto Usuario en un diccionario
    usuarios_dict = [
        {key: value for key, value in usuario.__dict__.items() if not key.startswith('_')}
        for usuario in usuarios
    ]
    
    return usuarios_dict

@view_config(route_name='obtener_usuario', renderer='json', request_method='GET')
def obtener_usuario(request):
    usuario_id = request.matchdict.get('id')
    service = UserService(request.dbsession)
    usuario = service.obtener_usuario(usuario_id)
    if not usuario:
        return HTTPNotFound(json_body={'error': 'Usuario no encontrado'})
    
    # Convierte el objeto en un diccionario serializable
    usuario_dict = {key: value for key, value in usuario.__dict__.items() if not key.startswith('_')}
    return usuario_dict

@view_config(route_name='crear_usuario', renderer='json', request_method='POST')
def crear_usuario(request):
    try:
        data = request.json_body
        service = UserService(request.dbsession)
        usuario = service.crear_usuario(data)        
        # Convierte el objeto en un diccionario serializable
        usuario_dict = {key: value for key, value in usuario.__dict__.items() if not key.startswith('_')}
        return usuario_dict
    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})

@view_config(route_name='actualizar_usuario', renderer='json', request_method='PUT')
def actualizar_usuario(request):
    usuario_id = request.matchdict.get('id')
    try:
        data = request.json_body
        service = UserService(request.dbsession)
        usuario = service.actualizar_usuario(usuario_id, data)
        if not usuario:
            return HTTPNotFound(json_body={'error': 'Usuario no encontrado'})
        usuario_dict = {key: value for key, value in usuario.__dict__.items() if not key.startswith('_')}
        return usuario_dict
    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})

@view_config(route_name='eliminar_usuario', renderer='json', request_method='DELETE')
def eliminar_usuario(request):
    usuario_id = request.matchdict.get('id')
    service = UserService(request.dbsession)
    usuario = service.eliminar_usuario(usuario_id)
    if not usuario:
        return HTTPNotFound(json_body={'error': 'Usuario no encontrado'})
    return HTTPOk(json_body={'message': 'Usuario eliminado'})