from django.db import models

class Vehiculo(models.Model):
    TIPO_CHOICES = [
        ('CAMION', 'Camión'),
        ('CAMIONETA', 'Camioneta'),
        ('MAQUINARIA', 'Maquinaria'),
    ]

    patente = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50, blank=True)
    modelo = models.CharField(max_length=50, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    anio = models.PositiveIntegerField()

    class Meta:
        db_table = 'vehiculo'
        ordering = ['patente']

    def __str__(self):
        return f"{self.patente} - {self.tipo}"

class MovimientoCarga(models.Model):
    MOVIMIENTO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('SALIDA', 'Salida'),
    ]

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='movimientos')
    tipo_movimiento = models.CharField(max_length=10, choices=MOVIMIENTO_CHOICES)
    fecha_hora = models.DateTimeField()
    origen = models.CharField(max_length=100, blank=True)
    destino = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        db_table = 'movimiento_carga'
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"{self.vehiculo.patente} | {self.tipo_movimiento} | {self.fecha_hora}"
