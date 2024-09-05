from django import forms 
from django.forms import ModelForm 
from django.contrib.auth.models import User
from .models import Utenti,Oggetti,Acquisti,Offerta,Messaggio
from django.core.exceptions import ValidationError
from datetime import date

class SignupForm(ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class SignupExtraForm(ModelForm):
    class Meta:
        model=Utenti
        fields=['mail','immagine_profilo']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ObjForm(ModelForm):
    class Meta:
        model=Oggetti
        fields=['nome','categoria','dettagli','prezzo','data','image']

    def clean_data(self):
        data_insert=self.cleaned_data.get('data')
        if data_insert<date.today():
            raise ValidationError("La data non può essere nel passato")
        return data_insert

categories=(
  ('---','---'),
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
class FindForm(forms.Form):
    nome=forms.CharField(label='Nome o Descrizione',required=False)
    categoria=forms.ChoiceField(choices=categories,required=False)
    prezzomax=forms.DecimalField(max_digits=6,decimal_places=2,label='Prezzo Massimo',required=False)
    data = forms.DateField(widget=forms.SelectDateWidget,label='Data',required=False)

class OffertaForm(forms.ModelForm):
    class Meta:
        model=Offerta
        fields=['importo']

    def __init__(self, *args, **kwargs):
        self.oggetto = kwargs.pop('oggetto', None)
        self.utente = kwargs.pop('utente', None)
        super().__init__(*args, **kwargs)

    def clean_importo(self):
        importo = self.cleaned_data.get('importo')
        ultima_offerta = self.oggetto.offerte.order_by('-importo').first()

        if ultima_offerta and importo <= ultima_offerta.importo:
            raise forms.ValidationError("L'importo dell'offerta deve essere maggiore dell'ultima offerta.")
        elif importo <= self.oggetto.prezzo:
            raise forms.ValidationError("L'importo dell'offerta deve essere maggiore del prezzo di partenza.")
        
        return importo

class ModificaProfiloForm(forms.ModelForm):
    first_name=forms.CharField(max_length=30,label='Nome')
    last_name=forms.CharField(max_length=30,label='Cognome')

    class Meta:
        model=Utenti
        fields=['first_name','last_name','mail','immagine_profilo']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ModificaProfiloForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

class MessaggioForm(forms.ModelForm):
    destinatario = forms.ModelChoiceField(queryset=User.objects.exclude(username='admin'), label="Destinatario")
    
    class Meta:
        model = Messaggio
        fields = ['destinatario', 'testo']
        widgets = {
            'testo': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }