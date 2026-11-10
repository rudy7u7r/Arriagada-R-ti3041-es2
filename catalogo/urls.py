from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('checkout/', views.confirmar_compra, name='confirmar_compra'),
    path('checkout/procesar/', views.procesar_compra, name='procesar_compra'),
    path('admin/', views.admin_panel, name='admin_panel'),
    path('crud/', views.productos_crud, name='productos_crud'),
    path('crud/nuevo/', views.producto_nuevo, name='producto_nuevo'),
    path('crud/editar/<int:producto_id>/', views.producto_editar, name='producto_editar'),
    path('crud/eliminar/<int:producto_id>/', views.producto_eliminar, name='producto_eliminar'),
]