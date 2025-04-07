from pyramid.view import view_config
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

@view_config(route_name='test_db_connection', renderer='json', request_method='GET')
def test_db_connection(request):
    try:
        result = request.dbsession.execute(text("SELECT 1")).scalar()
        return {"status": "success", "result": result}
    except SQLAlchemyError as e:
        return {"status": "error", "message": str(e)}