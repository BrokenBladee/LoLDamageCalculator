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


def calculation_of_stats_with_user_input_based_on_items_and_level_stats():
    user_input_id = UserInput.objects.values('id').last().get('id')
    user_input_dict = UserInput.objects.filter(id=user_input_id).values().first()

    champion_stats_based_on_level_id = CalculatedStatsWithLevel.objects.values('id').last().get('id')
    champion_stats_based_on_level_dict = CalculatedStatsWithLevel.objects.filter(id=champion_stats_based_on_level_id).values().first()

    champion_name = champion_stats_based_on_level_dict.get('champion_name')
    champion_level = champion_stats_based_on_level_dict.get('level')

    item_name_one = ""
    item_name_two = ""
    item_name_three = ""
    item_name_four = ""
    item_name_five = ""
    item_name_six = ""

    ability_q_level = user_input_dict.get('ability_q_level_index')
    ability_w_level = user_input_dict.get('ability_w_level_index')
    ability_e_level = user_input_dict.get('ability_e_level_index')
    ability_r_level = user_input_dict.get('ability_r_level_index')

    # RUNES MISSING HERE!!!!!!!!!!!!!!!

    champion_hp = champion_stats_based_on_level_dict.get('calc_health_points')
    champion_base_hp_regen = champion_stats_based_on_level_dict.get('calc_health_points_regen')
    champion_hp_regen = champion_base_hp_regen

    champion_mana = champion_stats_based_on_level_dict.get('calc_mana')
    champion_base_mana_regen = champion_stats_based_on_level_dict.get('calc_mana_regen')
    champion_mana_regen = champion_base_mana_regen

    champion_armor = champion_stats_based_on_level_dict.get('calc_armor')
    champion_mr = champion_stats_based_on_level_dict.get('calc_magic_resistance')

    champion_attack_damage = champion_stats_based_on_level_dict.get('calc_attack_damage')
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
            champion_hp += item_hp
            item_hp_regen = chosen_item.get('item_stat_hp_regen')
            if item_hp_regen > 0:
                champion_hp_regen += champion_base_hp_regen * item_hp_regen

            item_mana = chosen_item.get('item_stat_mana')
            champion_mana += item_mana
            item_mana_regen = chosen_item.get('item_stat_mana_regen')
            if item_mana_regen > 0:
                champion_mana_regen += champion_base_mana_regen * item_mana_regen

            item_armor = chosen_item.get('item_stat_armor')
            champion_armor += item_armor
            item_mr = chosen_item.get('item_stat_mr')
            champion_mr += item_mr

            item_attack_damage = chosen_item.get('item_stat_attack_damage')
            champion_attack_damage += item_attack_damage
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
                    champion_hp += item_mythic_hp
                    item_mythic_armor = chosen_item.get('mythic_stat_armor')
                    champion_armor += item_mythic_armor
                    item_mythic_mr = chosen_item.get('mythic_stat_mr')
                    champion_mr += item_mythic_mr

                    item_mythic_attack_damage = chosen_item.get('mythic_stat_attack_damage')
                    champion_attack_damage += item_mythic_attack_damage
                    item_mythic_attack_speed = chosen_item.get('mythic_stat_attack_speed')
                    champion_bonus_attack_speed += item_mythic_attack_speed
                    item_mythic_armor_pen_percentage = chosen_item.get('mythic_stat_armor_pen_percentage')
                    item_mythic_armor_pen_percentage = round(1 - item_mythic_armor_pen_percentage, 4)
                    if champion_armor_pen_percentage == 0:
                        champion_armor_pen_percentage = item_mythic_armor_pen_percentage
                    else:
                        champion_armor_pen_percentage *= item_mythic_armor_pen_percentage
                    item_mythic_armor_pen_flat = chosen_item.get('mythic_stat_armor_pen_flat')
                    champion_armor_pen_flat += item_mythic_armor_pen_flat

                    item_mythic_ability_power = chosen_item.get('mythic_stat_ability_power')
                    champion_ability_power += item_mythic_ability_power
                    item_mythic_ability_haste = chosen_item.get('mythic_stat_ability_haste')
                    champion_ability_haste += item_mythic_ability_haste
                    item_mythic_magic_pen_percentage = chosen_item.get('mythic_stat_magic_pen_percentage')
                    item_mythic_magic_pen_percentage = round(1 - item_mythic_magic_pen_percentage, 4)
                    if champion_magic_pen_percentage == 0:
                        champion_magic_pen_percentage = item_mythic_magic_pen_percentage
                    else:
                        champion_magic_pen_percentage *= item_mythic_magic_pen_percentage
                    item_mythic_magic_pen_flat = chosen_item.get('mythic_stat_magic_pen_flat')
                    champion_magic_pen_flat += item_mythic_magic_pen_flat

                    # item_mythic_movement_speed_percentage, item_mythic_movement_speed_flat not implemented yet, also not needed as of right now
                    item_mythic_movement_speed_percentage = chosen_item.get('mythic_stat_movement_speed_percentage')
                    item_mythic_movement_speed_flat = chosen_item.get('mythic_stat_movement_speed_flat')
                    item_mythic_tenacity = chosen_item.get('mythic_stat_tenacity')
                    item_mythic_tenacity = round(1 - item_mythic_tenacity, 4)
                    if champion_tenacity == 0:
                        champion_tenacity = item_mythic_tenacity
                    else:
                        champion_tenacity *= item_mythic_tenacity
                    item_mythic_slow_resistance = chosen_item.get('mythic_stat_slow_resistance')
                    item_mythic_slow_resistance = round(1 - item_mythic_slow_resistance, 4)
                    if champion_slow_resistance == 0:
                        champion_slow_resistance = item_mythic_slow_resistance
                    else:
                        champion_slow_resistance *= item_mythic_slow_resistance

                    item_mythic_omnivamp = chosen_item.get('mythic_stat_omnivamp')
                    champion_omnivamp += item_mythic_omnivamp

                    # item_mythic_size, item_mythic_empower_item_passive not necessary right now but nothing happens
                    item_mythic_size = chosen_item.get('mythic_stat_size')
                    item_mythic_empower_item_passive = chosen_item.get('mythic_stat_empower_item_passive')
    champion_armor_pen_percentage = 1 - champion_armor_pen_percentage
    champion_magic_pen_percentage = 1 - champion_magic_pen_percentage
    champion_tenacity = 1 - champion_tenacity
    champion_slow_resistance = 1 - champion_slow_resistance
    champion_attack_speed = attack_speed_calculation(champion_base_attack_speed, champion_attack_speed_ratio,
                                                     champion_bonus_attack_speed)

    FinalChampionStatsWithLevelItemsRunes.objects.create(health_points=champion_hp, health_points_regen=champion_hp_regen, mana=champion_mana,
                                                         mana_regen=champion_mana_regen, armor=champion_armor, magic_resistance=champion_mr,
                                                         attack_damage=champion_attack_damage, crit_damage=champion_crit_damage,
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


def calculation_of_damage():
    user_input_id = UserInput.objects.values('id').last().get('id')
    user_input_dict = UserInput.objects.filter(id=user_input_id).values().first()

    dummy_hp = user_input_dict.get('dummy_health_points')
    dummy_armor = user_input_dict.get('dummy_armor')
    dummy_mr = user_input_dict.get('dummy_magic_resistance')

    physical_damage = 0
    magic_damage = 0
    true_damage = 0

    DamageOutput.objects.create(dummy_hp=dummy_hp, dummy_armor=dummy_armor, dummy_mr=dummy_mr, physical_damage_dealt=physical_damage,
                                magical_damage_dealt=magic_damage, true_damage_dealt=true_damage)


def standard_stats_calculation_based_on_level(base_stat, growth_stat, level):
    return round(base_stat + growth_stat * (level - 1) * (0.7025 + 0.0175 * (level - 1)), 2)


def standard_stats_calculation_based_on_level_attack_speed(base_stat, growth_stat, level):
    return round(base_stat + growth_stat * (level - 1) * (0.7025 + 0.0175 * (level - 1)), 4)


def attack_speed_calculation(base_attack_speed, ratio_attack_speed, bonus_attack_speed):
    return round(base_attack_speed + ratio_attack_speed * bonus_attack_speed, 2)
