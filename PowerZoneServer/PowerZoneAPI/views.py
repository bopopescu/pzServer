from .models import Locale, Presa, Recensione
from .serializers import LocaleSerializer, PresaSerializer, RecensioneSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.registration.views import SocialLoginView
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly




class ListaLocali(generics.ListAPIView):
    queryset = Locale.objects.all()
    serializer_class = LocaleSerializer

    def post(self, request, format=None):
        serializer = LocaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DettaglioLocale(generics.RetrieveUpdateDestroyAPIView):
    queryset = Locale.objects.all()
    serializer_class = LocaleSerializer


class ListaPrese(generics.ListAPIView):
    queryset = Presa.objects.all()
    serializer_class = PresaSerializer

    def post(self, request, format=None):
        serializer = PresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DettaglioPresa(generics.RetrieveUpdateDestroyAPIView):
    queryset = Presa.objects.all()
    serializer_class = PresaSerializer


class ListaRecensioni(generics.ListAPIView):
    queryset = Recensione.objects.all()
    serializer_class = RecensioneSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def post(self, request, format=None):
        serializer = RecensioneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DettaglioRecensione(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recensione.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    serializer_class = RecensioneSerializer


class RecensioniLocale(generics.ListAPIView):
    serializer_class = RecensioneSerializer

    def get_queryset(self):
               #Questa view ritorna la lista delle recensioni di una presa
       
        localeid = self.kwargs['locale']
        return Recensione.objects.filter(locale_id=localeid)


class LocaliDistanza(generics.ListAPIView):
    serializer_class = LocaleSerializer


    def get_queryset(self):
        # Ritorna dato un punto e la distanza tutti i locali entro la distanza del punto

        dist = int(self.request.query_params.get('distanza',None))
        lon = float(self.request.query_params.get('lon'))
        lat = float(self.request.query_params.get('lat'))

        pnt = Point(lat, lon)
        return Locale.objects.filter(coordinate__distance_lte=(pnt, D(m=dist)))


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class LocaliDistanzaFiltro(generics.ListAPIView):
    serializer_class = LocaleSerializer


    def get_queryset(self):
        dist = self.request.query_params.get('distanza', None)
        lon = float(self.request.query_params.get('lon'))
        lat = float(self.request.query_params.get('lat'))
        tipo = self.request.query_params.get('tipo', None)
        presa = self.request.query_params.get('presa', None)
        if lon is not None and lat is not None:
            pnt = Point(lat, lon)
            if dist is not None:
                dist = int(dist)
                if tipo is not None:
                    if presa is not None:

                        return Locale.objects.filter(
                            coordinate__distance_lte=(pnt, D(m=dist)),
                            tipo_locale=tipo,
                            prese__tipo_presa__isnull=False,
                            prese__tipo_presa=presa)
                    else:
                        return Locale.objects.filter(coordinate__distance_lte=(pnt, D(m=dist)), tipo_locale=tipo)
                else:
                    return Locale.objects.filter(coordinate__distance_lte=(pnt, D(m=dist)))
            else:
                return Locale.objects.filter(coordinate__distance_lte=(pnt, D(m=1000)))

"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .models import Locale
from .serializers import LocaleSerializer


class ListaLocali(APIView):
    # ritorna tutti i locali
    def get(self,request, format=None):
        locali= Locale.objects.all()
        serializer = LocaleSerializer(locali, many=True)
        return Response(serializer.data)
    # Crea nuovo locale
    def post(self,request, format=None):
        serializer=LocaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DettaglioLocale(APIView):

    # Ricerca elemento
    def get_object(self, pk):
        try:
            return Locale.objects.get(pk=pk)
        except Locale.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        locale = self.get_object(pk)
        serializer = LocaleSerializer(locale)
        return Response(serializer.data)

    # Update locale
    def put(self, request, pk, format=None):
        locale=self.get_object(pk)
        serializer= LocaleSerializer(locale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Cancellazione locale
    def delete(self,request,pk,format=None):
        locale= self.get_object(pk)
        locale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
