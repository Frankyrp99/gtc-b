from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import User
from Registro.models import Entidad
from .serializers import UserSerializer, AuthTokenSerializer, EntidadSerializer


class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        # Solo usuarios de la misma entidad
        if self.request.user.role == "director":
            return User.objects.filter(entidad=self.request.user.entidad)
        # Superusuarios ven todos
        if self.request.user.is_superuser:
            return User.objects.all().prefetch_related("entidad")
        # Otros usuarios solo ven su propio perfil
        return User.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        user = self.request.user
        password = self.request.data.get("password")

        # Si es director, asigna su entidad y rol 'especialista'
        if user.role == "director":
            # ... lógica existente ...
            new_user = serializer.save(entidad=user.entidad, role="especialista")
        else:
            new_user = serializer.save()

        # Fuerza el hasheo si es necesario
        if password:
            new_user.set_password(password)
            new_user.save()


class RetriveUpdateUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpdateUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]

    def get_object(self):
        user_id = self.kwargs["pk"]
        return get_object_or_404(User, pk=user_id)

    def update(self, request, *args, **kwargs):
        # Depuración adicional

        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):

        serializer.is_valid(raise_exception=True)

        # Verificar el objeto entidad en el contexto
        if "entidad" in serializer.validated_data:
            entidad = serializer.validated_data["entidad"]

        return super().perform_update(serializer)


class EntidadDirectorView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EntidadSerializer  # Necesitarás crear este serializer
    queryset = Entidad.objects.all()


class EntidadListCreateView(ListCreateAPIView):
    serializer_class = EntidadSerializer

    queryset = Entidad.objects.all()


# token
class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )
