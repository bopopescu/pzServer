from rest_framework import serializers
from .models import Locale, Presa, Recensione, TipoPresa
from django.contrib.auth.models import User
from django.db.models import Count, Avg


class LocaleSerializer(serializers.ModelSerializer):
    totale_recensioni = serializers.SerializerMethodField(read_only=True)
    media_recensioni = serializers.FloatField(read_only=True)
    totale_prese = serializers.SerializerMethodField(read_only=True)
    
    def get_totale_prese(self, locale):
        return Presa.objects.values('presa__tipo').filter(locale=locale).annotate(num_prese=Count('presa__tipo'))
        
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
