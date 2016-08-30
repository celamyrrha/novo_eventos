# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from .models import Evento, Inscricao
from time import timezone
from datetime import datetime
from bootstrap3_datetime.widgets import DateTimePicker
from localflavor.br.forms import BRStateSelect, BRStateChoiceField

from novo_eventos.core.mail import send_mail_template

class ContatoParticipantes(forms.Form):
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea)
    
    def send_mail(self, evento):
        subject = '[%s] Contato' % evento
        context =  {
            'mensagem': self.cleaned_data['mensagem'],
        }
        template_name = 'email_participantes.html'
        inscricoes = Inscricao.objects.filter(evento=evento)
        for inscricao in inscricoes:
            recipient_list = [inscricao.user.email]
            send_mail_template(subject, template_name, context, recipient_list)
        


class ContatoEvento(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='Email')
    mensagem = forms.CharField(label='Mensagem/Dúvida', widget=forms.Textarea)
    
    def send_mail(self, evento):
        subject = '[%s] Contato' % evento
        context =  {
            'nome': self.cleaned_data['nome'],
            'email': self.cleaned_data['email'],
            'mensagem': self.cleaned_data['mensagem'],
        }
        template_name = 'email_contato.html'
        send_mail_template(subject, template_name, context, [settings.CONTACT_EMAIL])
        
class EventoForm(forms.ModelForm):
    
    class Meta:
        model = Evento
        
        estado = BRStateChoiceField()
        now = datetime.date(datetime.now())
        now = now.strftime('%m/%d/%y') 
        fields = ['nome_evento','data_inicio', 'data_fim', 'vagas_evento', 'descricao','nome_palestrante', 'tipo_evento', 'imagem_evento', 'local', 'cidade', 'estado']   
        widgets = {'data_inicio': DateTimePicker(options={
                        "format": "YYYY-MM-DD","pickTime": False, 'startDate': now,}),
                   'data_fim': DateTimePicker(options={
                        "format": "YYYY-MM-DD","pickTime": False, 'startDate': now}) }