from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPOk

from ..views.utils.auth_middleware import requiere_autenticacion
from .utils.utils import serialize_sqlalchemy_object
from ..services.order_detail_service import OrderDetailService


@view_config(route_name='listar_detalles_pedido', renderer='json', request_method='GET')
@requiere_autenticacion
def listar_detalles_pedido(context, request):
    pedido_id = request.params.get('pedido_id')
    service = OrderDetailService(request.dbsession)

    if not pedido_id:
        return HTTPBadRequest(json_body={'error': 'pedido_id es requerido'})

    detalles = service.listar_detalles_pedido_por_pedido(pedido_id)

    # Calcula el total del pedido
    total = sum(detalle.cantidad * float(detalle.precio_unitario) for detalle in detalles)

    # Serializa los detalles
    detalles_dict = [
        {
            "id": detalle.id,
            "pedido_id": detalle.pedido_id,
            "producto_id": detalle.producto_id,
            "producto_nombre": detalle.producto.nombre,
            "cantidad": detalle.cantidad,
            "precio_unitario": float(detalle.precio_unitario),
        }
        for detalle in detalles
    ]

    return {"detalles": detalles_dict, "total": total}


@view_config(route_name='obtener_detalle_pedido', renderer='json', request_method='GET')
@requiere_autenticacion
def obtener_detalle_pedido(context, request):
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
def crear_detalle_pedido(context, request):
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
def actualizar_detalle_pedido(context, request):
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
def eliminar_detalle_pedido(context, request):
    detallepedido_id = request.matchdict.get('id')
    service = OrderDetailService(request.dbsession)
    try:
        detallepedido = service.eliminar_detalle_pedido(detallepedido_id)
        if not detallepedido:
            return HTTPNotFound(json_body={'error': 'Detalle de pedido no encontrado'})

        # Recalcular el total del pedido
        service.actualizar_total_pedido(detallepedido.pedido_id)

        return HTTPOk(json_body={'message': 'Detalle de pedido eliminado'})
    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})
