import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from catalogo.models import Producto

productos_ferreteria = [
    # Herramientas Manuales
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

    # Herramientas Eléctricas
    {"nombre": "Taladro Percutor 650W", "categoria": "Herramientas Eléctricas", "precio": 45990, "stock": 12},
    {"nombre": "Esmeril Angular 4.5\" 700W", "categoria": "Herramientas Eléctricas", "precio": 32990, "stock": 10},
    {"nombre": "Sierra Caladora 500W", "categoria": "Herramientas Eléctricas", "precio": 38990, "stock": 8},
    {"nombre": "Atornillador Inalámbrico 12V", "categoria": "Herramientas Eléctricas", "precio": 29990, "stock": 16},
    {"nombre": "Lijadora Orbital 200W", "categoria": "Herramientas Eléctricas", "precio": 27990, "stock": 9},
    {"nombre": "Sierra Circular 7-1/4\" 1400W", "categoria": "Herramientas Eléctricas", "precio": 64990, "stock": 6},
    {"nombre": "Pistola de Calor 1800W", "categoria": "Herramientas Eléctricas", "precio": 21990, "stock": 11},
    {"nombre": "Rotomartillo SDS Plus 800W", "categoria": "Herramientas Eléctricas", "precio": 78990, "stock": 5},

    # Medición y Nivelación
    {"nombre": "Cinta Métrica 5m", "categoria": "Medición", "precio": 2990, "stock": 40},
    {"nombre": "Cinta Métrica 8m", "categoria": "Medición", "precio": 4990, "stock": 25},
    {"nombre": "Nivel de Aluminio 24\"", "categoria": "Medición", "precio": 7990, "stock": 15},
    {"nombre": "Escuadra de Carpintero 12\"", "categoria": "Medición", "precio": 3890, "stock": 28},
    {"nombre": "Pie de Metro Digital 150mm", "categoria": "Medición", "precio": 12990, "stock": 12},

    # Construcción y Fijaciones
    {"nombre": "Caja de Clavos para Madera 2\"", "categoria": "Fijaciones", "precio": 1990, "stock": 100},
    {"nombre": "Set de Tarugos y Tornillos 100 pzs", "categoria": "Fijaciones", "precio": 3490, "stock": 80},
    {"nombre": "Cinta Aisladora Negra 18m", "categoria": "Electricidad", "precio": 990, "stock": 150},
    {"nombre": "Silicona Transparente Multiuso 280ml", "categoria": "Adhesivos", "precio": 3290, "stock": 45},
    {"nombre": "Espuma de Poliuretano 500ml", "categoria": "Adhesivos", "precio": 5490, "stock": 30},
    {"nombre": "Adhesivo de Contacto 250ml", "categoria": "Adhesivos", "precio": 3890, "stock": 22},

    # Pintura y Acabados
    {"nombre": "Brocha para Pintura 3\"", "categoria": "Pintura", "precio": 2190, "stock": 50},
    {"nombre": "Rodillo Antigota 18cm", "categoria": "Pintura", "precio": 3990, "stock": 35},
    {"nombre": "Bandeja para Pintura Plástica", "categoria": "Pintura", "precio": 1490, "stock": 40},
    {"nombre": "Cinta Masking Tape 24mm x 40m", "categoria": "Pintura", "precio": 1890, "stock": 70},
    {"nombre": "Esmalte al Agua Blanco 1 Galón", "categoria": "Pintura", "precio": 18990, "stock": 14},

    # Seguridad y Almacenamiento
    {"nombre": "Guantes de Cabritilla Talla L", "categoria": "Seguridad", "precio": 3290, "stock": 60},
    {"nombre": "Lentes de Seguridad Transparentes", "categoria": "Seguridad", "precio": 1990, "stock": 80},
    {"nombre": "Mascarilla Detección Polvo (Pack 5)", "categoria": "Seguridad", "precio": 2490, "stock": 50},
    {"nombre": "Caja de Herramientas Plástica 16\"", "categoria": "Almacenamiento", "precio": 11990, "stock": 18},
    {"nombre": "Organizador de Tornillos 12 Compartimientos", "categoria": "Almacenamiento", "precio": 6990, "stock": 25},
    {"nombre": "Candado de Bronce 40mm", "categoria": "Seguridad", "precio": 4590, "stock": 32},
]

for prod in productos_ferreteria:
    Producto.objects.get_or_create(
        nombre=prod["nombre"],
        defaults={
            "categoria": prod["categoria"],
            "precio": prod["precio"],
            "stock": prod["stock"],
        }
    )

print("¡40 productos de ferretería cargados con éxito!")