from rest_framework import serializers
from .models import Locale, Presa, Recensione
from django.contrib.auth.models import User


class LocaleSerializer(serializers.ModelSerializer):
    #prese = serializers.StringRelatedField(many=True)
    #recensioni = serializers.StringRelatedField(many=True)
    prese = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='prese-detail'
    )
    recensioni = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='recensioni-detail'
    )

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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
