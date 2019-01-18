# Generated by Django 2.1.3 on 2018-12-28 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0005_auto_20181205_2233'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='sub_categoria',
            name='categoria',
        ),
        migrations.DeleteModel(
            name='Sub_Categoria',
        ),
        migrations.AddField(
            model_name='producto',
            name='tallas',
            field=models.ManyToManyField(blank=True, null=True, to='ecommerce.Talla'),
        ),
    ]