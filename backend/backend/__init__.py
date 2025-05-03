from pyramid.config import Configurator
from pyramid.response import Response

def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        origin = request.headers.get('Origin')
        allowed_origins = [
            "http://localhost:3000",
            "https://pyramid-project-frontend.onrender.com"
        ]
        if origin in allowed_origins:
            response.headers.update({
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
                "Access-Control-Allow-Credentials": "true",
            })
    event.request.add_response_callback(cors_headers)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)

    # Agrega el tween para manejar CORS
    config.add_subscriber(add_cors_headers_response_callback, 'pyramid.events.NewRequest')

    # Resto de la configuración
    config.include('pyramid_jinja2')
    config.include('.routes')
    config.include('.models')
    config.scan()
    return config.make_wsgi_app()
