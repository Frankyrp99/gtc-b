from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers


# clase que se encarga de transformar de json a User y de User a json



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = get_user_model()
        fields = ["id", "email","password",'role']
        extra_kwargs = {'email': {'required': False}}
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.get("password")
        email = validated_data.get("email")
        
        if email is not None and email != instance.email:
            if (
                self.Meta.model.objects.filter(email=email)
                .exclude(id=instance.id)
                .exists()
            ):
                raise serializers.ValidationError(
                    {"email": "Ya existe un usuario con este email."}
                )
            else:
                validated_data["email"] = email
       
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()
        print(validated_data)
        return instance


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
