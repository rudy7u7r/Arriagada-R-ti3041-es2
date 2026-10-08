from django.db import models

from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField()
    # Campo para la ruta estática local de la imagen
    imagen = models.CharField(max_length=255, default='catalogo/img/default.jpg')

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

    def descontar_stock(self, cantidad):
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

    def descontar_stock(self, cantidad):
        """Descuenta la cantidad comprada si hay stock suficiente."""
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
            return True
        return False