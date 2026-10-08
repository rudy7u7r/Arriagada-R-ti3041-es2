from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto

def lista_productos(request):
    productos = Producto.objects.all()

    query_nombre = request.GET.get('q', '')
    categoria_filtro = request.GET.get('categoria', '')

    if query_nombre:
        productos = productos.filter(nombre__icontains=query_nombre)

    if categoria_filtro:
        productos = productos.filter(categoria=categoria_filtro)

    categorias = Producto.objects.values_list('categoria', flat=True).distinct()

    # Cálculo del total de ítems en el carrito para el badge superior
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

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if producto.stock <= 0:
        messages.error(request, f'¡Sin stock disponible para {producto.nombre}!')
        return redirect('lista_productos')

    carrito = request.session.get('carrito', {})
    id_str = str(producto_id)
    
    cantidad_actual = carrito.get(id_str, 0)
    
    if cantidad_actual + 1 > producto.stock:
        messages.warning(request, f'No puedes agregar más unidades de {producto.nombre}. Stock máximo: {producto.stock}')
    else:
        carrito[id_str] = cantidad_actual + 1
        request.session['carrito'] = carrito
        messages.success(request, f'{producto.nombre} agregado al carrito.')

    return redirect('lista_productos')

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

def vaciar_carrito(request):
    if 'carrito' in request.session:
        del request.session['carrito']
        messages.info(request, 'El carrito ha sido vaciado.')
    return redirect('ver_carrito')

def procesar_compra(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('ver_carrito')

    # Validar y descontar stock por cada producto
    comprados = []
    for prod_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id=prod_id)
            if not producto.descontar_stock(cantidad):
                messages.error(request, f'Stock insuficiente para {producto.nombre}. Disponibles: {producto.stock}')
                return redirect('ver_carrito')
            comprados.append(producto.nombre)
        except Producto.DoesNotExist:
            continue

    # Limpiar carrito tras la compra exitosa
    request.session['carrito'] = {}
    messages.success(request, '¡Compra realizada con éxito en La Ferretería Mordekaiser! El stock se actualizó.')
    return redirect('lista_productos')