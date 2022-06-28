from django.http import HttpResponse
from django.shortcuts import render
from .models import Champion, UserInput, Items, CalculatedStatsWithLevel


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
    all_champions = Champion.objects.all()
    all_items = Items.objects.all()
    # UserInput.objects.last().delete()
    # print(UserInput.objects.first())
    CalculatedStatsWithLevel.objects.all().delete()
    calculation_of_stats_with_level_user_input_based_on_base_stats()
    return render(request, 'index.html', {'all_champions': all_champions, 'all_items': all_items})


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
    champion_bonus_attack_speed = standard_stats_calculation_based_on_level(0,
                                                                            current_champion_dict.get('attack_speed_bonus'),
                                                                            champion_level)
    champion_attack_speed = attackspeed_calculation_based_on_level(current_champion_dict.get('base_attack_speed'),
                                                                   current_champion_dict.get('attack_speed_ratio'),
                                                                   champion_bonus_attack_speed)
    print(
        f'''{champion_id} {champion_name} {champion_health_points} {champion_health_regen}
            {champion_mana} {champion_mana_regen} {champion_armor} {champion_magic_resistance}
            {champion_attack_damage} {champion_crit_damage} {champion_attack_speed}''')

    CalculatedStatsWithLevel.objects.create(level=champion_level, champion_name=champion_name, calc_health_points=champion_health_points,
                                            calc_health_points_regen=champion_health_regen, calc_mana=champion_mana,
                                            calc_mana_regen=champion_mana_regen, calc_armor=champion_armor,
                                            calc_magic_resistance=champion_magic_resistance, calc_attack_damage=champion_attack_damage,
                                            calc_crit_damage=champion_crit_damage, calc_attack_speed=champion_attack_speed)


def standard_stats_calculation_based_on_level(base_stat, growth_stat, level):
    return round(base_stat + growth_stat * (level - 1) * (0.7025 + 0.0175 * (level - 1)), 2)


def attackspeed_calculation_based_on_level(base_attack_speed, ratio_attack_speed, bonus_attack_speed):
    return round(base_attack_speed + ratio_attack_speed * bonus_attack_speed, 2)


def calculation_of_stats_item_user_input_based_on_level_stats():
    None
