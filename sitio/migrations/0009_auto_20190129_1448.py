# Generated by Django 2.1.3 on 2019-01-29 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0008_empresa_que_es'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='facebook',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='instagram',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='twiter',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='youtube',
            field=models.URLField(blank=True, null=True),
        ),
    ]
