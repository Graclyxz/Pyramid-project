from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPOk

from .utils.utils import serialize_sqlalchemy_object
from ..services.order_service import OrderService

@view_config(route_name='listar_pedidos', renderer='json', request_method='GET')
def listar_pedidos(request):
    service = OrderService(request.dbsession)
    pedidos = service.listar_pedidos()
    
    # Usa la función auxiliar para serializar cada pedido
    pedidos_dict = [serialize_sqlalchemy_object(pedido) for pedido in pedidos]
    
    return pedidos_dict

@view_config(route_name='obtener_pedido', renderer='json', request_method='GET')
def obtener_pedidos(request):
    pedido_id = request.matchdict.get('id')
    service = OrderService(request.dbsession)
    pedido = service.obtener_pedido(pedido_id)
    if not pedido:
        return HTTPNotFound(json_body={'error': 'Pedido no encontrado'})
    
    # Usa la función auxiliar para serializar el pedido
    pedido_dict = serialize_sqlalchemy_object(pedido)
    return pedido_dict

@view_config(route_name='crear_pedido', renderer='json', request_method='POST')
def crear_pedidos(request):
    try:
        data = request.json_body
        service = OrderService(request.dbsession)
        pedido = service.crear_pedido(data)
        
        # Usa la función auxiliar para serializar el pedido
        pedido_dict = serialize_sqlalchemy_object(pedido)
        return pedido_dict
    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})
    

@view_config(route_name='actualizar_pedido', renderer='json', request_method='PUT')
def actualizar_pedidos(request):
    pedido_id = request.matchdict.get('id')
    try:
        data = request.json_body
        service = OrderService(request.dbsession)
        pedido = service.actualizar_pedido(pedido_id, data)
        if not pedido:
            return HTTPNotFound(json_body={'error': 'Pedido no encontrado'})
        
        # Usa la función auxiliar para serializar el pedido
        pedido_dict = serialize_sqlalchemy_object(pedido)
        return pedido_dict
    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})
    

@view_config(route_name='eliminar_pedido', renderer='json', request_method='DELETE')
def eliminar_pedidos(request):
    pedido_id = request.matchdict.get('id')
    service = OrderService(request.dbsession)
    pedido = service.eliminar_pedido(pedido_id)
    if not pedido:
        return HTTPNotFound(json_body={'error': 'Pedido no encontrado'})
    
    # Usa la función auxiliar para serializar el pedido
    pedido_dict = serialize_sqlalchemy_object(pedido)
    return HTTPOk(json_body={'message': 'Pedido eliminado', 'Pedido': pedido_dict})