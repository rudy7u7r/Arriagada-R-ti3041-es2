import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')

# URLs DE IMÁGENES: una URL diferente para cada producto del catálogo inicial.
URL_IMAGENES = {
    "Martillo de Uña 16oz": "https://images.pexels.com/photos/4792530/pexels-photo-4792530.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Destornillador Phillips PH2": "https://images.pexels.com/photos/5583106/pexels-photo-5583106.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Destornillador Plano 6mm": "https://images.pexels.com/photos/5583095/pexels-photo-5583095.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Alicate Universal 8\"": "https://images.pexels.com/photos/5583081/pexels-photo-5583081.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Alicate de Punta 6\"": "https://images.pexels.com/photos/5583100/pexels-photo-5583100.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Juego de Llaves Allen 9 pzs": "https://images.pexels.com/photos/9607054/pexels-photo-9607054.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Llave Ajustable 10\" (Francesa)": "https://images.pexels.com/photos/30413496/pexels-photo-30413496.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Serrucho de Carpintero 20\"": "https://images.pexels.com/photos/11324766/pexels-photo-11324766.jpeg?cs=tinysrgb&dpr=1&w=700",
    "CortaCartón Profesional 18mm": "https://images.pexels.com/photos/5038398/pexels-photo-5038398.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Formón para Madera 3/4\"": "https://images.pexels.com/photos/19354576/pexels-photo-19354576.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Taladro Percutor 650W": "https://images.pexels.com/photos/3877525/pexels-photo-3877525.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Esmeril Angular 4.5\" 700W": "https://images.pexels.com/photos/37517095/pexels-photo-37517095.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Sierra Caladora 500W": "https://images.pexels.com/photos/1094766/pexels-photo-1094766.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Atornillador Inalámbrico 12V": "https://images.pexels.com/photos/8811530/pexels-photo-8811530.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Lijadora Orbital 200W": "https://images.pexels.com/photos/5059649/pexels-photo-5059649.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Sierra Circular 7-1/4\" 1400W": "https://images.pexels.com/photos/32391497/pexels-photo-32391497.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Pistola de Calor 1800W": "https://images.pexels.com/photos/17419786/pexels-photo-17419786.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Rotomartillo SDS Plus 800W": "https://images.pexels.com/photos/8487757/pexels-photo-8487757.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Cinta Métrica 5m": "https://images.pexels.com/photos/10895042/pexels-photo-10895042.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Cinta Métrica 8m": "https://images.pexels.com/photos/3143082/pexels-photo-3143082.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Nivel de Aluminio 24\"": "https://images.pexels.com/photos/6251067/pexels-photo-6251067.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Escuadra de Carpintero 12\"": "https://images.pexels.com/photos/29264971/pexels-photo-29264971.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Pie de Metro Digital 150mm": "https://images.pexels.com/photos/28231807/pexels-photo-28231807.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Caja de Clavos para Madera 2\"": "https://images.pexels.com/photos/190101/pexels-photo-190101.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Set de Tarugos y Tornillos 100 pzs": "https://images.pexels.com/photos/5583045/pexels-photo-5583045.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Cinta Aisladora Negra 18m": "https://images.pexels.com/photos/3614763/pexels-photo-3614763.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Silicona Transparente Multiuso 280ml": "https://images.pexels.com/photos/6124242/pexels-photo-6124242.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Espuma de Poliuretano 500ml": "https://images.pexels.com/photos/6124239/pexels-photo-6124239.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Adhesivo de Contacto 250ml": "https://images.pexels.com/photos/5691660/pexels-photo-5691660.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Brocha para Pintura 3\"": "https://images.pexels.com/photos/6925081/pexels-photo-6925081.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Rodillo Antigota 18cm": "https://images.pexels.com/photos/5583052/pexels-photo-5583052.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Bandeja para Pintura Plástica": "https://images.pexels.com/photos/5641684/pexels-photo-5641684.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Cinta Masking Tape 24mm x 40m": "https://images.pexels.com/photos/5583126/pexels-photo-5583126.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Esmalte al Agua Blanco 1 Galón": "https://images.pexels.com/photos/5691684/pexels-photo-5691684.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Guantes de Cabritilla Talla L": "https://images.pexels.com/photos/8488037/pexels-photo-8488037.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Lentes de Seguridad Transparentes": "https://images.pexels.com/photos/8943270/pexels-photo-8943270.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Mascarilla Detección Polvo (Pack 5)": "https://images.pexels.com/photos/8442810/pexels-photo-8442810.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Caja de Herramientas Plástica 16\"": "https://images.pexels.com/photos/9606740/pexels-photo-9606740.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Organizador de Tornillos 12 Compartimientos": "https://images.pexels.com/photos/8470252/pexels-photo-8470252.jpeg?cs=tinysrgb&dpr=1&w=700",
    "Candado de Bronce 40mm": "https://images.pexels.com/photos/36740854/pexels-photo-36740854.jpeg?cs=tinysrgb&dpr=1&w=700",
}

URLS_IMAGENES_ANTERIORES = {
    "https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1581783898377-1c85bf937427?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1530124566582-a618bc2615dc?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1581092921461-eab62e97a780?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1586864387967-d02ef85d93e8?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1616401784845-180882ba9ba8?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1540339832862-474599807836?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1572981779307-38b8cabb2407?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&w=900&q=80",
}

productos_ferreteria = [
    # --- Herramientas Manuales (10) ---
    {"nombre": "Martillo de Uña 16oz", "categoria": "Herramientas Manuales", "precio": 8990, "stock": 25},
    {"nombre": "Destornillador Phillips PH2", "categoria": "Herramientas Manuales", "precio": 3490, "stock": 50},
    {"nombre": "Destornillador Plano 6mm", "categoria": "Herramientas Manuales", "precio": 3290, "stock": 45},
    {"nombre": "Alicate Universal 8\"", "categoria": "Herramientas Manuales", "precio": 5990, "stock": 30},
    {"nombre": "Alicate de Punta 6\"", "categoria": "Herramientas Manuales", "precio": 5490, "stock": 22},
    {"nombre": "Juego de Llaves Allen 9 pzs", "categoria": "Herramientas Manuales", "precio": 6490, "stock": 20},
    {"nombre": "Llave Ajustable 10\" (Francesa)", "categoria": "Herramientas Manuales", "precio": 7990, "stock": 18},
    {"nombre": "Serrucho de Carpintero 20\"", "categoria": "Herramientas Manuales", "precio": 9990, "stock": 15},
    {"nombre": "CortaCartón Profesional 18mm", "categoria": "Herramientas Manuales", "precio": 2490, "stock": 60},
    {"nombre": "Formón para Madera 3/4\"", "categoria": "Herramientas Manuales", "precio": 4290, "stock": 14},

    # --- Herramientas Eléctricas (8) ---
    {"nombre": "Taladro Percutor 650W", "categoria": "Herramientas Eléctricas", "precio": 45990, "stock": 12},
    {"nombre": "Esmeril Angular 4.5\" 700W", "categoria": "Herramientas Eléctricas", "precio": 32990, "stock": 10},
    {"nombre": "Sierra Caladora 500W", "categoria": "Herramientas Eléctricas", "precio": 38990, "stock": 8},
    {"nombre": "Atornillador Inalámbrico 12V", "categoria": "Herramientas Eléctricas", "precio": 29990, "stock": 16},
    {"nombre": "Lijadora Orbital 200W", "categoria": "Herramientas Eléctricas", "precio": 27990, "stock": 9},
    {"nombre": "Sierra Circular 7-1/4\" 1400W", "categoria": "Herramientas Eléctricas", "precio": 64990, "stock": 6},
    {"nombre": "Pistola de Calor 1800W", "categoria": "Herramientas Eléctricas", "precio": 21990, "stock": 11},
    {"nombre": "Rotomartillo SDS Plus 800W", "categoria": "Herramientas Eléctricas", "precio": 78990, "stock": 5},

    # --- Medición y Nivelación (5) ---
    {"nombre": "Cinta Métrica 5m", "categoria": "Medición", "precio": 2990, "stock": 40},
    {"nombre": "Cinta Métrica 8m", "categoria": "Medición", "precio": 4990, "stock": 25},
    {"nombre": "Nivel de Aluminio 24\"", "categoria": "Medición", "precio": 7990, "stock": 15},
    {"nombre": "Escuadra de Carpintero 12\"", "categoria": "Medición", "precio": 3890, "stock": 28},
    {"nombre": "Pie de Metro Digital 150mm", "categoria": "Medición", "precio": 12990, "stock": 12},

    # --- Construcción y Fijaciones (6) ---
    {"nombre": "Caja de Clavos para Madera 2\"", "categoria": "Fijaciones", "precio": 1990, "stock": 100},
    {"nombre": "Set de Tarugos y Tornillos 100 pzs", "categoria": "Fijaciones", "precio": 3490, "stock": 80},
    {"nombre": "Cinta Aisladora Negra 18m", "categoria": "Electricidad", "precio": 990, "stock": 150},
    {"nombre": "Silicona Transparente Multiuso 280ml", "categoria": "Adhesivos", "precio": 3290, "stock": 45},
    {"nombre": "Espuma de Poliuretano 500ml", "categoria": "Adhesivos", "precio": 5490, "stock": 30},
    {"nombre": "Adhesivo de Contacto 250ml", "categoria": "Adhesivos", "precio": 3890, "stock": 22},

    # --- Pintura y Acabados (5) ---
    {"nombre": "Brocha para Pintura 3\"", "categoria": "Pintura", "precio": 2190, "stock": 50},
    {"nombre": "Rodillo Antigota 18cm", "categoria": "Pintura", "precio": 3990, "stock": 35},
    {"nombre": "Bandeja para Pintura Plástica", "categoria": "Pintura", "precio": 1490, "stock": 40},
    {"nombre": "Cinta Masking Tape 24mm x 40m", "categoria": "Pintura", "precio": 1890, "stock": 70},
    {"nombre": "Esmalte al Agua Blanco 1 Galón", "categoria": "Pintura", "precio": 18990, "stock": 14},

    # --- Seguridad y Almacenamiento (6) ---
    {"nombre": "Guantes de Cabritilla Talla L", "categoria": "Seguridad", "precio": 3290, "stock": 60},
    {"nombre": "Lentes de Seguridad Transparentes", "categoria": "Seguridad", "precio": 1990, "stock": 80},
    {"nombre": "Mascarilla Detección Polvo (Pack 5)", "categoria": "Seguridad", "precio": 2490, "stock": 50},
    {"nombre": "Caja de Herramientas Plástica 16\"", "categoria": "Almacenamiento", "precio": 11990, "stock": 18},
    {"nombre": "Organizador de Tornillos 12 Compartimientos", "categoria": "Almacenamiento", "precio": 6990, "stock": 25},
    {"nombre": "Candado de Bronce 40mm", "categoria": "Seguridad", "precio": 4590, "stock": 32},
]


def poblar_productos():
    from catalogo.models import Producto

    nombres_productos = {producto["nombre"] for producto in productos_ferreteria}
    urls_sin_producto = set(URL_IMAGENES) - nombres_productos
    productos_sin_url = nombres_productos - set(URL_IMAGENES)
    if urls_sin_producto or productos_sin_url:
        raise ValueError(
            "La lista de productos y las URLs de imagen deben coincidir. "
            f"Sin URL: {sorted(productos_sin_url)}; sin producto: {sorted(urls_sin_producto)}."
        )
    if len(set(URL_IMAGENES.values())) != len(URL_IMAGENES):
        raise ValueError("Cada producto debe tener una URL de imagen diferente.")

    creados = 0
    imagenes_actualizadas = 0
    for producto in productos_ferreteria:
        imagen_url = URL_IMAGENES[producto["nombre"]]
        producto_guardado, creado = Producto.objects.get_or_create(
            nombre=producto["nombre"],
            defaults={
                "categoria": producto["categoria"],
                "precio": producto["precio"],
                "stock": producto["stock"],
                "imagen": imagen_url,
            },
        )
        creados += creado
        if not creado and (
            not producto_guardado.imagen
            or producto_guardado.imagen.startswith("catalogo/img/")
            or producto_guardado.imagen in URLS_IMAGENES_ANTERIORES
        ):
            producto_guardado.imagen = imagen_url
            producto_guardado.save(update_fields=["imagen"])
            imagenes_actualizadas += 1

    print(
        f"Poblamiento completado: {creados} productos nuevos agregados; "
        f"{imagenes_actualizadas} imágenes locales actualizadas."
    )


if __name__ == "__main__":
    import django

    django.setup()
    poblar_productos()