# Generated by Django 2.1.3 on 2019-01-12 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0011_num_pedido'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario_Talla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='producto',
            name='inventario',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inventario_talla',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.Producto'),
        ),
        migrations.AddField(
            model_name='inventario_talla',
            name='talla',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.Talla'),
        ),
    ]
