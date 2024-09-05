from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q,Count
from django.urls import reverse
from .forms import SignupForm,SignupExtraForm,LoginForm,ObjForm,FindForm,OffertaForm,ModificaProfiloForm,MessaggioForm
from django.views.generic import ListView
from .models import Utenti,Oggetti,Acquisti,Notifiche,Offerta,Messaggio
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime
from django.contrib.auth.models import User
import matplotlib.pyplot as plt
import io
import base64

class HomeUser(ListView):
    model=Utenti
    template_name='homeuser.html'

class HomeAdmin(ListView):
    model=Utenti
    template_name='homeadmin.html'

def index(request):
    user_logout(request)
    return render(request,'index.html')

def user_signup(request):
    form = SignupForm(request.POST)
    form2 = SignupExtraForm(request.POST)
    mydict={'form':form,'form2':form2}
    if request.method == 'POST':
        form = SignupForm(request.POST)
        form2 = SignupExtraForm(request.POST)
        if form.is_valid() and form2.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()
            user_group = Group.objects.get_or_create(name='USER')
            user_group[0].user_set.add(user)
            return render(request,'index.html')
    return render(request, 'signup.html', context=mydict)


def user_login(request):
    form = LoginForm(request.POST)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.groups.filter(name='USER').exists():
                    return render(request,'homeuser.html')
                else:
                    return render(request,'homeadmin.html')
            else:
                return render(request,'nologin.html')
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def find(request):
    if request.method == 'POST':
        form = FindForm(request.POST)
        if form.is_valid():
            obj=Oggetti.objects.all()
            nome_o_descrizione = form.cleaned_data.get('nome')
            prezzo_massimo = form.cleaned_data.get('prezzomax')
            categoria = form.cleaned_data.get('categoria')
            data = form.cleaned_data.get('data')
            stato = "Vendita"
            obj=obj.filter(Q(nome__icontains=nome_o_descrizione) | Q(dettagli__icontains=nome_o_descrizione))
            if categoria != '---':
                obj=obj.filter(categoria=categoria)
            if prezzo_massimo:
                obj=obj.filter(prezzo__lte=prezzo_massimo)
            if data:
                obj=obj.filter(data__lte=data)
            obj=obj.filter(stato=stato)
            return render(request,'oggetti.html',{'obj':obj})
            
    else:
        form = FindForm()
    
    return render(request,'findobj.html',{'form': form})


@login_required(login_url='/errore/')
def sell(request):
    if request.method == 'POST':
        form = ObjForm(request.POST,request.FILES)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.stato="In Attesa"
            model_instance.save()
            model=get_object_or_404(Oggetti,id=model_instance.id)
            acq=Acquisti.objects.create(
                compratore='0',
                venditore=request.user.username,
                ogg=model,
                stato="In Attesa"
            )
            return render(request,'objaccept.html')
        else:
            return render(request,'objdeny.html')
    else:
        form = ObjForm()
        return render(request, "nuovo_oggetto.html", {'form': form})

@login_required(login_url='/errore/')
def visualizza_obj(request):
    return render(request,'visualizza.html')

@login_required(login_url='/errore/')
def oggetticomprati(request):
    acq=Acquisti.objects.filter(compratore=request.user.username,stato="Venduto")
    oggetti=[]
    for a in acq:
        pz=Offerta.objects.filter(oggetto=a.ogg).last()
        oggetti.append({
            'a':a,
            'pz':pz
        })
    return render(request,'oggetticomprati.html',{'oggetti':oggetti})

@login_required(login_url='/errore/')
def oggettivenduti(request):
    acq=Acquisti.objects.filter(venditore=request.user.username,stato="Venduto")
    oggetti=[]
    for a in acq:
        pz=Offerta.objects.filter(oggetto=a.ogg).last()
        oggetti.append({
            'a':a,
            'pz':pz
        })
    return render(request,'oggettivenduti.html',{'oggetti':oggetti})

@login_required(login_url='/errore/')
def oggettiattesa(request):
    acq=Acquisti.objects.filter(venditore=request.user.username,stato="In Attesa")
    return render(request,'oggettiattesa.html',{'acq':acq})

@login_required(login_url='/errore/')
def oggettiscaduti(request):
    acq=Acquisti.objects.filter(venditore=request.user.username)
    acq2=acq.filter(Q(stato='Negato') | Q(stato='Scaduto'))
    return render(request,'oggettino.html',{'acq2':acq2})

@login_required(login_url='/errore/')
def oggettivendita(request):
    acq=Acquisti.objects.filter(venditore=request.user.username,stato="Vendita")
    return render(request,'oggettivendita.html',{'acq':acq})

@user_passes_test(is_admin,login_url='/error/')
@login_required(login_url='/errore/')
def approva(request):
    oggetti_attesa=Oggetti.objects.filter(stato='In Attesa')

    if not oggetti_attesa.exists():
        return render(request,'fine_revisione.html')

    oggetto=oggetti_attesa.first()
    if request.method=='POST':
        a=Acquisti.objects.filter(ogg_id=oggetto).first()
        if 'approva' in request.POST:
            oggetto.stato = 'Vendita'
            noti=Notifiche.objects.create(
                utente=a.venditore,
                oggetto=oggetto,
                messaggio="Il tuo oggetto è stato approvato!",
                time=datetime.now()
            )
            a.stato='Vendita'
        elif 'nega' in request.POST:
            oggetto.stato = 'Negato'
            noti=Notifiche.objects.create(
                utente=a.venditore,
                oggetto=oggetto,
                messaggio="Il tuo oggetto è stato negato!",
                time=datetime.now()
            )
            a.stato='Negato'
        oggetto.save()
        a.save()
        return render(request,'scelta.html')

    return render(request, 'revisione_oggetti.html', {'oggetto': oggetto})

@user_passes_test(is_admin,login_url='/error/')
@login_required(login_url='/errore/')
def viewall(request):
    acq=Acquisti.objects.filter(stato='Venduto')
    return render(request,'visualizza_acquisti.html',{'acq':acq})

def tuttiacquisti(request):
    oggetti_vendita=Oggetti.objects.filter(stato='Vendita')
    is_admin = request.user.groups.filter(name='ADMIN').exists()
    is_user = request.user.groups.filter(name='USER').exists()
    context = {
        'is_admin': is_admin,
        'is_user': is_user,
    }
    return render(request,'oggetti_vendita.html',{'oggetti':oggetti_vendita,'context':context})

@login_required(login_url='/errore/')
def dettaglio_oggetto(request, pk):
    oggetto = get_object_or_404(Oggetti, pk=pk) 
    is_admin = request.user.groups.filter(name='ADMIN').exists()
    is_user = request.user.groups.filter(name='USER').exists()
    context = {
        'is_admin': is_admin,
        'is_user': is_user,
    }
    if request.method == 'POST':
        form = OffertaForm(request.POST, oggetto=oggetto,utente=request.user)
        if form.is_valid():
            acq=Acquisti.objects.filter(ogg_id=oggetto)
            for a in acq:
                if request.user.username==a.venditore:
                    return render(request,'same.html')
                else:
                    noti=Notifiche.objects.create(
                        utente=a.compratore,
                        oggetto=oggetto,
                        messaggio="La tua offerta è stata superata",
                        time=datetime.now()
                    )
                    a.compratore=request.user.username
            a.save()
            offerta = form.save(commit=False)
            offerta.oggetto = oggetto
            offerta.utente = request.user
            offerta.data=datetime.now()  
            offerta.save()             
            return redirect('dettaglio_oggetto', pk=oggetto.pk)
    else:
        form = OffertaForm(oggetto=oggetto,utente=request.user)

    ultime_offerte = oggetto.offerte.order_by('-importo')[:5]  #Visualizza le ultime 5 offerte

    return render(request, 'dettaglio_oggetto.html', {
        'oggetto': oggetto,
        'form': form,
        'ultime_offerte': ultime_offerte,
        'context':context
    })

@login_required(login_url='/errore/')
def view_notifiche(request):
    ora=datetime.now()
    noti=Notifiche.objects.filter(utente=request.user.username,time__lt=ora).order_by('-time')
    return render(request,'notifiche.html',{'noti':noti})

@user_passes_test(is_admin,login_url='/error/')
@login_required(login_url='/errore/')
def termina(request):
    obj=Oggetti.objects.filter(data=datetime.now(),stato='Vendita')
    acquisti_oggi=[]
    for o in obj:
        off=Offerta.objects.filter(oggetto=o).last()
        if off is not None:
            o.stato='Venduto'
            a=Acquisti.objects.get(ogg=o)
            a.stato='Venduto'
            noti=Notifiche.objects.create(
                    utente=a.compratore,
                    oggetto=o,
                    messaggio="Hai vinto l'asta. Complimenti!",
                    time=datetime.now()
                )
            noti2=Notifiche.objects.create(
                    utente=a.venditore,
                    oggetto=o,
                    messaggio="Hai venduto l'oggetto. Complimenti!",
                    time=datetime.now()
                )
            o.save()
            a.save()
            acquisti_oggi.append({
                    'a':a,
                    'off':off
            })
        else:
            o.stato='Scaduto'
            a=Acquisti.objects.get(ogg=o)
            a.stato='Scaduto'
            noti2=Notifiche.objects.create(
                    utente=a.venditore,
                    oggetto=o,
                    messaggio="Asta conclusa senza offerte",
                    time=datetime.now()
                )
            o.save()
            a.save()
            acquisti_oggi.append({
                    'a':a,
                    'off':off
            })

    oggetti_venduti = Oggetti.objects.filter(stato='Venduto')
    acquisti_venduti = Acquisti.objects.filter(ogg__in=oggetti_venduti)

    venditori = acquisti_venduti.values('venditore').annotate(total_vendite=Count('id')).order_by('-total_vendite')
    compratori =  acquisti_venduti.values('compratore').annotate(total_comprate=Count('id')).order_by('-total_comprate')

    #Risoluzione casi di parimerito in cui più utenti hanno lo stesso numero di oggetti venduti o comprati
    #A tutti quelli in parimerito è assegnato il basge
    max_ven=venditori[0]['total_vendite'] 
    top_ven=[vendita['venditore'] for vendita in venditori if vendita['total_vendite']==max_ven]

    max_com=compratori[0]['total_comprate']
    top_com=[compra['compratore'] for compra in compratori if compra['total_comprate']==max_com] 
    
    if top_ven:
        ux=Utenti.objects.all()
        for u in ux:
            if u.best_seller is not None:
                u.best_seller=None
                u.save()
        for ven in top_ven:
            user=Utenti.objects.get(user__username=ven)
            user.best_seller='images/bestseller.jpg'
            user.save()
    if top_com:
        ux=Utenti.objects.all()
        for u in ux:
            if u.best_buyer is not None:
                u.best_buyer=None
                u.save()
        for com in top_com:
            user=Utenti.objects.get(user__username=com)
            user.best_buyer='images/bestbuyer.jpg'
            user.save()
    return render(request,'termina.html',{'acquisti_oggi':acquisti_oggi})

@login_required(login_url='/errore/')
def profilo(request):
    user=Utenti.objects.get(user=request.user)
    return render(request,'profilo.html',{'user':user})

@login_required(login_url='/errore/')
def modifica_profilo(request):
    utente=get_object_or_404(Utenti,user=request.user)
    user=request.user
    if request.method == 'POST':
        form = ModificaProfiloForm(request.POST, request.FILES, instance=utente, user=user)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            form.save()
            return render(request,'profilo_salvato.html') 
    else:
        form = ModificaProfiloForm(instance=utente, user=user)

    return render(request, 'modifica_profilo.html', {'form': form})

@login_required
def dettaglio_asta(request,pk):
    obj=Oggetti.objects.get(pk=pk)
    offerte=Offerta.objects.filter(oggetto=obj).order_by('-data_offerta')

    importi=[offerta.importo for offerta in offerte]
    date_offerte=[offerta.data_offerta for offerta in offerte]

    plt.figure(figsize=(10, 8))
    plt.plot(importi, date_offerte, marker='o')
    plt.title(f"Tutte le offerte per {obj.nome}")
    plt.xlabel('Importo (€)')
    plt.ylabel('Data offerta')
    plt.xticks(rotation=45)
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()

    grafico_base64 = base64.b64encode(image_png).decode('utf-8')

    context = {
        'obj': obj,
        'grafico': grafico_base64,
        'offerte': offerte
    }

    return render(request, 'dettaglio_asta.html', context)

@login_required
def messaggi(request):
    return render(request,'messaggi.html')

@login_required
def invia_messaggio(request):
    if request.method == 'POST':
        form = MessaggioForm(request.POST)
        if form.is_valid():
            messaggio = form.save(commit=False)
            messaggio.mittente = request.user
            if messaggio.mittente==messaggio.destinatario:
                return render(request,'same_message.html')
            messaggio.save()
            return redirect('messaggi_inviati') 
    else:
        form = MessaggioForm()
    return render(request, 'invia_messaggio.html', {'form': form})

@login_required
def messaggi_inviati(request):
    messaggi = Messaggio.objects.filter(mittente=request.user)
    return render(request, 'messaggi_inviati.html', {'messaggi': messaggi})

@login_required
def messaggi_ricevuti(request):
    messaggi = Messaggio.objects.filter(destinatario=request.user)
    return render(request, 'messaggi_ricevuti.html', {'messaggi': messaggi})

def errore(request):
    return render(request,'error.html')

def error(request):
    return render(request,'error2.html')