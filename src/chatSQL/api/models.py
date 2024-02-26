from django.db import models

# Create your models here.
class adminList(models.Model):
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)

    def __str__(self):
        return self.username+" "+self.password

class dbList(models.Model):
    admin=models.ForeignKey(adminList,on_delete=models.CASCADE)
    dbName=models.CharField(max_length=255)
    dbStructure=models.CharField(max_length=255)

    def __str__(self):
        return self.dbName