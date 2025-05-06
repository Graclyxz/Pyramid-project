from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPOk

from .options_view import create_response

from .utils.utils import serialize_sqlalchemy_object
from ..services.order_service import OrderService
from .utils.auth_middleware import requiere_autenticacion

@view_config(route_name='listar_pedidos', renderer='json', request_method='GET')
@requiere_autenticacion
def listar_pedidos(context, request):
    usuario_id = request.usuario["id"]
    service = OrderService(request.dbsession)
    pedidos = service.listar_pedidos()
    pedidos_usuario = [pedido for pedido in pedidos if pedido.usuario_id == usuario_id]
    return create_response([serialize_sqlalchemy_object(pedido) for pedido in pedidos_usuario], 200)


@view_config(route_name='obtener_pedido', renderer='json', request_method='GET')
def obtener_pedidos(request):
    pedido_id = request.matchdict.get('id')
    service = OrderService(request.dbsession)
    pedido = service.obtener_pedido(pedido_id)
    if not pedido:
        return create_response(HTTPNotFound(json_body={'error': 'Pedido no encontrado'}), 404)
    # Usa la función auxiliar para serializar el pedido
    return create_response(serialize_sqlalchemy_object(pedido), 200)


@view_config(route_name='crear_pedido', renderer='json', request_method='POST')
def crear_pedidos(request):
    try:
        data = request.json_body
        service = OrderService(request.dbsession)
        pedido = service.crear_pedido(data)
        # Usa la función auxiliar para serializar el pedido
        return create_response(serialize_sqlalchemy_object(pedido), 200)
    except Exception as e:
        return create_response({'error': str(e)}, 404)
    

@view_config(route_name='actualizar_pedido', renderer='json', request_method='PUT')
def actualizar_pedidos(context, request):
    pedido_id = request.matchdict.get('id')
    try:
        data = request.json_body
        service = OrderService(request.dbsession)
        pedido = service.actualizar_pedido(pedido_id, data)
        if not pedido:
            return create_response({'error': 'Pedido no encontrado'}, 404)
        # Usa la función auxiliar para serializar el pedido
        return create_response(serialize_sqlalchemy_object(pedido), 200)
    except Exception as e:
        return create_response({'error': str(e)}, 404)
    

@view_config(route_name='eliminar_pedido', renderer='json', request_method='DELETE')
def eliminar_pedidos(context, request):
    pedido_id = request.matchdict.get('id')
    service = OrderService(request.dbsession)
    pedido = service.eliminar_pedido(pedido_id)
    if not pedido:
        return create_response({'error': 'Pedido no encontrado'}, 404)

    # Serializa manualmente el pedido eliminado
    pedido_dict = {
        'id': pedido.id,
        'usuario_id': pedido.usuario_id,
        'total': float(pedido.total),
        'estado': pedido.estado,
        'fecha_pedido': pedido.fecha_pedido.isoformat() if pedido.fecha_pedido else None
    }

    return create_response({'message': 'Pedido eliminado', 'Pedido': pedido_dict}, 200)