from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms
from django.contrib.auth.models import User
from django.db import DatabaseError
from django.db.models import Count, Q, Sum
from django.db.utils import OperationalError
from django.utils.text import slugify
from .models import Producto
from django.conf import settings
from django.core.files.storage import default_storage


CATEGORIAS_CATALOGO = {
    'Herramientas Eléctricas': {
        'icono': 'bi-lightning-charge',
        'resumen': 'Potencia y velocidad para avanzar en trabajos exigentes.',
        'uso': 'Ideales para perforar, cortar, lijar y atornillar con menos esfuerzo en obras y proyectos de renovación.',
    },
    'Herramientas Manuales': {
        'icono': 'bi-tools',
        'resumen': 'Control y precisión para los detalles de cada proyecto.',
        'uso': 'Úsalas para ajustar, sujetar, cortar y dar terminaciones con precisión en reparaciones y trabajos de carpintería.',
    },
    'Medición': {
        'icono': 'bi-rulers',
        'resumen': 'Mide y nivela antes de cada corte o instalación.',
        'uso': 'Permiten tomar medidas, comprobar niveles y marcar referencias para lograr instalaciones y cortes exactos.',
    },
    'Fijaciones': {
        'icono': 'bi-nut',
        'resumen': 'Uniones firmes para montajes que deben durar.',
        'uso': 'Clavos, tarugos y tornillos para fijar piezas de madera y asegurar montajes en distintos materiales.',
    },
    'Electricidad': {
        'icono': 'bi-plug',
        'resumen': 'Insumos prácticos para reparaciones eléctricas.',
        'uso': 'Productos para aislar y proteger conexiones durante trabajos de instalación y mantenimiento eléctrico.',
    },
    'Adhesivos': {
        'icono': 'bi-droplet',
        'resumen': 'Adhiere, sella y rellena según la necesidad del trabajo.',
        'uso': 'Soluciones para pegar materiales, sellar juntas y rellenar espacios en reparaciones y terminaciones.',
    },
    'Pintura': {
        'icono': 'bi-paint-bucket',
        'resumen': 'Prepara y renueva superficies con un acabado uniforme.',
        'uso': 'Brochas, rodillos y accesorios para aplicar pintura, proteger superficies y conseguir terminaciones prolijas.',
    },
    'Seguridad': {
        'icono': 'bi-shield-check',
        'resumen': 'Protección personal para trabajar con mayor seguridad.',
        'uso': 'Elementos de protección para reducir la exposición a polvo, impactos y riesgos comunes del trabajo.',
    },
    'Almacenamiento': {
        'icono': 'bi-box-seam',
        'resumen': 'Mantén tus herramientas e insumos ordenados y protegidos.',
        'uso': 'Cajas y organizadores para guardar herramientas, separar fijaciones y encontrar cada pieza rápidamente.',
    },
}


class ProductoForm(forms.ModelForm):
    imagen_url = forms.URLField(
        required=False,
        label='URL de la imagen',
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'})
    )
    imagen_archivo = forms.ImageField(
        required=False,
        label='Subir imagen desde archivo',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )

    imagen = forms.CharField(
        required=False,
        label='Ruta de imagen actual',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'catalogo/img/ejemplo.jpg'})
    )

    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio', 'stock', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        archivo = self.cleaned_data.get('imagen_archivo')
        url = self.cleaned_data.get('imagen_url')

        if archivo:
            nombre_archivo = default_storage.save(f'productos/{archivo.name}', archivo)
            instance.imagen = f"{settings.MEDIA_URL}{nombre_archivo}"
        elif url:
            instance.imagen = url
        elif not instance.imagen:
            instance.imagen = 'catalogo/img/default.jpg'

        if commit:
            instance.save()
        return instance


def staff_required(view_func):
    decorated = user_passes_test(lambda u: u.is_active and u.is_staff, login_url='login')(view_func)
    return decorated


def customer_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            messages.info(request, 'El carrito solo está disponible para cuentas de cliente.')
            return redirect('admin_panel')
        return view_func(request, *args, **kwargs)

    return login_required(login_url='login')(wrapped_view)


def _safe_db_call(request, callback, fallback=None, message='No se pudo acceder a la base de datos. Inténtalo más tarde.'):
    try:
        return callback()
    except (OperationalError, DatabaseError, Exception):
        messages.error(request, message)
        return fallback


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


class InicioSesionForm(AuthenticationForm):
    error_messages = AuthenticationForm.error_messages.copy()
    error_messages['invalid_login'] = 'Nombre de usuario o contraseña incorrectos.'


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
        form = InicioSesionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Sesión iniciada correctamente. ¡Hola, {user.username}!')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = InicioSesionForm()
    return render(request, 'catalogo/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado la sesión de forma segura.')
    return redirect('lista_productos')


# --- VISTAS DEL CATÁLOGO Y CARRITO ---

def lista_productos(request):
    auth_mode = ''
    auth_login_form = InicioSesionForm(request, prefix='login')
    auth_register_form = RegistroSencilloForm(prefix='register')
    if request.method == 'POST' and not request.user.is_authenticated:
        auth_mode = request.POST.get('auth_action', '')
        if auth_mode == 'login':
            auth_login_form = InicioSesionForm(request, data=request.POST, prefix='login')
            if auth_login_form.is_valid():
                user = auth_login_form.get_user()
                login(request, user)
                messages.success(request, f'Sesión iniciada correctamente. ¡Hola, {user.username}!')
                return redirect(request.get_full_path())
        elif auth_mode == 'register':
            auth_register_form = RegistroSencilloForm(request.POST, prefix='register')
            if auth_register_form.is_valid():
                user = User.objects.create_user(
                    username=auth_register_form.cleaned_data['username'],
                    password=auth_register_form.cleaned_data['password'],
                )
                login(request, user)
                messages.success(request, f'¡Cuenta creada con éxito! Bienvenido, {user.username}.')
                return redirect(request.get_full_path())
        else:
            return redirect('lista_productos')

    todos_productos = _safe_db_call(
        request,
        lambda: list(Producto.objects.all().order_by('categoria', 'nombre')),
        fallback=[],
        message='No se pudo cargar el catálogo porque la base de datos no está disponible.'
    )

    categorias = sorted({producto.categoria for producto in todos_productos})
    productos = todos_productos
    query_nombre = request.GET.get('q', '')
    categoria_filtro = request.GET.get('categoria', '')
    orden_actual = request.GET.get('orden', 'relevancia')
    if orden_actual not in {'relevancia', 'precio_asc', 'precio_desc', 'nombre'}:
        orden_actual = 'relevancia'

    if query_nombre:
        nombre_buscado = query_nombre.casefold()
        productos = [
            producto for producto in productos
            if nombre_buscado in producto.nombre.casefold()
        ]

    if categoria_filtro:
        productos = [
            producto for producto in productos
            if producto.categoria == categoria_filtro
        ]

    if orden_actual == 'precio_asc':
        productos.sort(key=lambda producto: (producto.precio, producto.nombre.casefold()))
    elif orden_actual == 'precio_desc':
        productos.sort(key=lambda producto: (-producto.precio, producto.nombre.casefold()))
    elif orden_actual == 'nombre':
        productos.sort(key=lambda producto: producto.nombre.casefold())

    categorias_conteo = [
        {
            'nombre': categoria,
            'cantidad': sum(
                producto.categoria == categoria
                for producto in todos_productos
            ),
            'icono': CATEGORIAS_CATALOGO.get(
                categoria,
                {'icono': 'bi-tools'},
            )['icono'],
        }
        for categoria in categorias
    ]

    productos_por_categoria = {}
    for producto in productos:
        productos_por_categoria.setdefault(producto.categoria, []).append(producto)

    if orden_actual != 'relevancia':
        categoria_seccion = categoria_filtro or 'Productos ordenados'
        detalles = CATEGORIAS_CATALOGO.get(categoria_filtro, {
            'icono': 'bi-sort-down',
            'resumen': 'Explora el catálogo ordenado según tu preferencia.',
            'uso': 'Compara precios y productos para elegir lo que mejor se ajuste a tu proyecto.',
        })
        secciones_catalogo = [{
            'nombre': categoria_seccion,
            'slug': 'productos-ordenados',
            'icono': detalles['icono'],
            'resumen': detalles['resumen'],
            'uso': detalles['uso'],
            'productos': productos,
        }]
    else:
        categorias_ordenadas = sorted(
            productos_por_categoria,
            key=lambda categoria: (
                categoria not in CATEGORIAS_CATALOGO,
                list(CATEGORIAS_CATALOGO).index(categoria)
                if categoria in CATEGORIAS_CATALOGO
                else categoria.casefold(),
            ),
        )
        secciones_catalogo = []
        for indice, categoria in enumerate(categorias_ordenadas, start=1):
            detalles = CATEGORIAS_CATALOGO.get(categoria, {
                'icono': 'bi-tools',
                'resumen': f'Productos y materiales de {categoria}.',
                'uso': 'Encuentra insumos y herramientas para tus tareas de construcción, reparación y mantenimiento.',
            })
            secciones_catalogo.append({
                'nombre': categoria,
                'slug': slugify(categoria) or f'categoria-{indice}',
                'icono': detalles['icono'],
                'resumen': detalles['resumen'],
                'uso': detalles['uso'],
                'productos': productos_por_categoria[categoria],
            })

    carrito = request.session.get('carrito', {})
    total_items_carrito = sum(carrito.values())

    context = {
        'secciones_catalogo': secciones_catalogo,
        'categorias': categorias,
        'categorias_conteo': categorias_conteo,
        'categorias_menu': categorias_conteo,
        'todos_productos_count': len(todos_productos),
        'query_nombre': query_nombre,
        'categoria_filtro': categoria_filtro,
        'orden_actual': orden_actual,
        'total_resultados': len(productos),
        'total_items_carrito': total_items_carrito,
        'auth_login_form': auth_login_form,
        'auth_register_form': auth_register_form,
        'auth_mode': auth_mode,
        'auth_modal_open': bool(auth_mode),
    }

    return render(request, 'catalogo/lista_productos.html', context)

@customer_required
def agregar_al_carrito(request, producto_id):
    try:
        producto = get_object_or_404(Producto, id=producto_id)
    except (OperationalError, DatabaseError, Exception):
        messages.error(request, 'La base de datos no está disponible en este momento.')
        return redirect('lista_productos')

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

@customer_required
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
        except (Producto.DoesNotExist, OperationalError, DatabaseError, Exception):
            continue

    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'catalogo/carrito.html', context)

@customer_required
def vaciar_carrito(request):
    if 'carrito' in request.session:
        del request.session['carrito']
        messages.info(request, 'El carrito ha sido vaciado.')
    return redirect('ver_carrito')

@customer_required
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
        except (Producto.DoesNotExist, OperationalError, DatabaseError, Exception):
            continue

    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'catalogo/confirmar_compra.html', context)

@customer_required
def procesar_compra(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        if not carrito:
            messages.error(request, 'Tu carrito está vacío.')
            return redirect('ver_carrito')

        try:
            for prod_id, cantidad in carrito.items():
                try:
                    producto = Producto.objects.get(id=prod_id)
                    if not producto.descontar_stock(cantidad):
                        messages.error(request, f'Sin inventario suficiente para {producto.nombre}. Disponibles: {producto.stock}')
                        return redirect('ver_carrito')
                except Producto.DoesNotExist:
                    continue
        except (OperationalError, DatabaseError, Exception):
            messages.error(request, 'No se pudo acceder a la base de datos para procesar tu compra. Inténtalo más tarde.')
            return redirect('ver_carrito')

        request.session['carrito'] = {}
        messages.success(request, '¡Compra realizada con éxito! El inventario ha sido actualizado correctamente.')
        return redirect('lista_productos')

    return redirect('ver_carrito')

# --- CRUD PRODUCTOS ---

@login_required(login_url='login')
@staff_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado con éxito.')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Error al crear el producto. Por favor verifica los datos.')
    else:
        form = ProductoForm()
    return render(request, 'catalogo/crear_producto.html', {'form': form})

@login_required(login_url='login')
@staff_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado con éxito.')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Error al actualizar el producto. Por favor verifica los datos.')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'catalogo/editar_producto.html', {'form': form, 'producto': producto})

@login_required(login_url='login')
@staff_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado con éxito.')
        return redirect('lista_productos')
    return render(request, 'catalogo/eliminar_producto.html', {'producto': producto})

@login_required(login_url='login')
@staff_required
def listar_productos_admin(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo/listar_productos_admin.html', {'productos': productos})

@staff_required
def productos_crud(request):
    productos = _safe_db_call(
        request,
        lambda: Producto.objects.all().order_by('id'),
        fallback=[],
        message='No se pudieron cargar los productos.'
    )
    return render(request, 'catalogo/crud_productos.html', {'productos': productos})


@staff_required
def producto_nuevo(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('productos_crud')
    else:
        form = ProductoForm()
    return render(request, 'catalogo/producto_form.html', {'form': form, 'titulo': 'Nuevo producto'})


@staff_required
def producto_editar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('productos_crud')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'catalogo/producto_form.html', {'form': form, 'titulo': 'Editar producto', 'producto': producto})


@staff_required
def producto_eliminar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    messages.success(request, 'Producto eliminado correctamente.')
    return redirect('productos_crud')


@user_passes_test(lambda u: u.is_active and u.is_staff)
def admin_panel(request):
    todos_productos = Producto.objects.all()
    query = request.GET.get('q', '').strip()
    productos = todos_productos.order_by('id')
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(categoria__icontains=query)
        )

    estadisticas = todos_productos.aggregate(
        total_stock=Sum('stock'),
        total_categorias=Count('categoria', distinct=True),
    )
    context = {
        'productos': productos,
        'query': query,
        'productos_encontrados': productos.count(),
        'total_productos': todos_productos.count(),
        'total_stock': estadisticas['total_stock'] or 0,
        'total_categorias': estadisticas['total_categorias'] or 0,
        'stock_bajo': todos_productos.filter(stock__lte=5).count(),
    }
    return render(request, 'catalogo/admin_panel.html', context)