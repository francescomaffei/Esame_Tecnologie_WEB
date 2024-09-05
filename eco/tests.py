from django.test import TestCase,Client
from .models import Oggetti
from django.urls import reverse

class OggettiSearchTestCase(TestCase):

    def setUp(self):
        # Creazione di alcuni oggetti di test
        self.client = Client()

        #Immagini placeholder
        Oggetti.objects.create(
            nome='Cuffie Wireless',
            categoria='Tech',
            dettagli='Cuffie senza fili con noise cancelling',
            prezzo=29.99,
            data='2024-12-31',
            stato='Vendita',
            image='images/bestseller.jpg'
        )
        Oggetti.objects.create(
            nome='Mouse Wireless',
            categoria='Tech',
            dettagli='Mouse ergonomico senza fili',
            prezzo=15.99,
            data='2024-12-30',
            stato='In Attesa',
            image='images/bestbuyer.jpg'
        )
        Oggetti.objects.create(
            nome='Cuffie Gaming',
            categoria='Tech',
            dettagli='Cuffie con microfono per gaming',
            prezzo=35.00,
            data='2024-12-31',
            stato='Vendita',
            image='images/bestseller.jpg'
        )

    def test_search_by_name(self):
        # Ricerca per nome parziale
        results = Oggetti.objects.filter(nome__icontains='Cuffie')
        self.assertEqual(results.count(), 2)
        self.assertTrue(results.filter(nome='Cuffie Wireless').exists())
        self.assertTrue(results.filter(nome='Cuffie Gaming').exists())

    def test_search_by_category_and_price(self):
        # Ricerca per categoria e prezzo
        results = Oggetti.objects.filter(categoria='Tech', prezzo__lte=30.00)
        self.assertEqual(results.count(), 2)
        self.assertTrue(results.filter(nome='Cuffie Wireless').exists())
        self.assertTrue(results.filter(nome='Mouse Wireless').exists())

    def test_search_by_date_and_status(self):
        # Ricerca per data massima e stato
        results = Oggetti.objects.filter(data='2024-12-31', stato='Vendita')
        self.assertEqual(results.count(), 2)
        self.assertTrue(results.filter(nome='Cuffie Wireless').exists())
        self.assertTrue(results.filter(nome='Cuffie Gaming').exists())

    def test_search_no_results(self):
        # Ricerca che non dovrebbe restituire risultati
        results = Oggetti.objects.filter(nome__icontains='Tastiera')
        self.assertEqual(results.count(), 0)

    def test_oggetti_vendita_view(self):
        url = reverse('tutti')  
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        
        self.assertTemplateUsed(response, 'oggetti_vendita.html')  

        #Verifica che solo gli oggetti con stato "Vendita" siano inclusi nel contesto
        self.assertContains(response, 'Cuffie Wireless')
        self.assertNotContains(response, 'Mouse Wireless')

    def test_oggetti_vendita_empty(self):
        # Cancella tutti gli oggetti con stato "Vendita" e controlla la pagina vuota
        Oggetti.objects.filter(stato='Vendita').delete()

        url = reverse('tutti')
        response = self.client.get(url)

        # Verifica che la pagina mostri un messaggio quando non ci sono oggetti in vendita
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nessun oggetto in vendita trovato.')


