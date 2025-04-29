import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Header.css';
import { UserContext } from '../../../context/UserContext'; // Importa el contexto del usuario

function Header() {
    const { user, setUser } = useContext(UserContext); // Obtén el usuario y la función para actualizarlo
    const navigate = useNavigate();

    const handleLogout = () => {
        // Lógica para cerrar sesión
        setUser(null); // Limpia el usuario del contexto
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
                                <Link to="/profile">{user.email}</Link> {/* Muestra el nombre del usuario */}
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