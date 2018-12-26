# Generated by Django 2.1.3 on 2018-11-29 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0010_venta_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='estado',
        ),
        migrations.AddField(
            model_name='mensaje',
            name='estado',
            field=models.CharField(choices=[('1', 'Sin leer'), ('2', 'Leido')], default='', max_length=50),
            preserve_default=False,
        ),
    ]
