from datetime import datetime, timedelta

# Lista en memoria para almacenar tokens revocados
TOKEN_BLACKLIST = {}

def agregar_token_a_blacklist(token, exp):
    """
    Agrega un token a la lista negra con su tiempo de expiración.
    """
    TOKEN_BLACKLIST[token] = exp

def es_token_revocado(token):
    """
    Verifica si un token está en la lista negra.
    """
    exp = TOKEN_BLACKLIST.get(token)
    if exp and exp > datetime.utcnow():
        return True
    # Elimina tokens expirados de la lista negra
    if exp and exp <= datetime.utcnow():
        del TOKEN_BLACKLIST[token]
    return False