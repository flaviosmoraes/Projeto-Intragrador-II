from django.shortcuts import render
from .models import postos_coleta, residuos
from geopy.geocoders import GoogleV3
from geopy.geocoders import Nominatim
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect


def gerenciamento(request):
    return render(request, 'gerenciamento.html')


def adicionar(request):
    if request.method == 'POST':
        nome_posto = request.POST.get('nome_posto')
        endereco_completo = request.POST.get('endereco_completo')
        if not nome_posto or not endereco_completo:
            if not nome_posto and endereco_completo:
                return HttpResponse('<p><em>ERRO:</em> Escreva o nome do posto.</p>')
            elif nome_posto and not endereco_completo:
                return HttpResponse('<p><em>ERRO:</em> Escreva o endereço do posto.</p>')
            return HttpResponse('<p><em>ERRO:</em> Escreva as informações de endereço e nome do posto.</p>')
        nome_e_endereco = nome_posto + ", " + endereco_completo
        novo_posto = postos_coleta()
        novo_posto.endereco_completo = endereco_completo
        novo_posto.nome_posto = nome_posto
        if nome_e_endereco:
            geolocator = GoogleV3(
                api_key='AIzaSyCpeQyKNjQSD-5Of4GBbOyVEwyDRL1lU3E')
            location = geolocator.geocode(nome_e_endereco)
            if location:
                novo_posto.latitude = location.latitude
                novo_posto.longitude = location.longitude
                novo_posto.save()
                return HttpResponse('<p>O posto ' + nome_posto + ' foi adicionado com sucesso</p>')
        return HttpResponse('<p><em>ERRO:</em> O endereço: ' + nome_e_endereco + ' não foi encontado e o posto não foi adicionado!</p>')
    else:
        return HttpResponseRedirect('/gerenciamento/')


def editar(request):
    if request.method == 'POST':
        id_posto_editar = request.POST.get('id_posto')
        endereco_completo = request.POST.get('endereco_completo')
        nome_posto = request.POST.get('nome_posto')
        if not id_posto_editar:
            return HttpResponse('<p><em>ERRO:</em> Digite o numero de um posto.</p>')
        if not nome_posto or not endereco_completo:
            if not nome_posto and endereco_completo:
                return HttpResponse('<p><em>ERRO:</em> Escreva o novo nome do posto.</p>')
            elif nome_posto and not endereco_completo:
                return HttpResponse('<p><em>ERRO:</em> Escreva o novo endereço do posto.</p>')
            return HttpResponse('<p><em>ERRO:</em> Escreva as novas informações de endereço e nome do posto.</p>')
        try:
            posto_a_editar = postos_coleta.objects.get(
                id_posto=id_posto_editar)
            nome_e_endereco = nome_posto + ", " + endereco_completo
            posto_a_editar.endereco_completo = endereco_completo
            posto_a_editar.nome_posto = nome_posto
            posto_a_editar.atualizado_em = timezone.now()
            geolocator = GoogleV3(
                api_key='AIzaSyCpeQyKNjQSD-5Of4GBbOyVEwyDRL1lU3E')
            location = geolocator.geocode(nome_e_endereco)
            if location:
                posto_a_editar.latitude = location.latitude
                posto_a_editar.longitude = location.longitude
                posto_a_editar.save()
                return HttpResponse('<p>O posto ' + id_posto_editar + ' foi editado com sucesso</p>')
            return HttpResponse('<p><em>ERRO:</em> O endereço: ' + nome_e_endereco + ' não foi encontado e o posto não foi editado!</p>')
        except postos_coleta.DoesNotExist:
            return HttpResponse('<p><em>ERRO:</em> Não exite um posoto com o id: ' + id_posto_editar + '</p>')
    else:
        return HttpResponseRedirect('/gerenciamento/')


def excluir(request):
    if request.method == 'POST':
        id_posto_excluir = request.POST.get('id_posto')
        if not id_posto_excluir:
            return HttpResponse('<p><em>ERRO:</em> Digite o numero de um posto.</p>')
        try:
            posto_a_excluir = postos_coleta.objects.get(
                id_posto=id_posto_excluir)
            nome_posto = posto_a_excluir.nome_posto
            posto_a_excluir.delete()
            return HttpResponse('<p>Sucesso ao excluir o posto ' + nome_posto + ' !</p>')
        except postos_coleta.DoesNotExist:
            return HttpResponse('<p><em>ERRO:</em> Não exite um posoto com o id: ' + id_posto_excluir + '</p>')
    else:
        return HttpResponseRedirect('/gerenciamento/')
