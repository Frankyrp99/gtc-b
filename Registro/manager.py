from django.db import models

class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get(self, *args, **kwargs):
        instance = super().get(*args, **kwargs)
        if instance:
            instance.actualizar_tiempo_proceso()
        return instance
