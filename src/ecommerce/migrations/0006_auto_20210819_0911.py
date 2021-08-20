# Generated by Django 3.2.6 on 2021-08-19 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0005_auto_20210819_0128'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='price',
            field=models.FloatField(blank=True, default=0, verbose_name='Prix'),
        ),
        migrations.AddField(
            model_name='command',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecommerce.status'),
        ),
    ]
