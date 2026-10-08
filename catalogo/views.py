from django.shortcuts import render
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

    context = {
        'productos': productos,
        'categorias': categorias,
        'query_nombre': query_nombre,
        'categoria_filtro': categoria_filtro,
    }

    return render(request, 'catalogo/lista_productos.html', context)