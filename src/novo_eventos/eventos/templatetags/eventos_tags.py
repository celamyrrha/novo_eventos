from django.template import Library

register = Library()

from novo_eventos.eventos.models import Inscricao

@register.inclusion_tag('templatetags/meus_eventos.html')
def meus_eventos(user):
    inscricoes = Inscricao.objects.filter(user=user)
    context = {'inscricoes':inscricoes}
    return context

@register.assignment_tag
def load_meus_eventos(user):
    return Inscricao.objects.filter(user=user)