# Generated by Django 2.1.3 on 2018-12-28 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0002_empresa_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='direccion',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empresa',
            name='telefono',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
