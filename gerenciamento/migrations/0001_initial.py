# Generated by Django 4.2.6 on 2023-10-24 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='postos_coleta',
            fields=[
                ('id_posto', models.AutoField(primary_key=True, serialize=False)),
                ('endereco_completo', models.TextField()),
                ('nome_posto', models.CharField(max_length=255)),
                ('atualizado_em', models.DateTimeField(auto_now_add=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='residuos',
            fields=[
                ('id_residuo', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade_kg', models.FloatField()),
                ('publicado_em', models.DateTimeField(auto_now_add=True, null=True)),
                ('publicado_por', models.CharField(max_length=255)),
                ('recolhido_em', models.DateTimeField(null=True)),
                ('foi_recolhido', models.BooleanField(default=False)),
                ('posto_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gerenciamento.postos_coleta')),
            ],
        ),
    ]