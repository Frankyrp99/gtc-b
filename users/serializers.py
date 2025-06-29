from django.contrib.auth import get_user_model, authenticate

from django.contrib.auth import get_user_model
from rest_framework import serializers
from Registro.models import Entidad, OpcionPersonalizada
from .models import User

# clase que se encarga de transformar de json a User y de User a json


class EntidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidad
        fields = ["id", "nombre", "director_general"]
        read_only_fields = ["id"]


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        if not user:
            raise serializers.ValidationError(
                "No se pudo autenticar", code="auhorization"
            )

        data["user"] = user
        return data


class OpcionPersonalizadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionPersonalizada
        fields = ["id", "tipo", "valor"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    entidad = serializers.PrimaryKeyRelatedField(
        queryset=Entidad.objects.all(), required=False, allow_null=True
    )
    opciones_entidad = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "password", "role", "entidad", "opciones_entidad"]
        extra_kwargs = {"email": {"required": True}, "role": {"required": True}}

    def to_internal_value(self, data):
        print("\n=== TO_INTERNAL_VALUE ===")
        print(f"Data recibida: {data}")
        return super().to_internal_value(data)

    def validate(self, attrs):
        print("\n=== VALIDATE ===")
        print(f"Atributos después de validación: {attrs}")
        return super().validate(attrs)

    def update(self, instance, validated_data):
        print("\n=== UPDATE ===")
        print(f"Datos validados: {validated_data}")

        # Manejar contraseña
        password = validated_data.pop("password", None)
        if password and password.strip():
            instance.set_password(password)
            print("Contraseña actualizada")

        # Manejar entidad
        if "entidad" in validated_data:
            instance.entidad = validated_data.pop("entidad")

        # Actualizar otros campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            print(f"Campo actualizado: {attr} -> {value}")

        instance.save()
        return instance

    def get_opciones_entidad(self, obj):
        if obj.entidad:
            opciones = OpcionPersonalizada.objects.filter(entidad=obj.entidad)
            return OpcionPersonalizadaSerializer(opciones, many=True).data
        return []
