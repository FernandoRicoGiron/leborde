# Generated by Django 2.1.3 on 2019-01-29 20:37

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0007_auto_20190129_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='que_es',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
