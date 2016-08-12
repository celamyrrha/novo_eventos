# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from bsddb.test.test_all import verbose
from django.conf import settings
from django.template.defaultfilters import default

# Create your models here.
class EventoManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(nome__icontains=query) | \
            models.Q(descricao__icontains=query)
        )    
class Evento(models.Model):
    TIPO_CHOICES = (
        (0,'Pago'),
        (1,'Gratuito'),
    )
    nome_evento = models.CharField('Nome do evento', max_length = 100)
    slug = models.SlugField('Atalho')
    data_inicio = models.DateField('Data de inicio', null = True, blank = True)
    data_fim = models.DateField('Data de término', null = True, blank = True)
    vagas_evento = models.IntegerField('Número de vagas', null = True, blank = True)
    descricao = models.TextField('Descrição do Evento', blank = True)
    nome_palestrante = models.CharField('Nome do palestrante', max_length = 100)
    tipo_evento = models.IntegerField('Tipo do Evento', choices = TIPO_CHOICES, default = 0, blank = True)
    imagem_evento = models.ImageField(upload_to='eventos/images', verbose_name = 'Imagem', null = True, blank = True)
    endereco = models.CharField(max_length=255, verbose_name=u'Endereço', help_text='Para uma melhor localiza��o no mapa, preencha sem abrevia��es. Ex: Rua Martinho Estrela,  1229') 
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255, help_text="Para uma melhor localizacao no mapa, preencha sem abreviacoes. Ex: Belo Horizonte")
    estado = models.CharField(max_length=2, null=True, blank=True)
    criado = models.DateTimeField('Criado em', auto_now_add=True)
    objects = EventoManager()
    
    def __str__(self):
        return self.nome_evento
    def __unicode__(self):
        return self.nome_evento
    
    @models.permalink
    def get_absolute_url(self):
        return ('eventos:detalhes', (), {'slug': self.slug})
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['nome_evento']

class Inscricao(models.Model):
    STATUS_CHOICES = (
        (0,'Pendente'),
        (1,'Aprovado'),
        (2,'Cancelado')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Usuário', related_name='inscricoes')
    evento = models.ForeignKey(Evento, verbose_name = 'Evento', related_name='inscricoes')
    status = models.IntegerField('Situação', choices = STATUS_CHOICES, default = 0, blank = True)
    criado = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado = models.DateTimeField('Atualizado em', auto_now=True)
    
    def active(self):
        self.status = 1
        self.save()
    
    def is_approved(self):
        return self.status == 1
    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'evento'), )
        
class Aviso(models.Model):
    evento = models.ForeignKey(Evento, verbose_name = 'Evento', related_name='avisos')
    titulo = models.CharField('Título', max_length=100)
    conteuto = models.TextField('Conteúdo')
    criado = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado = models.DateTimeField('Atualizado em', auto_now=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Aviso'
        verbose_name_plural = 'Avisos'
        ordering = ['-criado']