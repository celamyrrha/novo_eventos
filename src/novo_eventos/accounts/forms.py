# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from novo_eventos.core.mail import send_mail_template
from novo_eventos.core.utils import generate_hash_key

from .models import PasswordReset

User = get_user_model()
    
        
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError('Nenhum usuário encontrado com este e-mail')
    
    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.name)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'password_reset_mail.html'
        subject = 'Criar nova senha no Event4Us'
        context = { 'reset' : reset }
        send_mail_template(subject, template_name, context, [user.email])

class RegistroForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail')
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação de senha não está correta')
        return password2
    
    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    class Meta:
        model = User
        fields = ['username', 'email']
class EditaAccountForm(forms.ModelForm):
           
    
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'cidade', 'estado', 'sexo']   