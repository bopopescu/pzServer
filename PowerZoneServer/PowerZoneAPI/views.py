from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Locale, Presa, Recensione, ProfiloUtente
from .serializers import LocaleSerializer, PresaSerializer, RecensioneSerializer, RecensioneNewSerializer, LocaleNewSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from django.db.models import Avg, F

class ListaLocali(generics.ListAPIView):
    queryset = Locale.objects.all()
    serializer_class = LocaleNewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def post(self, request, format=None):
        serializer = LocaleNewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, owner=self.request.user)


class DettaglioLocale(generics.RetrieveUpdateDestroyAPIView):
    queryset = Locale.objects.all()
    serializer_class = LocaleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        return super().get_queryset().annotate(media_recensioni=Avg(F('recensioni__voto')))


class ListaPrese(generics.ListAPIView):
    queryset = Presa.objects.all()
    serializer_class = PresaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def post(self, request, format=None):
        serializer = PresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, owner=self.request.user)


class DettaglioPresa(generics.RetrieveUpdateDestroyAPIView):
    queryset = Presa.objects.all()
    serializer_class = PresaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class ListaRecensioni(generics.ListAPIView):
    queryset = Recensione.objects.all()
    serializer_class = RecensioneNewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def post(self, request, format=None):
        serializer = RecensioneNewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, owner=self.request.user)


class DettaglioRecensione(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recensione.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    serializer_class = RecensioneNewSerializer


class RecensioniLocale(generics.ListAPIView):
    serializer_class = RecensioneSerializer

    def get_queryset(self):
        # Questa view ritorna la lista delle recensioni di una presa

        localeid = self.kwargs['locale']
        return Recensione.objects.filter(locale_id=localeid)


class RecensioniUtente(generics.ListAPIView):
    serializer_class = RecensioneSerializer

    def get_queryset(self):
        utente = self.request.query_params.get('recensore', None)
        localeid = self.request.query_params.get('locale', None)
        if utente is not None:
            return Recensione.objects.filter(created_by=utente)
        elif localeid is not None:
            return Recensione.objects.filter(locale_id=localeid)


class LocaliDistanzaFiltro(generics.ListAPIView):
    serializer_class = LocaleSerializer

    def get_queryset(self):

        dist = self.request.query_params.get('distanza', None)
        lon = float(self.request.query_params.get('lon'))
        lat = float(self.request.query_params.get('lat'))
        tipo = self.request.query_params.get('tipo', None)

        presa = self.request.query_params.get('presa', None)
        if lon is not None and lat is not None:
            pnt = Point(lon, lat)
            if dist is not None:
                dist = int(dist)
                if tipo is not None:
                    tipo = tipo.split(',')
                    if presa is not None:

                        presa = presa.split(',')
                        return Locale.objects.filter(
                            coordinate__distance_lte=(pnt, D(m=dist)),
                            tipo_locale__in=tipo,
                            prese__presa__in=presa
                        ).annotate(media_recensioni=Avg(F('recensioni__voto')))
                    else:
                        return Locale.objects.filter(coordinate__distance_lte=(pnt, D(m=dist)),
                                                     tipo_locale__in=tipo).annotate(media_recensioni=Avg(F('recensioni__voto')))
                else:
                    if presa is not None:

                        presa = presa.split(',')
                        return Locale.objects.filter(
                            coordinate__distance_lte=(pnt, D(m=dist)),
                            prese__presa__in=presa
                        ).annotate(media_recensioni=Avg(F('recensioni__voto')))
                    else:
                        return Locale.objects.filter(coordinate__distance_lte=(pnt, D(m=dist))).annotate(media_recensioni=Avg(F('recensioni__voto')))
            else:
                if presa is not None:
                    presa = presa.split(',')
                    return Locale.objects.filter(
                        coordinate__distance_lte=(pnt, D(m=1000)),

                        prese__isnull=False,
                        prese__presa__in=presa
                    ).annotate(media_recensioni=Avg(F('recensioni__voto')))
                else:
                    return Locale.objects.filter(coordinate__distance_lte=(pnt, D(m=10000))).annotate(media_recensioni=Avg(F('recensioni__voto')))


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


