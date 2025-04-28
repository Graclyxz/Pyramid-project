import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Home.css';

function Home() {
    const [productos, setProductos] = useState([]);

    useEffect(() => {
        // Llama al backend para obtener los productos
        axios.get('/api/productos') // Cambia esta URL según tu backend
            .then(response => {
                setProductos(response.data);
            })
            .catch(error => {
                console.error('Error al cargar los productos:', error);
            });
    }, []);

    return (
        <div className="home">
            <h1>Productos Disponibles</h1>
            <div className="productos-grid">
                {productos.map(producto => (
                    <div key={producto.id} className="producto-card">
                        <img src={producto.imagen} alt={producto.nombre} className="producto-imagen" />
                        <h2>{producto.nombre}</h2>
                        <p><strong>Marca:</strong> {producto.marca}</p>
                        <p>{producto.desc}</p>
                        <p><strong>Precio:</strong> ${producto.precio.toFixed(2)}</p>
                        <p><strong>Disponibles:</strong> {producto.cant_dis}</p>
                        <button className="btn-agregar">Añadir al Carrito</button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Home;