# -*- coding: utf-8 -*-
from django.shortcuts import render
from novo_eventos.eventos.models import Evento

# Create your views here.
def home(request):
    eventos = Evento.objects.all()[0:4]
    template_name = 'home.html'
    context = {
        'eventos': eventos,      
        }
    return render(request, template_name, context)

def contact (request):
    return render(request, 'contato.html')