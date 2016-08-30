# -*- coding: utf-8 -*-
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from novo_eventos.eventos.models import Evento
# Create your tests here.
class ContactEventoTestCase(TestCase):
    def setUp(self):
        self.evento = Evento.objects.create(nome_evento='Django', slug='django')
        
    def tearDown(self):
        self.evento.delete()
            
        
    def test_contact_form_sucess(self):
        data = {'nome':'Fulano', 'email':'fulano@oi.com','mensagem':'Oi'}
        client = Client()
        path = reverse('eventos:detalhes', args=[self.evento.slug])
        response = client.post(path, data)
        self.assertEqual(len(mail.outbox), 1) 
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL]) 