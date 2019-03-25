from rest_framework import serializers
from .models import Locale, Presa, Recensione
from django.contrib.auth.models import User
from django.db.models import Count


class LocaleSerializer(serializers.ModelSerializer):
    prese = serializers.StringRelatedField(many=True)
    recensioni = serializers.StringRelatedField(many=True)
    totale_recensioni = serializers.SerializerMethodField(read_only=True);


    totale_prese = serializers.SerializerMethodField(read_only=True);
    
    def get_totale_prese(self, locale):

        return Locale.objects.values('prese__presa__tipo').order_by().annotate(Count('prese__presa__tipo'))
        #return Locale.objects.annotate(numero_prese_tipo=Count(''))
        #return Locale.objects.filter(id=id).values('prese__presa__tipo').annotate(dcount=Count('prese__presa__tipo'))

    def get_totale_recensioni(self, locale):
        return locale.recensioni.count()

    class Meta:
        model = Locale
        fields = '__all__'


class PresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presa
        fields = '__all__'


class RecensioneSerializer(serializers.ModelSerializer):
    recensore = serializers.ReadOnlyField(source='recensore.username')

    class Meta:
        model = Recensione
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')
