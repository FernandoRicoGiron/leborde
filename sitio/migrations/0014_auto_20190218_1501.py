# Generated by Django 2.1.3 on 2019-02-18 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0013_empresa_correopaypal'),
    ]

    operations = [
        migrations.AddField(
            model_name='secciones',
            name='imagenppaypal',
            field=models.ImageField(blank=True, default='coleccion3.jpg', null=True, upload_to='Secciones'),
        ),
        migrations.AddField(
            model_name='secciones',
            name='tituloppaypal',
            field=models.CharField(default='Proceder al pago con paypal', max_length=200),
        ),
    ]