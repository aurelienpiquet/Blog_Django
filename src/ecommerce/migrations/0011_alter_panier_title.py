# Generated by Django 3.2.6 on 2021-08-19 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_alter_panier_nb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panier',
            name='title',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='Numéro de panier'),
        ),
    ]
