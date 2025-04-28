import React from 'react';
import './Footer.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebook, faTwitter, faInstagram } from '@fortawesome/free-brands-svg-icons';
import { faEye, faThumbsUp, faCheck, faKey, faEnvelope } from '@fortawesome/free-solid-svg-icons';

function Footer() {
    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="social-media">
                    <h4><FontAwesomeIcon icon={faThumbsUp} /> Síguenos</h4>
                    <ul>
                        <li>
                            <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">
                                <FontAwesomeIcon icon={faFacebook} /> Facebook
                            </a>
                        </li>
                        <li>
                            <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">
                                <FontAwesomeIcon icon={faTwitter} /> Twitter
                            </a>
                        </li>
                        <li>
                            <a href="https://instagram.com" target="_blank" rel="noopener noreferrer">
                                <FontAwesomeIcon icon={faInstagram} /> Instagram
                            </a>
                        </li>
                    </ul>
                </div>
                <div className="footer-links">
                    <h4><FontAwesomeIcon icon={faEye} /> Enlaces Útiles</h4>
                    <ul>
                        <li>
                            <a href="/terms">
                                <FontAwesomeIcon icon={faCheck} /> Términos y Condiciones
                            </a>
                        </li>
                        <li>
                            <a href="/privacy">
                                <FontAwesomeIcon icon={faKey} /> Política de Privacidad
                            </a>
                        </li>
                        <li>
                            <a href="/contact">
                                <FontAwesomeIcon icon={faEnvelope} /> Contacto
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
            <div className="footer-bottom">
                <p>&copy; 2025 Pyramid Project. Todos los derechos reservados.</p>
            </div>
        </footer>
    );
}

export default Footer;