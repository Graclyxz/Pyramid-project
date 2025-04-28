import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header() {
    return (
        <header className="header">
            <div className="logo">
                <Link to="/">Pyramid Project</Link>
            </div>
            <nav>
                <ul className="nav-links">
                    <li>
                        <Link to="/login">Iniciar Sesión</Link>
                    </li>
                    <li>
                        <Link to="/register">Crear Cuenta</Link>
                    </li>
                </ul>
            </nav>
        </header>
    );
}

export default Header;