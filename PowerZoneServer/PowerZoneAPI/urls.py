from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from PowerZoneAPI import views

urlpatterns = [
    path('locali/', views.ListaLocali.as_view()),
    path('locali/<int:pk>/', views.DettaglioLocale.as_view()),
    path('prese/', views.ListaPrese.as_view()),
    path('prese/<int:pk>/', views.DettaglioPresa.as_view()),
    path('recensioni/', views.ListaRecensioni.as_view()),
    path('recensioni/<int:pk>', views.DettaglioRecensione.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)