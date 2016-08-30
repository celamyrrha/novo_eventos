# -*- coding: utf-8 -*-
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from novo_eventos.eventos.models import Evento

class EventoManagerTestCase(TestCase):
    def setUp(self):
        
    