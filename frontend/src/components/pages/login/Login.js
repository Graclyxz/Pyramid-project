import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Login.css';
import { UserContext } from '../../../context/UserContext';

const BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

function Login() {
    const [formData, setFormData] = useState({ email: '', password: '' });
    const [error, setError] = useState('');
    const { setUser } = useContext(UserContext); // Obtén la función para actualizar el usuario
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            // Solicita el token al iniciar sesión
            const loginResponse = await axios.post(`${BASE_URL}/login`, formData);
            const { token } = loginResponse.data;

            // Guarda el token en localStorage
            localStorage.setItem('token', token);

            // Usa el token para obtener los datos del usuario
            const userResponse = await axios.get(`${BASE_URL}/me`, {
                headers: {
                    Authorization: `Bearer ${token}`, // Envía el token en los encabezados
                },
            });

            // Actualiza el contexto con los datos del usuario
            setUser(userResponse.data);

            // Redirige al usuario a la página principal
            navigate('/');
        } catch (err) {
            console.error('Error al iniciar sesión:', err);
            setError('Credenciales incorrectas o problema al obtener los datos del usuario.');
        }
    };

    return (
        <div className="login-container">
            <title>Pyramid Project | Iniciar Sesión</title>
            <h1>Iniciar Sesión</h1>
            <form onSubmit={handleSubmit} className="login-form">
                <div className="form-group">
                    <label htmlFor="email">Correo Electrónico</label>
                    <input
                        type="email"
                        name="email"
                        id="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="Correo electrónico"
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Contraseña</label>
                    <input
                        type="password"
                        name="password"
                        id="password"
                        value={formData.password}
                        onChange={handleChange}
                        placeholder="Contraseña"
                        required
                    />
                </div>
                {error && <p className="error-message">{error}</p>}
                <button type="submit" className="btn-login">Iniciar Sesión</button>
            </form>
        </div>
    );
}

export default Login;