# Generated by Django 5.2.2 on 2025-06-26 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_entidad_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Administrador'), ('director', 'Director General'), ('especialista', 'Especialista')], default='especialista', max_length=20),
        ),
    ]
