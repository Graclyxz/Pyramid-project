import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Importa useNavigate para redirigir
import axios from 'axios';
import './Register.css';

function Register() {
    const [formData, setFormData] = useState({
        nombre: '',
        email: '',
        password: '',
        direccion: '',
        telefono: '',
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false); // Cambia a booleano para manejar el modal
    const navigate = useNavigate(); // Hook para redirigir

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess(false);

        try {
            const response = await axios.post('/create/usuarios', formData);
            console.log('Registro exitoso:', response.data);
            setSuccess(true); // Muestra el modal de éxito
            setFormData({
                nombre: '',
                email: '',
                password: '',
                direccion: '',
                telefono: '',
            });
        } catch (err) {
            console.error('Error al registrar usuario:', err);
            setError('Hubo un problema al registrar el usuario. Inténtalo de nuevo.');
        }
    };

    const handleModalClose = () => {
        setSuccess(false); // Oculta el modal
        navigate('/login'); // Redirige al inicio de sesión
    };

    return (
        <div className="register-container">
            <title>Pyramid Project | Crear Cuenta</title>
            <h1>Crear Cuenta</h1>
            <form onSubmit={handleSubmit} className="register-form">
                <div className="form-group">
                    <label htmlFor="nombre">Nombre</label>
                    <input
                        type="text"
                        id="nombre"
                        name="nombre"
                        value={formData.nombre}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="email">Correo Electrónico</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Contraseña</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="direccion">Dirección</label>
                    <input
                        type="text"
                        id="direccion"
                        name="direccion"
                        value={formData.direccion}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="telefono">Teléfono</label>
                    <input
                        type="text"
                        id="telefono"
                        name="telefono"
                        value={formData.telefono}
                        onChange={handleChange}
                        required
                    />
                </div>
                {error && <p className="error-message">{error}</p>}
                <button type="submit" className="btn-register">Registrarse</button>
            </form>

            {/* Modal de éxito */}
            {success && (
                <div className="modal">
                    <div className="modal-content">
                        <p>Usuario registrado exitosamente.</p>
                        <button onClick={handleModalClose} className="btn-ok">OK</button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Register;