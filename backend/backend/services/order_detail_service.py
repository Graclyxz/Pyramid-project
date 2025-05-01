from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from ..models.modelsBase import DetallePedido, Pedidos

class OrderDetailService:
    def __init__(self, dbsession):
        self.dbsession = dbsession

    def listar_detalles_pedido(self):
        return self.dbsession.query(DetallePedido).all()

    def listar_detalles_pedido_por_pedido(self, pedido_id):
        # Incluye la relación con Producto para obtener el nombre del producto
        return (
            self.dbsession.query(DetallePedido)
            .options(joinedload(DetallePedido.producto))  # Carga la relación con Producto
            .filter(DetallePedido.pedido_id == pedido_id)
            .all()
        )

    def obtener_detalle_pedido(self, pedido_id):
        return self.dbsession.query(DetallePedido).filter(DetallePedido.id == pedido_id).first()

    def crear_detalle_pedido(self, data):
        nuevo_detalle = DetallePedido(**data)
        self.dbsession.add(nuevo_detalle)
        try:
            self.dbsession.flush()

            # Recalcular el total del pedido
            pedido_id = data['pedido_id']
            self.actualizar_total_pedido(pedido_id)

            return nuevo_detalle
        except SQLAlchemyError:
            self.dbsession.rollback()
            raise

    def actualizar_total_pedido(self, pedido_id):
        # Obtén todos los detalles del pedido
        detalles = self.dbsession.query(DetallePedido).filter(DetallePedido.pedido_id == pedido_id).all()

        # Calcula el nuevo total
        nuevo_total = sum(detalle.cantidad * float(detalle.precio_unitario) for detalle in detalles)

        # Actualiza el total en la tabla Pedidos
        pedido = self.dbsession.query(Pedidos).filter(Pedidos.id == pedido_id).first()
        if pedido:
            pedido.total = nuevo_total
            try:
                self.dbsession.flush()
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