from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from .models import Producto

# --- FORMULARIO DE REGISTRO SENCILLO EN ESPAÑOL ---

class RegistroSencilloForm(forms.ModelForm):
    username = forms.CharField(label="Nombre de usuario", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}))
    confirm_password = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}))

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        return cleaned_data


# --- VISTAS DE AUTENTICACIÓN ---

def register_view(request):
    if request.user.is_authenticated:
        return redirect('lista_productos')
    if request.method == 'POST':
        form = RegistroSencilloForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            messages.success(request, f'¡Cuenta creada con éxito! Bienvenido, {user.username}.')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Ocurrió un error en el registro. Por favor verifica los datos.')
    else:
        form = RegistroSencilloForm()
    return render(request, 'catalogo/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('lista_productos')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Sesión iniciada correctamente. ¡Hola, {user.username}!')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'catalogo/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado la sesión de forma segura.')
    return redirect('lista_productos')


# --- VISTAS DEL CATÁLOGO Y CARRITO ---

def lista_productos(request):
    productos = Producto.objects.all()

    query_nombre = request.GET.get('q', '')
    categoria_filtro = request.GET.get('categoria', '')

    if query_nombre:
        productos = productos.filter(nombre__icontains=query_nombre)

    if categoria_filtro:
        productos = productos.filter(categoria=categoria_filtro)

    categorias = Producto.objects.values_list('categoria', flat=True).distinct()

    carrito = request.session.get('carrito', {})
    total_items_carrito = sum(carrito.values())

    context = {
        'productos': productos,
        'categorias': categorias,
        'query_nombre': query_nombre,
        'categoria_filtro': categoria_filtro,
        'total_items_carrito': total_items_carrito,
    }

    return render(request, 'catalogo/lista_productos.html', context)

@login_required(login_url='login')
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if producto.stock <= 0:
        messages.error(request, f'¡Sin unidades disponibles para {producto.nombre}!')
        return redirect('lista_productos')

    carrito = request.session.get('carrito', {})
    id_str = str(producto_id)
    
    cantidad_actual = carrito.get(id_str, 0)
    
    if cantidad_actual + 1 > producto.stock:
        messages.warning(request, f'No puedes agregar más unidades de {producto.nombre}. Límite en bodega: {producto.stock}')
    else:
        carrito[id_str] = cantidad_actual + 1
        request.session['carrito'] = carrito
        messages.success(request, f'{producto.nombre} agregado a tu compra.')

    return redirect('lista_productos')

@login_required(login_url='login')
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0

    for prod_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id=prod_id)
            subtotal = producto.precio * cantidad
            total += subtotal
            items.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
        except Producto.DoesNotExist:
            continue

    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'catalogo/carrito.html', context)

@login_required(login_url='login')
def vaciar_carrito(request):
    if 'carrito' in request.session:
        del request.session['carrito']
        messages.info(request, 'El carrito ha sido vaciado.')
    return redirect('ver_carrito')

@login_required(login_url='login')
def confirmar_compra(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.error(request, 'Tu carrito de compras está vacío.')
        return redirect('ver_carrito')

    items = []
    total = 0
    for prod_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id=prod_id)
            subtotal = producto.precio * cantidad
            total += subtotal
            items.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
        except Producto.DoesNotExist:
            continue

    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'catalogo/confirmar_compra.html', context)

@login_required(login_url='login')
def procesar_compra(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        if not carrito:
            messages.error(request, 'Tu carrito está vacío.')
            return redirect('ver_carrito')

        for prod_id, cantidad in carrito.items():
            try:
                producto = Producto.objects.get(id=prod_id)
                if not producto.descontar_stock(cantidad):
                    messages.error(request, f'Sin inventario suficiente para {producto.nombre}. Disponibles: {producto.stock}')
                    return redirect('ver_carrito')
            except Producto.DoesNotExist:
                continue

        request.session['carrito'] = {}
        messages.success(request, '¡Compra realizada con éxito! El inventario ha sido actualizado correctamente.')
        return redirect('lista_productos')
    
    return redirect('ver_carrito')