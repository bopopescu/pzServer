from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geo


class TipoPresa(models.Model):
    tipo = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.tipo


class Locale(models.Model):
        # Possibili tipi di locale
    TIPI_LOCALE = (
        ('FREE', 'Gratis'),
        ('CONS', 'Previa consumazione'),
        ('PAY', 'A pagamento'),
    )
    nome = models.CharField(max_length=45, blank=True, default='')
    tipo_locale = models.CharField(max_length=4, choices=TIPI_LOCALE, default='FREE')
    coordinate = geo.PointField(srid=4326)
    email = models.EmailField(max_length=100, blank=True, default='')
    telefono = models.CharField(max_length=15, blank=True, default='')
    sitoweb = models.URLField(blank=True, default='')

    def __str__(self):
        return self.nome


class Recensione(models.Model):
    VOTI = [(i+1, i+1) for i in range(5)]
    voto = models.IntegerField(choices=VOTI)
    testo = models.CharField(max_length=250)
    locale = models.ForeignKey(Locale, related_name='recensioni', on_delete=models.CASCADE)
    recensore = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class Presa(models.Model):
    """TIPI_PRESA = (
        ('PR16', 'Presa elettrica grande'),
        ('PR10', 'Presa elettrica piccola'),
        ('PRSC', 'Presa Schuko'),
        ('PRU2', 'Presa USB'),
        ('PRU3', 'Presa USB 3.0'),
        ('PRAU', 'Presa auto elettrica'),
        ('PRBI', 'Bipresa'),
    )"""
    locale = models.ForeignKey(Locale, related_name='prese', on_delete=models.CASCADE)
    presa = models.ForeignKey(TipoPresa, on_delete=models.CASCADE)
    descrizione = models.CharField(max_length=250, blank=True, default='')
    path_foto = models.ImageField(upload_to='foto_prese/', default='', blank=True)

    # Questo metodo ritorna durante la stampa solo i dati richiesti
    def __str__(self):
        return self.presa.tipo + " : " + self.locale.nome

