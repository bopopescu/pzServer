from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from PowerZoneAPI import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('locali/', views.ListaLocali.as_view()),
    path('locali/<int:pk>/', views.DettaglioLocale.as_view()),
    path('locali/filtra', views.LocaliDistanzaFiltro.as_view()),

    path('prese/', views.ListaPrese.as_view()),
    path('prese/<int:pk>/', views.DettaglioPresa.as_view(), name='prese-detail'),
    path('recensioni/', views.ListaRecensioni.as_view()),
    path('recensioni/filtra', views.RecensioniUtente.as_view()),
    path('recensioni/<int:pk>', views.DettaglioRecensione.as_view(), name='recensioni-detail'),
    #path('recensioni/locale=<int:locale>', views.RecensioniLocale.as_view()),
    path('rest-auth/twitter/', views.TwitterLogin.as_view(), name='twitter_login'),
    path('rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/google/', views.GoogleLogin.as_view(), name='goggle_login'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
