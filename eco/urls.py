from django.urls import path
from django.conf.urls import include
from django.contrib import admin
from . import views
from .views  import HomeUser,HomeAdmin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('findobj/', views.find, name='findobj'),
    path('sell/', views.sell, name='sell'),
    path('userhome/', HomeUser.as_view(), name='homeuser'),
    path('adminhome/', HomeAdmin.as_view(), name='homeadmin'),
    path('visualizza/',views.visualizza_obj,name='visualizza'), 
    path('oggetticomprati/', views.oggetticomprati ,name='oggetticomprati'),
    path('oggettivenduti/', views.oggettivenduti,name='oggettivenduti'),  
    path('oggettiattesa/', views.oggettiattesa,name='oggettiattesa'),
    path('oggettiscaduti/', views.oggettiscaduti,name='oggettiscaduti'),
    path('oggettivendita/', views.oggettivendita,name='oggettivendita'),
    path('revisione/', views.approva, name='approva'),
    path('acquisti/', views.viewall, name='viewall'),
    path('tutti/', views.tuttiacquisti, name='tutti'),
    path('oggetti/<int:pk>/', views.dettaglio_oggetto, name='dettaglio_oggetto') ,
    path('notifiche/',views.view_notifiche,name='notifiche'),
    path('termina/',views.termina,name='termina'),
    path('profilo/',views.profilo,name='profilo'),   
    path('modifica_profilo/',views.modifica_profilo,name='modifica'),
    path('asta/<int:pk>/', views.dettaglio_asta, name='dettaglio_asta'),
    path('messaggi/', views.messaggi, name='messaggi'),
    path('invia_messaggio/', views.invia_messaggio, name='invia_messaggio'),
    path('messaggi_inviati/', views.messaggi_inviati, name='messaggi_inviati'),
    path('messaggi_ricevuti/', views.messaggi_ricevuti, name='messaggi_ricevuti'),
    path('errore/', views.errore, name='errore'),
    path('error/',views.error,name='error')   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)