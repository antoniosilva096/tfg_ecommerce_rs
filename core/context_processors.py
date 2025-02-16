def navbar_items(request):
    if request.user.is_authenticated:
        menu_items = [
            {'url_name': 'home', 'text': 'Inicio', 'icon_class': 'fas fa-home'},
            {'url_name': 'perfil', 'text': 'Perfil', 'icon_class': 'fas fa-user'},
        ]

        if request.user.is_staff:
            menu_items.append({'url_name': 'empleado_list', 'text': 'Gestión de empleados', 'icon_class': 'fas fa-users'})

    else:
        menu_items = []  # No mostrar menú a usuarios no autenticados

    return {'menu_items': menu_items}