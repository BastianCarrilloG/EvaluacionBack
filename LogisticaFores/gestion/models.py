from django.db import models
from django.core.exceptions import ValidationError
import re

def validar_patente(valor):
    """
    Valida el formato de patente chilena nueva:
    4 letras + 2 números (Ej: ABCD12)
    """
    patron = r'^[A-Z]{4}[0-9]{2}$'
    if not re.match(patron, valor.upper()):
        raise ValidationError("La patente debe tener el formato AAAA11 (4 letras seguidas de 2 números).")

class Vehiculo(models.Model):
    TIPO_CHOICES = [
        ('CAMION', 'Camión'),
        ('CAMIONETA', 'Camioneta'),
        ('MAQUINARIA', 'Maquinaria'),
    ]

    patente = models.CharField(
        max_length=6,
        unique=True,
        validators=[validar_patente],
    )
    marca = models.CharField(max_length=50, blank=True)
    modelo = models.CharField(max_length=50, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    año = models.PositiveIntegerField()

    class Meta:
        db_table = 'vehiculo'
        ordering = ['patente']

    def clean(self):
        """Asegura que la patente siempre se guarde en mayúsculas."""
        self.patente = self.patente.upper()
        validar_patente(self.patente)

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
