from django.db import models
from .enums import FieldType


class StrutturaDatabase(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class Tabella(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    structure = models.OneToOneField(StrutturaDatabase, on_delete=models.CASCADE, related_name='table')

class Campo(models.Model):
    name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=10, choices=[(tag.value, tag.name) for tag in FieldType])
    description = models.TextField()
    synonyms = models.JSONField(null=True, blank=True) 
    #another way to store synonyms is with comma separated values: synonyms = models.CharField(max_length=255)
    table = models.ForeignKey(Tabella, on_delete=models.CASCADE, related_name='field')
    
