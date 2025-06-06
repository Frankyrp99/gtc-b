from rest_framework import generics
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from django.db.models import Prefetch
from .models import Solicitud
from .serializers import SolicitudSerializer


class SolicitudListCreateView(ListCreateAPIView):
    queryset = Solicitud.objects.all().order_by("id")
    serializer_class = SolicitudSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        new_status = data.get("estado", "En Proceso")

        # Crear la solicitud usando el serializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)  # Guarda la instancia en la BD
        instance = serializer.instance  # ← Obtiene la instancia creada

        # Lógica de actualización
        if new_status in ["Cancelado", "Entregado"]:
            instance.actualizar_tiempo_proceso()
            instance.save()  # Guardar cambios si actualizar_tiempo_proceso modifica campos

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Actualizar días trabajados para solicitudes Canceladas/Entregadas
        for obj in queryset:
            if obj.estado in ["Cancelado", "Entregado"]:
                obj.actualizar_tiempo_proceso()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    


class SolicitudRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Solicitud.objects.all().order_by("id")
    serializer_class = SolicitudSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_status = instance.estado
        new_status = request.data.get("estado", instance.estado)
        
        # Actualizar todos los campos primero
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Si el estado cambia a Cancelado/Entregado, ejecutar lógica adicional
        if new_status in ["Cancelado", "Entregado"] and new_status != old_status:
            instance.refresh_from_db()  # Recargar datos actualizados
            instance.update_status(new_status)
        
        return Response(serializer.data, )