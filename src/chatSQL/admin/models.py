from django.db import models
from .enums import FieldType

class DatabaseStructure(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
class DatabaseTable(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    structure = models.OneToOneField(DatabaseStructure, on_delete=models.CASCADE, related_name='table')
    
class DatabaseField(models.Model):
    name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=10, choices=[(tag.value, tag.name) for tag in FieldType])
    description = models.TextField()
    synonyms = models.JSONField(null=True, blank=True) #another way to store synonyms is with comma separated values: synonyms = models.CharField(max_length=255)
    table = models.ForeignKey(DatabaseTable, on_delete=models.CASCADE, related_name='field')
    
