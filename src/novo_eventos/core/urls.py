from django.conf.urls import url, patterns

urlpatterns =  patterns('novo_eventos.core.views',
    url(r'^$', 'home', name='home'),
    url(r'^contato/$', 'contact', name='contact'),
)