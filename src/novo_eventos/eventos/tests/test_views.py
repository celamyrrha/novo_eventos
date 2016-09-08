# -*- coding: utf-8 -*-
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from novo_eventos.eventos.models import Evento
from novo_eventos.accounts.models import User

# Create your tests here.
class ContatoEventoTestCase(TestCase):
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
        
class ViewTestCase(TestCase):
    def test_home(self):
        response=self.client.get("/")
        self.assertEqual(response.status_code,200)     
        
        
class LoginTestCase(TestCase):
    def test_login(self):
        c = Client()
        c.login(username='fred', password='secret')
        
    def assertLoginRequired(self, url):
        response = self.client.get(url)
        redirect_url = settings.LOGIN_URL + '?next=' + url
        self.assertRedirects(response, redirect_url)

    def assertContextItem(self, response, key, value):
        self.assertIn(
                      key, response.context, msg='Key "%s" not found in context' % key
        )
        context_obj = response.context[key]
        self.assertEqual(value, context_obj)

    def assertFormInContext(self, response, key, form_class):
        self.assertIn(
            key, response.context, msg='Key "%s" not found in context' % key
        )
        form = response.context[key]
        self.assertIsInstance(form, form_class)

    def assertStatusCode(self, status_code, response):
        msg = "Response wasn't %d: %d" % (status_code, response.status_code)
        self.assertEqual(status_code, response.status_code, msg=msg)

    def assert404(self, response):
        self.assertStatusCode(404, response)

    def assert200(self, response):
        self.assertStatusCode(200, response)
