import React, { useState, useContext } from 'react'; // Importa useContext
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css';
import { UserContext } from '../../../context/UserContext'; // Importa el contexto del usuario

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const { setUser } = useContext(UserContext); // Obtén la función para actualizar el usuario

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const response = await axios.post('/login', { email, password });
            console.log('Inicio de sesión exitoso:', response.data);

            // Guarda el token en localStorage
            localStorage.setItem('token', response.data.token);

            // Actualiza el contexto del usuario
            setUser({
                email: email,
                nombre: response.data.nombre,
                es_admin: response.data.es_admin,
            });

            navigate('/'); // Redirige al usuario
        } catch (err) {
            console.error('Error al iniciar sesión:', err);
            setError('Credenciales inválidas. Por favor, inténtalo de nuevo.');
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
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Contraseña</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
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