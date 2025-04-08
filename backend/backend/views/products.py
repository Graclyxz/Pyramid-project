from decimal import Decimal
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPOk
from ..services.product_service import ProductService

@view_config(route_name='listar_productos', renderer='json', request_method='GET')
def listar_productos(request):
    service = ProductService(request.dbsession)
    productos = service.listar_productos()
    
    # Convierte cada objeto Producto en un diccionario y maneja los valores Decimal
    productos_dict = [
        {
            key: float(value) if isinstance(value, Decimal) else value
            for key, value in producto.__dict__.items()
            if not key.startswith('_')
        }
        for producto in productos
    ]
    
    return productos_dict

@view_config(route_name='obtener_productos', renderer='json', request_method='GET')
def obtener_productos(request):
    producto_id = request.matchdict.get('id')
    service = ProductService(request.dbsession)
    producto = service.obtener_producto(producto_id)
    if not producto:
        return HTTPNotFound(json_body={'error': 'Producto no encontrado'})
    
    # Convierte el objeto en un diccionario serializable y maneja los valores Decimal
    producto_dict = {
        key: float(value) if isinstance(value, Decimal) else value
        for key, value in producto.__dict__.items()
        if not key.startswith('_')
    }
    return producto_dict

@view_config(route_name='crear_productos', renderer='json', request_method='POST')
def crear_productos(request):
    try:
        data = request.json_body
        service = ProductService(request.dbsession)
        producto = service.crear_producto(data)        
        # Convierte el objeto en un diccionario serializable
        producto_dict = {key: value for key, value in producto.__dict__.items() if not key.startswith('_')}
        return producto_dict
    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})
    
@view_config(route_name='actualizar_productos', renderer='json', request_method='PUT')
def actualizar_productos(request):
    producto_id = request.matchdict.get('id')
    try:
        data = request.json_body
        service = ProductService(request.dbsession)
        producto = service.actualizar_producto(producto_id, data)
        if not producto:
            return HTTPNotFound(json_body={'error': 'Producto no encontrado'})
        producto_dict = {key: value for key, value in producto.__dict__.items() if not key.startswith('_')}
        return producto_dict
    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})
    
@view_config(route_name='eliminar_productos', renderer='json', request_method='DELETE')
def eliminar_productos(request):
    producto_id = request.matchdict.get('id')
    service = ProductService(request.dbsession)
    producto = service.eliminar_producto(producto_id)
    if not producto:
        return HTTPNotFound(json_body={'error': 'Producto no encontrado'})
    
    # Convierte el objeto en un diccionario serializable y maneja los valores Decimal
    producto_dict = {
        key: float(value) if isinstance(value, Decimal) else value
        for key, value in producto.__dict__.items()
        if not key.startswith('_')
    }
    
    return HTTPOk(json_body=producto_dict)
