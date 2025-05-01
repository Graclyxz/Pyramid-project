import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Profile.css';

function Profile() {
    const [userData, setUserData] = useState({
        nombre: '',
        email: '',
        direccion: '',
        telefono: '',
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    useEffect(() => {
        // Llama al backend para obtener los datos del usuario autenticado
        axios.get('/me', {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`, // Asegúrate de enviar el token
            },
        })
            .then(response => {
                setUserData(response.data);
            })
            .catch(error => {
                console.error('Error al cargar los datos del usuario:', error);
                setError('No se pudieron cargar los datos del usuario.');
            });
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUserData({ ...userData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        try {
            // Obtén el ID del usuario desde los datos actuales
            const userId = userData.id;

            // Envía la solicitud PUT al backend con la URL correcta y el token
            const response = await axios.put(`/update/usuarios/${userId}`, userData, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`, // Envía el token JWT
                },
            });

            console.log('Datos actualizados:', response.data);
            setSuccess('Datos actualizados exitosamente.');
        } catch (err) {
            console.error('Error al actualizar los datos:', err.response || err);
            setError('Hubo un problema al actualizar los datos. Inténtalo de nuevo.');
        }
    };

    return (
        <div className="profile-container">
            <h1>Mi Perfil</h1>
            <form onSubmit={handleSubmit} className="profile-form">
                <div className="form-group">
                    <label htmlFor="nombre">Nombre</label>
                    <input
                        type="text"
                        id="nombre"
                        name="nombre"
                        value={userData.nombre}
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
                        value={userData.email}
                        onChange={handleChange}
                        required
                        disabled // El email no debe ser editable
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="direccion">Dirección</label>
                    <input
                        type="text"
                        id="direccion"
                        name="direccion"
                        value={userData.direccion}
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
                        value={userData.telefono}
                        onChange={handleChange}
                        required
                    />
                </div>
                {error && <p className="error-message">{error}</p>}
                {success && <p className="success-message">{success}</p>}
                <button type="submit" className="btn-update">Actualizar Datos</button>
            </form>
        </div>
    );
}

export default Profile;