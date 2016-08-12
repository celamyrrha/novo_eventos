 # -*- coding: utf-8 -*-
from django import forms
from django.core.mail import send_mail
from django.conf import settings

from novo_eventos.core.mail import send_mail_template

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