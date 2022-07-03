from django.http import HttpResponse
from django.shortcuts import render
from .models import Champion, UserInput, Items, CalculatedStatsWithLevel, FinalChampionStatsWithLevelItemsRunes, DamageOutput


# Create your views here.


def dmgcalc_function(request):
    if request.method == 'POST':
        UserInput.objects.create(champion_index=request.POST['chosenChampion'],
                                 level=request.POST['chosenLevel'],
                                 item1_index=request.POST['chosenItem1'],
                                 item2_index=request.POST['chosenItem2'],
                                 item3_index=request.POST['chosenItem3'],
                                 item4_index=request.POST['chosenItem4'],
                                 item5_index=request.POST['chosenItem5'],
                                 item6_index=request.POST['chosenItem6'],
                                 ability_q_level_index=request.POST['chosenAbility1Level'],
                                 ability_w_level_index=request.POST['chosenAbility2Level'],
                                 ability_e_level_index=request.POST['chosenAbility3Level'],
                                 ability_r_level_index=request.POST['chosenAbility4Level'],
                                 rune_keystone_index=request.POST['chosenRuneKeystone'],
                                 rune_primary1_index=request.POST['chosenRunePrimary1'],
                                 rune_primary2_index=request.POST['chosenRunePrimary2'],
                                 rune_primary3_index=request.POST['chosenRunePrimary3'],
                                 rune_secondary1_index=request.POST['chosenRuneSecondary1'],
                                 rune_secondary2_index=request.POST['chosenRuneSecondary2'],
                                 ability1=request.POST['chosenAbility1'],
                                 ability2=request.POST['chosenAbility2'],
                                 ability3=request.POST['chosenAbility3'],
                                 ability4=request.POST['chosenAbility4'],
                                 ability5=request.POST['chosenAbility5'],
                                 ability6=request.POST['chosenAbility6'],
                                 ability7=request.POST['chosenAbility7'],
                                 ability8=request.POST['chosenAbility8'],
                                 ability9=request.POST['chosenAbility9'],
                                 ability10=request.POST['chosenAbility10'],
                                 ability11=request.POST['chosenAbility11'],
                                 ability12=request.POST['chosenAbility12'],
                                 ability13=request.POST['chosenAbility13'],
                                 ability14=request.POST['chosenAbility14'],
                                 ability15=request.POST['chosenAbility15'],
                                 dummy_health_points=request.POST['chosenDummyHP'],
                                 dummy_armor=request.POST['chosenDummyArmor'],
                                 dummy_magic_resistance=request.POST['chosenDummyMR'])
        CalculatedStatsWithLevel.objects.all().delete()
        calculation_of_stats_with_level_user_input_based_on_base_stats()
        FinalChampionStatsWithLevelItemsRunes.objects.all().delete()
        calculation_of_stats_with_user_input_based_on_items_and_level_stats()
        DamageOutput.objects.all().delete()
        calculation_of_damage()

    all_champions = Champion.objects.all()
    all_items = Items.objects.all()

    # UserInput.objects.last().delete()
    all_damage = DamageOutput.objects.all()
    all_stats = FinalChampionStatsWithLevelItemsRunes.objects.all()
    print(all_stats)
    return render(request, 'index.html', {'all_champions': all_champions, 'all_items': all_items, 'all_stats': all_stats, 'all_damage': all_damage})


def calculation_of_stats_with_level_user_input_based_on_base_stats():
    champion_level = UserInput.objects.values('level').last().get('level')
    champion_id = UserInput.objects.values('champion_index').last().get('champion_index')
    current_champion_dict = Champion.objects.filter(id=champion_id + 1).values().first()

    champion_name = current_champion_dict.get('champion_name')

    champion_health_points = standard_stats_calculation_based_on_level(current_champion_dict.get('base_health_points'),
                                                                       current_champion_dict.get('health_points_per_level'),
                                                                       champion_level)
    champion_health_regen = standard_stats_calculation_based_on_level(current_champion_dict.get('base_health_regen'),
                                                                      current_champion_dict.get('health_regen_per_level'),
                                                                      champion_level)
    champion_mana = standard_stats_calculation_based_on_level(current_champion_dict.get('base_mana'),
                                                              current_champion_dict.get('mana_per_level'),
                                                              champion_level)
    champion_mana_regen = standard_stats_calculation_based_on_level(current_champion_dict.get('base_mana_regen'),
                                                                    current_champion_dict.get('mana_regen_per_level'),
                                                                    champion_level)
    champion_armor = standard_stats_calculation_based_on_level(current_champion_dict.get('base_armor'),
                                                               current_champion_dict.get('armor_per_level'),
                                                               champion_level)
    champion_magic_resistance = standard_stats_calculation_based_on_level(current_champion_dict.get('base_magic_resistance'),
                                                                          current_champion_dict.get('magic_resistance_per_level'),
                                                                          champion_level)
    champion_attack_damage = standard_stats_calculation_based_on_level(current_champion_dict.get('base_attack_damage'),
                                                                       current_champion_dict.get('attack_damage_per_level'),
                                                                       champion_level)
    champion_crit_damage = current_champion_dict.get('base_crit_damage')
    champion_bonus_attack_speed = standard_stats_calculation_based_on_level_attack_speed(0,
                                                                                         current_champion_dict.get('attack_speed_bonus'),
                                                                                         champion_level)
    # print(
    #   f'''{champion_id} {champion_name} {champion_health_points} {champion_health_regen}
    #      {champion_mana} {champion_mana_regen} {champion_armor} {champion_magic_resistance}
    #     {champion_attack_damage} {champion_crit_damage}''')

    CalculatedStatsWithLevel.objects.create(level=champion_level, champion_name=champion_name, calc_health_points=champion_health_points,
                                            calc_health_points_regen=champion_health_regen, calc_mana=champion_mana,
                                            calc_mana_regen=champion_mana_regen, calc_armor=champion_armor,
                                            calc_magic_resistance=champion_magic_resistance, calc_attack_damage=champion_attack_damage,
                                            calc_crit_damage=champion_crit_damage, calc_bonus_attack_speed=champion_bonus_attack_speed)


user_input_dict = {}
champion_stats_based_on_level_dict = {}
champion_name = ""
champion_level = 0
item_name_one = item_name_two = item_name_three = item_name_four = item_name_five = item_name_six = ""
ability_q_level = ability_w_level = ability_e_level = ability_r_level = champion_base_hp = bonus_champion_hp = champion_hp = champion_base_hp_regen \
    = champion_hp_regen = champion_base_mana = bonus_champion_mana = champion_mana = champion_base_mana_regen = champion_mana_regen \
    = champion_base_armor = bonus_champion_armor = champion_armor = champion_base_mr = bonus_champion_mr = champion_mr = champion_base_attack_damage \
    = bonus_champion_attack_damage = champion_attack_damage = champion_base_attack_speed = champion_attack_speed_ratio = champion_bonus_attack_speed \
    = champion_attack_speed = champion_crit_damage = champion_crit_chance = champion_armor_pen_percentage = champion_armor_pen_flat \
    = champion_ability_power = champion_ability_haste = champion_magic_pen_percentage = champion_magic_pen_flat = champion_movement_speed \
    = champion_attack_speed_windup = champion_life_steal = champion_physical_vamp = champion_omnivamp = champion_gold_generation \
    = champion_heal_and_shield_power = champion_tenacity = champion_slow_resistance = chosen_item = 0
has_mythic = has_steraks_gage = has_rabadons_deathcap = has_demonic_embrace = has_titanic_hydra = False

dummy_hp = dummy_armor = dummy_mr = 0


def calculation_of_stats_with_user_input_based_on_items_and_level_stats():
    global user_input_dict, champion_stats_based_on_level_dict, champion_name, champion_level, item_name_one, item_name_two, item_name_three, \
        item_name_four, item_name_five, item_name_six, ability_q_level, ability_w_level, ability_e_level, ability_r_level, champion_base_hp, \
        bonus_champion_hp, champion_hp, champion_base_hp_regen, champion_hp_regen, champion_base_mana, bonus_champion_mana, champion_mana, \
        champion_base_mana_regen, champion_mana_regen, champion_base_armor, bonus_champion_armor, champion_armor, champion_base_mr, \
        bonus_champion_mr, champion_mr, champion_base_attack_damage, bonus_champion_attack_damage, champion_attack_damage, \
        champion_base_attack_speed, champion_attack_speed_ratio, champion_bonus_attack_speed, champion_attack_speed, champion_crit_damage, \
        champion_crit_chance, champion_armor_pen_percentage, champion_armor_pen_flat, champion_ability_power, champion_ability_haste, \
        champion_magic_pen_percentage, champion_magic_pen_flat, champion_movement_speed, champion_attack_speed_windup, champion_life_steal, \
        champion_physical_vamp, champion_omnivamp, champion_gold_generation, champion_heal_and_shield_power, champion_tenacity, \
        champion_slow_resistance, chosen_item, has_mythic, has_steraks_gage, has_rabadons_deathcap, has_demonic_embrace, has_titanic_hydra

    user_input_id = UserInput.objects.values('id').last().get('id')
    user_input_dict = UserInput.objects.filter(id=user_input_id).values().first()
    champion_stats_based_on_level_id = CalculatedStatsWithLevel.objects.values('id').last().get('id')
    champion_stats_based_on_level_dict = CalculatedStatsWithLevel.objects.filter(id=champion_stats_based_on_level_id).values().first()

    champion_name = champion_stats_based_on_level_dict.get('champion_name')
    champion_level = champion_stats_based_on_level_dict.get('level')

    # item_name_one = ""
    # item_name_two = ""
    # item_name_three = ""
    # item_name_four = ""
    # item_name_five = ""
    # item_name_six = ""

    ability_q_level = user_input_dict.get('ability_q_level_index')
    ability_w_level = user_input_dict.get('ability_w_level_index')
    ability_e_level = user_input_dict.get('ability_e_level_index')
    ability_r_level = user_input_dict.get('ability_r_level_index')

    # RUNES MISSING HERE!!!!!!!!!!!!!!!

    champion_base_hp = champion_stats_based_on_level_dict.get('calc_health_points')
    bonus_champion_hp = 0
    champion_hp = 0
    champion_base_hp_regen = champion_stats_based_on_level_dict.get('calc_health_points_regen')
    champion_hp_regen = champion_base_hp_regen

    champion_base_mana = champion_stats_based_on_level_dict.get('calc_mana')
    bonus_champion_mana = 0
    champion_mana = 0
    champion_base_mana_regen = champion_stats_based_on_level_dict.get('calc_mana_regen')
    champion_mana_regen = champion_base_mana_regen

    champion_base_armor = champion_stats_based_on_level_dict.get('calc_armor')
    bonus_champion_armor = 0
    champion_armor = 0
    champion_base_mr = champion_stats_based_on_level_dict.get('calc_magic_resistance')
    bonus_champion_mr = 0
    champion_mr = 0

    champion_base_attack_damage = champion_stats_based_on_level_dict.get('calc_attack_damage')
    bonus_champion_attack_damage = 0
    champion_attack_damage = 0
    champion_base_attack_speed = Champion.objects.filter(id=user_input_dict.get('champion_index') + 1).values().first().get('base_attack_speed')
    champion_attack_speed_ratio = Champion.objects.filter(id=user_input_dict.get('champion_index') + 1).values().first().get('attack_speed_ratio')
    champion_bonus_attack_speed = champion_stats_based_on_level_dict.get('calc_bonus_attack_speed')
    champion_attack_speed = 0

    champion_crit_damage = champion_stats_based_on_level_dict.get('calc_crit_damage')
    champion_crit_chance = 0
    champion_armor_pen_percentage = 0
    champion_armor_pen_flat = 0

    champion_ability_power = 0
    champion_ability_haste = 0
    champion_magic_pen_percentage = 0
    champion_magic_pen_flat = 0

    # champion_movement_speed not needed right now not doing anything
    champion_movement_speed = Champion.objects.filter(id=user_input_dict.get('champion_index') + 1).values().first().get('base_movement_speed')  #

    # champion_attack_speed_windup not needed right now not doing anything
    champion_attack_speed_windup = Champion.objects.filter(id=user_input_dict.get('champion_index') + 1).values().first().get('attack_speed_windup')

    champion_life_steal = 0
    champion_physical_vamp = 0
    champion_omnivamp = 0
    champion_gold_generation = 20.4
    champion_heal_and_shield_power = 0
    champion_tenacity = 0
    champion_slow_resistance = 0

    #

    mythic_armor_pen_perc = 0
    mythic_magic_pen_perc = 0
    mythic_tenacity = 0
    mythic_slow_resist = 0

    chosen_item = None
    has_mythic = False
    has_steraks_gage = False
    has_rabadons_deathcap = False
    has_demonic_embrace = False
    has_titanic_hydra = False

    number_of_legendary = 0

    for i in range(1, 7):
        if i == 1:
            chosen_item = Items.objects.filter(id=user_input_dict.get('item1_index') + 1).values().first()
            item_name_one = chosen_item.get('item_name')
        elif i == 2:
            chosen_item = Items.objects.filter(id=user_input_dict.get('item2_index') + 1).values().first()
            item_name_two = chosen_item.get('item_name')
        elif i == 3:
            chosen_item = Items.objects.filter(id=user_input_dict.get('item3_index') + 1).values().first()
            item_name_three = chosen_item.get('item_name')
        elif i == 4:
            chosen_item = Items.objects.filter(id=user_input_dict.get('item4_index') + 1).values().first()
            item_name_four = chosen_item.get('item_name')
        elif i == 5:
            chosen_item = Items.objects.filter(id=user_input_dict.get('item5_index') + 1).values().first()
            item_name_five = chosen_item.get('item_name')
        elif i == 6:
            chosen_item = Items.objects.filter(id=user_input_dict.get('item6_index') + 1).values().first()
            item_name_six = chosen_item.get('item_name')

        if chosen_item and chosen_item.get('id') != 1:
            item_name = chosen_item.get('item_name')
            item_id = chosen_item.get('id')
            print(item_name)
            item_type = chosen_item.get('type_of_item')
            if item_type == 8:
                number_of_legendary += 1
            if item_type == 9:
                has_mythic = True
            if item_id == 161:
                has_steraks_gage = True
            if item_id == 189:
                has_rabadons_deathcap = True
            if item_id == 177:
                has_titanic_hydra = True
            if item_id == 156:
                has_demonic_embrace = True

            # item_gold_cost not need right now or necessary
            item_gold_cost = chosen_item.get('gold_cost')

            item_hp = chosen_item.get('item_stat_hp')
            bonus_champion_hp += item_hp
            item_hp_regen = chosen_item.get('item_stat_hp_regen')
            if item_hp_regen > 0:
                champion_hp_regen += champion_base_hp_regen * item_hp_regen

            item_mana = chosen_item.get('item_stat_mana')
            bonus_champion_mana += item_mana
            item_mana_regen = chosen_item.get('item_stat_mana_regen')
            if item_mana_regen > 0:
                champion_mana_regen += champion_base_mana_regen * item_mana_regen

            item_armor = chosen_item.get('item_stat_armor')
            bonus_champion_armor += item_armor
            item_mr = chosen_item.get('item_stat_mr')
            bonus_champion_mr += item_mr

            item_attack_damage = chosen_item.get('item_stat_attack_damage')
            bonus_champion_attack_damage += item_attack_damage
            item_attack_speed = chosen_item.get('item_stat_attack_speed')
            champion_bonus_attack_speed += item_attack_speed

            item_crit_damage = chosen_item.get('item_stat_crit_damage')
            champion_crit_damage = item_crit_damage
            item_crit_chance = chosen_item.get('item_stat_crit_chance')
            champion_crit_chance += item_crit_chance

            item_armor_pen_percentage = chosen_item.get('item_stat_armor_pen_percentage')
            item_armor_pen_percentage = round(1 - item_armor_pen_percentage, 4)
            if champion_armor_pen_percentage == 0:
                champion_armor_pen_percentage = item_armor_pen_percentage
            else:
                champion_armor_pen_percentage *= item_armor_pen_percentage

            item_armor_pen_flat = chosen_item.get('item_stat_armor_pen_flat')
            champion_armor_pen_flat += item_armor_pen_flat

            item_ability_power = chosen_item.get('item_stat_ability_power')
            champion_ability_power += item_ability_power
            item_ability_haste = chosen_item.get('item_stat_ability_haste')
            champion_ability_haste += item_ability_haste

            item_magic_pen_percentage = chosen_item.get('item_stat_magic_pen_percentage')
            item_magic_pen_percentage = round(1 - item_magic_pen_percentage, 4)
            if champion_magic_pen_percentage == 0:
                champion_magic_pen_percentage = item_magic_pen_percentage
            else:
                champion_magic_pen_percentage *= item_magic_pen_percentage

            item_magic_pen_flat = chosen_item.get('item_stat_magic_pen_flat')
            champion_magic_pen_flat += item_magic_pen_flat

            # item_movement_speed_percentage, item_movement_speed_flat not implemented yet, also not needed as of right now
            item_movement_speed_percentage = chosen_item.get('item_stat_movement_speed_percentage')
            item_movement_speed_flat = chosen_item.get('item_stat_movement_speed_flat')
            item_tenacity = chosen_item.get('item_stat_tenacity')
            item_tenacity = round(1 - item_tenacity, 4)
            if champion_tenacity == 0:
                champion_tenacity = item_tenacity
            else:
                champion_tenacity *= item_tenacity
            item_slow_resistance = chosen_item.get('item_stat_slow_resistance')
            item_slow_resistance = round(1 - item_slow_resistance, 4)
            if champion_slow_resistance == 0:
                champion_slow_resistance = item_slow_resistance
            else:
                champion_slow_resistance *= item_slow_resistance

            item_heal_and_shield_power = chosen_item.get('item_stat_heal_and_shield_power')
            champion_heal_and_shield_power += item_heal_and_shield_power
            item_life_steal = chosen_item.get('item_stat_life_steal')
            champion_life_steal += item_life_steal
            item_physical_vamp = chosen_item.get('item_stat_physical_vamp')
            champion_physical_vamp += item_physical_vamp
            item_omnivamp = chosen_item.get('item_stat_omnivamp')
            champion_omnivamp += item_omnivamp

            item_gold_generation = chosen_item.get('item_stat_gold_generation')
            champion_gold_generation += item_gold_generation
            # item_grievous_wounds not needed right now still needs to be implemented
            item_grievous_wounds = chosen_item.get('item_stat_grievous_wounds')

    if has_mythic:
        for i in range(1, 7):
            if i == 1:
                chosen_item = Items.objects.filter(id=user_input_dict.get('item1_index') + 1).values().first()
            elif i == 2:
                chosen_item = Items.objects.filter(id=user_input_dict.get('item2_index') + 1).values().first()
            elif i == 3:
                chosen_item = Items.objects.filter(id=user_input_dict.get('item3_index') + 1).values().first()
            elif i == 4:
                chosen_item = Items.objects.filter(id=user_input_dict.get('item4_index') + 1).values().first()
            elif i == 5:
                chosen_item = Items.objects.filter(id=user_input_dict.get('item5_index') + 1).values().first()
            elif i == 6:
                chosen_item = Items.objects.filter(id=user_input_dict.get('item6_index') + 1).values().first()

            item_type = chosen_item.get('type_of_item')

            if chosen_item and chosen_item.get('id') != 1 and item_type == 9:
                for i in range(0, number_of_legendary):
                    item_mythic_hp = chosen_item.get('mythic_stat_hp')
                    bonus_champion_hp += item_mythic_hp
                    item_mythic_armor = chosen_item.get('mythic_stat_armor')
                    bonus_champion_armor += item_mythic_armor
                    item_mythic_mr = chosen_item.get('mythic_stat_mr')
                    bonus_champion_mr += item_mythic_mr

                    item_mythic_attack_damage = chosen_item.get('mythic_stat_attack_damage')
                    bonus_champion_attack_damage += item_mythic_attack_damage
                    item_mythic_attack_speed = chosen_item.get('mythic_stat_attack_speed')
                    champion_bonus_attack_speed += item_mythic_attack_speed
                    item_mythic_armor_pen_percentage = chosen_item.get('mythic_stat_armor_pen_percentage')
                    if mythic_armor_pen_perc == 0:
                        mythic_armor_pen_perc = item_mythic_armor_pen_percentage
                    else:
                        mythic_armor_pen_perc += item_mythic_armor_pen_percentage
                    item_mythic_armor_pen_flat = chosen_item.get('mythic_stat_armor_pen_flat')
                    champion_armor_pen_flat += item_mythic_armor_pen_flat

                    item_mythic_ability_power = chosen_item.get('mythic_stat_ability_power')
                    champion_ability_power += item_mythic_ability_power
                    item_mythic_ability_haste = chosen_item.get('mythic_stat_ability_haste')
                    champion_ability_haste += item_mythic_ability_haste
                    item_mythic_magic_pen_percentage = chosen_item.get('mythic_stat_magic_pen_percentage')
                    if mythic_magic_pen_perc == 0:
                        mythic_magic_pen_perc = item_mythic_magic_pen_percentage
                    else:
                        mythic_magic_pen_perc += item_mythic_magic_pen_percentage
                    item_mythic_magic_pen_flat = chosen_item.get('mythic_stat_magic_pen_flat')
                    champion_magic_pen_flat += item_mythic_magic_pen_flat

                    # item_mythic_movement_speed_percentage, item_mythic_movement_speed_flat not implemented yet, also not needed as of right now
                    item_mythic_movement_speed_percentage = chosen_item.get('mythic_stat_movement_speed_percentage')
                    item_mythic_movement_speed_flat = chosen_item.get('mythic_stat_movement_speed_flat')
                    item_mythic_tenacity = chosen_item.get('mythic_stat_tenacity')
                    if mythic_tenacity == 0:
                        mythic_tenacity = item_mythic_tenacity
                    else:
                        mythic_tenacity += item_mythic_tenacity
                    item_mythic_slow_resistance = chosen_item.get('mythic_stat_slow_resistance')
                    if mythic_slow_resist == 0:
                        mythic_slow_resist = item_mythic_slow_resistance
                    else:
                        mythic_slow_resist += item_mythic_slow_resistance

                    item_mythic_omnivamp = chosen_item.get('mythic_stat_omnivamp')
                    champion_omnivamp += item_mythic_omnivamp

                    # item_mythic_size, item_mythic_empower_item_passive not necessary right now but nothing happens
                    item_mythic_size = chosen_item.get('mythic_stat_size')
                    item_mythic_empower_item_passive = chosen_item.get('mythic_stat_empower_item_passive')
    if has_steraks_gage:
        bonus_champion_attack_damage += round(0.45 * champion_base_attack_damage, 2)
    if has_titanic_hydra:
        bonus_champion_attack_damage += 0.02 * bonus_champion_hp
    if has_demonic_embrace:
        champion_ability_power += 0.02 * bonus_champion_hp
    if has_rabadons_deathcap:
        champion_ability_power *= 1.35
    # DARK SEAL/MEJAI'S TECHNICALLY BUT NOT WORKING ANYWAYS
    champion_hp += bonus_champion_hp
    champion_hp += champion_base_hp

    champion_mana += bonus_champion_mana
    champion_mana += champion_base_mana

    champion_armor += bonus_champion_armor
    champion_armor += champion_base_armor

    champion_mr += bonus_champion_mr
    champion_mr += champion_base_mr

    champion_attack_damage += bonus_champion_attack_damage
    champion_attack_damage += champion_base_attack_damage

    mythic_armor_pen_perc = round(1 - mythic_armor_pen_perc, 4)
    champion_armor_pen_percentage *= mythic_armor_pen_perc
    champion_armor_pen_percentage = round(1 - champion_armor_pen_percentage, 4)

    mythic_magic_pen_perc = round(1 - mythic_magic_pen_perc, 4)
    champion_magic_pen_percentage *= mythic_magic_pen_perc
    champion_magic_pen_percentage = round(1 - champion_magic_pen_percentage, 4)

    mythic_tenacity = round(1 - mythic_tenacity, 4)
    champion_tenacity *= mythic_tenacity
    champion_tenacity = round(1 - champion_tenacity, 4)

    mythic_slow_resist = round(1 - mythic_slow_resist, 4)
    champion_slow_resistance *= mythic_slow_resist
    champion_slow_resistance = 1 - champion_slow_resistance

    champion_crit_chance = round(champion_crit_chance, 4)
    champion_attack_speed = attack_speed_calculation(champion_base_attack_speed, champion_attack_speed_ratio,
                                                     champion_bonus_attack_speed)

    FinalChampionStatsWithLevelItemsRunes.objects.create(health_points=champion_hp, base_health_points=champion_base_hp,
                                                         bonus_health_points=bonus_champion_hp, health_points_regen=champion_hp_regen,
                                                         mana=champion_mana, base_mana=champion_base_mana, bonus_mana=bonus_champion_mana,
                                                         mana_regen=champion_mana_regen, armor=champion_armor, base_armor=champion_base_armor,
                                                         bonus_armor=bonus_champion_armor, magic_resistance=champion_mr,
                                                         base_magic_resistance=champion_base_mr, bonus_magic_resistance=bonus_champion_mr,
                                                         attack_damage=champion_attack_damage, base_attack_damage=champion_base_attack_damage,
                                                         bonus_attack_damage=bonus_champion_attack_damage, crit_damage=champion_crit_damage,
                                                         crit_chance=champion_crit_chance, armor_pen_percentage=champion_armor_pen_percentage,
                                                         armor_pen_flat=champion_armor_pen_flat, ability_power=champion_ability_power,
                                                         ability_haste=champion_ability_haste, magic_pen_percentage=champion_magic_pen_percentage,
                                                         magic_pen_flat=champion_magic_pen_flat, movement_speed=champion_movement_speed,
                                                         attack_speed=champion_attack_speed, attack_speed_windup=champion_attack_speed_windup,
                                                         tenacity=champion_tenacity, life_steal=champion_life_steal,
                                                         physical_vamp=champion_physical_vamp, omnivamp=champion_omnivamp,
                                                         gold_generation=champion_gold_generation,
                                                         heal_and_shield_power=champion_heal_and_shield_power,
                                                         slow_resistance=champion_slow_resistance, champion_name=champion_name,
                                                         champion_level=champion_level, item_name_one=item_name_one, item_name_two=item_name_two,
                                                         item_name_three=item_name_three, item_name_four=item_name_four,
                                                         item_name_five=item_name_five,
                                                         item_name_six=item_name_six, ability_q_level=ability_q_level,
                                                         ability_w_level=ability_w_level, ability_e_level=ability_e_level,
                                                         ability_r_level=ability_r_level)


seraphine_note_counter = 0
dummy_current_hp = 0


def calculate_damage_based_on_mr_and_armor(damage, mr, armor):
    damage_dealt = [0, '']
    physical_damage_multiplier = 100 / (100 + armor)
    magic_damage_multiplier = 100 / (100 + mr)

    if damage[1] == 'physical':
        damage_dealt[0] = damage[0] * physical_damage_multiplier
        damage_dealt[1] = 'physical'

    if damage[1] == 'magic':
        damage_dealt[0] = damage[0] * magic_damage_multiplier
        damage_dealt[1] = 'magic'

    return damage_dealt


def calculation_of_damage():
    global dummy_hp, dummy_armor, dummy_mr, dummy_current_hp
    dummy_hp = user_input_dict.get('dummy_health_points')
    dummy_armor = user_input_dict.get('dummy_armor')
    dummy_mr = user_input_dict.get('dummy_magic_resistance')

    physical_damage = 0
    magic_damage = 0
    true_damage = 0

    abilities = [user_input_dict.get('ability1'), user_input_dict.get('ability2'), user_input_dict.get('ability3'), user_input_dict.get('ability4'),
                 user_input_dict.get('ability5'), user_input_dict.get('ability6'), user_input_dict.get('ability7'), user_input_dict.get('ability8'),
                 user_input_dict.get('ability9'), user_input_dict.get('ability10'), user_input_dict.get('ability11'),
                 user_input_dict.get('ability12'), user_input_dict.get('ability13'), user_input_dict.get('ability14'),
                 user_input_dict.get('ability14'), user_input_dict.get('ability15')]

    abilities_damage_dealt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    print(abilities)

    dummy_current_hp = dummy_hp
    for x in range(0, 15):
        if abilities[x] > -1:
            if abilities[x] == 0:
                auto_attack_damage = calculate_damage_based_on_mr_and_armor(seraphine_auto_dmg(champion_attack_damage), dummy_mr, dummy_armor)
                dummy_current_hp -= auto_attack_damage[0]
                if auto_attack_damage[1] == 'physical':
                    physical_damage += auto_attack_damage[0]
                if auto_attack_damage[1] == 'magic':
                    magic_damage += auto_attack_damage[0]
                abilities_damage_dealt[x] = round(auto_attack_damage[0], 2)
            elif abilities[x] == 1:
                passive_damage = calculate_damage_based_on_mr_and_armor(seraphine_passive_dmg(champion_ability_power, champion_level), dummy_mr,
                                                                        dummy_armor)
                dummy_current_hp -= passive_damage[0]
                if passive_damage[1] == 'physical':
                    physical_damage += passive_damage[0]
                if passive_damage[1] == 'magic':
                    magic_damage += passive_damage[0]
                abilities_damage_dealt[x] = round(passive_damage[0], 2)
            elif abilities[x] == 2:
                q_damage = calculate_damage_based_on_mr_and_armor(
                    seraphine_q_dmg(champion_ability_power, ability_q_level, dummy_current_hp, dummy_hp),
                    dummy_mr,
                    dummy_armor)
                dummy_current_hp -= q_damage[0]
                if q_damage[1] == 'physical':
                    physical_damage += q_damage[0]
                if q_damage[1] == 'magic':
                    magic_damage += q_damage[0]
                abilities_damage_dealt[x] = round(q_damage[0], 2)
            elif abilities[x] == 3:
                w_damage = 0
                dummy_current_hp -= w_damage
                physical_damage += w_damage
                magic_damage += w_damage
                abilities_damage_dealt[x] = w_damage
            elif abilities[x] == 4:
                e_damage = calculate_damage_based_on_mr_and_armor(seraphine_e_dmg(champion_ability_power, ability_e_level),
                                                                  dummy_mr,
                                                                  dummy_armor)
                dummy_current_hp -= e_damage[0]
                if e_damage[1] == 'physical':
                    physical_damage += e_damage[0]
                if e_damage[1] == 'magic':
                    magic_damage += e_damage[0]
                abilities_damage_dealt[x] = round(e_damage[0], 2)
            elif abilities[x] == 5:
                r_damage = calculate_damage_based_on_mr_and_armor(seraphine_r_dmg(champion_ability_power, ability_r_level),
                                                                  dummy_mr,
                                                                  dummy_armor)
                dummy_current_hp -= r_damage[0]
                if r_damage[1] == 'physical':
                    physical_damage += r_damage[0]
                if r_damage[1] == 'magic':
                    magic_damage += r_damage[0]
                abilities_damage_dealt[x] = round(r_damage[0], 2)
            elif abilities[x] == 6:
                pass
            elif abilities[x] == 7:
                pass
            elif abilities[x] == 8:
                pass
            elif abilities[x] == 9:
                pass
            elif abilities[x] == 10:
                pass
            elif abilities[x] == 11:
                pass

    print(abilities_damage_dealt)

    physical_damage = round(physical_damage, 2)
    magic_damage = round(magic_damage, 2)
    true_damage = round(true_damage, 2)

    DamageOutput.objects.create(dummy_hp=dummy_hp, dummy_armor=dummy_armor, dummy_mr=dummy_mr, physical_damage_dealt=physical_damage,
                                magical_damage_dealt=magic_damage, true_damage_dealt=true_damage, ability1=abilities_damage_dealt[0],
                                ability2=abilities_damage_dealt[1], ability3=abilities_damage_dealt[2], ability4=abilities_damage_dealt[3],
                                ability5=abilities_damage_dealt[4], ability6=abilities_damage_dealt[5], ability7=abilities_damage_dealt[6],
                                ability8=abilities_damage_dealt[7], ability9=abilities_damage_dealt[8], ability10=abilities_damage_dealt[9],
                                ability11=abilities_damage_dealt[10], ability12=abilities_damage_dealt[11], ability13=abilities_damage_dealt[12],
                                ability14=abilities_damage_dealt[13], ability15=abilities_damage_dealt[14])


def seraphine_auto_dmg(ad):
    return [ad, 'physical']


def seraphine_passive_dmg(ap, level):
    global seraphine_note_counter
    damage = 0
    if seraphine_note_counter > 4:
        seraphine_note_counter = 4
    if level < 6:
        # level 1-5 4 dmg
        damage = (4 + ap * 0.07) * seraphine_note_counter
        pass
    elif level < 11:
        # level 5-10 8 dmg
        damage = (8 + ap * 0.07) * seraphine_note_counter
        pass
    elif level < 16:
        # level 11-15 14 dmg
        damage = (14 + ap * 0.07) * seraphine_note_counter
        pass
    elif level < 19:
        # level 16-18 24 dmg
        damage = (24 + ap * 0.07) * seraphine_note_counter
        pass
    seraphine_note_counter = 0
    return [damage, 'magic']


def seraphine_q_dmg(ap, skill_level, current_hp, hp):
    global seraphine_note_counter
    damage_amplifier = 0
    damage = 0
    seraphine_note_counter += 1

    # if skill_level == 0:
    #    damage = 0
    # elif skill_level == 1:
    #    damage = (55 + 0.45 * ap)
    # elif skill_level == 2:
    #    damage = (70 + 0.50 * ap)
    # elif skill_level == 3:
    #    damage = (85 + 0.55 * ap)
    # elif skill_level == 4:
    #    damage = (100 + 0.60 * ap)
    # elif skill_level == 5:
    #    damage = (115 + 0.65 * ap)

    # current_hp -= damage
    missing_health = round(hp - current_hp, 4)
    missing_health_perc = round(missing_health / hp, 6)
    print(damage, hp, current_hp, missing_health, missing_health_perc)
    x = 0.0003
    y = 0.0002
    for i in range(0, 2501):
        if missing_health_perc < 0.0003:
            damage_amplifier = 0
            break
        elif missing_health_perc > x and missing_health_perc < (x + 0.0003) or missing_health_perc == x:
            damage_amplifier = y
            break
        x = round(x + 0.0003, 5)
        y = round(y + 0.0002, 5)

    # if missing_health_perc < 0.075:
    #     damage_amplifier = 0
    # elif missing_health > 0.015 and missing_health_perc < 0.030:
    #     damage_amplifier = 0.01
    # elif missing_health > 0.030 and missing_health_perc < 0.045:
    #     damage_amplifier = 0.02
    # elif missing_health > 0.045 and missing_health_perc < 0.060:
    #     damage_amplifier = 0.03
    # elif missing_health > 0.060 and missing_health_perc < 0.075:
    #     damage_amplifier = 0.04
    # elif missing_health > 0.075 and missing_health_perc < 0.090:
    #     damage_amplifier = 0.05
    # elif missing_health > 0.090 and missing_health_perc < 0.105:
    #     damage_amplifier = 0.06
    # elif missing_health > 0.105 and missing_health_perc < 0.120:
    #     damage_amplifier = 0.07
    # elif missing_health > 0.120 and missing_health_perc < 0.135:
    #     damage_amplifier = 0.08
    # elif missing_health > 0.135 and missing_health_perc < 0.150:
    #     damage_amplifier = 0.09
    # elif missing_health > 0.150 and missing_health_perc < 0.165:
    #     damage_amplifier = 0.10
    # elif missing_health > 0.165 and missing_health_perc < 0.180:
    #     damage_amplifier = 0.1
    # elif missing_health > 0.180 and missing_health_perc < 0.195:
    #     damage_amplifier = 0.15
    # elif missing_health > 0.300 and missing_health_perc < 0.375:
    #     damage_amplifier = 0.20
    # elif missing_health > 0.375 and missing_health_perc < 0.450:
    #     damage_amplifier = 0.25
    # elif missing_health > 0.450 and missing_health_perc < 0.525:
    #     damage_amplifier = 0.30
    # elif missing_health > 0.525 and missing_health_perc < 0.600:
    #     damage_amplifier = 0.35
    # elif missing_health > 0.600 and missing_health_perc < 0.675:
    #     damage_amplifier = 0.40
    # elif missing_health > 0.675 and missing_health_perc < 0.750:
    #     damage_amplifier = 0.45
    # elif missing_health > 0.750:
    #     damage_amplifier = 0.50

    print(damage_amplifier)

    if skill_level == 0:
        damage = 0
    elif skill_level == 1:
        damage = (55 + 0.45 * ap) + ((55 + 0.45 * ap) * damage_amplifier)
    elif skill_level == 2:
        damage = (70 + 0.50 * ap) + ((70 + 0.50 * ap) * damage_amplifier)
    elif skill_level == 3:
        damage = (85 + 0.55 * ap) + ((85 + 0.55 * ap) * damage_amplifier)
    elif skill_level == 4:
        damage = (100 + 0.60 * ap) + ((100 + 0.60 * ap) * damage_amplifier)
    elif skill_level == 5:
        damage = (115 + 0.65 * ap) + ((115 + 0.65 * ap) * damage_amplifier)

    print(damage)
    return [damage, 'magic']


def seraphine_w_dmg():
    global seraphine_note_counter
    seraphine_note_counter += 1
    return 0


def seraphine_e_dmg(ap, skill_level):
    global seraphine_note_counter
    seraphine_note_counter += 1
    damage = 0
    if skill_level == 0:
        damage = 0
    elif skill_level == 1:
        damage = (60 + 0.35 * ap)
    elif skill_level == 2:
        damage = (80 + 0.35 * ap)
    elif skill_level == 3:
        damage = (100 + 0.35 * ap)
    elif skill_level == 4:
        damage = (120 + 0.35 * ap)
    elif skill_level == 5:
        damage = (140 + 0.35 * ap)

    return [damage, 'magic']


def seraphine_r_dmg(ap, skill_level):
    global seraphine_note_counter
    seraphine_note_counter += 1
    damage = 0
    if skill_level == 0:
        damage = 0
    elif skill_level == 1:
        damage = (150 + 0.60 * ap)
    elif skill_level == 2:
        damage = (200 + 0.60 * ap)
    elif skill_level == 3:
        damage = (250 + 0.60 * ap)

    return [damage, 'magic']


def standard_stats_calculation_based_on_level(base_stat, growth_stat, level):
    return round(base_stat + growth_stat * (level - 1) * (0.7025 + 0.0175 * (level - 1)), 2)


def standard_stats_calculation_based_on_level_attack_speed(base_stat, growth_stat, level):
    return round(base_stat + growth_stat * (level - 1) * (0.7025 + 0.0175 * (level - 1)), 4)


def attack_speed_calculation(base_attack_speed, ratio_attack_speed, bonus_attack_speed):
    return round(base_attack_speed + ratio_attack_speed * bonus_attack_speed, 2)
