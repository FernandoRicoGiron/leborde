# Generated by Django 2.1.3 on 2019-01-07 21:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administracion', '0017_pedido_comprobante'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='usuario',
        ),
        migrations.AddField(
            model_name='pedido',
            name='producto',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]