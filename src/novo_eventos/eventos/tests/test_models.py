# -*- coding: utf-8 -*-
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from model_mommy import mommy

from novo_eventos.accounts.models import User

from novo_eventos.eventos.models import Evento, Inscricao, Palestra, Material

class EventoManagerTestCase(TestCase):
    def setUp(self):
        self.eventos_django = mommy.make('eventos.Evento', nome_evento='Python com Django 2', imagem_evento='test.jpg', _quantity=10)
        self.eventos_dev = mommy.make('eventos.Evento', nome_evento='Python para Devs', imagem_evento='test.jpg', _quantity=10)
        self.client = Client()
        
    def tearDown(self):
        Evento.objects.all().delete()  
        
    def test_evento_search(self):    
        search = Evento.objects.search('django')
        self.assertEqual(len(search), 10)
        search = Evento.objects.search('devs')
        self.assertEqual(len(search), 10)
        
class InscricaoTesteCase(TestCase):
    def setUp(self): 
        self.evento = mommy.make('Evento', imagem_evento = 'teste.jpg')
        self.user = mommy.make('accounts.User')
        
        self.inscricao = mommy.make('Inscricao', user=self.user, evento = self.evento)
        
    def test_inscricao(self):
        self.inscricao.save()
        inscricao = Inscricao.objects.all()
        self.assertEqual(len(inscricao), 1)
        
    def tearDown(self):
        Inscricao.objects.all().delete()
        Evento.objects.all().delete()
        User.objects.all().delete()

class PalestraTesteCase(TestCase):
    def setUp(self):
        self.evento = mommy.make('eventos.Evento', imagem_evento = 'teste.jpg')
        self.palestra = mommy.make('palestra.Palestra', evento = self.evento)
        self.material = mommy.make('material.Material', palestra = self.palestra)
        
    def tearDown(self):
        Evento.objects.all().delete()
        Palestra.objects.all().delete()
        Material.objects.all().delete()