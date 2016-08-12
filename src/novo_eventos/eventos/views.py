# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ContatoEvento
from .models import Evento, Inscricao

# Create your views here.
def lista_eventos(request):
    eventos = Evento.objects.all()
    template_name = 'lista_eventos.html'
    context = {
        'eventos': eventos       
        }
    return render(request, template_name, context)

# def detalhes(request, pk):
#    evento = get_object_or_404(Evento, pk=pk)
#    context = { 'evento':evento}
#    template_name = 'detalhes.html'
#    return render(request, template_name, context)

def detalhes(request, slug):
    evento = get_object_or_404(Evento, slug=slug)
    #vagas = Evento.objects.all().extra()
    context = { }
    if request.method == 'POST':
        form = ContatoEvento(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(evento)
            form = ContatoEvento()  
    else:
        form = ContatoEvento()    
    context['form'] = form
    context['evento'] = evento
    template_name = 'detalhes.html'
    return render(request, template_name, context)

@login_required
def inscricoes(request, slug):
    evento = get_object_or_404(Evento, slug=slug)
    inscricao, created =  Inscricao.objects.get_or_create(
        user=request.user, evento=evento
    )
    if created:
        inscricao.active()
        messages.success(request, 'Você foi inscrito no curso com sucesso!')
    else:
        messages.info(request, 'Você já está inscrito no curso.')
    return redirect('accounts:painel_usuario')

@login_required
def cancelar_inscricao(request,slug):
    evento = get_object_or_404(Evento, slug=slug)
    inscricao = get_object_or_404(Inscricao, user=request.user, evento=evento)
    if request.method == 'POST':
        inscricao.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso!')
        return redirect('accounts:painel_usuario')
    template = 'cancelar_inscricao.html'
    context = {'inscricao':inscricao,
               'evento':evento,
    }
    return render(request, template, context)

@login_required
def avisos(request, slug):
    evento = get_object_or_404(Evento, slug=slug)
    if not request.user.is_staff:
        inscricao = get_object_or_404(Inscricao, user=request.user, evento=evento)
        if not inscricao.is_approved():
            messages.error(request, 'Sua inscrição está pendente.')
            return redirect('accounts : painel_usuario')
    template = 'avisos.html'
    context = {'evento': evento, 'avisos':evento.avisos.all()}    
    return render(request, template, context)    