from pyramid.config import Configurator
from pyramid.response import Response
from backend.routes import includeme

def add_cors_tween(handler, registry):
    def cors_tween(request):
        if request.method == 'OPTIONS':
            origin = request.headers.get('Origin')
            allowed_origins = [
                "http://localhost:3000"
            ]
            if origin in allowed_origins:
                headers = {
                    'Access-Control-Allow-Origin': origin,
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                    'Access-Control-Allow-Credentials': 'true',
                }
                return Response(status=200, headers=headers)
            return Response(status=403, json_body={'error': 'Origin not allowed'})
        return handler(request)
    return cors_tween

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
"""
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.include('.models')
        config.include(includeme)
        config.add_tween('backend.add_cors_tween')
        config.scan()
    return config.make_wsgi_app()
