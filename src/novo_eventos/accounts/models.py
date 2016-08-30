# -*- coding: utf-8 -*-
import re

from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin,UserManager)
from django.conf import settings
from django.template.defaultfilters import default
from reportlab.lib.colors import black


class User(AbstractBaseUser, PermissionsMixin):

    STATE_CHOICES = (('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'))
    SEXO_CHOICES = (
        ('F','Feminino'),
        ('M','Masculino'),
    )
    
    username = models.CharField(
        'Nome de Usuario', max_length=30, unique=True, 
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
            'O nome de usuario só pode conter letras, dígitos ou os '
            'seguintes caracteres: @/./+/-/_', 'invalid')]
    )
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    cidade = models.CharField(max_length=255)
    estado = models.CharField('Estado', choices = STATE_CHOICES, blank = True, max_length=2)
    sexo = models.CharField('Sexo', choices = SEXO_CHOICES, blank = True, max_length = 1)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        
class PasswordReset (models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name = "usuario", 
        related_name='resets'
        )
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)
    
    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)
    
    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']