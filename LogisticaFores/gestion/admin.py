from django.contrib import admin
from .models import Vehiculo, MovimientoCarga


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('patente', 'marca', 'modelo', 'tipo', 'año')
    list_display_links = ('patente',)
    search_fields = ('patente', 'marca', 'modelo')
    list_filter = ('tipo', 'año')
    ordering = ('patente',)
    list_per_page = 25
    # Opcional: si quieres mostrar campos en readonly cuando se vea el detalle
    # readonly_fields = ('patente',)


@admin.register(MovimientoCarga)
class MovimientoCargaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'tipo_movimiento', 'fecha_hora', 'origen', 'destino')
    list_display_links = ('vehiculo',)
    search_fields = ('vehiculo__patente', 'origen', 'destino', 'descripcion')
    list_filter = ('tipo_movimiento',)
    ordering = ('-fecha_hora',)
    list_per_page = 25
    # Usar raw_id_fields mejora el rendimiento para relaciones con muchas filas
    raw_id_fields = ('vehiculo',)
