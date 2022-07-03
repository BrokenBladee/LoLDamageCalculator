from django.db import models


# Create your models here.

class Champion(models.Model):
    id = models.IntegerField(primary_key=True)

    champion_name = models.CharField(max_length=200)

    base_health_points = models.FloatField(default=0)
    health_points_per_level = models.FloatField(default=0)

    base_health_regen = models.FloatField(default=0)
    health_regen_per_level = models.FloatField(default=0)

    base_mana = models.FloatField(default=0)
    mana_per_level = models.FloatField(default=0)

    base_mana_regen = models.FloatField(default=0)
    mana_regen_per_level = models.FloatField(default=0)

    base_armor = models.FloatField(default=0)
    armor_per_level = models.FloatField(default=0)

    base_magic_resistance = models.FloatField(default=0)
    magic_resistance_per_level = models.FloatField(default=0)

    base_attack_damage = models.FloatField(default=0)
    attack_damage_per_level = models.FloatField(default=0)

    base_crit_damage = models.FloatField(default=0)

    base_attack_speed = models.FloatField(default=0)
    attack_speed_ratio = models.FloatField(default=0)
    attack_speed_windup = models.FloatField(default=0)
    attack_speed_bonus = models.FloatField(default=0)

    base_movement_speed = models.FloatField(default=0)

    # champion_icon = models.ImageField()

    def __str__(self):
        return str(self.id) + ' ' + self.champion_name


class CalculatedStatsWithLevel(models.Model):
    level = models.FloatField(default=1)
    champion_name = models.CharField(max_length=200, default='')

    calc_health_points = models.FloatField(default=0)
    calc_health_points_regen = models.FloatField(default=0)

    calc_mana = models.FloatField(default=0)
    calc_mana_regen = models.FloatField(default=0)

    calc_armor = models.FloatField(default=0)

    calc_magic_resistance = models.FloatField(default=0)

    calc_attack_damage = models.FloatField(default=0)

    calc_crit_damage = models.FloatField(default=0)

    calc_bonus_attack_speed = models.FloatField(default=0)


class FinalChampionStatsWithLevelItemsRunes(models.Model):
    champion_name = models.CharField(max_length=200, default='')
    champion_level = models.FloatField(default=1)

    item_name_one = models.CharField(max_length=200, default='')
    item_name_two = models.CharField(max_length=200, default='')
    item_name_three = models.CharField(max_length=200, default='')
    item_name_four = models.CharField(max_length=200, default='')
    item_name_five = models.CharField(max_length=200, default='')
    item_name_six = models.CharField(max_length=200, default='')

    ability_q_level = models.FloatField(default=0)
    ability_w_level = models.FloatField(default=0)
    ability_e_level = models.FloatField(default=0)
    ability_r_level = models.FloatField(default=0)

    # RUNES STILL MISSING HERE!!!!!!!!!!!

    health_points = models.FloatField(default=0)
    base_health_points = models.FloatField(default=0)
    bonus_health_points = models.FloatField(default=0)
    health_points_regen = models.FloatField(default=0)
    base_health_points_regen = models.FloatField(default=0)

    mana = models.FloatField(default=0)
    base_mana = models.FloatField(default=0)
    bonus_mana = models.FloatField(default=0)
    mana_regen = models.FloatField(default=0)
    base_mana_regen = models.FloatField(default=0)

    armor = models.FloatField(default=0)
    base_armor = models.FloatField(default=0)
    bonus_armor = models.FloatField(default=0)

    magic_resistance = models.FloatField(default=0)
    base_magic_resistance = models.FloatField(default=0)
    bonus_magic_resistance = models.FloatField(default=0)

    attack_damage = models.FloatField(default=0)
    base_attack_damage = models.FloatField(default=0)
    bonus_attack_damage = models.FloatField(default=0)

    crit_damage = models.FloatField(default=0)
    crit_chance = models.FloatField(default=0)

    armor_pen_percentage = models.FloatField(default=0)
    armor_pen_flat = models.FloatField(default=0)

    ability_power = models.FloatField(default=0)

    ability_haste = models.FloatField(default=0)

    magic_pen_percentage = models.FloatField(default=0)
    magic_pen_flat = models.FloatField(default=0)

    movement_speed = models.FloatField(default=0)

    attack_speed = models.FloatField(default=0)
    attack_speed_windup = models.FloatField(default=0)

    tenacity = models.FloatField(default=0)
    slow_resistance = models.FloatField(default=0)

    heal_and_shield_power = models.FloatField(default=0)

    life_steal = models.FloatField(default=0)
    physical_vamp = models.FloatField(default=0)
    omnivamp = models.FloatField(default=0)

    gold_generation = models.FloatField(default=20.4)


class Items(models.Model):
    id = models.IntegerField(primary_key=True)
    item_name = models.CharField(max_length=200)
    # starter: 1, consumables: 2, trinkets: 3, distributed: 4, boots: 5, basic: 6, epic: 7, legendary: 8, mythic: 9, champ_exc: 10, ornn: 11
    type_of_item = models.IntegerField(default=0)

    item_stat_hp = models.FloatField(default=0)
    item_stat_hp_regen = models.FloatField(default=0)

    item_stat_mana = models.FloatField(default=0)
    item_stat_mana_regen = models.FloatField(default=0)

    item_stat_armor = models.FloatField(default=0)
    item_stat_mr = models.FloatField(default=0)

    item_stat_attack_damage = models.FloatField(default=0)

    item_stat_crit_damage = models.FloatField(default=0)
    item_stat_crit_chance = models.FloatField(default=0)

    item_stat_armor_pen_percentage = models.FloatField(default=0)
    item_stat_armor_pen_flat = models.FloatField(default=0)

    item_stat_ability_power = models.FloatField(default=0)

    item_stat_ability_haste = models.FloatField(default=0)

    item_stat_magic_pen_percentage = models.FloatField(default=0)
    item_stat_magic_pen_flat = models.FloatField(default=0)

    item_stat_movement_speed_percentage = models.FloatField(default=0)
    item_stat_movement_speed_flat = models.FloatField(default=0)

    item_stat_attack_speed = models.FloatField(default=0)

    item_stat_tenacity = models.FloatField(default=0)
    item_stat_slow_resistance = models.FloatField(default=0)

    item_stat_heal_and_shield_power = models.FloatField(default=0)

    item_stat_life_steal = models.FloatField(default=0)
    item_stat_physical_vamp = models.FloatField(default=0)
    item_stat_omnivamp = models.FloatField(default=0)
    item_stat_gold_generation = models.FloatField(default=0)

    item_stat_grievous_wounds = models.FloatField(default=0.0)

    ##

    mythic_stat_hp = models.FloatField(default=0)
    mythic_stat_armor = models.FloatField(default=0)
    mythic_stat_mr = models.FloatField(default=0)

    mythic_stat_attack_damage = models.FloatField(default=0)
    mythic_stat_attack_speed = models.FloatField(default=0)
    mythic_stat_armor_pen_percentage = models.FloatField(default=0)
    mythic_stat_armor_pen_flat = models.FloatField(default=0)

    mythic_stat_magic_pen_percentage = models.FloatField(default=0)
    mythic_stat_magic_pen_flat = models.FloatField(default=0)

    mythic_stat_ability_power = models.FloatField(default=0)
    mythic_stat_ability_haste = models.FloatField(default=0)

    mythic_stat_movement_speed_percentage = models.FloatField(default=0)
    mythic_stat_movement_speed_flat = models.FloatField(default=0)

    mythic_stat_tenacity = models.FloatField(default=0)
    mythic_stat_slow_resistance = models.FloatField(default=0)
    mythic_stat_size = models.FloatField(default=0)
    mythic_stat_empower_item_passive = models.FloatField(default=0)
    mythic_stat_omnivamp = models.FloatField(default=0)

    gold_cost = models.IntegerField(default=0)


class Abilities(models.Model):
    id = models.IntegerField(primary_key=True)
    ability_name = models.CharField(max_length=200)


class Runes(models.Model):
    id = models.IntegerField(primary_key=True)
    rune_name = models.CharField(max_length=200)


class UserInput(models.Model):
    champion_index = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    item1_index = models.IntegerField(default=0)
    item2_index = models.IntegerField(default=0)
    item3_index = models.IntegerField(default=0)
    item4_index = models.IntegerField(default=0)
    item5_index = models.IntegerField(default=0)
    item6_index = models.IntegerField(default=0)
    ability_q_level_index = models.IntegerField(default=0)
    ability_w_level_index = models.IntegerField(default=0)
    ability_e_level_index = models.IntegerField(default=0)
    ability_r_level_index = models.IntegerField(default=0)
    rune_keystone_index = models.IntegerField(default=0)
    rune_primary1_index = models.IntegerField(default=0)
    rune_primary2_index = models.IntegerField(default=0)
    rune_primary3_index = models.IntegerField(default=0)
    rune_secondary1_index = models.IntegerField(default=0)
    rune_secondary2_index = models.IntegerField(default=0)

    ability1 = models.IntegerField(default=0)
    ability2 = models.IntegerField(default=0)
    ability3 = models.IntegerField(default=0)
    ability4 = models.IntegerField(default=0)
    ability5 = models.IntegerField(default=0)
    ability6 = models.IntegerField(default=0)
    ability7 = models.IntegerField(default=0)
    ability8 = models.IntegerField(default=0)
    ability9 = models.IntegerField(default=0)
    ability10 = models.IntegerField(default=0)
    ability11 = models.IntegerField(default=0)
    ability12 = models.IntegerField(default=0)
    ability13 = models.IntegerField(default=0)
    ability14 = models.IntegerField(default=0)
    ability15 = models.IntegerField(default=0)

    dummy_health_points = models.FloatField(default=0)
    dummy_armor = models.FloatField(default=0)
    dummy_magic_resistance = models.FloatField(default=0)


class DamageOutput(models.Model):
    physical_damage_dealt = models.FloatField(default=0)
    magical_damage_dealt = models.FloatField(default=0)
    true_damage_dealt = models.FloatField(default=0)
    dummy_hp = models.FloatField(default=0)
    dummy_armor = models.FloatField(default=0)
    dummy_mr = models.FloatField(default=0)

    ability1 = models.FloatField(default=0)
    ability2 = models.FloatField(default=0)
    ability3 = models.FloatField(default=0)
    ability4 = models.FloatField(default=0)
    ability5 = models.FloatField(default=0)
    ability6 = models.FloatField(default=0)
    ability7 = models.FloatField(default=0)
    ability8 = models.FloatField(default=0)
    ability9 = models.FloatField(default=0)
    ability10 = models.FloatField(default=0)
    ability11 = models.FloatField(default=0)
    ability12 = models.FloatField(default=0)
    ability13 = models.FloatField(default=0)
    ability14 = models.FloatField(default=0)
    ability15 = models.FloatField(default=0)
