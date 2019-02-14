# Generated by Django 2.1.3 on 2019-02-12 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0009_auto_20190129_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='Secciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tituloqs', models.CharField(default='¿Quiénes Somos?', max_length=200)),
                ('imagenqs', models.ImageField(blank=True, default='coleccion3.jpg', null=True, upload_to='Secciones')),
                ('titulot', models.CharField(default='Tienda', max_length=200)),
                ('imagent', models.ImageField(blank=True, default='coleccion3.jpg', null=True, upload_to='Secciones')),
                ('tituloc', models.CharField(default='Contacto', max_length=200)),
                ('imagenc', models.ImageField(blank=True, default='coleccion3.jpg', null=True, upload_to='Secciones')),
                ('titulodp', models.CharField(default='Datos para el pago', max_length=200)),
                ('imagendp', models.ImageField(blank=True, default='coleccion3.jpg', null=True, upload_to='Secciones')),
                ('titulop', models.CharField(default='Datos de perfil', max_length=200)),
                ('imagenp', models.ImageField(blank=True, default='coleccion3.jpg', null=True, upload_to='Secciones')),
                ('titulopedidos', models.CharField(default='Mis Pedidos', max_length=200)),
                ('imagenpedidos', models.ImageField(blank=True, default='coleccion3.jpg', null=True, upload_to='Secciones')),
                ('titulopreguntas', models.CharField(default='Preguntas Frecuentes', max_length=200)),
                ('imagenpreguntas', models.ImageField(blank=True, default='coleccion3.jpg', null=True, upload_to='Secciones')),
            ],
        ),
    ]