# Generated by Django 5.0.2 on 2024-09-03 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0022_utenti_best_buyer_utenti_best_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oggetti',
            name='categoria',
            field=models.CharField(choices=[('Tech', 'tech'), ('Abbigliamento', 'abbigliamento'), ('Casa e Giardino', 'casa e giardino'), ('Libri', 'Libri'), ('Sport e Tempo Libero', 'sport e tempo libero'), ('Salute e Bellezza', 'salute e bellezza'), ('Gioielli e Accessori', 'gioielli e accessori'), ('Auto e Motori', 'auto e motori'), ('Giocattoli e Infanzia', 'giocattoli e infanzia'), ('Arte e Collezionismo', 'arte e collezionismo'), ('Strumenti musicali e DJ', 'strumenti musicali e dj'), ('Fai da te', 'fai da te')], default='Tech', max_length=30),
        ),
    ]
