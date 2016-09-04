#-*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from .models import (Evento, Inscricao, Aviso, Material, Palestra)


class EventoAdmin(admin.ModelAdmin):
    list_display = ['nome_evento', 'criado']
    search_fields = ['nome_evento', 'slug']
    prepopulated_fields = {"slug": ("nome_evento",)}
    
class MaterialInlineAdmin(admin.StackedInline):
    model = Material

class PalestraAdmin(admin.ModelAdmin):
    list_display = ['nome', 'evento', 'release_date']
    search_fields = ['nome', 'descricao']
    list_filter = ['criado']
    inlines = [MaterialInlineAdmin]
    
admin.site.register(Evento, EventoAdmin)
admin.site.register([Inscricao, Aviso, Material])
admin.site.register(Palestra, PalestraAdmin)

