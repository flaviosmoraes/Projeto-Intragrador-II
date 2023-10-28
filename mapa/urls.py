from django.urls import path
from . import views

urlpatterns = [
    path('', views.mapa, name="mapa"),
    path('getGeoJSON', views.getgeojson, name="getgeojson")
]
