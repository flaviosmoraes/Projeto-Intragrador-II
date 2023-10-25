from django.shortcuts import render
from .models import postos_coleta, residuos
from geopy.geocoders import GoogleV3
from geopy.geocoders import Nominatim
from django.utils import timezone
from django.http import HttpResponse


def gerenciamento(request):
    return render(request, 'gerenciamento.html')


def adicionar(request):
    endereco_completo = request.POST.get(
        'nome_posto') + ", " + request.POST.get('endereco_completo')
    # endereco_completo = request.POST.get('endereco_completo')
    novo_posto = postos_coleta()
    novo_posto.endereco_completo = request.POST.get('endereco_completo')
    novo_posto.nome_posto = request.POST.get('nome_posto')
    if endereco_completo:
        geolocator = GoogleV3(
            api_key='AIzaSyCpeQyKNjQSD-5Of4GBbOyVEwyDRL1lU3E')
        # geolocator = Nominatim(user_agent="compostcollectorv2")
        location = geolocator.geocode(endereco_completo)
        if location:
            novo_posto.latitude = location.latitude
            novo_posto.longitude = location.longitude
            novo_posto.save()
            return HttpResponse('Sucesso ao inserir')
    return HttpResponse('Erro ao inserir')


def editar(request):
    id_posto_editar = request.POST.get('id_posto')
    posto_a_editar = postos_coleta.objects.get(id_posto=id_posto_editar)
    endereco_completo = request.POST.get(
        'nome_posto') + ", " + request.POST.get('endereco_completo')
    # endereco_completo = request.POST.get('endereco_completo')
    posto_a_editar.endereco_completo = request.POST.get('endereco_completo')
    posto_a_editar.nome_posto = request.POST.get('nome_posto')
    posto_a_editar.atualizado_em = timezone.now()
    if endereco_completo:
        geolocator = GoogleV3(
            api_key='AIzaSyCpeQyKNjQSD-5Of4GBbOyVEwyDRL1lU3E')
        # geolocator = Nominatim(user_agent="compostcollectorv2")
        location = geolocator.geocode(endereco_completo)
        if location:
            posto_a_editar.latitude = location.latitude
            posto_a_editar.longitude = location.longitude
            posto_a_editar.save()
            return HttpResponse('Sucesso ao editar')
    return HttpResponse('Erro ao editar')


def excluir(request):
    id_posto_excluir = request.POST.get('id_posto')
    posto_a_excluir = postos_coleta.objects.get(id_posto=id_posto_excluir)
    posto_a_excluir.delete()
    return HttpResponse('Sucesso ao excluir')
