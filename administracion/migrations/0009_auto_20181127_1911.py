# Generated by Django 2.1.3 on 2018-11-27 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0008_auto_20181127_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='fecha',
            field=models.DateTimeField(),
        ),
    ]
