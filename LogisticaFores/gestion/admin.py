from django.contrib import admin
from .models import Vehiculo, MovimientoCarga

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('patente', 'marca', 'modelo', 'tipo', 'anio')
    search_fields = ('patente', 'marca', 'modelo')
    list_filter = ('tipo', 'anio')

@admin.register(MovimientoCarga)
class MovimientoCargaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'tipo_movimiento', 'fecha_hora', 'origen', 'destino')
    search_fields = ('vehiculo__patente', 'origen', 'destino')
    list_filter = ('tipo_movimiento',)
