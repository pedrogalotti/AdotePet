from django.shortcuts import render, redirect
from divulgar.models import Pet, Raca
from django.contrib import messages
from .models import PedidoAdocao
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail


@login_required(login_url='/auth/login/?required=1')
def listar_pets(request):
    if request.method == 'GET':
        pets = Pet.objects.filter(status='P')
        racas = Raca.objects.all()


        # Filtragem
        cidade = request.GET.get('cidade')
        raca_filter = request.GET.get('raca')

        # Filtragem
        if cidade:
            pets = pets.filter(cidade__icontains=cidade)

        if raca_filter:
            pets = pets.filter(raca__id = raca_filter)
            raca_filter = Raca.objects.get(id=raca_filter)

        context = {
            'pets': pets,
            'racas': racas,
            'cidade': cidade,
            'raca_filter': raca_filter,
        }
        return render(request, 'listar_pets.html', context=context)



@login_required(login_url='/auth/login/?required=1')
def pedido_adocao(request, id_pet):
    pet = Pet.objects.filter(id=id_pet).filter(status='P')

    if not pet.exists():
        messages.warning(request, 'Esse pet já foi adotado')    
        return redirect('/adotar/')


    pedido = PedidoAdocao(pet=pet.first(), user=request.user, data=datetime.now())

    pedido.save()

    messages.success(request, 'Pedido de adoção realizado com secesso')    
    return redirect('/adotar/')


@login_required(login_url='/auth/login/?required=1')
def processa_pedido_adocao(request, id_pedido):

    status = request.GET.get('status')
    pedido = PedidoAdocao.objects.get(id=id_pedido)

    if status == 'A':
        pedido.status = 'AP'
        string = '''Olá, sua adoção foi aprovada com sucesso...'''
    elif status ==  'R':
        pedido.status = 'R'
        string = '''Olá, sua adoção foi recusa...'''

    pedido.save()

    email = send_mail(
        'Sua adoção foi processada',
        string,
        'suport.pedrodev@gmail.com',
        [pedido.user.email,]
    )

    messages.success(request, 'Pedido de adoção processado com sucesso.')
    return redirect('/divulgar/ver_pedido_adocao/')