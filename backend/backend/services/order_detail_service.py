from sqlalchemy.exc import SQLAlchemyError
from ..models.modelsBase import DetallePedido

class OrderDetailService:
    def __init__(self, dbsession):
        self.dbsession = dbsession

    def listar_detalles_pedido(self):
        return self.dbsession.query(DetallePedido).all()

    def obtener_detalle_pedido(self, pedido_id):
        return self.dbsession.query(DetallePedido).filter(DetallePedido.id == pedido_id).first()

    def crear_detalle_pedido(self, data):
        nuevo_pedido = DetallePedido(**data)
        self.dbsession.add(nuevo_pedido)
        try:
            self.dbsession.flush()
            return nuevo_pedido
        except SQLAlchemyError:
            self.dbsession.rollback()
            raise

    def actualizar_detalle_pedido(self, pedido_id, data):
        pedido = self.obtener_detalle_pedido(pedido_id)
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

    def eliminar_detalle_pedido(self, pedido_id):
        pedido = self.obtener_detalle_pedido(pedido_id)
        if not pedido:
            return None
        self.dbsession.delete(pedido)
        try:
            self.dbsession.flush()
            return pedido
        except SQLAlchemyError:
            self.dbsession.rollback()
            raise