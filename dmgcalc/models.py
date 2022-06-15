from django.db import models


# Create your models here.

class Champion(models.Model):
    championName = models.CharField(max_length=200)
    level = models.IntegerField(default=1)



    def __str__(self):
        return str(self.id) + ' ' + self.championName