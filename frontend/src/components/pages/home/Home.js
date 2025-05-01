import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Home.css';
import { UserContext } from '../../../context/UserContext';

function Home() {
    const [productos, setProductos] = useState([]);
    const [pedidoActivo, setPedidoActivo] = useState(null); // Pedido activo
    const [modalVisible, setModalVisible] = useState(false);
    const [modalMessage, setModalMessage] = useState('');
    const { user } = useContext(UserContext);
    const navigate = useNavigate();

    useEffect(() => {
        // Llama al backend para obtener los productos
        axios.get('/productos')
            .then(response => {
                setProductos(response.data);
            })
            .catch(error => {
                console.error('Error al cargar los productos:', error);
            });

        // Verifica si hay un pedido activo
        if (user) {
            axios.get('/pedidos', {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
            }).then(response => {
                const pedidoPendiente = response.data.find(pedido => pedido.estado === 'pendiente');
                if (pedidoPendiente) {
                    setPedidoActivo(pedidoPendiente);
                }
            }).catch(error => {
                console.error('Error al verificar pedidos activos:', error);
            });
        }
    }, [user]);

    const handleAgregarProducto = async (producto) => {
        if (!user) {
            navigate('/login');
            return;
        }

        try {
            let pedidoId = pedidoActivo?.id;

            // Si no hay un pedido activo, crea uno
            if (!pedidoActivo) {
                const nuevoPedido = await axios.post('/create/pedidos', {
                    usuario_id: user.id,
                    total: 0,
                    estado: 'pendiente',
                }, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
                });
                pedidoId = nuevoPedido.data.id;
                setPedidoActivo(nuevoPedido.data);
            }

            // Añade el producto al pedido activo
            await axios.post('/create/detalles_pedido', {
                pedido_id: pedidoId,
                producto_id: producto.id,
                cantidad: 1,
                precio_unitario: producto.precio,
            }, {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
            });

            setModalMessage(`Producto "${producto.nombre}" añadido al pedido.`);
            setModalVisible(true);
        } catch (error) {
            console.error('Error al añadir el producto al pedido:', error);
        }
    };

    const closeModal = () => {
        setModalVisible(false);
    };

    return (
        <div className="home">
            <h1>Productos Disponibles</h1>
            {modalVisible && (
                <div className="modal">
                    <div className="modal-content">
                        <p>{modalMessage}</p>
                        <button onClick={closeModal} className="btn-close-modal">Cerrar</button>
                    </div>
                </div>
            )}
            <div className="productos-grid">
                {productos.map(producto => (
                    <div key={producto.id} className="producto-card">
                        <img src={producto.imagen} alt={producto.nombre} className="producto-imagen" />
                        <h2>{producto.nombre}</h2>
                        <p><strong>Marca:</strong> {producto.marca}</p>
                        <p>{producto.descripcion}</p>
                        <p><strong>Precio:</strong> ${producto.precio.toFixed(2)}</p>
                        <p><strong>Disponibles:</strong> {producto.cant_dis}</p>
                        <button
                            className="btn-agregar"
                            onClick={() => handleAgregarProducto(producto)}
                        >
                            Añadir al Pedido
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Home;