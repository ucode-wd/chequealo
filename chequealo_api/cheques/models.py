from django.db import models

class ChequeProcesado(models.Model):
    imagen = models.ImageField(upload_to='cheques/', null=True, blank=True)
    numero_cheque = models.CharField(max_length=30)
    codigo_entidad = models.CharField(max_length=30)
    cuit = models.CharField(max_length=20)
    datos_denunciado = models.JSONField(null=True, blank=True)
    datos_rechazado = models.JSONField(null=True, blank=True)
    datos_deudas = models.JSONField(null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cheque {self.numero_cheque} - CUIT {self.cuit}"
