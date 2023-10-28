from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Sum, F, FloatField
from gerenciamento.models import postos_coleta, residuos


def mapa(request):
    return render(request, 'mapa.html')


def getgeojson(request):
    if request.method == 'POST':
        postos = postos_coleta.objects.all()

        geojson_data = {
            "type": "FeatureCollection",
            "features": []
        }

        for posto in postos:
            total_residuos_a_recolher = residuos.objects.filter(posto_fk=posto, foi_recolhido=False).aggregate(
                total=Sum(F('quantidade_kg'), output_field=FloatField()))['total'] or 0.0
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [posto.longitude, posto.latitude]
                },
                "properties": {
                    "id_posto": posto.id_posto,
                    "endereco_completo": posto.endereco_completo,
                    "nome_posto": posto.nome_posto,
                    "total_a_recolher": total_residuos_a_recolher
                }
            }
            geojson_data["features"].append(feature)

        return JsonResponse(geojson_data)
    else:
        return HttpResponseRedirect('/mapa/')
