from django.conf.urls import url, patterns

urlpatterns =  patterns('novo_eventos.eventos.views',
    url(r'^$', 'lista_eventos', name='index'),
    url(r'^novo/$', 'add_evento', name='add_evento'),
    url(r'^(?P<slug>[\w_-]+)/editar/$', 'edita_evento', name='edita_evento'),
    url(r'^(?P<slug>[\w_-]+)/excluir/$', 'exclui_evento', name='exclui_evento'),
    
    url(r'^(?P<slug>[\w_-]+)/lista_presenca/$', 'lista_presenca', name='lista_presenca'),
    url(r'^(?P<slug>[\w_-]+)/lista_presenca/print', 'imprimir_lista', name='imprimir_lista'),
    url(r'^(?P<slug>[\w_-]+)/$', 'detalhes', name='detalhes'),
    
    url(r'^(?P<slug>[\w_-]+)/inscricao/$', 'inscricoes', name='inscricoes'),
    url(r'^(?P<slug>[\w_-]+)/cancelar_inscricao/$', 'cancelar_inscricao', name='cancelar_inscricao'),
    
    url(r'^(?P<slug>[\w_-]+)/avisos/$', 'avisos', name='avisos'),
    url(r'^(?P<slug>[\w_-]+)/avisos/novo/$', 'add_aviso', name='add_aviso'),
    url(r'^(?P<slug>[\w_-]+)/avisos/(?P<pk>\d+)/editar/$', 'edita_aviso', name='edita_aviso'),
    url(r'^(?P<slug>[\w_-]+)/avisos/(?P<pk>\d+)/exclui/$', 'exclui_aviso', name='exclui_aviso'),
    
    url(r'^(?P<slug>[\w_-]+)/palestras/$', 'palestras', name='palestras'),
    url(r'^(?P<slug>[\w_-]+)/palestras/(?P<pk>\d+)/$', 'palestra', name='palestra'),
    url(r'^(?P<slug>[\w_-]+)/palestras/novo/$', 'add_palestra', name='add_palestra'),
    url(r'^(?P<slug>[\w_-]+)/palestras/(?P<pk>\d+)/editar/$', 'edita_palestra', name='edita_palestra'),
    url(r'^(?P<slug>[\w_-]+)/palestras/(?P<pk>\d+)/exclui/$', 'exclui_palestra', name='exclui_palestra'),
    
    
    url(r'^(?P<slug>[\w_-]+)/materiais/(?P<pk>\d+)/$', 'material', name='material'),
    
    url(r'^(?P<slug>[\w_-]+)/cracha/$', 'cracha', name='cracha'),
    url(r'^(?P<slug>[\w_-]+)/certificado/$', 'certificado', name='certificado'),
    
    url(r'^(?P<slug>[\w_-]+)/email-participantes/$', 'email_participantes', name='email_participantes'),
    url(r'^(?P<slug>[\w_-]+)/certificado-palestrante/$', 'certificado_palestrante', name='certificado_palestrante'),
    
    url(r'^(?P<slug>[\w_-]+)/pdf/$', 'relatorio_inscritos', name='relatorio_inscritos'),
    url(r'^(?P<slug>[\w_-]+)/grafico-sexo/$', 'grafico_sexo', name='grafico_sexo'),
    url(r'^(?P<slug>[\w_-]+)/grafico-cidade/$', 'grafico_cidade', name='grafico_cidade'),
)