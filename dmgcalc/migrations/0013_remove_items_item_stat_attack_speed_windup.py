# Generated by Django 4.0.5 on 2022-06-27 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dmgcalc', '0012_rename_item_stat_crit_change_items_item_stat_crit_chance_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='item_stat_attack_speed_windup',
        ),
    ]
