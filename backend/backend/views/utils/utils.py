from datetime import datetime
from decimal import Decimal

def serialize_sqlalchemy_object(obj):
    """
    Convierte un objeto de SQLAlchemy en un diccionario serializable.
    Maneja tipos como Decimal y datetime.
    """
    return {
        key: (
            float(value) if isinstance(value, Decimal) else
            value.isoformat() if isinstance(value, datetime) else
            value
        )
        for key, value in obj.__dict__.items()
        if not key.startswith('_')  # Ignora atributos internos de SQLAlchemy
    }