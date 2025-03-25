from django.db import models

class PagaduriasLinix(models.Model):
    n_nomina = models.CharField(max_length=200)
    nit  = models.CharField(max_length=200)
    n_razon = models.CharField(max_length=200)
    f_creacion = models.CharField(max_length=200)
    sigla = models.CharField(max_length=200)
    k_tipoem = models.CharField(max_length=200)
    pais = models.CharField(max_length=200)
    departamento = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=200)
    num_representante = models.CharField(max_length=200)
    representante = models.CharField(max_length=200)
    k_nomina = models.CharField(max_length=200)
    num_asociados = models.CharField(max_length=200)
    num_cdat = models.CharField(max_length=200)
    num_cooviahorros = models.CharField(max_length=200)
    num_creditos = models.CharField(max_length=200)
    num_ahorroVista = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.n_nomina} - {self.k_nomina}"