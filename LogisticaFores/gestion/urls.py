from django.urls import path
from . import views

urlpatterns = [
    # Página de inicio
    path('', views.home, name='home'),

    # --------------------------
    #        VEHÍCULOS
    # --------------------------
    path('vehiculos/', views.vehiculo_list, name='vehiculo_list'),
    path('vehiculos/crear/', views.vehiculo_create, name='vehiculo_create'),
    path('vehiculos/editar/<int:id>/', views.vehiculo_update, name='vehiculo_update'),
    path('vehiculos/eliminar/<int:id>/', views.vehiculo_delete, name='vehiculo_delete'),

    # --------------------------
    #   MOVIMIENTOS DE CARGA
    # --------------------------
    path('movimientos/', views.movimiento_list, name='movimiento_list'),
    path('movimientos/crear/', views.movimiento_create, name='movimiento_create'),
    path('movimientos/editar/<int:id>/', views.movimiento_update, name='movimiento_update'),
    path('movimientos/eliminar/<int:id>/', views.movimiento_delete, name='movimiento_delete'),
]
