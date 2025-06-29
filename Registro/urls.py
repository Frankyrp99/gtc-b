from django.urls import path
from Registro.views import SolicitudListCreateView, SolicitudRetrieveUpdateDestroyView, OpcionesEntidadView, OpcionDetailView

urlpatterns = [
    path("Solicitudes/", SolicitudListCreateView.as_view(), name="solicitud-list"),
    path(
        "Solicitudes/<int:pk>/",
        SolicitudRetrieveUpdateDestroyView.as_view(),
        name="solicitud-detail",
    ),
    path(
        "Entidades/",
        OpcionesEntidadView.as_view(),
        name="entidades-list",
    ),
    path(
        "Entidades/<int:pk>/",
        OpcionDetailView.as_view(),
        name="entidades-detail",
    ),
 
]
