"""Modelos de datos para la gestión operativa de logística forestal.

Este módulo define los modelos principales de la aplicación:
- Vehiculo: Registra vehículos de transporte (camiones, camionetas, maquinaria).
- MovimientoCarga: Registra ingresos/salidas de cargas con referencias a vehículos.

Todos los modelos incluyen validaciones de datos críticos y constraints de base de datos.
"""

from django.db import models
from django.core.exceptions import ValidationError
import re

def validar_patente(valor):
    """Valida el formato de patente chilena nueva: 4 letras + 2 números (Ej: ABCD12).
    
    Args:
        valor (str): Patente a validar.
        
    Raises:
        ValidationError: Si el formato no coincide con AAAA11.
    """
    patron = r'^[A-Z]{4}[0-9]{2}$'
    if not re.match(patron, valor.upper()):
        raise ValidationError("La patente debe tener el formato AAAA11 (4 letras seguidas de 2 números).")

class Vehiculo(models.Model):
    """Modelo de vehículos de transporte para operaciones forestales.
    
    Almacena información de camiones, camionetas y maquinaria usados en procesos logísticos.
    Cada vehículo se identifica por su patente única y contiene datos operativos básicos.
    """
    
    TIPO_CHOICES = [
        ('CAMION', 'Camión'),
        ('CAMIONETA', 'Camioneta'),
        ('MAQUINARIA', 'Maquinaria'),
    ]

    patente = models.CharField(
        max_length=6,
        unique=True,
        validators=[validar_patente],
        help_text="Formato: 4 letras + 2 números (Ej: ABCD12)"
    )
    marca = models.CharField(max_length=50, blank=True, help_text="Marca del vehículo (Volvo, Ford, etc.)")
    modelo = models.CharField(max_length=50, blank=True, help_text="Modelo del vehículo")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, help_text="Tipo de vehículo")
    año = models.PositiveIntegerField(help_text="Año de fabricación")

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
    """Modelo de movimientos de carga (ingresos/salidas).
    
    Registra cada movimiento de carga asociado a un vehículo: origen, destino, tipo y fecha.
    Permite auditoría completa de operaciones logísticas y trazabilidad de cargas.
    """
    
    MOVIMIENTO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('SALIDA', 'Salida'),
    ]

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name='movimientos',
        help_text="Vehículo que realiza el movimiento"
    )
    tipo_movimiento = models.CharField(
        max_length=10,
        choices=MOVIMIENTO_CHOICES,
        help_text="Tipo de movimiento: Ingreso o Salida"
    )
    fecha_hora = models.DateTimeField(help_text="Fecha y hora del movimiento")
    origen = models.CharField(max_length=100, blank=True, help_text="Lugar de origen")
    destino = models.CharField(max_length=100, blank=True, help_text="Lugar de destino")
    descripcion = models.TextField(blank=True, help_text="Descripción detallada del movimiento")

    class Meta:
        db_table = 'movimiento_carga'
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"{self.vehiculo.patente} | {self.tipo_movimiento} | {self.fecha_hora}"
