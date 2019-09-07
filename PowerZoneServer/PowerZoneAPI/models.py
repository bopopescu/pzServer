from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geo


class Locale(models.Model):
    # Possibili tipi di locale
    TIPI_LOCALE = (
        ('FREE', 'Gratis'),
        ('CONS', 'Previa consumazione'),
        ('PAY', 'A pagamento'),
    )
    nome = models.CharField(max_length=45, blank=True, default='')
    tipo_locale = models.CharField(max_length=4, choices=TIPI_LOCALE, default='FREE')
    coordinate = geo.PointField(spatial_index=True, geography=True)
    latitudine = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitudine = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, default='')
    telefono = models.CharField(max_length=15, blank=True, default='')
    sitoweb = models.URLField(blank=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='locali_inseriti')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Recensione(models.Model):
    VOTI = [(i+1, i+1) for i in range(5)]
    voto = models.IntegerField(choices=VOTI)
    testo = models.CharField(max_length=250)
    locale = models.ForeignKey(Locale, related_name='recensioni', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recensioni')


class Presa(models.Model):
    TIPI_PRESA = (
        ('PREL', 'Presa elettrica'),
        ('PUSB', 'Presa USB'),
        ('PRAU', 'Presa auto elettrica'),
    )
    locale = models.ForeignKey(Locale, related_name='prese', on_delete=models.CASCADE)
    presa = models.CharField(max_length=4, choices=TIPI_PRESA, default='PREL')

    descrizione = models.CharField(max_length=250, blank=True, default='')
    path_foto = models.ImageField(upload_to='foto_prese/', default='', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='prese_inserite')
    created_at = models.DateField(auto_now_add=True)
    # Questo metodo ritorna durante la stampa solo i dati richiesti
    def __str__(self):
        return self.presa + " : " + self.locale.nome


class ProfiloUtente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='immagini-profilo/', blank=True)

