# users/models.py
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

class UserManager(BaseUserManager):
    def create_user(self, email, password, entidad=None, **extra_fields):
        if not email:
            raise ValueError("Falta el Email")
        user = self.model(email=email, entidad=entidad, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    USER_ROLES = (
        ("admin", "Administrador"),
        ("director", "Director General"),
        ("especialista", "Especialista"),
        
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, default="especialista")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    entidad = models.ForeignKey(  # Nueva relación
        'Registro.Entidad', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='usuarios'
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"