from django.conf.urls import url, patterns

urlpatterns =  patterns('',
    url(r'^$', 'novo_eventos.accounts.views.painel_usuario', 
        name='painel_usuario'),                    
    url(r'^entrar/$', 'django.contrib.auth.views.login', 
        {'template_name': 'login.html'}, name='login'),
    url(r'^sair/$', 'django.contrib.auth.views.logout', 
        {'next_page':'core:home'}, name='logout'),                    
    url(r'^cadastro/$', 'novo_eventos.accounts.views.registro', 
        name='registro'), 
    url(r'^cadastro-organizador/$', 'novo_eventos.accounts.views.registro_organizador', 
        name='registro_organizador'),                     
    url(r'^nova-senha/$', 'novo_eventos.accounts.views.password_reset', 
        name='password_reset'),    
    url(r'^confirmar-nova-senha/(?P<key>\w+)/$', 'novo_eventos.accounts.views.password_reset_confirm', 
        name='password_reset_confirm'),                                         
    url(r'^editar/$', 'novo_eventos.accounts.views.editar', 
        name='editar'),
    url(r'^editar-senha/$', 'novo_eventos.accounts.views.editar_senha', 
        name='editar_senha'),                    
                                                                
                        
)