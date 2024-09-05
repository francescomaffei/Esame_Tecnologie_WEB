from django.db import models
from django.contrib.auth.models import User

class Utenti(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE)
  mail= models.EmailField()
  immagine_profilo=models.ImageField(upload_to='images/',null=True,blank=True)
  best_buyer=models.ImageField(upload_to='images/',null=True,blank=True)
  best_seller=models.ImageField(upload_to='images/',null=True,blank=True)

cat=(
  ('Tech','tech'),
  ('Abbigliamento','abbigliamento'),
  ('Casa e Giardino','casa e giardino'),
  ('Libri','libri'),
  ('Sport e Tempo Libero','sport e tempo libero'),
  ('Salute e Bellezza','salute e bellezza'),
  ('Gioielli e Accessori','gioielli e accessori'),
  ('Auto e Motori','auto e motori'),
  ('Giocattoli e Infanzia','giocattoli e infanzia'),
  ('Arte e Collezionismo','arte e collezionismo'),
  ('Strumenti musicali e DJ','strumenti musicali e dj'),
  ('Fai da te','fai da te')
)
class Oggetti(models.Model):
  nome=models.CharField(max_length=255)
  categoria=models.CharField(max_length=30,choices=cat,default='Tech')
  dettagli=models.CharField(max_length=255)
  prezzo=models.DecimalField(max_digits=6,decimal_places=2)
  data=models.DateField()
  image=models.ImageField(upload_to='images/')
  stato=models.CharField(max_length=255)  

class Acquisti(models.Model):
    compratore = models.CharField(max_length=255)
    venditore = models.CharField(max_length=255)
    ogg = models.ForeignKey(Oggetti, on_delete=models.CASCADE)
    stato = models.CharField(max_length=255)

class Offerta(models.Model):
  oggetto = models.ForeignKey(Oggetti, related_name='offerte', on_delete=models.CASCADE)
  utente = models.ForeignKey(User,on_delete=models.CASCADE)
  importo = models.DecimalField(max_digits=8, decimal_places=2)
  data_offerta = models.DateTimeField(auto_now_add=True)

class Notifiche(models.Model):
  utente=models.CharField(max_length=255)
  oggetto=models.ForeignKey(Oggetti, related_name='notifica', on_delete=models.CASCADE)
  messaggio=models.CharField(max_length=255)
  time=models.DateTimeField(auto_now_add=True)

class Messaggio(models.Model):
    mittente = models.ForeignKey(User, related_name='messaggi_inviati', on_delete=models.CASCADE)
    destinatario = models.ForeignKey(User, related_name='messaggi_ricevuti', on_delete=models.CASCADE)
    testo = models.TextField()
    data_invio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Da: {self.mittente.username} A: {self.destinatario.username} - {self.data_invio}"