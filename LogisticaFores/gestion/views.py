"""Vistas para la gestión operativa de logística forestal.

Este módulo implementa todas las vistas de la aplicación:
- Vista de inicio que redirige según autenticación
- CRUD completo para Vehículos (crear, leer, actualizar, eliminar)
- CRUD completo para Movimientos de Carga
- Todas las vistas requieren autenticación mediante @login_required
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Vehiculo, MovimientoCarga
from .forms import VehiculoForm, MovimientoForm


# --------------------------
#        INICIO
# --------------------------
def home(request):
    """Vista de inicio que redirige según estado de autenticación.
    
    Si el usuario está autenticado, redirige a la lista de vehículos.
    Si no está autenticado, redirige a la página de login.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponseRedirect: Redirección a vehiculo_list o login.
    """
    if request.user.is_authenticated:
        return redirect("vehiculo_list")
    return redirect("login")


# --------------------------
#     CRUD VEHÍCULOS
# --------------------------

@login_required
def vehiculo_list(request):
    """Lista todos los vehículos registrados en el sistema.
    
    Requiere autenticación. Obtiene todos los vehículos de la base de datos
    y los pasa a la plantilla para su visualización en una tabla.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Plantilla vehiculos/list.html con lista de vehículos.
    """
    vehiculos = Vehiculo.objects.all()
    return render(request, "vehiculos/list.html", {"vehiculos": vehiculos})


@login_required
def vehiculo_create(request):
    """Crea un nuevo vehículo en el sistema.
    
    GET: Muestra formulario vacío de creación.
    POST: Valida datos y guarda nuevo vehículo. Redirige a lista si es exitoso,
          muestra errores en formulario si hay problemas de validación.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Formulario (GET) o redirección a lista (POST exitoso).
    """
    if request.method == "POST":
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo creado correctamente.")
            return redirect("vehiculo_list")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = VehiculoForm()
    return render(request, "vehiculos/form.html", {"form": form, "accion": "Crear"})


@login_required
def vehiculo_update(request, id):
    """Actualiza los datos de un vehículo existente.
    
    GET: Muestra formulario precargado con datos del vehículo.
    POST: Valida cambios y actualiza registro. Redirige a lista si es exitoso.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        id (int): ID del vehículo a editar.
        
    Returns:
        HttpResponse: Formulario (GET) o redirección a lista (POST exitoso).
        Http404: Si el vehículo no existe.
    """
    vehiculo = get_object_or_404(Vehiculo, id=id)
    if request.method == "POST":
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo actualizado correctamente.")
            return redirect("vehiculo_list")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, "vehiculos/form.html", {"form": form, "accion": "Editar"})


@login_required
def vehiculo_delete(request, id):
    """Elimina un vehículo del sistema.
    
    POST directo: Elimina el vehículo. También elimina movimientos asociados
    por relación CASCADE. Redirige a lista de vehículos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        id (int): ID del vehículo a eliminar.
        
    Returns:
        HttpResponseRedirect: Redirección a vehiculo_list.
        Http404: Si el vehículo no existe.
    """
    vehiculo = get_object_or_404(Vehiculo, id=id)
    vehiculo.delete()
    messages.success(request, "Vehículo eliminado correctamente.")
    return redirect("vehiculo_list")


# --------------------------
#   CRUD MOVIMIENTO CARGA
# --------------------------

@login_required
def movimiento_list(request):
    """Lista todos los movimientos de carga del sistema.
    
    Utiliza select_related para optimizar consultas a BD (obtiene vehiculo
    en una sola query). Ordena movimientos por fecha descendente.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Plantilla movimientos/list.html con lista de movimientos.
    """
    movimientos = MovimientoCarga.objects.select_related('vehiculo').all()
    return render(request, "movimientos/list.html", {"movimientos": movimientos})


@login_required
def movimiento_create(request):
    """Registra un nuevo movimiento de carga.
    
    GET: Muestra formulario vacío para crear movimiento.
    POST: Valida datos (incluida fecha no futura) y guarda movimiento.
          Redirige a lista si es exitoso.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Formulario (GET) o redirección a lista (POST exitoso).
    """
    if request.method == "POST":
        form = MovimientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Movimiento registrado correctamente.")
            return redirect("movimiento_list")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = MovimientoForm()
    return render(request, "movimientos/form.html", {"form": form, "accion": "Crear"})


@login_required
def movimiento_update(request, id):
    """Actualiza los datos de un movimiento de carga existente.
    
    GET: Muestra formulario con datos del movimiento.
    POST: Valida cambios y actualiza registro.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        id (int): ID del movimiento a editar.
        
    Returns:
        HttpResponse: Formulario (GET) o redirección a lista (POST exitoso).
        Http404: Si el movimiento no existe.
    """
    movimiento = get_object_or_404(MovimientoCarga, id=id)
    if request.method == "POST":
        form = MovimientoForm(request.POST, instance=movimiento)
        if form.is_valid():
            form.save()
            messages.success(request, "Movimiento actualizado correctamente.")
            return redirect("movimiento_list")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = MovimientoForm(instance=movimiento)
    return render(request, "movimientos/form.html", {"form": form, "accion": "Editar"})


@login_required
def movimiento_delete(request, id):
    """Elimina un registro de movimiento de carga.
    
    POST directo: Elimina el movimiento y redirige a lista.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        id (int): ID del movimiento a eliminar.
        
    Returns:
        HttpResponseRedirect: Redirección a movimiento_list.
        Http404: Si el movimiento no existe.
    """
    movimiento = get_object_or_404(MovimientoCarga, id=id)
    movimiento.delete()
    messages.success(request, "Movimiento eliminado correctamente.")
    return redirect("movimiento_list")
