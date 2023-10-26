from django.urls import path
from . import views

urlpatterns = [
    path('', views.gerenciamento, name="gerenciamento"),
    path('adicionar', views.adicionar, name="adicionar"),
    path('editar', views.editar, name="editar"),
    path('excluir', views.excluir, name="excluir"),
    path('atualizar', views.atualizar, name="atualizar")
]
