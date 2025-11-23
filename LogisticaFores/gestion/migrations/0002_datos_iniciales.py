# gestion/migrations/0002_datos_iniciales.py
from django.db import migrations
from django.utils import timezone

def crear_datos_iniciales(apps, schema_editor):
    Vehiculo = apps.get_model('gestion', 'Vehiculo')
    MovimientoCarga = apps.get_model('gestion', 'MovimientoCarga')

    # Crear 5 vehículos
    v1 = Vehiculo.objects.create(patente='ABC123', marca='Volvo', modelo='FH16', tipo='CAMION', anio=2020)
    v2 = Vehiculo.objects.create(patente='XYZ789', marca='Scania', modelo='R500', tipo='CAMION', anio=2019)
    v3 = Vehiculo.objects.create(patente='KLM456', marca='Ford', modelo='F-150', tipo='CAMIONETA', anio=2018)
    v4 = Vehiculo.objects.create(patente='DEF234', marca='JohnDeere', modelo='310L', tipo='MAQUINARIA', anio=2015)
    v5 = Vehiculo.objects.create(patente='GHI567', marca='Mercedes', modelo='Atego', tipo='CAMION', anio=2021)

    now = timezone.now()

    # Crear algunos movimientos de carga de ejemplo
    MovimientoCarga.objects.create(vehiculo=v1, tipo_movimiento='INGRESO', fecha_hora=now, origen='Planta A', destino='Bodega Central', descripcion='Carga de tablones')
    MovimientoCarga.objects.create(vehiculo=v2, tipo_movimiento='SALIDA', fecha_hora=now, origen='Bodega Central', destino='Puerto', descripcion='Despacho a puerto')
    MovimientoCarga.objects.create(vehiculo=v3, tipo_movimiento='INGRESO', fecha_hora=now, origen='Proveedor X', destino='Planta A', descripcion='Entrega de insumos')
    # opcional: dos movimientos más (puedes borrar si no quieres)
    MovimientoCarga.objects.create(vehiculo=v4, tipo_movimiento='INGRESO', fecha_hora=now, origen='Campo Sur', destino='Planta B', descripcion='Maquinaria para mantención')
    MovimientoCarga.objects.create(vehiculo=v5, tipo_movimiento='SALIDA', fecha_hora=now, origen='Bodega Central', destino='Obra Y', descripcion='Transporte de material')

def reverse_func(apps, schema_editor):
    Vehiculo = apps.get_model('gestion', 'Vehiculo')
    MovimientoCarga = apps.get_model('gestion', 'MovimientoCarga')
    # Borrar los registros creados por esta migración (si se revierte)
    MovimientoCarga.objects.filter(descripcion__in=[
        'Carga de tablones','Despacho a puerto','Entrega de insumos',
        'Maquinaria para mantención','Transporte de material'
    ]).delete()
    Vehiculo.objects.filter(patente__in=['ABC123','XYZ789','KLM456','DEF234','GHI567']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_datos_iniciales, reverse_func),
    ]
