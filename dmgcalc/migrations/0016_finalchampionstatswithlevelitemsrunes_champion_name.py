# Generated by Django 4.0.5 on 2022-07-01 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmgcalc', '0015_champion_base_movement_speed'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalchampionstatswithlevelitemsrunes',
            name='champion_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
