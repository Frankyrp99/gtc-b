from django.db import models
from django.utils import timezone
from users.models import User

class Entidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    director_general = models.OneToOneField(  # Director asignado
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entidad_dirigida'
    )
    
    def __str__(self):
        return self.nombre

class OpcionPersonalizada(models.Model):
    TIPO_CHOICES = [
        ('ASENTAMIENTO', 'Asentamiento'),
        ('PERSONAL', 'Personal de atención'),
    ]
    
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    valor = models.CharField(max_length=255)
    
    class Meta:
        unique_together = [('entidad', 'tipo', 'valor')]
    
    def __str__(self):
        return f"{self.get_tipo_display()}: {self.valor}"

class CustomManager(models.Manager):
    def get(self, *args, **kwargs):
        instance = super().get(*args, **kwargs)
        if instance:
            instance.actualizar_tiempo_proceso()
        return instance

class Solicitud(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
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
    
    objects = CustomManager()
    
    class Meta:
        unique_together = [('entidad', 'numero_orden')]
    
    def __str__(self):
        return f"{self.entidad}: {self.numero_orden} - {self.nombre_apellidos}"
    
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