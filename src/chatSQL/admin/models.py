from django.db import models
from .enums import TipoCampo


class StrutturaDatabase(models.Model):
    nome = models.CharField(max_length=255)
    descrizione = models.TextField()

    def __str__(self):
        return self.nome

class Tabella(models.Model):
    nome = models.CharField(max_length=255)
    descrizione = models.TextField()
    sinonimi = models.CharField(max_length=255, null=True, blank=True)
    struttura = models.ForeignKey(StrutturaDatabase, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Campo(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10, choices=[(tag.value, tag.name) for tag in TipoCampo])
    descrizione = models.TextField()
    sinonimi = models.CharField(max_length=255, null=True, blank=True)
    #another way to store synonyms is with comma separated values: synonyms = models.JSONField(null=True, blank=True) 
    tabella = models.ForeignKey(Tabella, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome
