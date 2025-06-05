from django.db import models
from django.utils import timezone

class CustomManager(models.Manager):
    def get(self, *args, **kwargs):
        instance = super().get(*args, **kwargs)
        if instance:
            instance.actualizar_tiempo_proceso()
        return instance

class Solicitud(models.Model):
    numero_orden = models.CharField(max_length=10)
    numero_certificado = models.CharField(max_length=10)
    nombre_apellidos = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    fecha_entrada = models.DateField(editable=True)
    personal_atencion = models.CharField(max_length=255)
    estado = models.CharField(max_length=50)
    asentamiento = models.CharField(max_length=50)
    persona = models.CharField(max_length=50)
    fecha_entrega = models.DateField(blank=True, null=True)
    tiempo_proceso = models.IntegerField(null=True, blank=True)
    
    objects = CustomManager()  # Esto faltaba en tu código original
    
    def __str__(self):  # Corregido de str a __str__
        return f"{self.numero_orden} - {self.nombre_apellidos}"
    
    def update_status(self, new_status):
        current_status = self.estado
        if new_status in ["Cancelado", "Entregado"]:
            # Si no hay fecha de entrega, establecer la fecha actual
            if not self.fecha_entrega:
                self.fecha_entrega = timezone.now().date()
            self.actualizar_tiempo_proceso()
        
        self.estado = new_status
        self.save()

    def actualizar_tiempo_proceso(self):
        days = self.calcular_tiempo_proceso
        self.tiempo_proceso = days
        self.save()

    @property
    def calcular_tiempo_proceso(self):
        if self.fecha_entrega:
            diff = self.fecha_entrega - self.fecha_entrada
        else:
            diff = timezone.now().date() - self.fecha_entrada
        return diff.days