from django.conf.urls import url, patterns

urlpatterns =  patterns('novo_eventos.eventos.views',
    url(r'^$', 'lista_eventos', name='index'),
    #url(r'^(?P<pk>\d+)/$', 'detalhes', name='detalhes'),
    url(r'^(?P<slug>[\w_-]+)/$', 'detalhes', name='detalhes'),
    url(r'^(?P<slug>[\w_-]+)/inscricao/$', 'inscricoes', name='inscricoes'),
    url(r'^(?P<slug>[\w_-]+)/cancelar_inscricao/$', 'cancelar_inscricao', name='cancelar_inscricao'),
        url(r'^(?P<slug>[\w_-]+)/avisos/$', 'avisos', name='avisos'),
)