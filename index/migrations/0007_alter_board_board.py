# Generated by Django 3.2.23 on 2024-02-10 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='board',
            field=models.BinaryField(max_length=2000000),
        ),
    ]
