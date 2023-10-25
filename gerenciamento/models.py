from django.db import models
from django.utils import timezone


class postos_coleta(models.Model):
    id_posto = models.AutoField(primary_key=True)
    endereco_completo = models.TextField(null=False)
    nome_posto = models.CharField(max_length=255)
    atualizado_em = models.DateTimeField(auto_now_add=True, null=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


class residuos(models.Model):
    id_residuo = models.AutoField(primary_key=True)
    quantidade_kg = models.FloatField()
    publicado_em = models.DateTimeField(auto_now_add=True, null=True)
    publicado_por = models.CharField(max_length=255)
    recolhido_em = models.DateTimeField(null=True)
    foi_recolhido = models.BooleanField(default=False)
    posto_fk = models.ForeignKey(postos_coleta, on_delete=models.CASCADE)
