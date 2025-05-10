from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPOk

from .options_view import create_response

from .utils.utils import serialize_sqlalchemy_object
from ..services.product_service import ProductService
from .utils.auth_middleware import requiere_autenticacion, requiere_admin

@view_config(route_name='listar_productos', renderer='json', request_method='GET')
def listar_productos(request):
    print(f"Origin: {request.headers.get('Origin')}")
    service = ProductService(request.dbsession)
    productos = service.listar_productos()
    return create_response([serialize_sqlalchemy_object(producto) for producto in productos], 200)


@view_config(route_name='obtener_producto', renderer='json', request_method='GET')
def obtener_productos(request):
    producto_id = request.matchdict.get('id')
    service = ProductService(request.dbsession)
    producto = service.obtener_producto(producto_id)
    if not producto:
        return create_response({'error': 'Producto no encontrado'}, 404)
    
    return create_response(serialize_sqlalchemy_object(producto), 200)


@view_config(route_name='crear_producto', renderer='json', request_method='POST')
@requiere_autenticacion
@requiere_admin
def crear_productos(context, request):
    try:
        data = request.json_body
        service = ProductService(request.dbsession)
        producto = service.crear_producto(data)
        return create_response(serialize_sqlalchemy_object(producto), 200)
    except Exception as e:
        return create_response({"error": str(e)}, 404)
    

@view_config(route_name='actualizar_producto', renderer='json', request_method='PUT')
@requiere_autenticacion
@requiere_admin
def actualizar_productos(context, request):
    producto_id = request.matchdict.get('id')
    try:
        data = request.json_body
        service = ProductService(request.dbsession)
        producto = service.actualizar_producto(producto_id, data)
        if not producto:
            return create_response({'error': 'Producto no encontrado'}, 404)
        
        return create_response(serialize_sqlalchemy_object(producto), 200)
    except Exception as e:
        return create_response({'error': str(e)}, 404)
    

@view_config(route_name='eliminar_producto', renderer='json', request_method='DELETE')
@requiere_autenticacion
@requiere_admin
def eliminar_productos(context, request):
    producto_id = request.matchdict.get('id')
    service = ProductService(request.dbsession)
    producto = service.eliminar_producto(producto_id)
    if not producto:
        return create_response({'error': 'Producto no encontrado'}, 404)
    
    return create_response({'message': 'Producto eliminado', 
                             'Producto': serialize_sqlalchemy_object(producto)}, 200)
