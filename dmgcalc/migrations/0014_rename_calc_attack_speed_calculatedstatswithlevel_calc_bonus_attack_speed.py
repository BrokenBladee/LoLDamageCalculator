# Generated by Django 4.0.5 on 2022-06-29 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dmgcalc', '0013_remove_items_item_stat_attack_speed_windup'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calculatedstatswithlevel',
            old_name='calc_attack_speed',
            new_name='calc_bonus_attack_speed',
        ),
    ]