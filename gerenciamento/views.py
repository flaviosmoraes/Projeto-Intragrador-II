from django.shortcuts import render
from .models import postos_coleta, residuos
from geopy.geocoders import GoogleV3
from geopy.geocoders import Nominatim
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.db.models import Sum, F
from time import sleep
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd


def gerenciamento(request):
    context = {
        'postos': postos_coleta.objects.all(),
        'residuos': residuos.objects.filter(foi_recolhido=True).values('publicado_por').annotate(total_quantidade_kg=Sum('quantidade_kg'))
    }
    return render(request, 'gerenciamento.html', context)


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


def excluir(request, id):
    if request.method == 'POST':
        if id == 1:
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
        if id == 2:
            residuos_recolhidos = residuos.objects.filter(foi_recolhido=True)
            if residuos_recolhidos:
                residuos_recolhidos.delete()
                return HttpResponse('<p>Os resíduos coletados foram limpos do banco de dados.</p>')
            else:
                return HttpResponse('<p><em>ERRO:</em> Não há resíduos marcados como recolhidos para serem limpos.</p>')
    else:
        return HttpResponseRedirect('/gerenciamento/')


def atualizar(request, id):
    if request.method == 'POST':
        if id == 1:
            context = {
                'residuos': residuos.objects.filter(foi_recolhido=True).values('publicado_por').annotate(total_quantidade_kg=Sum('quantidade_kg'))
            }
            return TemplateResponse(request, 'tabela_residuos_gerenciamento.html', context)
        if id == 2:
            postos = {
                'postos': postos_coleta.objects.all()
            }
            return TemplateResponse(request, 'tabela_postos.html', postos)
    else:
        return HttpResponseRedirect('/gerenciamento/')


def download(request):
    if request.method == 'POST':
        # Obtenha os dados que você deseja exportar para o Excel
        residuos_data = residuos.objects.filter(foi_recolhido=True).values(
            'publicado_por').annotate(total_quantidade_kg=Sum('quantidade_kg'))

        # Crie um DataFrame pandas com os dados
        df = pd.DataFrame(residuos_data)

        # Crie um novo Workbook Excel usando openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active

        # Use dataframe_to_rows para carregar os dados do DataFrame para a planilha Excel
        for row in dataframe_to_rows(df, index=False, header=True):
            ws.append(row)

        # Crie uma resposta HTTP com o conteúdo Excel
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=residuos.xlsx'

        # Salve o Workbook Excel na resposta
        wb.save(response)

        return response
    else:
        return HttpResponseRedirect('/gerenciamento/')
