from django.shortcuts import render
from .models import Champion, UserInput, Items


# Create your views here.

def dmgcalc(request):
    if request.method == 'POST':
        print('Received Data ', request.POST['chosenChampion'])
        UserInput.objects.create(champion_index=request.POST['chosenChampion'], level=request.POST['chosenLevel'],
                                 item1_index=request.POST['chosenItem1'], item2_index=request.POST['chosenItem2'],
                                 item3_index=request.POST['chosenItem3'], item4_index=request.POST['chosenItem4'],
                                 item5_index=request.POST['chosenItem5'], item6_index=request.POST['chosenItem6'],
                                 ability_q_level_index=request.POST['chosenAbility1Level'], ability_w_level_index=request.POST['chosenAbility2Level'],
                                 ability_e_level_index=request.POST['chosenAbility3Level'], ability_r_level_index=request.POST['chosenAbility4Level'],
                                 rune_keystone_index=request.POST['chosenRuneKeystone'], rune_primary1_index=request.POST['chosenRunePrimary1'],
                                 rune_primary2_index=request.POST['chosenRunePrimary2'], rune_primary3_index=request.POST['chosenRunePrimary3'],
                                 rune_secondary1_index=request.POST['chosenRuneSecondary1'],
                                 rune_secondary2_index=request.POST['chosenRuneSecondary2'], ability1=request.POST['chosenAbility1'],
                                 ability2=request.POST['chosenAbility2'], ability3=request.POST['chosenAbility3'],
                                 ability4=request.POST['chosenAbility4'], ability5=request.POST['chosenAbility5'],
                                 ability6=request.POST['chosenAbility6'], ability7=request.POST['chosenAbility7'],
                                 ability8=request.POST['chosenAbility8'], ability9=request.POST['chosenAbility9'],
                                 ability10=request.POST['chosenAbility10'], ability11=request.POST['chosenAbility11'],
                                 ability12=request.POST['chosenAbility12'], ability13=request.POST['chosenAbility13'],
                                 ability14=request.POST['chosenAbility14'], ability15=request.POST['chosenAbility15'],
                                 dummy_health_points=request.POST['chosenDummyHP'], dummy_armor=request.POST['chosenDummyArmor'],
                                 dummy_magic_resistance=request.POST['chosenDummyMR'])
    all_champions = Champion.objects.all()
    all_items = Items.objects.all()
    # UserInput.objects.all().delete()
    # print(UserInput.objects.first())
    print(all_champions)
    return render(request, 'index.html', {'all_champions': all_champions, 'all_items': all_items})
