from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    Text,
    ForeignKey,
    DateTime,
    Numeric,
)
from .meta import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    direccion = Column(Text)
    telefono = Column(String(20))
    es_admin = Column(Boolean, default=False)

    pedidos = relationship("Pedidos", back_populates="usuario", cascade="all, delete")

class Producto(Base):
    __tablename__ = 'producto'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    marca = Column(String(100))
    descripcion = Column(Text)
    precio = Column(Numeric(10, 2), nullable=False)
    cant_dis = Column(Integer, default=0)
    categoria = Column(String(100))
    imagen = Column(Text)

class Pedidos(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(50), default='pendiente')
    fecha_pedido = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="pedidos")
