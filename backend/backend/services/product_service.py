from sqlalchemy.exc import SQLAlchemyError
from ..models.modelsBase import Producto

class ProductService:
    def __init__(self, dbsession):
        self.dbsession = dbsession

    def listar_productos(self):
        return self.dbsession.query(Producto).all()

    def obtener_producto(self, producto_id):
        return self.dbsession.query(Producto).filter(Producto.id == producto_id).first()

    def crear_producto(self, data):
        nuevo_producto = Producto(**data)
        self.dbsession.add(nuevo_producto)
        try:
            self.dbsession.flush()
            return nuevo_producto
        except SQLAlchemyError:
            self.dbsession.rollback()
            raise

    def actualizar_producto(self, producto_id, data):
        producto = self.obtener_producto(producto_id)
        if not producto:
            return None
        for key, value in data.items():
            setattr(producto, key, value)
        try:
            self.dbsession.flush()
            return producto
        except SQLAlchemyError:
            self.dbsession.rollback()
            raise

    def eliminar_producto(self, producto_id):
        producto = self.obtener_producto(producto_id)
        if not producto:
            return None
        self.dbsession.delete(producto)
        try:
            self.dbsession.flush()
            return producto
        except SQLAlchemyError:
            self.dbsession.rollback()
            raise