from django.db import models


# Create your models here.

class Champion(models.Model):
    championName = models.CharField(max_length=200)
    level = models.IntegerField(default=1)
    health_points = models.IntegerField(default=0)
    attack_damage = models.IntegerField(default=0)
    armour = models.IntegerField(default=0)
    magic_resistance = models.IntegerField(default=0)
  #  champion_icon = models.ImageField()

    def __str__(self):
        return str(self.id) + ' ' + self.championName