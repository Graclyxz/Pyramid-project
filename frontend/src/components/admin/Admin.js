import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Admin.css';

function Admin() {
    const [usuarios, setUsuarios] = useState([]);
    const [nuevoProducto, setNuevoProducto] = useState({
        nombre: '',
        marca: '',
        desc: '',
        precio: '',
        cant_dis: '',
        categoria: '',
        imagen: '',
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    useEffect(() => {
        // Cargar usuarios
        axios.get('/api/usuarios') // Cambia esta URL según tu backend
            .then(response => {
                setUsuarios(response.data);
            })
            .catch(error => {
                console.error('Error al cargar los usuarios:', error);
                setError('No se pudieron cargar los usuarios.');
            });
    }, []);

    const handleProductoChange = (e) => {
        const { name, value } = e.target;
        setNuevoProducto({ ...nuevoProducto, [name]: value });
    };

    const handleCrearProducto = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        try {
            const response = await axios.post('/api/productos', nuevoProducto); // Cambia esta URL según tu backend
            console.log('Producto creado:', response.data);
            setSuccess('Producto creado exitosamente.');
            setNuevoProducto({
                nombre: '',
                marca: '',
                desc: '',
                precio: '',
                cant_dis: '',
                categoria: '',
                imagen: '',
            });
        } catch (err) {
            console.error('Error al crear el producto:', err);
            setError('Hubo un problema al crear el producto. Inténtalo de nuevo.');
        }
    };

    return (
        <div className="admin-container">
            <h1>Panel de Administración</h1>

            {error && <p className="error-message">{error}</p>}
            {success && <p className="success-message">{success}</p>}

            <section className="usuarios-section">
                <h2>Usuarios</h2>
                <ul>
                    {usuarios.map(usuario => (
                        <li key={usuario.id}>
                            <p><strong>ID:</strong> {usuario.id}</p>
                            <p><strong>Nombre:</strong> {usuario.nombre}</p>
                            <p><strong>Email:</strong> {usuario.email}</p>
                            <p><strong>Teléfono:</strong> {usuario.telefono}</p>
                        </li>
                    ))}
                </ul>
            </section>

            <section className="crear-producto-section">
                <h2>Crear Producto</h2>
                <form onSubmit={handleCrearProducto}>
                    <div className="form-group">
                        <label htmlFor="nombre">Nombre</label>
                        <input
                            type="text"
                            id="nombre"
                            name="nombre"
                            value={nuevoProducto.nombre}
                            onChange={handleProductoChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="marca">Marca</label>
                        <input
                            type="text"
                            id="marca"
                            name="marca"
                            value={nuevoProducto.marca}
                            onChange={handleProductoChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="desc">Descripción</label>
                        <textarea
                            id="desc"
                            name="desc"
                            value={nuevoProducto.desc}
                            onChange={handleProductoChange}
                            required
                        ></textarea>
                    </div>
                    <div className="form-group">
                        <label htmlFor="precio">Precio</label>
                        <input
                            type="number"
                            id="precio"
                            name="precio"
                            value={nuevoProducto.precio}
                            onChange={handleProductoChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="cant_dis">Cantidad Disponible</label>
                        <input
                            type="number"
                            id="cant_dis"
                            name="cant_dis"
                            value={nuevoProducto.cant_dis}
                            onChange={handleProductoChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="categoria">Categoría</label>
                        <input
                            type="text"
                            id="categoria"
                            name="categoria"
                            value={nuevoProducto.categoria}
                            onChange={handleProductoChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="imagen">URL de la Imagen</label>
                        <input
                            type="text"
                            id="imagen"
                            name="imagen"
                            value={nuevoProducto.imagen}
                            onChange={handleProductoChange}
                            required
                        />
                    </div>
                    <button type="submit" className="btn-crear-producto">Crear Producto</button>
                </form>
            </section>
        </div>
    );
}

export default Admin;