# Generated by Django 5.0.2 on 2024-08-30 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0020_notifiche'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utenti',
            name='type',
        ),
        migrations.AddField(
            model_name='utenti',
            name='immagine_profilo',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
