import json
from pyramid.view import view_config
from pyramid.response import Response
import logging

logger = logging.getLogger(__name__)

@view_config(route_name='options', request_method='OPTIONS')
def options_view(request):
    origin = request.headers.get('Origin')
    allowed_origins = [
        "http://localhost:3000",
        "https://pyramid-project-frontend.onrender.com"
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

def create_response(request, data, status_code):
    origin = request.headers.get('Origin')
    allowed_origins = [
        "http://localhost:3000",
        "https://pyramid-project-frontend.onrender.com"
    ]
    headers = {}
    if origin in allowed_origins:
        headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Credentials": "true"
        }
    response = Response(json.dumps(data), content_type="application/json; charset=utf-8", status=status_code)
    response.headers.update(headers)
    return response