from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Vehiculo, MovimientoCarga
from .forms import VehiculoForm, MovimientoForm


# --------------------------
#        INICIO
# --------------------------
def home(request):
    # Si está logueado, enviar directo a la lista
    if request.user.is_authenticated:
        return redirect("vehiculo_list")
    return redirect("login")  # Ir a login por defecto


# --------------------------
#     CRUD VEHÍCULOS
# --------------------------

@login_required
def vehiculo_list(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, "vehiculos/list.html", {"vehiculos": vehiculos})


@login_required
def vehiculo_create(request):
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
    vehiculo = get_object_or_404(Vehiculo, id=id)
    vehiculo.delete()
    messages.success(request, "Vehículo eliminado correctamente.")
    return redirect("vehiculo_list")


# --------------------------
#   CRUD MOVIMIENTO CARGA
# --------------------------

@login_required
def movimiento_list(request):
    movimientos = MovimientoCarga.objects.select_related("vehiculo").all()
    return render(request, "movimientos/list.html", {"movimientos": movimientos})


@login_required
def movimiento_create(request):
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
    return render(request, "movimientos/form.html", {"form": form, "accion": "Registrar"})


@login_required
def movimiento_update(request, id):
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
    movimiento = get_object_or_404(MovimientoCarga, id=id)
    movimiento.delete()
    messages.success(request, "Movimiento eliminado correctamente.")
    return redirect("movimiento_list")
