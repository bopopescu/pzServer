from rest_framework import serializers
from .models import Locale, Presa, Recensione, ProfiloUtente
from django.db.models import Count
from rest_auth.serializers import UserDetailsSerializer



class LocaleNewSerializer(serializers.ModelSerializer):
    #created_by = serializers.HiddenField(default=serializers.CurrentUserDefault)

    class Meta:
        model = Locale
        fields = '__all__'
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}


class LocaleSerializer(serializers.ModelSerializer):
    totale_recensioni = serializers.SerializerMethodField(read_only=True)
    media_recensioni = serializers.FloatField(read_only=True)
    totale_prese = serializers.SerializerMethodField(read_only=True)

    def get_totale_recensioni(self, locale):
        return Recensione.objects.filter(locale=locale).count()

    def get_totale_prese(self, locale):
        return Presa.objects.values('presa').filter(locale=locale).annotate(num_prese=Count('presa'))

    class Meta:
        model = Locale
        fields = '__all__'
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}


class PresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presa
        fields = ['presa', 'locale', 'created_by']


class RecensioneSerializer(serializers.ModelSerializer):
    #recensore = serializers.ReadOnlyField(source='created_by')
    created_by = serializers.ReadOnlyField(source='created_by.username')
    locale_nome = serializers.ReadOnlyField(source='locale.nome')

    class Meta:
        model = Recensione
        #exclude = ['created_by']
        fields = '__all__'
        #extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}


class RecensioneNewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recensione
        fields = '__all__'
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}


class UserSerializer(UserDetailsSerializer):
    avatar = serializers.ImageField(source="profiloutente.avatar")
    recensioni_inserite = serializers.SerializerMethodField(read_only=True)
    locali_inseriti = serializers.SerializerMethodField(read_only=True)
    prese_inserite = serializers.SerializerMethodField(read_only=True)

    def get_recensioni_inserite(self, user):
        return Recensione.objects.filter(created_by=user).count()

    def get_prese_inserite(self, user):
        return Presa.objects.filter(created_by=user).count()

    def get_locali_inseriti(self, user):
        return Locale.objects.filter(created_by=user).count()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('avatar', 'locali_inseriti', 'prese_inserite', 'recensioni_inserite')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profiloutente', {})
        avatar = profile_data.get('avatar')
        instance = super(UserSerializer, self).update(instance, validated_data)
        #get e update profiloutente
        profilo = instance.profiloutente
        if profile_data and avatar:
            profilo.avatar = avatar
            profilo.save()
        return instance
