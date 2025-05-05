import React, { useContext, useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Importa useNavigate
import './Header.css';
import { UserContext } from '../../../context/UserContext';
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

function Header() {
    const { user, setUser } = useContext(UserContext);
    const [isPedidoPendiente, setisPedidoPendiente] = useState(false);
    const navigate = useNavigate(); // Inicializa useNavigate

    useEffect(() => {
        if (user) {
            axios.get(`${BASE_URL}/pedidos`, {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
            })
                .then(response => {
                    const pedidosPendientes = response.data.filter(pedido => pedido.estado === 'pendiente');
                    setisPedidoPendiente(pedidosPendientes.length > 0);
                })
                .catch(error => {
                    console.error('Error al verificar pedidos pendientes:', error);
                });
        }
    }, [user]);

    const handleLogout = () => {
        localStorage.removeItem('token');
        setUser(null);
        navigate('/'); // Redirige al inicio
    };

    return (
        <header className="header">
            <div className="logo">
                <Link to="/">Pyramid Project</Link>
            </div>
            <nav>
                <ul className="nav-links">
                    {user ? (
                        <>
                            <li>
                                <Link to="/profile">{user.nombre}</Link>
                            </li>
                            <li className="nav-item-orders">
                                <Link to="/orders">
                                    {isPedidoPendiente && <span className="icon-carrito"></span>}
                                    Mis Pedidos
                                </Link>
                            </li>
                            <li>
                                <button onClick={handleLogout} className="btn-logout">Cerrar Sesión</button>
                            </li>
                        </>
                    ) : (
                        <>
                            <li>
                                <Link to="/login">Iniciar Sesión</Link>
                            </li>
                            <li>
                                <Link to="/register">Crear Cuenta</Link>
                            </li>
                        </>
                    )}
                </ul>
            </nav>
        </header>
    );
}

export default Header;