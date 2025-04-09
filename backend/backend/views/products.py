from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPOk

from .utils.utils import serialize_sqlalchemy_object
from ..services.product_service import ProductService
from .utils.auth_middleware import requiere_autenticacion, requiere_admin

@view_config(route_name='listar_productos', renderer='json', request_method='GET')
def listar_productos(request):
    service = ProductService(request.dbsession)
    productos = service.listar_productos()
    return [serialize_sqlalchemy_object(producto) for producto in productos]


@view_config(route_name='obtener_producto', renderer='json', request_method='GET')
def obtener_productos(request):
    producto_id = request.matchdict.get('id')
    service = ProductService(request.dbsession)
    producto = service.obtener_producto(producto_id)
    if not producto:
        return HTTPNotFound(json_body={'error': 'Producto no encontrado'})
    
    return serialize_sqlalchemy_object(producto)


@view_config(route_name='crear_producto', renderer='json', request_method='POST')
@requiere_autenticacion
@requiere_admin
def crear_productos(request):
    try:
        data = request.json_body
        service = ProductService(request.dbsession)
        producto = service.crear_producto(data)
        return serialize_sqlalchemy_object(producto)
    except Exception as e:
        return HTTPBadRequest(json_body={"error": str(e)})
    

@view_config(route_name='actualizar_producto', renderer='json', request_method='PUT')
@requiere_autenticacion
@requiere_admin
def actualizar_productos(request):
    producto_id = request.matchdict.get('id')
    try:
        data = request.json_body
        service = ProductService(request.dbsession)
        producto = service.actualizar_producto(producto_id, data)
        if not producto:
            return HTTPNotFound(json_body={'error': 'Producto no encontrado'})
        
        return serialize_sqlalchemy_object(producto)
    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})
    

@view_config(route_name='eliminar_producto', renderer='json', request_method='DELETE')
@requiere_autenticacion
@requiere_admin
def eliminar_productos(request):
    producto_id = request.matchdict.get('id')
    service = ProductService(request.dbsession)
    producto = service.eliminar_producto(producto_id)
    if not producto:
        return HTTPNotFound(json_body={'error': 'Producto no encontrado'})
    
    return HTTPOk(json_body={'message': 'Producto eliminado', 
                             'Producto': serialize_sqlalchemy_object(producto)})
