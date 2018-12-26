# Generated by Django 2.1.3 on 2018-11-25 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_auto_20181116_0625'),
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto_Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='productos',
        ),
        migrations.AddField(
            model_name='producto_pedido',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.Pedido'),
        ),
        migrations.AddField(
            model_name='producto_pedido',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.Producto'),
        ),
    ]
