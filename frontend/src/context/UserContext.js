import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            // Intenta obtener los datos del usuario con el token
            axios
                .get('/me', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                })
                .then((response) => {
                    setUser(response.data); // Establece los datos del usuario en el contexto
                })
                .catch((err) => {
                    console.error('Error al recuperar la sesión:', err);
                    localStorage.removeItem('token'); // Elimina el token si es inválido
                });
        }
    }, []); // Se ejecuta solo una vez al cargar el componente

    return (
        <UserContext.Provider value={{ user, setUser }}>
            {children}
        </UserContext.Provider>
    );
};