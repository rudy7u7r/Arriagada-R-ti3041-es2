from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

    def descontar_stock(self, cantidad):
        """Descuenta la cantidad comprada si hay stock suficiente."""
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
            return True
        return False