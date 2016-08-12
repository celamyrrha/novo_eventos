from django.contrib import admin

# Register your models here.
from .models import Evento, Inscricao, Aviso


class EventoAdmin(admin.ModelAdmin):
    list_display = ['nome_evento', 'criado']
    search_fields = ['nome_evento', 'slug']
    prepopulated_fields = {"slug": ("nome_evento",)}
    
admin.site.register(Evento, EventoAdmin)
admin.site.register([Inscricao, Aviso])
