# Generated by Django 2.1.3 on 2019-08-03 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0017_auto_20190802_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='secciones',
            name='imagenpoliticas',
            field=models.ImageField(blank=True, default='coleccion3.jpg', null=True, upload_to='Secciones'),
        ),
        migrations.AddField(
            model_name='secciones',
            name='imagenterminos',
            field=models.ImageField(blank=True, default='coleccion3.jpg', null=True, upload_to='Secciones'),
        ),
        migrations.AddField(
            model_name='secciones',
            name='titulopoliticas',
            field=models.CharField(default='Aviso de Privacidad', max_length=200),
        ),
        migrations.AddField(
            model_name='secciones',
            name='tituloterminos',
            field=models.CharField(default='Terminos y Condiciones', max_length=200),
        ),
    ]
