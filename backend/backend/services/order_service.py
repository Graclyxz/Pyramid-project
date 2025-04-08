from sqlalchemy.exc import SQLAlchemyError
from ..models.modelsBase import Pedidos

class OrderService:
    def __init__(self, dbsession):
        self.dbsession = dbsession

    def listar_pedidos(self):
        return self.dbsession.query(Pedidos).all()

    def obtener_pedido(self, pedido_id):
        return self.dbsession.query(Pedidos).filter(Pedidos.id == pedido_id).first()

    def crear_pedido(self, data):
        nuevo_pedido = Pedidos(**data)
        self.dbsession.add(nuevo_pedido)
        try:
            self.dbsession.flush()
            return nuevo_pedido
        except SQLAlchemyError:
            self.dbsession.rollback()
            raise

    def actualizar_pedido(self, pedido_id, data):
        pedido = self.obtener_pedido(pedido_id)
        if not pedido:
            return None
        for key, value in data.items():
            setattr(pedido, key, value)
        try:
            self.dbsession.flush()
            return pedido
        except SQLAlchemyError:
            self.dbsession.rollback()
            raise

    def eliminar_pedido(self, pedido_id):
        pedido = self.obtener_pedido(pedido_id)
        if not pedido:
            return None
        self.dbsession.delete(pedido)
        try:
            self.dbsession.flush()
            return pedido
        except SQLAlchemyError:
            self.dbsession.rollback()
            raise

