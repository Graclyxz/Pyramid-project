from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPOk

from ..views.utils.auth_middleware import requiere_autenticacion
from .utils.utils import serialize_sqlalchemy_object
from ..services.order_detail_service import OrderDetailService


@view_config(route_name='listar_detalles_pedido', renderer='json', request_method='GET')
@requiere_autenticacion
def listar_detalles_pedido(request):
    service = OrderDetailService(request.dbsession)
    detallepedidos = service.listar_detalles_pedido()
    
    # Usa la función auxiliar para serializar cada detalle
    detalles_dict = [serialize_sqlalchemy_object(detallepedido) for detallepedido in detallepedidos]
    
    return detalles_dict


@view_config(route_name='obtener_detalle_pedido', renderer='json', request_method='GET')
@requiere_autenticacion
def obtener_detalle_pedido(request):
    detallepedido_id = request.matchdict.get('id')
    service = OrderDetailService(request.dbsession)
    detallepedido = service.obtener_detalle_pedido(detallepedido_id)
    if not detallepedido:
        return HTTPNotFound(json_body={'error': 'Detalle de pedido no encontrado'})
    
    # Usa la función auxiliar para serializar el detalle
    detalle_dict = serialize_sqlalchemy_object(detallepedido)
    return detalle_dict


@view_config(route_name='crear_detalle_pedido', renderer='json', request_method='POST')
@requiere_autenticacion
def crear_detalle_pedido(request):
    try:
        data = request.json_body
        service = OrderDetailService(request.dbsession)
        detallepedido = service.crear_detalle_pedido(data)
        
        # Usa la función auxiliar para serializar el detalle
        detalle_dict = serialize_sqlalchemy_object(detallepedido)
        return detalle_dict
    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})
    

@view_config(route_name='actualizar_detalle_pedido', renderer='json', request_method='PUT')
@requiere_autenticacion
def actualizar_detalle_pedido(request):
    detallepedido_id = request.matchdict.get('id')
    try:
        data = request.json_body
        service = OrderDetailService(request.dbsession)
        detallepedido = service.actualizar_detalle_pedido(detallepedido_id, data)
        if not detallepedido:
            return HTTPNotFound(json_body={'error': 'Detalle de pedido no encontrado'})
        
        # Usa la función auxiliar para serializar el detalle
        detalle_dict = serialize_sqlalchemy_object(detallepedido)
        return detalle_dict
    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})
    

@view_config(route_name='eliminar_detalle_pedido', renderer='json', request_method='DELETE')
@requiere_autenticacion
def eliminar_detalle_pedido(request):
    detallepedido_id = request.matchdict.get('id')
    service = OrderDetailService(request.dbsession)
    detallepedido = service.eliminar_detalle_pedido(detallepedido_id)
    if not detallepedido:
        return HTTPNotFound(json_body={'error': 'Detalle de pedido no encontrado'})
    
    # Usa la función auxiliar para serializar el detalle
    detalle_dict = serialize_sqlalchemy_object(detallepedido)
    return HTTPOk(json_body={'message': 'Detalle de pedido eliminado', 'Detalle de pedido': detalle_dict})
