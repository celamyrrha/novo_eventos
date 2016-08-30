# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Evento, Inscricao
from django.template.context_processors import request

def inscricao_required(view_func):
    def _wrapper(request, *args, **kwargs):
        slug = kwargs['slug']
        evento = get_object_or_404(Evento, slug=slug)
        has_permission = request.user.is_staff
        if not has_permission:
            try:
                inscricao = Inscricao.objects.get(user=request.user, evento=evento)
            except Inscricao.DoesNotExist:
                message = 'Desculpe, mas você não tem permissão para acessar esta página'
            else:
                if inscricao.is_approved():
                    has_permission = True
                else:
                    message = 'A sua inscrição no curso ainda está pendente'
        if not has_permission:
            messages.error(request, message)
            return redirect('accounts:painel_usuario')
        request.evento = evento
        return view_func(request, *args, **kwargs)
    return _wrapper