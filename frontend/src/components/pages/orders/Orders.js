import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Orders.css';

function Orders() {
    const [pedidos, setPedidos] = useState([]);
    const [detalles, setDetalles] = useState([]);
    const [selectedPedido, setSelectedPedido] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        // Llama al backend para obtener los pedidos del usuario
        axios.get('/pedidos') // Cambia esta URL según tu backend
            .then(response => {
                setPedidos(response.data);
            })
            .catch(error => {
                console.error('Error al cargar los pedidos:', error);
                setError('No se pudieron cargar los pedidos.');
            });
    }, []);

    const handleViewDetails = (pedidoId) => {
        // Llama al backend para obtener los detalles del pedido seleccionado
        axios.get(`/api/pedidos/${pedidoId}/detalles`) // Cambia esta URL según tu backend
            .then(response => {
                setDetalles(response.data);
                setSelectedPedido(pedidoId);
            })
            .catch(error => {
                console.error('Error al cargar los detalles del pedido:', error);
                setError('No se pudieron cargar los detalles del pedido.');
            });
    };

    return (
        <div className="orders-container">
            <title>Pyramid Project | Pedidos</title>
            <h1>Mis Pedidos</h1>
            {error && <p className="error-message">{error}</p>}
            <div className="pedidos-list">
                {pedidos.map(pedido => (
                    <div key={pedido.id} className="pedido-card">
                        <p><strong>ID Pedido:</strong> {pedido.id}</p>
                        <p><strong>Total:</strong> ${pedido.total.toFixed(2)}</p>
                        <p><strong>Estado:</strong> {pedido.estado}</p>
                        <p><strong>Fecha:</strong> {new Date(pedido.fecha_pedido).toLocaleDateString()}</p>
                        <button onClick={() => handleViewDetails(pedido.id)} className="btn-detalles">
                            Ver Detalles
                        </button>
                    </div>
                ))}
            </div>
            {selectedPedido && (
                <div className="detalles-pedido">
                    <h2>Detalles del Pedido #{selectedPedido}</h2>
                    <ul>
                        {detalles.map(detalle => (
                            <li key={detalle.id}>
                                <p><strong>Producto ID:</strong> {detalle.producto_id}</p>
                                <p><strong>Cantidad:</strong> {detalle.cantidad}</p>
                                <p><strong>Precio Unitario:</strong> ${detalle.precio_unitario.toFixed(2)}</p>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default Orders;