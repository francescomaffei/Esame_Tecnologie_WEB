# Generated by Django 5.0.2 on 2024-08-27 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0012_oggetti_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='oggetti',
            name='stato',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
