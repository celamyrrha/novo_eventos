# -*- coding: utf-8 -*-
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from cgi import escape


from .forms import ContatoEvento, EventoForm, ContatoParticipantes
from .models import Evento, Inscricao, Palestra, Material
from novo_eventos.accounts.models import User
from .decorators import inscricao_required
from django.template.context_processors import request
from django.db.models.aggregates import Count

# Create your views here.

    
def lista_eventos(request):
    eventos = Evento.objects.all()
    template_name = 'lista_eventos.html'
    context = {
        'eventos': eventos       
        }
    return render(request, template_name, context)

@login_required
def lista_presenca(request, slug):
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito aos organizadores')
        return redirect('eventos:index')
    evento = get_object_or_404(Evento, slug=slug)
    inscricoes =  Inscricao.objects.filter(evento=evento)
   # if request.method == 'POST':
    #    Inscricao.vagas_evento = evento.vagas_evento + 1
     #   Inscricao.save()
      #  messages.success(request, 'Sua inscrição foi cancelada com sucesso!')
       # return redirect('accounts:painel_usuario')
    template_name = 'lista_presenca.html'
    context = {
        'evento': evento,
        'inscricoes': inscricoes       
        }
    return render(request, template_name, context)

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

@login_required
def relatorio_inscritos(request, slug):
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito aos organizadores')
        return redirect('eventos:index')
    evento = get_object_or_404(Evento, slug=slug)
    inscricoes =  Inscricao.objects.filter(evento=evento)
    #Retrieve data or whatever you need
    return render_to_pdf(
            'inscritos.html',
            {
                'pagesize':'A4',
                'evento': evento,
                'inscricoes': inscricoes 
            }
        )

@login_required
def grafico_sexo(request, slug):
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito aos organizadores')
        return redirect('eventos:index')
    evento = get_object_or_404(Evento, slug=slug)
    inscricoes = Inscricao.objects.filter(evento=evento)
    sexo = User.objects.filter(inscricoes=inscricoes).values('sexo').annotate(count=Count('sexo'))
    template_name = 'grafico_sexo.html'
    context = {
        'evento': evento,
        'inscricoes': inscricoes,
        'sexo': sexo,   
        }
    return render(request, template_name, context)

@login_required
def grafico_cidade(request, slug):
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito aos organizadores')
        return redirect('eventos:index')
    evento = get_object_or_404(Evento, slug=slug)
    inscricoes =  Inscricao.objects.filter(evento=evento)
    cidades = User.objects.filter(inscricoes=inscricoes).values('cidade').annotate(count=Count('cidade'))
    template_name = 'grafico_cidade.html'
    context = {
        'evento': evento,
        'inscricoes': inscricoes,
        'cidades':cidades,
        }
    return render(request, template_name, context)

@login_required
def certificado_palestrante(request, slug):
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito aos organizadores')
        return redirect('eventos:index')
    evento = get_object_or_404(Evento, slug=slug)
    inscricoes =  Inscricao.objects.filter(evento=evento)
    template = 'certificado_palestrante.html'
    context = {'evento':evento,'inscricoes': inscricoes}
    return render(request, template, context)         


@login_required
def add_evento(request):
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito aos organizadores')
        return redirect('eventos:index')
    if request.method == "POST":
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.save()
            return redirect('eventos:index')
    else:
        form = EventoForm()
    template_name = 'edit_evento.html'
    context = {'form': form}
    return render(request, template_name, context)

@login_required
def edita_evento(request, slug):
    evento = get_object_or_404(Evento, slug=slug)
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito aos organizadores')
        return redirect('eventos:index')
    if request.method == "POST":
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.save()
            return redirect('eventos:index')
    else:
        form = EventoForm(instance=evento)
    template_name = 'edit_evento.html'
    context = {'form': form}
    return render(request, template_name, context)

@login_required
def exclui_evento(request, slug):
    evento = get_object_or_404(Evento, slug=slug)
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito aos organizadores')
        return redirect('eventos:index')
    evento.delete()
    messages.success(request, 'Evento excluído com sucesso.')
    return redirect('eventos:index')

@login_required
def email_participantes(request, slug):
    evento = get_object_or_404(Evento, slug=slug)
    context = { }
    if request.method == 'POST':
        form = ContatoParticipantes(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(evento)
            form = ContatoParticipantes()  
    else:
        form = ContatoParticipantes()    
    context['form'] = form
    context['evento'] = evento
    template_name = 'form_email_participantes.html'
    return render(request, template_name, context)


def detalhes(request, slug):
    evento = get_object_or_404(Evento, slug=slug)
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
        evento.vagas_evento = evento.vagas_evento - 1
        evento.save()
    else:
        messages.info(request, 'Você já está inscrito no curso.')
    return redirect('accounts:painel_usuario')

@login_required
def cancelar_inscricao(request,slug):
    evento = get_object_or_404(Evento, slug=slug)
    inscricao = get_object_or_404(Inscricao, user=request.user, evento=evento)
    if request.method == 'POST':
        inscricao.delete()
        evento.vagas_evento = evento.vagas_evento + 1
        evento.save()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso!')
        return redirect('accounts:painel_usuario')
    template = 'cancelar_inscricao.html'
    context = {'inscricao':inscricao,
               'evento':evento,
    }
    return render(request, template, context)

@login_required
@inscricao_required
def avisos(request, slug):
    evento = request.evento
    template = 'avisos.html'
    context = {'evento': evento, 'avisos':evento.avisos.all()}    
    return render(request, template, context)    

@login_required
@inscricao_required
def palestras(request, slug):
    evento = request.evento
    template = 'palestras.html'
    palestras = evento.release_palestra()
    if request.user.is_staff:
        palestras = evento.palestras.all()
    context = {'evento': evento, 'palestras': palestras}
    return render(request, template, context)

@login_required
@inscricao_required
def palestra(request, slug, pk):
    evento = request.evento
    palestra = get_object_or_404(Palestra, pk=pk, evento=evento)
    if not request.user.is_staff and not palestra.is_available():
        messages.error(request, 'Esta palestra não está disponível.')
        return redirect('eventos:palestras', slug=evento.slug)
    template = 'palestra.html'
    context = {'evento':evento, 'palestra':palestra}
    return render(request, template, context)
    
@login_required
@inscricao_required
def material(request, slug, pk):
    evento = request.evento
    material = get_object_or_404(Material, pk=pk, palestra__evento=evento)
    palestra = material.palestra
    if not request.user.is_staff and not palestra.is_available():
        messages.error(request, 'Este material não está disponível.')
        return redirect('eventos:palestra', slug=evento.slug, pk=palestra.pk)
    if not material.is_embedded():
        return redirect(material.arquivo.url)
    template = 'material.html'
    context = {'evento':evento, 'palestra':palestra, 'material':material}
    return render(request, template, context)    
    
@login_required
@inscricao_required
def cracha(request, slug):
    evento = request.evento
    inscricao = get_object_or_404(Inscricao, user=request.user, evento=evento)
    template = 'cracha.html'
    context = {'evento':evento,'inscricao': inscricao}
    return render(request, template, context) 

@login_required
@inscricao_required
def certificado(request, slug):
    evento = request.evento
    inscricao = get_object_or_404(Inscricao, user=request.user, evento=evento)
    template = 'certificado.html'
    context = {'evento':evento,'inscricao': inscricao}
    return render(request, template, context)          