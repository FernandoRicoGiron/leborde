# Generated by Django 2.1.3 on 2019-02-14 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0020_auto_20190107_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensaje',
            name='telefono',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
