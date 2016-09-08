# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import signals 
from signals import create_slug
from django.template.defaultfilters import slugify
from django.db import models
from django.conf import settings
from novo_eventos.core.mail import send_mail_template
from django.db.models.fields import CharField
from django.template.defaultfilters import default
from time import timezone
from datetime import datetime
from localflavor.br.forms import BRStateSelect, BRStateChoiceField
from stdimage.models import StdImageField


# Create your models here.
class EventoManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(nome_evento__icontains=query) | \
            models.Q(descricao__icontains=query)
        )    
class Evento(models.Model):
    STATE_CHOICES = (('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'))
    TIPO_CHOICES = (
        (0,'Pago'),
        (1,'Gratuito'),
    )
    nome_evento = models.CharField('Nome do evento', max_length = 100)
    slug = models.SlugField('Atalho', unique=True)
    data_inicio = models.DateField('Data de inicio', null = True, blank = True)
    data_fim = models.DateField('Data de término', null = True, blank = True)
    vagas_evento = models.IntegerField('Número de vagas', null = True, blank = True)
    descricao = models.TextField('Descrição do Evento', blank = True)
    nome_palestrante = models.CharField('Nome do palestrante', max_length = 100)
    tipo_evento = models.IntegerField('Tipo do Evento', choices = TIPO_CHOICES, default = 0, blank = True)
    imagem_evento = StdImageField(upload_to='eventos/images', variations={'thumbnail': {"width": 325, "height": 250, "crop": True}}, verbose_name = 'Imagem')
    local = models.CharField(max_length=255, verbose_name='Local do Evento') 
    cidade = models.CharField(max_length=255)
    estado = models.CharField('Estado', choices = STATE_CHOICES, blank = True, max_length=2)
    criado = models.DateTimeField('Criado em', auto_now_add=True)
    objects = EventoManager() 
    slug_field_name = 'slug'
    slug_from = 'nome_evento'
    
    def __str__(self):
        return self.nome_evento
    def __unicode__(self):
        return self.nome_evento
    
    @models.permalink
    def get_absolute_url(self):
        return ('eventos:detalhes', (), {'slug': self.slug})
    
    def release_palestra(self):
        today = datetime.now().date()
        return self.palestras.filter(release_date__gte=today)
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['nome_evento']
        
signals.post_save.connect(create_slug, sender=Evento)    

class Palestra(models.Model):
    nome = models.CharField('Nome', max_length = 100)
    descricao = models.TextField('Descrição', blank = True)
    release_date = models.DateField('Data de liberação', null = True, blank = True)
    
    evento = models.ForeignKey(Evento, verbose_name='Evento', related_name='palestras')
    
    criado = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado = models.DateTimeField('Atualizado em', auto_now=True)
    
    def __str__(self):
        return self.nome
    
    def is_available(self):
        if self.release_date:
            today = datetime.now().date()
            return self.release_date >= today
        return False
    
    class Meta:
        verbose_name = 'Palestra'
        verbose_name_plural = 'Palestras'
        ordering = ['release_date']
        
class Material(models.Model):
    nome = models.CharField('Identificação do Material', max_length = 100)
    embedded = models.TextField('Vídeo embedded', blank = True)
    arquivo = models.FileField(upload_to='palestras/materiais', blank = True, null = True) 
    
    palestra = models.ForeignKey(Palestra, verbose_name='Palestra', related_name='materiais')
    
    def is_embedded(self):
        return bool(self.embedded)       
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'
        
        
class Inscricao(models.Model):
    STATUS_CHOICES = (
        (0,'Pendente'),
        (1,'Aprovado'),
        (2,'Concluído')
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
    conteudo = models.TextField('Conteúdo')
    criado = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado = models.DateTimeField('Atualizado em', auto_now=True)
    
    def __str__(self):
        return self.titulo

    
    class Meta:
        verbose_name = 'Aviso'
        verbose_name_plural = 'Avisos'
        ordering = ['-criado']
        
def post_save_avisos(instance, created, **kwargs):
    if created:
        subject = instance.titulo
        context = { 'aviso': instance }
        template_name = 'aviso_email.html'
        inscricoes = Inscricao.objects.filter(evento=instance.evento, status=1)
        for inscricao in inscricoes:
            recipient_list = [inscricao.user.email]
            send_mail_template(subject, template_name, context, recipient_list)
    
models.signals.post_save.connect(post_save_avisos, sender=Aviso, dispatch_uid='post_save_avisos')

