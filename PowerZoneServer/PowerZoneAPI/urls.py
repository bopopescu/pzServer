from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from PowerZoneAPI import views

urlpatterns = [
    path('locali/', views.ListaLocali.as_view()),
    path('locali/<int:pk>/', views.DettaglioLocale.as_view()),
    path('locali/v1/', views.LocaliDistanza.as_view()),
    path('prese/', views.ListaPrese.as_view()),
    path('prese/<int:pk>/', views.DettaglioPresa.as_view()),
    path('recensioni/', views.ListaRecensioni.as_view()),
    path('recensioni/<int:pk>', views.DettaglioRecensione.as_view()),
    path('recensioni/locale=<int:locale>', views.RecensioniLocale.as_view()),
    path('rest-auth/twitter/', views.TwitterLogin.as_view(), name='twitter_login'),
    path('rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),

]

urlpatterns = format_suffix_patterns(urlpatterns)