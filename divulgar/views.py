from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Tag, Raca, Pet
from adotar.models import PedidoAdocao
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/auth/login/?required=1')
def novo_pet(request):
    if request.method == 'GET':

        tags = Tag.objects.all()
        racas = Raca.objects.all()

        context = {
            'tags': tags,
            'racas': racas
        }

        return render(request, 'novo_pet.html', context=context)
    elif request.method == 'POST':
        #receber arquivos
        foto = request.FILES.get('foto')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        telefone = request.POST.get('telefone')
        # get = pega(guarda) uma informação ||| getlist pega mais de um dado
        tags = request.POST.getlist('tags')
        raca = request.POST.get('raca')

        #TODO: validar os dados

        if len(nome.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Campo Nome inválido.')
            return redirect('/divulgar/novo_pet/')
        if len(descricao.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Campo Descrição inválido.')
            return redirect('/divulgar/novo_pet/')
        if len(estado.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Campo Estado inválido.')
            return redirect('/divulgar/novo_pet/')
        if len(cidade.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Campo Cidade inválido.')
            return redirect('/divulgar/novo_pet/')
        if len(telefone.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Campo Telefone inválido.')
            return redirect('/divulgar/novo_pet/')

        try:
            pet = Pet(
                usuario = request.user,
                foto = foto,
                nome = nome,
                descricao = descricao,
                estado = estado,
                cidade = cidade,
                telefone = telefone,
                raca_id = raca
            )
            pet.save()
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema.')
            return redirect('/divulgar/novo_pet/')


        for tag_id in tags:
            tag = Tag.objects.get(id = tag_id)
            pet.tags.add(tag)

        pet.save()

        messages.add_message(request, constants.SUCCESS, 'Pet cadastrado')
        return redirect('/divulgar/seus_pets/')


@login_required(login_url='/auth/login/?required=1')
def seus_pets(request):
    if request.method == 'GET':
        pets = Pet.objects.filter(usuario=request.user)

        context = {
            'pets': pets,
        }

        return render(request, 'seus_pets.html', context=context)

@login_required(login_url='/auth/login/?required=1')
def remover_pet(request, id):
    pet = Pet.objects.get(id=id)

    if not pet.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Esse pet não é seu')
        return redirect('/divulgar/seus_pets/')

    pet.delete()
    messages.add_message(request, constants.SUCCESS, 'Pet deletado com sucesso')

    return redirect('/divulgar/seus_pets/')

@login_required(login_url='/auth/login/?required=1')
def ver_pet(request, id):
    if request.method == 'GET':
        pet = Pet.objects.get(id=id)
        return render(request, 'ver_pet.html', {'pet': pet})


@login_required(login_url='/auth/login/?required=1')
def ver_pedido_adocao(request):

    if request.method == 'GET':

        pedidos = PedidoAdocao.objects.filter(user=request.user).filter(status='AG')



        return render(request, 'ver_pedido_adocao.html', {'pedidos': pedidos})

@login_required(login_url='/auth/login/?required=1')
def dashboard(request):
    if request.method == 'GET':
        return render(request, 'dashboard.html')

@csrf_exempt
def api_adocoes_por_raca(request):
    racas = Raca.objects.all()

    qtd_adocoes = []
    for raca in racas:
        adocoes = PedidoAdocao.objects.filter(pet__raca=raca).filter(status='R').count()
        qtd_adocoes.append(adocoes)

    racas = [raca.raca for raca in racas]
    data = {'qtd_adocoes': qtd_adocoes,
            'labels': racas}

    return JsonResponse(data)