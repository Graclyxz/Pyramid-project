import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Orders.css';

function Orders() {
    const [pedidosPendientes, setPedidosPendientes] = useState([]);
    const [pedidosEnviados, setPedidosEnviados] = useState([]);
    const [detalles, setDetalles] = useState([]);
    const [selectedPedido, setSelectedPedido] = useState(null);
    const [modalVisible, setModalVisible] = useState(false);
    const [modalMessage, setModalMessage] = useState('');
    const [isPedidoPendiente, setIsPedidoPendiente] = useState(false); // Nuevo estado para verificar si el pedido es pendiente

    useEffect(() => {
        axios.get('/pedidos', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        })
            .then(response => {
                const pedidos = response.data;
                setPedidosPendientes(pedidos.filter(pedido => pedido.estado === 'pendiente'));
                setPedidosEnviados(pedidos.filter(pedido => pedido.estado === 'enviado'));
            })
            .catch(error => {
                console.error('Error al cargar los pedidos:', error);
            });
    }, []);

    const handleVerDetalles = (pedidoId) => {
        axios.get(`/detalles_pedido?pedido_id=${pedidoId}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        })
            .then(response => {
                setDetalles(response.data.detalles);
                setSelectedPedido(pedidoId);
                setIsPedidoPendiente(pedidosPendientes.some(pedido => pedido.id === pedidoId)); // Verifica si el pedido es pendiente
                setModalMessage('');
                setModalVisible(true);
            })
            .catch(error => {
                console.error('Error al cargar los detalles del pedido:', error);
            });
    };

    const handleEnviarPedido = async (pedidoId) => {
        try {
            await axios.put(`/update/pedidos/${pedidoId}`, {
                estado: 'enviado',
            }, {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
            });

            const pedidoEnviado = pedidosPendientes.find(pedido => pedido.id === pedidoId);
            setPedidosPendientes(pedidosPendientes.filter(pedido => pedido.id !== pedidoId));
            setPedidosEnviados([...pedidosEnviados, { ...pedidoEnviado, estado: 'enviado' }]);

            setModalMessage('Pedido enviado exitosamente.');
            setModalVisible(true);
        } catch (error) {
            console.error('Error al enviar el pedido:', error);
        }
    };

    const handleEliminarProducto = async (detalleId) => {
        try {
            await axios.delete(`/delete/detalles_pedido/${detalleId}`, {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
            });

            // Actualiza la lista de detalles después de eliminar el producto
            setDetalles(detalles.filter(detalle => detalle.id !== detalleId));
        } catch (error) {
            console.error('Error al eliminar el producto del pedido:', error);
        }
    };

    const handleEliminarPedido = async (pedidoId) => {
        try {
            await axios.delete(`/delete/pedidos/${pedidoId}`, {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
            });

            // Actualiza la lista de pedidos pendientes después de eliminar el pedido
            setPedidosPendientes(pedidosPendientes.filter(pedido => pedido.id !== pedidoId));
        } catch (error) {
            console.error('Error al eliminar el pedido:', error);
        }
    };

    const closeModal = () => {
        setModalVisible(false);
        setSelectedPedido(null);
        setDetalles([]);
        setModalMessage('');
        setIsPedidoPendiente(false); // Restablece el estado
    };

    return (
        <div className="orders-container">
            <h1>Mis Pedidos</h1>
            <div className="pedidos-section">
                <h2>Pedidos Pendientes</h2>
                <div className="pedidos-list">
                    {pedidosPendientes.length > 0 ? (
                        pedidosPendientes.map(pedido => (
                            <div key={pedido.id} className="pedido-card">
                                <p><strong>ID Pedido:</strong> {pedido.id}</p>
                                <p><strong>Total:</strong> ${pedido.total.toFixed(2)}</p>
                                <p><strong>Estado:</strong> {pedido.estado}</p>
                                <p><strong>Fecha:</strong> {new Date(pedido.fecha_pedido).toLocaleDateString()}</p>
                                <button
                                    className="btn-detalles"
                                    onClick={() => handleVerDetalles(pedido.id)}
                                >
                                    Ver Detalles
                                </button>
                                <button
                                    className="btn-enviar"
                                    onClick={() => handleEnviarPedido(pedido.id)}
                                >
                                    Enviar Pedido
                                </button>
                                <button
                                    className="btn-eliminar-pedido"
                                    onClick={() => handleEliminarPedido(pedido.id)}
                                >
                                    Eliminar Pedido
                                </button>
                            </div>
                        ))
                    ) : (
                        <p>No hay pedidos pendientes.</p>
                    )}
                </div>
            </div>
            <div className="pedidos-section">
                <h2>Pedidos Enviados</h2>
                <div className="pedidos-list">
                    {pedidosEnviados.length > 0 ? (
                        pedidosEnviados.map(pedido => (
                            <div key={pedido.id} className="pedido-card">
                                <p><strong>ID Pedido:</strong> {pedido.id}</p>
                                <p><strong>Total:</strong> ${pedido.total.toFixed(2)}</p>
                                <p><strong>Estado:</strong> {pedido.estado}</p>
                                <p><strong>Fecha:</strong> {new Date(pedido.fecha_pedido).toLocaleDateString()}</p>
                                <button
                                    className="btn-detalles"
                                    onClick={() => handleVerDetalles(pedido.id)}
                                >
                                    Ver Detalles
                                </button>
                            </div>
                        ))
                    ) : (
                        <p>No hay pedidos enviados.</p>
                    )}
                </div>
            </div>

            {modalVisible && (
                <div className="modal">
                    <div className="modal-content">
                        {modalMessage ? (
                            <p>{modalMessage}</p>
                        ) : (
                            <>
                                <h2>Detalles del Pedido #{selectedPedido}</h2>
                                <ul className="detalles-list">
                                    {detalles.map(detalle => (
                                        <li key={detalle.id} className="detalle-item">
                                            <div className="detalle-content">
                                                <div className="detalle-info">
                                                    <p><strong>Producto:</strong> {detalle.producto_nombre}</p>
                                                    <p><strong>Cantidad:</strong> {detalle.cantidad}</p>
                                                    <p><strong>Precio Unitario:</strong> ${detalle.precio_unitario.toFixed(2)}</p>
                                                    <p><strong>Subtotal:</strong> ${(detalle.cantidad * detalle.precio_unitario).toFixed(2)}</p>
                                                </div>
                                                {isPedidoPendiente && (
                                                    <button
                                                        className="btn-eliminar"
                                                        onClick={() => handleEliminarProducto(detalle.id)}
                                                    >
                                                        X
                                                    </button>
                                                )}
                                            </div>
                                        </li>
                                    ))}
                                </ul>
                                <h3>Total del Pedido: ${detalles.reduce((total, detalle) => total + detalle.cantidad * detalle.precio_unitario, 0).toFixed(2)}</h3>
                            </>
                        )}
                        <button onClick={closeModal} className="btn-close-modal">Cerrar</button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Orders;