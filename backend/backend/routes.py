def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('listar_usuarios', '/usuarios')
    config.add_route('obtener_usuario', '/usuarios/{id}')
    config.add_route('crear_usuario', '/create/usuarios')
    config.add_route('actualizar_usuario', '/update/usuarios/{id}')
    config.add_route('eliminar_usuario', '/delete/usuarios/{id}')

    config.add_route('listar_productos', '/productos')
    config.add_route('obtener_productos', '/productos/{id}')
    config.add_route('crear_productos', '/create/productos')
    config.add_route('actualizar_productos', '/update/productos/{id}')
    config.add_route('eliminar_productos', '/delete/productos/{id}')

    config.add_route('test_db_connection', '/test-db-connection')  # Nueva ruta