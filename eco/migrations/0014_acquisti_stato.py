# Generated by Django 5.0.2 on 2024-08-27 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0013_oggetti_stato'),
    ]

    operations = [
        migrations.AddField(
            model_name='acquisti',
            name='stato',
            field=models.CharField(default=2, max_length=255),
            preserve_default=False,
        ),
    ]
