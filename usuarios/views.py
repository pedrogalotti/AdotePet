from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login as logar, logout


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet/')
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/auth/cadastro/')

        if len(senha) < 8:
            messages.add_message(request, constants.ERROR, 'Sua senha tem que ter pelo menos 8 digitos')
            return redirect('/auth/cadastro/')

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'A confirmação de senha é diferente da senha')
            return redirect('/auth/cadastro/')

        try:
            user = User.objects.create_user(
                username = nome,
                email = email,
                password = senha,
            )
            # Mensagem de sucesso
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastro com secesso')
            
            return redirect('/auth/cadastro/')
        except:
            # Mensagem de erro
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema. Tente novamente mais tarde')
            
            return redirect('/auth/cadastro/')

def login(request):
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet/')
    if request.method == 'GET':
        required = request.GET.get('required')
        return render(request, 'login.html', {'required': required})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')

        user = authenticate(username=nome,
                            password=senha)


        if user is not None:
            logar(request, user)
            
            return redirect('/divulgar/novo_pet/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário não existe. \n Já redirecionamos você para a página de cadastro ')
            
            return redirect('/auth/cadastro/')

def sair(request):
    logout(request)
    return redirect('/auth/login/')