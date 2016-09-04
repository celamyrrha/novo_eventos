# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from .models import Evento, Inscricao, Aviso, Material, Palestra
from time import timezone
from datetime import datetime
from bootstrap3_datetime.widgets import DateTimePicker
from localflavor.br.forms import BRStateChoiceField
from django.forms.models import inlineformset_factory

from novo_eventos.core.mail import send_mail_template

class ContatoParticipantes(forms.Form):
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea(attrs={'class' : 'form-control', 'rows' :'8'}))
    
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
    nome = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class' : 'form-control'}))
    mensagem = forms.CharField(label='Mensagem/Dúvida', widget=forms.Textarea(attrs={'class' : 'form-control', 'rows' :'7'}))
    
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
        exclude = ['slug']   
        widgets = {'data_inicio': DateTimePicker(options={
                        "format": "YYYY-MM-DD","pickTime": False, 'startDate': now,}),
                   'data_fim': DateTimePicker(options={
                        "format": "YYYY-MM-DD","pickTime": False, 'startDate': now}) }

    def __init__(self, *args, **kwargs):
        super(EventoForm, self).__init__(*args, **kwargs)
        self.fields['nome_evento'].widget.attrs.update({'class' : 'form-control'})
        self.fields['vagas_evento'].widget.attrs.update({'class' : 'form-control'})
        self.fields['descricao'].widget.attrs.update({'class' : 'form-control'})
        self.fields['nome_palestrante'].widget.attrs.update({'class' : 'form-control'})
        self.fields['tipo_evento'].widget.attrs.update({'class' : 'form-control'})
        self.fields['imagem_evento'].widget.attrs.update({'class' : 'form-control'})
        self.fields['local'].widget.attrs.update({'class' : 'form-control'})
        self.fields['cidade'].widget.attrs.update({'class' : 'form-control'})
        self.fields['estado'].widget.attrs.update({'class' : 'form-control'})
        
class AvisoForm(forms.ModelForm):
        
    class Meta:
        model = Aviso
        fields = ['titulo', 'conteudo']
        
    def __init__(self, *args, **kwargs):
        super(AvisoForm, self).__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update({'class' : 'form-control'})
        self.fields['conteudo'].widget.attrs.update({'class' : 'form-control'})
            
MaterialFormSet = inlineformset_factory(Palestra, Material,can_delete=False,fields='__all__',
        widgets = {
            'nome': forms.TextInput(attrs={'class' : 'form-control'}),
            'embedded': forms.Textarea(attrs={'class' : 'form-control', 'rows' :'3'}),
            'arquivo': forms.FileInput(attrs={'class' : 'form-control'}),
        })    
     
class PalestraForm(forms.ModelForm):
        
    class Meta:
        model = Palestra
        now = datetime.date(datetime.now())
        now = now.strftime('%m/%d/%y') 
        fields = ['nome', 'descricao', 'release_date']   
        widgets = {'release_date': DateTimePicker(options={
                        "format": "YYYY-MM-DD","pickTime": False, 'startDate': now,}) }

    def __init__(self, *args, **kwargs):
        super(PalestraForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class' : 'form-control'})
        self.fields['descricao'].widget.attrs.update({'class' : 'form-control'}) 
                    