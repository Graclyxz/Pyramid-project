def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('listar_usuarios', '/usuarios')
    config.add_route('obtener_usuario', '/usuarios/{id}')
    config.add_route('crear_usuario', '/create/usuarios')
    config.add_route('actualizar_usuario', '/update/usuarios/{id}')
    config.add_route('eliminar_usuario', '/delete/usuarios/{id}')

    config.add_route('listar_productos', '/productos')
    config.add_route('obtener_producto', '/productos/{id}')
    config.add_route('crear_producto', '/create/productos')
    config.add_route('actualizar_producto', '/update/productos/{id}')
    config.add_route('eliminar_producto', '/delete/productos/{id}')

    config.add_route('listar_pedidos', '/pedidos')
    config.add_route('obtener_pedido', '/pedidos/{id}')
    config.add_route('crear_pedido', '/create/pedidos')
    config.add_route('actualizar_pedido', '/update/pedidos/{id}')
    config.add_route('eliminar_pedido', '/delete/pedidos/{id}')

    config.add_route('listar_detalles_pedido', '/detalles_pedido')
    config.add_route('obtener_detalle_pedido', '/detalles_pedido/{id}')
    config.add_route('crear_detalle_pedido', '/create/detalles_pedido')
    config.add_route('actualizar_detalle_pedido', '/update/detalles_pedido/{id}')
    config.add_route('eliminar_detalle_pedido', '/delete/detalles_pedido/{id}')

    config.add_route('test_db_connection', '/test-db-connection')  # Nueva ruta