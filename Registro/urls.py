from django.urls import path
from .views import SolicitudListCreateView, SolicitudRetrieveUpdateDestroyView

urlpatterns = [
    path("Solicitudes/", SolicitudListCreateView.as_view(), name="solicitud-list"),
    path(
        "Solicitudes/<int:pk>/",
        SolicitudRetrieveUpdateDestroyView.as_view(),
        name="solicitud-detail",
    ),
]
