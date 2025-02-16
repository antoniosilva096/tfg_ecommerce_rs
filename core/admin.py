from django.contrib import admin
from .models import Empleado

# Register your models here.
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dni', 'codigo_nfc', 'estado')
    search_fields = ('nombre', 'dni', 'codigo_nfc')
    list_filter = ('estado',)