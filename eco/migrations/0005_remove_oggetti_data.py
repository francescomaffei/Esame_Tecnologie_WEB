# Generated by Django 5.0.2 on 2024-08-17 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0004_oggetti_data_alter_oggetti_categoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oggetti',
            name='data',
        ),
    ]
