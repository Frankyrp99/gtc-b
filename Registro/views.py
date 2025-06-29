from rest_framework import generics
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from django.db.models import Prefetch
from .models import Solicitud, OpcionPersonalizada
from .serializers import SolicitudSerializer
from users.serializers import OpcionPersonalizadaSerializer
from users.permissions import HasEntidad
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.authentication import TokenAuthentication

class SolicitudListCreateView(ListCreateAPIView):
   
    serializer_class = SolicitudSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        # Filtrar por entidad del usuario
        if not hasattr(self.request.user, 'entidad') or not self.request.user.entidad:
            raise PermissionDenied("Su usuario no tiene una entidad asignada")
            
        return Solicitud.objects.filter(
            entidad=self.request.user.entidad
        ).order_by("id")

    
    
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
    
class OpcionesEntidadView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = OpcionPersonalizadaSerializer
    
    
    def get_queryset(self):
        # Verificar si el usuario tiene entidad
        if not hasattr(self.request.user, 'entidad') or not self.request.user.entidad:
            
            raise PermissionDenied("Su usuario no tiene una entidad asignada")
        return OpcionPersonalizada.objects.filter(entidad=self.request.user.entidad)
    
    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'entidad') or not self.request.user.entidad:
            raise PermissionDenied("Su usuario no tiene una entidad asignada")
        serializer.save(entidad=self.request.user.entidad)
        
    def get_queryset(self):
        user = self.request.user
        
        if not user.is_authenticated:
            raise NotAuthenticated("Usuario no autenticado")
            
        print(f"Usuario autenticado: {user.email}")  # Para diagnóstico
        
        if not hasattr(user, 'entidad'):
            raise PermissionDenied("El modelo de usuario no tiene atributo 'entidad'")
            
        if user.entidad is None:
            raise PermissionDenied("Usuario no tiene entidad asignada")
            
        return OpcionPersonalizada.objects.filter(entidad=user.entidad)

class OpcionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OpcionPersonalizadaSerializer
    authentication_classes = [TokenAuthentication]
    
    
    def get_queryset(self):
        # Verificar si el usuario tiene entidad
        if not hasattr(self.request.user, 'entidad') or not self.request.user.entidad:
            raise PermissionDenied("Su usuario no tiene una entidad asignada")
        return OpcionPersonalizada.objects.filter(entidad=self.request.user.entidad)