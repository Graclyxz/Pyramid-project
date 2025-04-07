from sqlalchemy.exc import SQLAlchemyError
from ..models.modelsBase import Usuario

class UsuarioService:
    def __init__(self, dbsession):
        self.dbsession = dbsession

    def listar_usuarios(self):
        return self.dbsession.query(Usuario).all()

    def obtener_usuario(self, usuario_id):
        return self.dbsession.query(Usuario).filter(Usuario.id == usuario_id).first()

    def crear_usuario(self, data):
        nuevo_usuario = Usuario(**data)
        self.dbsession.add(nuevo_usuario)
        try:
            self.dbsession.flush()
            return nuevo_usuario
        except SQLAlchemyError:
            self.dbsession.rollback()
            raise

    def actualizar_usuario(self, usuario_id, data):
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return None
        for key, value in data.items():
            setattr(usuario, key, value)
        try:
            self.dbsession.flush()
            return usuario
        except SQLAlchemyError:
            self.dbsession.rollback()
            raise

    def eliminar_usuario(self, usuario_id):
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return None
        self.dbsession.delete(usuario)
        try:
            self.dbsession.flush()
            return usuario
        except SQLAlchemyError:
            self.dbsession.rollback()
            raise