from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import class_mapper

def serialize_sqlalchemy_object(obj):
    """
    Serializa un objeto SQLAlchemy a un diccionario JSON serializable.
    Convierte valores Decimal a float y datetime a cadenas ISO 8601.
    """
    if obj is None:
        return None

    columns = [c.key for c in class_mapper(obj.__class__).columns]
    data = {}
    for column in columns:
        value = getattr(obj, column)
        if isinstance(value, Decimal):
            data[column] = float(value)  # Convierte Decimal a float
        elif isinstance(value, datetime):
            data[column] = value.isoformat()  # Convierte datetime a cadena ISO 8601
        else:
            data[column] = value

    return data