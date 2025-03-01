def navbar_items(request):
    if request.user.is_authenticated:
        menu_items = [
            {'url_name': 'home', 'text': 'Inicio', 'icon_class': 'fas fa-home'},
            {'url_name': 'perfil', 'text': 'Perfil', 'icon_class': 'fas fa-user'},
            {'url_name': 'product-list', 'text': 'Catálogo de productos', 'icon_class': 'fas fa-box-open'},
        ]

        if request.user.is_staff:
            pass  # Aquí podrías agregar más opciones para administradores

    else:
        menu_items = []  # No mostrar menú a usuarios no autenticados

    return {'menu_items': menu_items}
