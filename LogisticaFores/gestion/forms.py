"""Formularios para la gestión operativa de logística forestal.

Este módulo contiene formularios personalizados para:
- Autenticación con estilos Bootstrap personalizados
- CRUD de vehículos con validaciones de patente y año
- CRUD de movimientos de carga con validación de fechas

Todos los formularios incluyen validaciones de negocio personalizadas.
"""

from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
import re

from .models import Vehiculo, MovimientoCarga
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthForm(AuthenticationForm):
    """Formulario de autenticación personalizado con estilos Bootstrap.
    
    Extiende AuthenticationForm para aplicar clases CSS de Bootstrap (form-control-lg)
    a los campos username y password, mejorando la experiencia visual sin modificar plantillas.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Estilizar los campos del formulario de login para usar Bootstrap
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({
                'class': 'form-control form-control-lg',
                'placeholder': 'Usuario',
                'autofocus': 'autofocus',
                'autocomplete': 'username',
                'id': 'id_username',
            })
        if 'password' in self.fields:
            self.fields['password'].widget.attrs.update({
                'class': 'form-control form-control-lg',
                'placeholder': 'Contraseña',
                'autocomplete': 'current-password',
                'id': 'id_password',
            })

# Regex para validar 4 letras + 2 números
PATENTE_REGEX = re.compile(r'^[A-Z]{4}[0-9]{2}$')

class VehiculoForm(forms.ModelForm):
    """Formulario CRUD para vehículos con validaciones personalizadas.
    
    Valida:
    - Patente: formato chileno (AAAA11) y unicidad en BD
    - Año: rango 1900 a año actual + 1
    
    Attributes:
        Meta.model: Modelo Vehiculo
        Meta.fields: patente, marca, modelo, tipo, año
    """
    class Meta:
        model = Vehiculo
        # conservamos el nombre del campo 'año' tal como lo tienes en el modelo
        fields = ['patente', 'marca', 'modelo', 'tipo', 'año']
        widgets = {
            'patente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ABCD12', 'maxlength': 6}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'año': forms.NumberInput(attrs={'class': 'form-control', 'min': 1900}),
        }
        labels = {
            'patente': 'Patente',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'tipo': 'Tipo',
            'año': 'Año',
        }

    def clean_patente(self):
        """Valida que la patente tenga formato correcto y sea única.
        
        Returns:
            str: Patente en mayúsculas si es válida.
            
        Raises:
            ValidationError: Si el formato es inválido o la patente ya existe.
        """
        p = self.cleaned_data.get('patente', '')
        if p is None or str(p).strip() == '':
            raise ValidationError("La patente es obligatoria.")
        p = str(p).strip().upper()

        if not PATENTE_REGEX.match(p):
            raise ValidationError("Formato inválido: debe ser 4 letras + 2 números, ejemplo ABCD12.")

        # Verificar duplicado (más amigable que dejar el error de DB)
        qs = Vehiculo.objects.filter(patente=p)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Ya existe un vehículo con esa patente.")

        return p

    def clean_año(self):
        """Valida que el año sea un valor razonable.
        
        Returns:
            int: Año si es válido (entre 1900 y año actual + 1).
            
        Raises:
            ValidationError: Si el año está fuera del rango permitido.
        """
        anio = self.cleaned_data.get('año')
        if anio is None or str(anio).strip() == '':
            raise ValidationError("El año es obligatorio.")
        try:
            anio_int = int(anio)
        except (ValueError, TypeError):
            raise ValidationError("Año inválido.")
        current = timezone.now().year
        if anio_int < 1900 or anio_int > current + 1:
            raise ValidationError(f"Año inválido. Debe estar entre 1900 y {current+1}.")
        return anio_int


class MovimientoForm(forms.ModelForm):
    """Formulario CRUD para movimientos de carga con validación temporal.
    
    Valida:
    - Fecha/hora: no puede ser en el futuro (validación de negocio)
    
    Attributes:
        Meta.model: Modelo MovimientoCarga
        Meta.fields: vehiculo, tipo_movimiento, fecha_hora, origen, destino, descripcion
    """
    class Meta:
        model = MovimientoCarga
        fields = ['vehiculo', 'tipo_movimiento', 'fecha_hora', 'origen', 'destino', 'descripcion']
        widgets = {
            'vehiculo': forms.Select(attrs={'class': 'form-select'}),
            'tipo_movimiento': forms.Select(attrs={'class': 'form-select'}),
            # datetime-local requiere que el valor que se pase esté en el formato adecuado desde la vista/template.
            'fecha_hora': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'origen': forms.TextInput(attrs={'class': 'form-control'}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'vehiculo': 'Vehículo',
            'tipo_movimiento': 'Tipo de movimiento',
            'fecha_hora': 'Fecha y hora',
            'origen': 'Origen',
            'destino': 'Destino',
            'descripcion': 'Descripción',
        }

    def clean_fecha_hora(self):
        """Valida que la fecha/hora no sea en el futuro.
        
        Returns:
            datetime: Fecha/hora si es válida (presente o pasada).
            
        Raises:
            ValidationError: Si la fecha es en el futuro.
        """
        fecha = self.cleaned_data.get('fecha_hora')
        if fecha is None:
            raise ValidationError("La fecha y hora es obligatoria.")
        # Evitar fechas futuras
        if fecha > timezone.now():
            raise ValidationError("La fecha no puede ser futura.")
        return fecha
