# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, EditaAccountForm, PasswordResetForm, OrganizadorForm
from .models import PasswordReset
from django.contrib import messages

User = get_user_model()
# Create your views here.

def registro(request):
    template_name = 'registro.html'
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                    username=user.username, password=form.cleaned_data['password1']
                )
            login(request, user)
            return redirect('core:home')
    else:
        form = RegistroForm()        
    context = {'form': form}
    return render(request, template_name, context)

def registro_organizador(request):
    template_name = 'registro_organizador.html'
    if request.method == 'POST':
        form = OrganizadorForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                    username=user.username, password=form.cleaned_data['password1']
                )
            login(request, user)
            return redirect('core:home')
    else:
        form = OrganizadorForm()        
    context = {'form': form}
    return render(request, template_name, context)

def password_reset(request):
    template_name = 'password_reset.html'
    context = {  }
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        form.save()
        context['success']= True
    context['form']= form
    
    return render(request, template_name, context)

def password_reset_confirm(request, key):
    template_name = 'password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form    
    return render(request, template_name, context)

@login_required   
def painel_usuario(request):
    template_name = 'painel.html'
    context = {}
    return render(request, template_name, context)    

@login_required   
def editar(request):
    template_name = 'editar.html'
    context = {}
    if request.method == 'POST':
        form = EditaAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Os dados da sua conta foram alterados com sucesso.')
            return redirect('accounts:painel_usuario')
            
    else:
        form = EditaAccountForm(instance=request.user)
    context ['form'] = form
    return render(request, template_name, context)

@login_required   
def editar_senha(request):
    template_name = 'editar_senha.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context ['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)
    context ['form'] = form
    return render(request, template_name, context)