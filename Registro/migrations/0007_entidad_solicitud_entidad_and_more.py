# Generated by Django 5.2.2 on 2025-06-22 16:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registro', '0006_alter_solicitud_fecha_entrega'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('director_general', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entidad_dirigida', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='solicitud',
            name='entidad',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Registro.entidad'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='solicitud',
            unique_together={('entidad', 'numero_orden')},
        ),
        migrations.CreateModel(
            name='OpcionPersonalizada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('ASENTAMIENTO', 'Asentamiento'), ('PERSONAL', 'Personal de atención')], max_length=20)),
                ('valor', models.CharField(max_length=255)),
                ('entidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.entidad')),
            ],
            options={
                'unique_together': {('entidad', 'tipo', 'valor')},
            },
        ),
    ]
