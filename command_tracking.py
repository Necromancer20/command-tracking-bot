import asyncio
import datetime
import os
import random
import time
from json import loads, dumps

import discord
import sqlitedict
from sqlitedict import SqliteDict

if not os.path.exists("./databases"):
    os.mkdir("./databases")

pet_adventure_rewards_db = SqliteDict("./databases/pet_adventure_rewards.sqlite")
agrees_to_track_db = SqliteDict("./databases/agreements.sqlite")

GLOBAL_USER = 950107553470226443


def get_pet_adventure_rewards_db():
    return pet_adventure_rewards_db


EPIC_RPG_ID = 555955826880413696
HUNT_MOB_NAMES = ['WOLF', 'SLIME', 'GOBLIN', 'NYMPH', 'SKELETON', 'ZOMBIE', 'GHOST', 'BABY DEMON', 'WITCH', 'IMP',
                  'UNICORN', 'GHOUL', 'GIANT SCORPION', 'SORCERER', 'BABY ROBOT', 'MERMAID', 'CECAELIA',
                  'GIANT PIRANHA', 'NEREID', 'GIANT CROCODILE', 'KILLER ROBOT', 'DEMON', 'HARPY', 'MANTICORE',
                  'DULLAHAN', 'SCALED BABY DRAGON', 'BABY DRAGON', 'YOUNG DRAGON', 'KID DRAGON',
                  'SCALED KID DRAGON', 'NOT SO YOUNG DRAGON', 'TEEN DRAGON', 'SCALED TEEN DRAGON',
                  'DEFINITELY NOT YOUNG DRAGON', 'ADULT DRAGON', 'SCALED ADULT DRAGON', 'NOT YOUNG AT ALL DRAGON',
                  'OLD DRAGON', 'SCALED OLD DRAGON', 'HOW DO YOU DARE CALL THIS DRAGON \"YOUNG\"???',
                  'VOID FRAGMENT', 'VOID PARTICLES', 'VOID SHARD',
                  'ABYSS BUG', 'NOTHING', 'SHADOW HANDS', 'EPIC NPC']

ADV_MOB_NAMES = ['MUTANT WATER BOTTLE', 'GIANT SPIDER', 'BUNCH OF BEES', 'OGRE', 'DARK KNIGHT', 'HYPER GIANT BOWL',
                 'MUTANT SHOE', 'WEREWOLF', 'CENTAUR', 'CHIMERA', 'HYPER GIANT AERONAUTICAL ENGINE', 'GOLEM',
                 'MAMMOTH', 'MUTANT \'ESC\' KEY', 'ENT', 'DINOSAUR', 'HYPER GIANT DOOR', 'CYCLOPS', 'ATTACK HELICOPTER',
                 'MUTANT BOOK', 'HYDRA', 'KRAKEN', 'HYPER GIANT CHEST', 'LEVIATHAN', 'WAR TANK', 'MUTANT BACKPACK',
                 'WYRM', 'HYPER GIANT TOILET', 'TITAN', 'TYPHON',
                 'EVEN MORE ANCIENT DRAGON', 'ANCIENTEST DRAGON',
                 'ANOTHER MUTANT DRAGON LIKE IN AREA 11 BUT STRONGER', 'just purple DRAGON',
                 'YES, AS YOU EXPECTED, ANOTHER HYPER GIANT DRAGON BUT OP ETC', 'i have no more ideas DRAGON',
                 'MUTANTEST DRAGON', 'HYPER GIANT DRAGON', 'MUTANT DRAGON', 'ANCIENT DRAGON',
                 'VOID CONE', 'VOID CUBE', 'VOID SPHERE',
                 'ABYSS WORM', 'SHADOW CREATURE', 'SHADOW ENTITY', 'EPIC NPC']

ADV_MOB_EMOJIS = {'MUTANT WATER BOTTLE': '<:water_bottle:979020267902894130>',
                  'GIANT SPIDER': '<:spider:979020307723603968>',
                  'BUNCH OF BEES': '<:bees:979020350547456080>',
                  'OGRE': '<:ogre:979024287375687760>',
                  'DARK KNIGHT': '<:dark_knight:979024374361362462>',
                  'HYPER GIANT BOWL': '<:bowl:979024419517267978>',
                  'MUTANT SHOE': '<:mutant_shoe:979025461873106974>',
                  'WEREWOLF': '<:werefolf:979025514528383007>',
                  'CENTAUR': '<:centaur:979025628001095710>',
                  'CHIMERA': '<:chimera:979026795745660938>',
                  'HYPER GIANT AERONAUTICAL ENGINE': '<:aeronautical:979026849801863188>',
                  'GOLEM': '<:golem:979026887139536936>',
                  'MAMMOTH': '<:mamooth:979027649676582963>',
                  'MUTANT \'ESC\' KEY': '<:esc_key:979027691317645373>',
                  'ENT': '<:ent:979027757210161213>',
                  'DINOSAUR': '<:dinosaur:979028474549379082>',
                  'HYPER GIANT DOOR': '<:door:979028556543848468>',
                  'CYCLOPS': '<:cyclops:979028595211112469>',
                  'ATTACK HELICOPTER': '<:attack_heli:979031121545273394>',
                  'MUTANT BOOK': '<:mutant_book:979031172678037534>',
                  'HYDRA': '<:hydra:979031206479929354>',
                  'KRAKEN': '<:kraken:979031386742730792>',
                  'HYPER GIANT CHEST': '<:chest:979031422046208071>',
                  'LEVIATHAN': '<:leviathan:979031490987958342>',
                  'WAR TANK': '<:war_tank:979031822006640680>',
                  'MUTANT BACKPACK': '<:backpack:979032834419327066>',
                  'WYRM': '<:wyhrm:979032920557752380>',
                  'HYPER GIANT TOILET': '<:hypertoiler:979031652296687636>',
                  'TITAN': '<:titan:979031710740152350>',
                  'TYPHON': '<:thypoon:979033166192988230>',
                  'EVEN MORE ANCIENT DRAGON': '<:Even_More_Ancient_Dragon:979033775201747014>',
                  'ANCIENTEST DRAGON': '<:ancientest_dragon:979033950628495392>',
                  'ANOTHER MUTANT DRAGON LIKE IN AREA 11 BUT STRONGER': '<:stupid_dtagon:979034146942881814>',
                  'just purple DRAGON': '<:just_purple_dragon:979034389868593184>',
                  'YES, AS YOU EXPECTED, ANOTHER HYPER GIANT DRAGON BUT OP ETC': '<:lol_Dragom:979034457568854046>',
                  'i have no more ideas DRAGON': '<:i_have_no_more_idea:979034708870565978>',
                  'MUTANTEST DRAGON': '<:Lindorei_helped_me:979034794501476352>',
                  'HYPER GIANT DRAGON': '<:hyper_giant_dragon:979033678086815774>',
                  'MUTANT DRAGON': '<:mutant_dragon:979033469592158298>',
                  'ANCIENT DRAGON': '<:ancient_dragon:979033403309576212>',
                  'VOID CONE': '<:void_cone:979035235574484992>',
                  'VOID CUBE': '<:void_cube:979035292105326602>',
                  'VOID SPHERE': '<:void_spere:979035352897572884>',
                  'ABYSS WORM': '<:abyss_Worm:979035620414459964>',
                  'SHADOW CREATURE': '<:shadow_creature:979035693328252968>',
                  'SHADOW ENTITY': '<:shadow_entity:979035766325927986>'}

HUNT_MOB_EMOJIS = {'WOLF': '<:wolf:979020076973965342>',
                   'SLIME': '<:slime:979020154014924850>',
                   'GOBLIN': '<:goblin:979020212995256360>',
                   'NYMPH': '<:nympth:979024203124723752>',
                   'SKELETON': '<:skeleton:979024239447392266>',
                   'ZOMBIE': '<:zombie:979024904554946621>',
                   'GHOST': '<:ghost:979025291303321660>',
                   'BABY DEMON': '<:baby_demon:979025387864596550>',
                   'WITCH': '<:witch:979026686442098708>',
                   'IMP': '<:imp:979026731799294032>',
                   'UNICORN': '<:unicorn:979027505702920192>',
                   'GHOUL': '<:ghoul:979027547306225754>',
                   'GIANT SCORPION': '<:giant_scorpio:979027612724781097>',
                   'SORCERER': '<:sorcerer:979028295926575144>',
                   'BABY ROBOT': '<:baby_robot:979028418005958656>',
                   'MERMAID': '<:mermaid:979030980461477948>',
                   'CECAELIA': '<:caecelioa:979031017228751008>',
                   'GIANT PIRANHA': '<:piranha:979031066708934656>',
                   'NEREID': '<:nereid:979031301199913001>',
                   'GIANT CROCODILE': '<:giant_crocodile:979031352718536774>',
                   'KILLER ROBOT': '<:killer_robot:979031537989337138>',
                   'DEMON': '<:demon:979032634992754718>',
                   'HARPY': '<:harpy:979032673391616071>',
                   'MANTICORE': '<:manticore:979031561913663528>',
                   'DULLAHAN': '<:dullahan:979031603995091004>',
                   'SCALED BABY DRAGON': '<:scaled_baby_dragon:979033238477606963>',
                   'BABY DRAGON': '<:scaled_baby_dragon:979033238477606963>',
                   'YOUNG DRAGON': '<:young_dragon:979033354462703646>',
                   'KID DRAGON': '<:kid_dragon:979033541163769876>',
                   'SCALED KID DRAGON': '<:kid_dragon:979033541163769876>',
                   'NOT SO YOUNG DRAGON': '<:not_so_young_dragon:979033622306750464>',
                   'TEEN DRAGON': '<:teen_dragon:979033834173648966>',
                   'SCALED TEEN DRAGON': '<:teen_dragon:979033834173648966>',
                   'DEFINITELY NOT YOUNG DRAGON': '<:dny_dragon:979033882420736050>',
                   'ADULT DRAGON': '<:adult_dragon:979034240442331196>',
                   'SCALED ADULT DRAGON': '<:adult_dragon:979034240442331196>',
                   'NOT YOUNG AT ALL DRAGON': '<:not_soy_dragon:979034319286841374>',
                   'OLD DRAGON': '<:old_dragon:979034586149453874>',
                   'SCALED OLD DRAGON': '<:old_dragon:979034586149453874>',
                   'HOW DO YOU DARE CALL THIS DRAGON \"YOUNG\"???': '<:how_Do_you_dare:979034650775261214>',
                   'VOID FRAGMENT': '<:void_fragment:979035019504926770>',
                   'VOID PARTICLES': '<:void_particles:979035088543170580>',
                   'VOID SHARD': '<:void_shards:979035154225963048>',
                   'ABYSS BUG': '<:abyss_bug:979035459932012634>',
                   'NOTHING': '<:noting:979035508934066226>',
                   'SHADOW HANDS': '<:shadow_hands:979035567759183872>'}

PET_EMOJIS = {'fish': '<:pinkfish:951188363443060796>',
              'hamster': '<:hamster:951188393679814707>',
              'snowball': '<:snowball:951188439603220521>',
              'bat': '<:pumpkin:951188486596198450>',
              'pony': '<:pony:951188510189187083>',
              'panda': '<:panda:951188542464335982>',
              'bunny': '<:bunny:951188566237650955>',
              'dog': "<:dog:951188071368495134>",
              'cat': "<:cat:951188235814572052>",
              'dragon': "<:dragon:951188278667800598>"}

EMOJIS = {
    'wolf_skin': '<:wolf_skin:977504213334626364>',
    'zombie_eye': '<:zombie_eye:977504302631378975>',
    'unicorn_horn': '<:unicorn_horn:977504406926929950>',
    'mermaid_hair': '<:mermaid_hair:977504503265886239>',
    'chip': '<:chip:977504591174311956>',
    'dragon_scale': '<:dragon_scale:977504671289733180>',

    'common': '<:common:977507553221169172>',
    'uncommon': '<:uncommon:977507667100729394>',
    'rare': '<:rare:977507728270430219>',
    'epic': '<:epic:977507783878533200>',
    'edgy': '<:edgy:977507842405855283>',
    'omega': '<:omega:977507981686087692>',
    'godly': '<:godly:977508095678877706>',
    'void': '<:void:977508192219197481>',

    'dark_energy': '<:dark_energy:977504748561395753>',

    'coin': '<:coin:977515127458922516>',
    'lifepotion': '<:lifepotion:996011675977257040>',
    'xp': '<:level:977515526400135168>',
    'mob_drops': '<:MOB_DROPS:977857793551925248>',

    'normie': '<:normie:951178147259371531>',
    'fish': '<:fish:978368532951752734>',
    'golden': '<:golden_fish:978394974968229888>',
    'epic_fish': '<:epic_fish:978395022045110312>',
    'super_fish': '<:super_fish:978394723083489371>',

    'wooden': '<:wooden_log:978367965831499786>',
    'epic_log': '<:epic_log:978368027336794192>',
    'super': '<:super_log:978368102532255855>',
    'mega': '<:mega_log:978368176100360273>',
    'hyper': '<:hyper_log:978368293448597624>',
    'ultra': '<:ultra_log:978368406795464764>',
    'ultimate': '<:untimate_log:978368479184973894>',
    'ruby': '<:ruby:978382141543034910>',

    'banana': '<:banana:978395455685808169>',
    'apple': '<:apple:978402281684860958>',
    'watermelon': '<:watermelon:978402379097587753>',

    'bread': '<:bread:979089161757802566>',
    'carrot': '<:carrot:979089346667880588>',
    'potato': '<:potato:979089287331082240>',
    'seed_bread': '<:bread_seed:979089658136895569>',
    'seed_carrot': '<:carrot_seed:979089411507630100>',
    'seed_potato': '<:potato_seed:979089492608712705>',

    'epic_coin': '<:epic_coin:982614769527828521>',
    'cookie': '<:cookie:982614836192092180>',
    'time_travel': '<:time_travel:982614916345262080>',
    'randompet': '<:cat:951188235814572052>',
    'coolness': '<:coolness:995637370114277416>',

    'fast': "<:fast:950726322177572914>",
    'happy': "<:happy:950871652818882590>",
    'clever': '<:clever:950871676298620928>',
    'digger': '<:digger:950871706573103104>',
    'lucky': "<:lucky:950714030660653097>",
    'time': '<:timetraveler:950871739359981600>',
    'epic_skill': '<:epic:950871780036325408>'
}

emoji_name_to_item = {'woodenlog': 'wooden',
                      'coin': 'coin',
                      'normiefish': 'fish',
                      'EPIClog': 'epic_log',
                      'goldenfish': 'golden',
                      'wolfskin': 'wolf_skin',
                      'commonlootbox': 'common',
                      'zombieeye': 'zombie_eye',
                      'SUPERlog': 'super',
                      'Apple': 'apple',
                      'Banana': 'banana',
                      'uncommonlootbox': 'uncommon',
                      'unicornhorn': 'unicorn_horn',
                      'MEGAlog': 'mega',
                      'ruby': 'ruby',
                      'rarelootbox': 'rare',
                      'mermaidhairs': 'mermaid_hair',
                      'HYPERlog': 'hyper',
                      'chip': 'chip',
                      'EPIClootbox': 'epic',
                      'EPICcoin': 'epic_coin',
                      'EPICfish': 'epic_fish',
                      'ULTRAlog': 'ultra',
                      'dragonscale': 'dragon_scale',
                      'arenacookie': 'cookie',
                      'ULTIMATElog': 'ultimate',
                      'timetravel': 'time_travel',
                      'darkenergy': 'dark_energy',
                      'Watermelon': 'watermelon',
                      'SUPERfish': 'super_fish',
                      '<a': 'randompet',
                      'coolness': 'coolness',
                      'lifepotion': 'lifepotion'}

WORKING_COMMANDS = (
    'rpg chainsaw', 'rpg bowsaw', 'rpg axe', 'rpg chop', 'rpg dynamite', 'rpg drill', 'rpg mine', 'rpg pickaxe',
    'rpg bigboat', 'rpg boat', 'rpg net', 'rpg fish', 'rpg greenhouse', 'rpg tractor', 'rpg ladder',
    'rpg pickup',
    '<@555955826880413696> chainsaw', '<@555955826880413696> bowsaw', '<@555955826880413696> axe',
    '<@555955826880413696> chop', '<@555955826880413696> dynamite', '<@555955826880413696> drill',
    '<@555955826880413696> mine', '<@555955826880413696> pickaxe', '<@555955826880413696> bigboat',
    '<@555955826880413696> boat', '<@555955826880413696> net', '<@555955826880413696> fish',
    '<@555955826880413696> greenhouse', '<@555955826880413696> tractor', '<@555955826880413696> ladder',
    '<@555955826880413696> pickup')

LOOTBOX_NAMES = ('common', 'c', 'uncommon', 'u', 'rare', 'r', 'epic', 'ep', 'edgy', 'ed', 'omega', 'o',
                 'godly', 'g', 'void', 'v')


async def track_command(message: discord.Message, database, client, mob_database):
    data = database[message.author.id]
    if data['info']['disabled_tracking']:
        return

    args = [i for i in message.content.lower().split(' ') if i != '']
    if len(args) <= 1:
        return
    command = args[0] + ' ' + args[1]

    if command in ('rpg hunt', "<@555955826880413696> hunt"):
        await add_hunt(message, database, client, mob_database)

    elif command in WORKING_COMMANDS:
        await add_working_commands(message, database, client, args[1])

    elif command in ('rpg farm', "<@555955826880413696> farm"):
        command_crop = 'none'
        if len(args) >= 3:
            for crop in ('carrot', 'bread', 'potato'):
                if args[2] == crop:
                    command_crop = crop
                    break
        await add_farm(message, database, client, command_crop)

    elif command in ('rpg adv', 'rpg adventure', '<@555955826880413696> adv', 'rpg adventure'):
        await add_adventure(message, database, client, mob_database)

    elif command in ('rpg training', 'rpg tr', '<@555955826880413696> training', '<@555955826880413696> tr'):
        await add_training(message, database, client)

    elif command in ('rpg open', '<@555955826880413696> open'):
        if len(args) >= 3 and args[2] in LOOTBOX_NAMES:
            if 'area' not in data['info']:
                return
            await add_lootbox(message, database, data['info']['area'], client)

    elif len(args) >= 4 and args[1] in ('pet', 'pets') and args[2] in ('adv', 'adventure') and args[3] == 'claim':
        await track_pet_rewards(message, client)

    elif command in ('rpg horse', '<@555955826880413696> horse') or len(args) == 2 and (
            command in ('rpg profile', 'rpg profile', '<@555955826880413696> p', '<@555955826880413696> p')):
        await get_horse_tier(message, database, client)

    elif command in (
    'rpg pr', 'rpg profession', 'rpg professions', '<@555955826880413696> pr', '<@555955826880413696> profession',
    '<@555955826880413696> professions'):
        await get_worker_pr_level(message, database, client)

    elif command.startswith(('rpg pet', 'rpg p', 'rpg profile', '<@555955826880413696> pet', '<@555955826880413696> p',
                             '<@555955826880413696> profile')):
        if command.startswith(('rpg pet', '<@555955826880413696> pet')):
            await track_time_travel(message, database, client, 'pet')


async def track_pet_rewards(message, client):
    def check_if_pet_claim_embed(msg):
        if msg.author.id != EPIC_RPG_ID:
            return False

        if msg.channel.id != message.channel.id:
            return False

        if not msg.embeds:
            return
        EMBED = msg.embeds[0].to_dict()

        if 'author' in EMBED and f"{message.author.name} — pets" in EMBED['author']['name']:
            return 'title' in EMBED and EMBED['title'] == 'Pet adventure rewards'

    try:
        response = await client.wait_for('message', timeout=10, check=check_if_pet_claim_embed)
    except asyncio.TimeoutError:
        return

    rewards = get_pet_rewards_from_embed(response.embeds[0].to_dict())

    if message.author.id not in pet_adventure_rewards_db:
        pet_adventure_rewards_db[message.author.id] = {'pony': {'successfully': 0, 'fail': 0},
                                                       'snowball': {'successfully': 0, 'fail': 0},
                                                       'pumpkin bat': {'successfully': 0, 'fail': 0}}
    if GLOBAL_USER not in pet_adventure_rewards_db:
        pet_adventure_rewards_db[GLOBAL_USER] = {'pony': {'successfully': 0, 'fail': 0},
                                                 'snowball': {'successfully': 0, 'fail': 0},
                                                 'pumpkin bat': {'successfully': 0, 'fail': 0}}

    data = pet_adventure_rewards_db[message.author.id]
    global_data = pet_adventure_rewards_db[GLOBAL_USER]

    for tier in rewards:
        if tier in ('snowball', 'pony', 'pumpkin bat'):
            if rewards[tier]:
                data[tier]['successfully'] += 1
                global_data[tier]['successfully'] += 1
            else:
                data[tier]['fail'] += 1
                global_data[tier]['fail'] += 1
            continue

        if tier not in data:
            data[tier] = {}

        if tier not in global_data:
            global_data[tier] = {}

        for item in rewards[tier]:
            if item not in data[tier]:
                data[tier][item] = rewards[tier][item]
            else:
                data[tier][item] += rewards[tier][item]

            if item not in global_data[tier]:
                global_data[tier][item] = rewards[tier][item]
            else:
                global_data[tier][item] += rewards[tier][item]

    pet_adventure_rewards_db[message.author.id] = data
    pet_adventure_rewards_db[GLOBAL_USER] = global_data


async def show_pet_reward(channel, author, clean_text_command, client, interaction=None, user=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    args = clean_text_command.split()

    if not user:
        last_arg = args[-1]
        if last_arg == 'global':
            last_arg = str(GLOBAL_USER)

        if get_user(last_arg):
            try:
                user = await client.fetch_user(get_user(last_arg))
            except discord.HTTPException:
                user = author
        else:
            user = author

    if user.id not in pet_adventure_rewards_db:
        await send_response(content=
                            f"<@{author.id}> I don't have any `pet reward` data stored for that user or you used an invalid user ID!")
        return

    if user.id not in agrees_to_track_db:
        await send_response(content=f"<@{author.id}> I didn't track anything for this user!")
        return

    data = pet_adventure_rewards_db[user.id]

    tiers = 0
    if len(args) >= 4 and args[3].isnumeric() and len(str(args[3])) <= 2:
        tiers = int(args[3])
        if 0 > tiers > 99:
            await send_response(content=
                                f"<@{author.id}> The pet tier must be between 0 and 99! Example: `pog tr petadv 4 global`")
            return

    if tiers == 0:
        tiers = list(range(1, 99))
    else:
        tiers = [tiers]

    items = {}

    for tier in data:
        if tier not in tiers:
            continue

        if isinstance(tier, int):
            for item in data[tier]:
                if item not in items:
                    items[item] = data[tier][item]
                else:
                    items[item] += data[tier][item]

    items_text = ""
    pets_text = ""
    total_pets_found = 0
    for i in range(1, 99):
        key = f"pet{i}"
        if key in items:
            total_pets_found += items[key]

    for i in range(1, 99):
        key = f"pet{i}"
        if key in items:
            pets_text += f"{PET_EMOJIS[random.choice(list(PET_EMOJIS.keys()))]} **Tier {i}** `x{items[key]:,}` times ({items[key] / total_pets_found * 100:.2f}%) \n"

    for item in EMOJIS:
        if item not in items:
            continue
        if 'pet' in item:
            continue
        if 'skill_up' in item:
            continue

        items_text += f"{EMOJIS[item]} > `collected:` {items[item]:,}\n"

    skill_up_text = ''
    if 'skill_up' in items:
        skill_up_text += f"> <:clever:950871676298620928> **SKILL RANK UP**: {items['skill_up']:,} times"

    description = f"""
> <:cat_bread:957316952227995659> **PET ADVENTURE REWARDS STATS**
Use `pog tr petadv <pet_tier>` for seeing the data only for a single pet tier.
—————————————————————
> <:potato:979089287331082240> **ITEMS FOUND**:
{items_text}

> 🐈 **PETS FOUND**
{pets_text}

{skill_up_text}

"""
    # {'pony': {'successfully': 0, 'fail': 0}, 'snowball': {'successfully': 0, 'fail': 0}, 'pumpkin bat': {'successfully': 0, 'fail': 0}}
    if data['pony']['successfully'] or data['pony']['fail']:
        description += f"> {PET_EMOJIS['pony']} BRING BACK SEED chance: **{data['pony']['successfully'] / (data['pony']['successfully'] + data['pony']['fail']) * 100:.2f}%**\n"

    if data['snowball']['successfully'] or data['snowball']['fail']:
        description += f"> {PET_EMOJIS['snowball']} BRING BACK LOOTBOX chance: **{data['snowball']['successfully'] / (data['snowball']['successfully'] + data['snowball']['fail']) * 100:.2f}%**\n"

    if data['pumpkin bat']['successfully'] or data['pumpkin bat']['fail']:
        description += f"> {PET_EMOJIS['bat']} BRING BACK MOB DROP chance: **{data['pumpkin bat']['successfully'] / (data['pumpkin bat']['successfully'] + data['pumpkin bat']['fail']) * 100:.2f}%**"

    embed = discord.Embed(colour=random.randint(0, 0xffffff), description=description)
    embed.set_author(name=f"{user.name}'s pet rewards stats", icon_url=user.avatar)
    embed.set_footer(text="Use [pog help stats] to learn more about command tracking")
    await send_response(embed=embed)


def get_pet_rewards_from_embed(embed_dict):
    tiers = {}
    for field in embed_dict['fields']:
        tier = roman_to_int(field['name'].split(' — TIER ')[1])
        if tier not in tiers:
            tiers[tier] = {}

        if 'advanced a rank!' in field['value']:
            amount = 1
            item = 'skill_up'
        else:
            amount = int(field['value'].split(' ')[0].replace(',', ''))
            item = emoji_name_to_item[field['value'].split(' ')[1].replace('<:', '').split(':')[0]]

        if item not in tiers[tier]:
            tiers[tier][item] = amount
        else:
            tiers[tier][item] += amount

        if '**__Pet found__**' in field['value']:
            try:
                pet_found_tier = roman_to_int(field['value'].split(' — TIER ')[1].replace('\n', ''))
            except KeyError:
                pet_found_tier = roman_to_int(field['value'].split(' — TIER ')[1].split('\n')[0])

            if f"pet{pet_found_tier}" not in tiers[tier]:
                tiers[tier][f"pet{pet_found_tier}"] = 1
            else:
                tiers[tier][f"pet{pet_found_tier}"] += 1

        if 'Pumpkin bat' in field['name']:
            if '**__Item found__**' not in field['value']:
                tiers['pumpkin bat'] = 0
            else:
                tiers['pumpkin bat'] = 1

        elif ' Snowball ' in field['name']:
            if '**__Item found__**' not in field['value']:
                tiers['snowball'] = 0
            else:
                tiers['snowball'] = 1

        elif ' Pony ' in field['name']:
            if '**__Item found__**' not in field['value']:
                tiers['pony'] = 0
            else:
                tiers['pony'] = 1

    return tiers


async def track_time_travel(message, command_trackin_db, client, command_type):
    def check_if_pet_embed(msg):
        if msg.author.id != EPIC_RPG_ID:
            return False

        if msg.channel.id != message.channel.id:
            return False

        if not msg.embeds:
            return
        EMBED = msg.embeds[0].to_dict()

        if 'author' not in EMBED or f"{message.author.name} — pets" not in EMBED['author']['name']:
            return

        return 'description' in EMBED and 'Total pets' in EMBED['description']

    time_travel = 0
    if command_type == 'pet':
        try:
            response = await client.wait_for('message', timeout=10, check=check_if_pet_embed)
        except asyncio.TimeoutError:
            return
        time_travel = int(
            response.embeds[0].description.split('**__Total pets__**: ')[1].split('\n')[0].split('/')[1]) - 5

    data = command_trackin_db[message.author.id]

    if 'tt' not in data['info']:
        data['info']['tt'] = time_travel

    else:
        if time_travel > data['info']['tt']:
            data['info']['tt'] = time_travel
        else:
            return

    command_trackin_db[message.author.id] = data


async def show_training(channel, author, clean_text_command, client, command_tracking_db, interaction=None, user=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    last_arg = clean_text_command.split()[-1]
    pre_last_arg = clean_text_command.split()[-2]

    tier = ''
    if not user:
        if last_arg == 'global':
            last_arg = str(GLOBAL_USER)
        elif last_arg == 'globalt10':
            last_arg = str(GLOBAL_USER)
            tier = 'T10'
        elif last_arg == 'globalt9':
            last_arg = str(GLOBAL_USER)
            tier = 'T9'
        elif last_arg.startswith('globalt'):
            last_arg = str(GLOBAL_USER)
            tier = 'T8'

        if get_user(last_arg):
            try:
                user = await client.fetch_user(get_user(last_arg))
            except discord.HTTPException:
                user = author
        else:
            user = author

    if author.id == user.id:
        pre_last_arg = last_arg

    if user.id not in agrees_to_track_db:
        await send_response(content=f"<@{author.id}> I didn't track anything for this user!")
        return

    if user.id not in command_tracking_db:
        await send_response(content=
                            f"<@{author.id}> I don't have any data stored for that user or you used an invalid user ID")
        return

    if tier.startswith('T') and tier[1:].isnumeric():
        display_tier = tier

        if f"{GLOBAL_USER}-tr{tier}" not in command_tracking_db:
            await send_response(content=f"<@{author.id}> I don't have any data stored for that.")
            return

        data = command_tracking_db[f"{GLOBAL_USER}-tr{tier}"]

    else:
        display_tier = 'ANY'
        data = command_tracking_db[user.id]

    if 'training' not in data or data['training']['count'] == 0:
        await send_response(content=
                            f"<@{author.id}> I don't have any training data stored for that user or you used an invalid user ID")
        return

    data = data['training']
    tier_pet_amounts = {i: 0 for i in range(1, 11)}
    skills = {}

    if pre_last_arg.isnumeric():
        command_amount = int(pre_last_arg)
        if command_amount not in data:
            await send_response(content=
                                f"<@{author.id}> I don't have data stored for {command_amount} commands yet.")
            return

        for tier in data[command_amount]['pet_tiers']:
            tier_pet_amounts[tier] += data[command_amount]['pet_tiers'][tier]

        for skill in data[command_amount]['pet_skills']:
            if skill.lower() not in skills:
                skills[skill.lower()] = data[command_amount]['pet_skills'][skill]
            else:
                skills[skill.lower()] += data[command_amount]['pet_skills'][skill]
    else:
        command_amount = 'ANY'
        for i in range(0, 7):
            if i in data:
                for tier in data[i]['pet_tiers']:
                    tier_pet_amounts[tier] += data[i]['pet_tiers'][tier]

        for i in range(0, 7):
            if i in data:
                for skill in data[i]['pet_skills']:
                    if skill.lower() not in skills:
                        skills[skill.lower()] = data[i]['pet_skills'][skill]
                    else:
                        skills[skill.lower()] += data[i]['pet_skills'][skill]

    # {'count': 0, 'successful': 0, 'failed': 0, 'pets_earned': 0, }
    description = f"""
> <:ascended:950871761719812096> **TRAINING STATS**
🔹 Commands used to catch the pet: **{command_amount}**
🔹 Horse tier for global data: **{display_tier}**

:dart: **Total commands tracked:** {data['count']}
✅ **Total successful trainings:** {data['successful']} ({data['successful'] / data['count'] * 100:.2f}%)
❌ **Total failed trainings:** {data['failed']} ({data['failed'] / data['count'] * 100:.2f}%) 
<:cat:951188235814572052> **Pets found:** {sum(list(tier_pet_amounts.values()))} ({sum(list(tier_pet_amounts.values())) / data['successful'] * 100:.2f}%)
"""
    if '' in skills:
        description += f"🚩 **Pets lost:** {skills['']} ({skills[''] / (sum(list(skills.values()))) * 100:.2f}%)\n"
        del skills['']

    description += """
—————————————————————
> <:pony:951188510189187083> **PET TIERS SEEN**:
"""

    skill_order = ('normie', 'fast', 'happy', 'clever', 'digger', 'lucky', 'time', 'epic')
    if pre_last_arg.isnumeric():
        command_amount = int(pre_last_arg)
        if 1 > command_amount > 6:
            await send_response(content=f"<@{author.id}> The command amount must be 1 to 6!")
            return
        tier_pet_amounts = {i: 0 for i in range(1, 11)}

        if command_amount not in data:
            await send_response(content=
                                f"<@{author.id}> I don't have data stored for {command_amount} commands yet.")
            return

        for tier in data[command_amount]['pet_tiers']:
            tier_pet_amounts[tier] += data[command_amount]['pet_tiers'][tier]

        for tier in tier_pet_amounts:
            if tier_pet_amounts[tier]:
                description += f"**Tier {tier}:** — `x{tier_pet_amounts[tier]}` ({tier_pet_amounts[tier] / (sum(list(tier_pet_amounts.values()))) * 100:.2f}%)\n"

        description += f"\n—————————————————————\n> <:faster:954662907252178984> **PET SKILLS OBTAINED**:\n"

        for skill in skill_order:
            if skill not in skills:
                continue
            if skill.lower() == 'epic':
                skill_name = 'epic_skill'
            else:
                skill_name = skill.lower()
            description += f"{EMOJIS[skill_name]} **{skill.title()}:** — `x{skills[skill]}` ({skills[skill] / (sum(list(skills.values()))) * 100:.2f}%)\n"

        description += 'ㅤ\n'

    else:
        # global_data['training'][command_amount]['pet_tiers'][pet_tier OR skill] = 'pet_tiers': {}, 'pet_skills': {}
        tier_pet_amounts = {i: 0 for i in range(1, 11)}
        for i in range(0, 7):
            if i in data:
                for tier in data[i]['pet_tiers']:
                    tier_pet_amounts[tier] += data[i]['pet_tiers'][tier]

        for tier in tier_pet_amounts:
            if tier_pet_amounts[tier]:
                description += f"**Tier {tier}:** — `x{tier_pet_amounts[tier]}` ({tier_pet_amounts[tier] / (sum(list(tier_pet_amounts.values()))) * 100:.2f}%)\n"

        description += f"\n—————————————————————\n> <:faster:954662907252178984> **PET SKILLS OBTAINED**:\n"

        for skill in skill_order:
            if skill not in skills:
                continue
            if skill.lower() == 'epic':
                skill_name = 'epic_skill'
            else:
                skill_name = skill.lower()
            description += f"{EMOJIS[skill_name]} **{skill.title()}:** — `x{skills[skill]}` ({skills[skill] / (sum(list(skills.values()))) * 100:.2f}%)\n"

        description += 'ㅤ\n'

    if last_arg == str(GLOBAL_USER):
        description += ":warning: Use `globalT10`, `globalT9`... to see the training stats for specific horse tiers."

    embed = discord.Embed(colour=random.randint(0, 0xffffff), description=description)
    embed.set_author(name=f"{user.name}'s training stats", icon_url=user.avatar)
    embed.set_footer(text="Use [pog help stats] to learn more about command tracking")
    await send_response(embed=embed)


async def add_training(message, command_tracking_db, client):
    results = await training_waiting(message, client)
    if not results:
        return

    sucess, command_amount, pet_tier, skill = results
    data = command_tracking_db[message.author.id]
    global_data = command_tracking_db[GLOBAL_USER]

    if 'training' not in data:
        data['training'] = {'count': 0, 'successful': 0, 'failed': 0, 'pets_earned': 0}

    if 'training' not in global_data:
        global_data['training'] = {'count': 0, 'successful': 0, 'failed': 0, 'pets_earned': 0}

    add_per_tier = False
    if 'horse_tier' in data['info']:
        add_per_tier = True

    if add_per_tier:
        tier = data['info']['horse_tier'] if data['info']['horse_tier'] in ('T10', 'T9') else 'T8'
        if f"{GLOBAL_USER}-tr{tier}" not in command_tracking_db:
            command_tracking_db[f"{GLOBAL_USER}-tr{tier}"] = {
                'training': {'count': 0, 'successful': 0, 'failed': 0, 'pets_earned': 0}}

    data['training']['count'] += 1
    if sucess:
        data['training']['successful'] += 1
    else:
        data['training']['failed'] += 1

    time_travel = 0
    if 'tt' in data['info']:
        time_travel = data['info']['tt']

    if pet_tier:
        if command_amount not in data['training']:
            data['training'][command_amount] = {'pet_tiers': {}, 'pet_skills': {}}

        data['training']['pets_earned'] += 1

        if pet_tier not in data['training'][command_amount]['pet_tiers']:
            data['training'][command_amount]['pet_tiers'][pet_tier] = 1
        else:
            data['training'][command_amount]['pet_tiers'][pet_tier] += 1

        if skill not in data['training'][command_amount]['pet_skills']:
            data['training'][command_amount]['pet_skills'][skill] = 1
        else:
            data['training'][command_amount]['pet_skills'][skill] += 1

    if time_travel >= 2:
        global_data['training']['count'] += 1
        if sucess:
            global_data['training']['successful'] += 1
        else:
            global_data['training']['failed'] += 1

        if pet_tier:
            if command_amount not in global_data['training']:
                global_data['training'][command_amount] = {'pet_tiers': {}, 'pet_skills': {}}

            global_data['training']['pets_earned'] += 1

            if pet_tier not in global_data['training'][command_amount]['pet_tiers']:
                global_data['training'][command_amount]['pet_tiers'][pet_tier] = 1
            else:
                global_data['training'][command_amount]['pet_tiers'][pet_tier] += 1

            if skill not in global_data['training'][command_amount]['pet_skills']:
                global_data['training'][command_amount]['pet_skills'][skill] = 1
            else:
                global_data['training'][command_amount]['pet_skills'][skill] += 1

        if add_per_tier:
            tier = data['info']['horse_tier'] if data['info']['horse_tier'] in ('T10', 'T9') else 'T8'
            tier_data = command_tracking_db[f"{GLOBAL_USER}-tr{tier}"]
            if 'training' not in tier_data:
                tier_data = {'training': {'count': 0, 'successful': 0, 'failed': 0, 'pets_earned': 0}}

            tier_data['training']['count'] += 1
            if sucess:
                tier_data['training']['successful'] += 1
            else:
                tier_data['training']['failed'] += 1

            if pet_tier:
                if command_amount not in tier_data['training']:
                    tier_data['training'][command_amount] = {'pet_tiers': {}, 'pet_skills': {}}

                tier_data['training']['pets_earned'] += 1

                if pet_tier not in tier_data['training'][command_amount]['pet_tiers']:
                    tier_data['training'][command_amount]['pet_tiers'][pet_tier] = 1
                else:
                    tier_data['training'][command_amount]['pet_tiers'][pet_tier] += 1

                if skill not in tier_data['training'][command_amount]['pet_skills']:
                    tier_data['training'][command_amount]['pet_skills'][skill] = 1
                else:
                    tier_data['training'][command_amount]['pet_skills'][skill] += 1

            command_tracking_db[f"{GLOBAL_USER}-tr{tier}"] = tier_data

    command_tracking_db[message.author.id] = data
    command_tracking_db[GLOBAL_USER] = global_data


async def training_waiting(message, client):
    # ==============================================================================================================
    # Wait for epic rpg to send the training message
    def check(msg: discord.Message):
        if msg.author.id == message.author.id and (
                is_command_again(msg, 'rpg training') or is_command_again(msg, 'rpg tr')):
            return True

        if msg.author.id != EPIC_RPG_ID:
            return False

        if msg.channel.id != message.channel.id:
            return False

        if message.author.name not in msg.content:
            return

        return 'is training in the' in msg.content

    try:
        response = await client.wait_for('message', check=check, timeout=15)
    except asyncio.TimeoutError:
        return

    if is_command_again(response, 'rpg training') or is_command_again(response, 'rpg tr'):
        return

    # ==============================================================================================================
    # Wait for the fail/sucess of training
    def check_training_response(msg: discord.Message):
        if msg.author.id != EPIC_RPG_ID:
            return False

        if msg.channel.id != message.channel.id:
            return False

        if message.author.name not in msg.content:
            return

        return 'Better luck next time, ' in msg.content or 'Well done, ' in msg.content

    try:
        response = await client.wait_for('message', check=check_training_response, timeout=15)
    except asyncio.TimeoutError:
        return

    sucess = 0
    if 'Well done, ' in response.content:
        sucess = 1

    # ==============================================================================================================
    # wait 5s to see if a pet spawned
    response = None

    def check_if_pet_spawned(msg: discord.Message):
        if msg.author.id != EPIC_RPG_ID:
            return False

        if msg.channel.id != message.channel.id:
            return False

        return is_pet_from_training_embed(msg)

    try:
        response = await client.wait_for('message', check=check_if_pet_spawned, timeout=5)
    except asyncio.TimeoutError:
        pass

    command_amount = 0
    pet_tier = 0
    skill = ''
    if response:
        EMBED = response.embeds[0].to_dict()
        pet_tier = roman_to_int(EMBED['fields'][0]['name'].split(' TIER ')[1].split('**')[1])

        def wait_for_feed_pat(msg: discord.Message):
            if msg.author.id != message.author.id:
                return False

            if msg.channel.id != message.channel.id:
                return False

            if 'feed' not in msg.content.lower() and 'pat' not in msg.content.lower():
                return False
            cuddles = [o for o in msg.content.lower().split(' ') if o in ('feed', 'pat')]
            for command in cuddles:
                if command not in ('feed', 'pat'):
                    return False
            if len(cuddles) > 6:
                return False

            return True

        try:
            response = await client.wait_for('message', check=wait_for_feed_pat, timeout=45)
        except asyncio.TimeoutError:
            pass
        else:
            command_amount = len([o for o in response.content.lower().split(' ') if o in ('feed', 'pat')])

            def check_if_pet_caught(msg: discord.Message):
                if msg.author.id != EPIC_RPG_ID:
                    return False

                if msg.channel.id != message.channel.id:
                    return False

                return is_pet_caught_embed(msg)

            try:
                response = await client.wait_for('message', check=check_if_pet_caught, timeout=45)
            except asyncio.TimeoutError:
                pass
            else:
                EMBED = response.embeds[0].to_dict()
                caught = True if 'got bored and left' not in EMBED['fields'][0]['value'] else False
                if caught:
                    if 'Normie' in EMBED['fields'][0]['value']:
                        skill = EMBED['fields'][0]['value'].split('\n')[5].split('**')[1]
                    else:
                        skill = EMBED['fields'][0]['value'].split('\n')[5].split('**')[1].split(' ')[1]

    return sucess, command_amount, pet_tier, skill


def roman_to_int(s):
    rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    int_val = 0
    s = s.upper()
    for i in range(len(s)):
        if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
            int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
        else:
            int_val += rom_val[s[i]]

    return int_val


def is_pet_caught_embed(message):
    if not message.embeds:
        return False
    EMBED = message.embeds[0].to_dict()
    return 'fields' in EMBED and ((' is now following ' in EMBED['fields'][0][
        'value'] and 'See your pets with `pets`' in EMBED['fields'][0]['value']) or
                                  'got bored and left' in EMBED['fields'][0]['value'])


def is_pet_from_training_embed(message):
    if not message.embeds:
        return False
    EMBED = message.embeds[0].to_dict()
    return 'fields' in EMBED and 'SUDDENLY, A' in EMBED['fields'][0]['name'] and 'IS APPROACHING' in EMBED['fields'][0][
        'name']


async def add_lootbox(message, database, area, client):
    def check(msg: discord.Message):
        if msg.author.id == message.author.id and is_command_again(msg, 'rpg open '):
            return True

        if msg.author.id != EPIC_RPG_ID:
            return False

        if msg.channel.id != message.channel.id:
            return False

        if not msg.embeds:
            return False

        EMBED = msg.embeds[0].to_dict()

        if 'author' not in EMBED:
            return False

        if f"{message.author.name} — lootbox" in EMBED['author']['name']:
            return True

    try:
        response = await client.wait_for('message', check=check, timeout=15)
    except asyncio.TimeoutError:
        return

    if is_command_again(response, 'rpg open '):
        return

    if area % 2 == 1:
        area += 1

    if area >= 11:
        area = 12

    if area == 16:
        return

    EMBED = response.embeds[0].to_dict()
    lootbox_type = EMBED['fields'][0]['name'].split(' ')[1].lower()
    lootbox_contents = EMBED['fields'][0]['value'].split('\n')

    if ' (x' in EMBED['fields'][0]['name']:
        lootbox_amount = int(EMBED['fields'][0]['name'].split(' ')[4].lower().replace('(x', '').replace(')', ''))
    else:
        lootbox_amount = 1

    data = database[message.author.id]
    global_data = database[GLOBAL_USER]

    data = add_lootbox_structure_data(data, area, lootbox_type)
    global_data = add_lootbox_structure_data(global_data, area, lootbox_type)

    lootbox_dict = {}
    for line in lootbox_contents:
        splits = line.split(' ')
        item = splits[1].replace('<:', '')[:splits[1].replace('<:', '').index(':')]
        amount = int(line.split(' ')[0].replace('+', ''))
        lootbox_dict[emoji_name_to_item[item]] = amount

    if lootbox_amount == 1:
        add_lootbox_items(data, lootbox_dict, area, lootbox_type, 1, 'lootboxes_one')
        add_lootbox_items(data, lootbox_dict, area, lootbox_type, 1, 'lootboxes')

        add_lootbox_items(global_data, lootbox_dict, area, lootbox_type, 1, 'lootboxes_one')
        add_lootbox_items(global_data, lootbox_dict, area, lootbox_type, 1, 'lootboxes')
    else:
        add_lootbox_items(data, lootbox_dict, area, lootbox_type, lootbox_amount, 'lootboxes')
        add_lootbox_items(global_data, lootbox_dict, area, lootbox_type, lootbox_amount, 'lootboxes')

    database[message.author.id] = data
    database[GLOBAL_USER] = global_data


def add_lootbox_items(data, lootbox_dict, area, lootbox_type, lootbox_amount, data_set_name):
    for item in lootbox_dict:
        if item not in data[data_set_name][area][lootbox_type]['loot']:
            data[data_set_name][area][lootbox_type]['loot'][item] = {'found': lootbox_dict[item],
                                                                     'min': lootbox_dict[item],
                                                                     'max': lootbox_dict[item],
                                                                     'count': 1}
        else:
            data[data_set_name][area][lootbox_type]['loot'][item]['count'] += lootbox_amount
            data[data_set_name][area][lootbox_type]['loot'][item]['found'] += lootbox_dict[item]

            if data_set_name == 'lootboxes_one':
                amount = lootbox_dict[item]
                if amount > data[data_set_name][area][lootbox_type]['loot'][item]['max']:
                    data[data_set_name][area][lootbox_type]['loot'][item]['max'] = amount

                if amount < data[data_set_name][area][lootbox_type]['loot'][item]['min']:
                    data[data_set_name][area][lootbox_type]['loot'][item]['min'] = amount

    data[data_set_name][area][lootbox_type]['count'] += lootbox_amount


def add_lootbox_structure_data(data, area, lootbox):
    """ Gets the area and the lootbox, and adds them to data, if they are not in already """
    if 'lootboxes' not in data:
        data['lootboxes'] = {}

    if area not in data['lootboxes']:
        data['lootboxes'][area] = {}

    if lootbox not in data['lootboxes'][area]:
        data['lootboxes'][area][lootbox] = {'count': 0, 'loot': {}}

    if 'lootboxes_one' not in data:
        data['lootboxes_one'] = {}

    if area not in data['lootboxes_one']:
        data['lootboxes_one'][area] = {}

    if lootbox not in data['lootboxes_one'][area]:
        data['lootboxes_one'][area][lootbox] = {'count': 0, 'loot': {}}

    return data


async def show_lootbox(channel, author, lootbox_type, clean_text_command, client, database, interaction=None,
                       user=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    if not user:
        last_arg = clean_text_command.split()[-1]

        if last_arg == 'global':
            pre_last_arg = clean_text_command.split()[-2]  # for getting the keyword "one"
            last_arg = str(GLOBAL_USER)
        else:
            pre_last_arg = last_arg

        if get_user(last_arg):
            try:
                user = await client.fetch_user(get_user(last_arg))
            except discord.HTTPException:
                user = author
        else:
            user = author

    if user.id not in agrees_to_track_db:
        await send_response(content=f"<@{author.id}> I didn't track anything for this user!")
        return

    if user.id not in database:
        await send_response(content=
                            f"<@{author.id}> I don't have any data stored for that user or you used an invalid user ID")
        return

    data = database[user.id]
    if 'lootboxes' not in data:
        await send_response(content=
                            f"<@{author.id}> I don't have any lootbox data tracked. The bot also needs to know your area, so hunt once before opening.")
        return

    if pre_last_arg == 'one':
        data = data['lootboxes_one']
    else:
        data = data['lootboxes']

    description = """🔹 `col` - total collected in all lootboxes
🔹 `avg` - average items per lootbox
🔹 `amt` - how many items you can find at once in a lootbox  
🔹 `%` - the chance that the lootbox will contain this item\n
"""

    description += f"> {EMOJIS[lootbox_type]} - **{lootbox_type.title()} Lootbox stats**"
    if pre_last_arg == 'one':
        description += " - **ONE BY ONE**"

    description += f"\n\n**Total opened:** {get_col(lootbox_type, 'lol', data, only_lb_amount=True)}\n" \
                   f"—————————————————————\n"

    for item in emoji_name_to_item.values():
        if pre_last_arg == 'one':
            description += get_col(lootbox_type, item, data, one_by_one=True)
        else:
            description += get_col(lootbox_type, item, data)

    if pre_last_arg == 'one':
        description += '—————————————————————'
    else:
        description += f"""—————————————————————
:warning: Please use `pog tr {lootbox_type} one` to get the chances of items, the bot can't calculate that when you open more than 1 lootbox at once.
Also please consider opening your lootboxes one by one to help in gathering data!"""

    embed = discord.Embed(colour=random.randint(0, 0xffffff), description=description)
    embed.set_author(name=f"{user.name}'s lootbox stats", icon_url=user.avatar)
    embed.set_footer(text='Use `pog help stats` for the list of stat commands | Pog <3')

    await send_response(embed=embed)


def get_col(lootbox, item, data, only_lb_amount=False, one_by_one=False):
    lowest_area = 0
    if item == 'zombie_eye':
        lowest_area = 4
    elif item in ('unicorn_horn', 'ruby'):
        lowest_area = 6
    elif item == 'mermaid_hair':
        lowest_area = 8
    elif item == 'chip':
        lowest_area = 10
    elif item == 'dragon_scale':
        lowest_area = 12

    lowest = 10000
    highest = 0
    col = 0
    count = 0
    lb_count = 0

    for area in data:
        if only_lb_amount:
            if lootbox in data[area]:
                lb_count += data[area][lootbox]['count']
            continue

        if area < lowest_area or lootbox not in data[area]:
            continue

        lb_count += data[area][lootbox]['count']

        if item not in data[area][lootbox]['loot']:
            continue

        if data[area][lootbox]['loot'][item]['min'] < lowest:
            lowest = data[area][lootbox]['loot'][item]['min']

        if data[area][lootbox]['loot'][item]['max'] > highest:
            highest = data[area][lootbox]['loot'][item]['max']

        col += data[area][lootbox]['loot'][item]['found']
        count += data[area][lootbox]['loot'][item]['count']

    if only_lb_amount:
        return lb_count

    if not lb_count:
        return ''

    if not count:
        return ""

    if not one_by_one:
        return f"{EMOJIS[item]} > `collected:` {col}\n"
    else:
        return f"{EMOJIS[item]} > `col:` {col}, `avg:` {col / lb_count:.2f}, `amt:` {lowest} ~ {highest} → ({(count / lb_count) * 100:.2f}%)\n"


async def get_worker_pr_level(message, database, client):
    def check(msg: discord.Message):
        if not msg.author.id == EPIC_RPG_ID:
            return False

        if msg.channel.id != message.channel.id:
            return False

        if not msg.embeds:
            return
        EMBED = msg.embeds[0].to_dict()
        if 'author' in EMBED and f"{message.author.name} — professions" in EMBED['author']['name']:
            return True

    try:
        response = await client.wait_for('message', check=check, timeout=5)
    except asyncio.TimeoutError:
        return
    EMBED = response.embeds[0].to_dict()

    worker_level = 0
    try:
        worker_level = int(
            EMBED['fields'][0]['name'].split("<:EPIClog:541056003517710348> Worker Lv ")[1].split(' ')[0])
    except:
        return
    data = database[message.author.id]
    data['info']['worker'] = worker_level
    database[message.author.id] = data


async def get_horse_tier(message, database, client):
    def check(msg: discord.Message):
        if not msg.author.id == EPIC_RPG_ID:
            return False

        if msg.channel.id != message.channel.id:
            return False

        if not msg.embeds:
            return
        EMBED = msg.embeds[0].to_dict()
        if 'author' in EMBED and f"{message.author.name} — horse" in EMBED['author']['name']:
            return True
        if 'author' in EMBED and f"{message.author.name} — profile" in EMBED['author']['name']:
            return True

    try:
        response = await client.wait_for('message', check=check, timeout=5)
    except asyncio.TimeoutError:
        return
    EMBED = response.embeds[0].to_dict()

    time_travel = 0
    try:
        tier = 0
        if 'author' in EMBED and f"{message.author.name} — horse" in EMBED['author']['name']:
            tier = EMBED['fields'][0]['value'].split('\n')[0].split('**Horse Tier** - ')[1].split(' ')[0]
        elif 'author' in EMBED and f"{message.author.name} — profile" in EMBED['author']['name']:
            tier = EMBED['fields'][2]['value'].split('\n')[2].replace('mount', ' ').split('<:tier')[1].split(' ')[0]
            if 'Time travels' in response.embeds[0].fields[0].value:
                time_travel = int(response.embeds[0].fields[0].value.split('\n**Time travels**: ')[1])

    except (IndexError, ValueError):
        return

    data = database[message.author.id]
    if tier in ('X', '10'):
        data['info']['horse_tier'] = 'T10'
        data['tier_10']['has_t10'] = True
    elif tier in ('IX', '9'):
        data['info']['horse_tier'] = 'T9'
    elif tier in ('VIII', '8'):
        data['info']['horse_tier'] = 'T8'
    elif tier in ('VII', '7'):
        data['info']['horse_tier'] = 'T7'
    elif tier in ('VI', '6'):
        data['info']['horse_tier'] = 'T6'
    else:
        data['info']['horse_tier'] = ''

    if 'tt' not in data['info'] and time_travel:
        data['info']['tt'] = time_travel

    elif time_travel:
        if time_travel > data['info']['tt']:
            data['info']['tt'] = time_travel
        else:
            pass

    database[message.author.id] = data


def get_farm_keywords(crop):
    if crop == 'none':
        return " seed in the ground..."
    elif crop == 'potato':
        return " potato seed in the ground..."
    elif crop == 'carrot':
        return " carrot seed in the ground..."
    elif crop == 'bread':
        return " bread seed in the ground..."


async def add_farm(message, database, client, crop):
    data = database[message.author.id]
    look_for = get_farm_keywords(crop)

    def check(msg: discord.Message):
        if msg.author.id == message.author.id and is_command_again(msg, 'rpg farm'):
            return True

        if not msg.author.id == EPIC_RPG_ID:
            return False

        if msg.channel.id != message.channel.id:
            return False

        if message.author.name not in msg.content:
            return

        return look_for in msg.content

    try:
        response = await client.wait_for('message', check=check, timeout=15)
    except asyncio.TimeoutError:
        return

    if is_command_again(response, 'rpg farm'):
        return

    global_data = database[GLOBAL_USER]

    # channel = client.get_channel(866253782228926514)
    # response = await channel.fetch_message(965688231872069662)
    # message = await channel.fetch_message(965688230697652284)
    # return

    if 'farm' not in data or 'special_event' not in data['farm'] or 'normal_farm' not in data['farm']:
        if 'farm' in data['working_commands']:
            del data['working_commands']['farm']
        data['farm'] = {'xp_gained': 0,
                        'special_event': {'count': 0, 'won': [0, 0]},
                        'special_seeds': {'count': 0,
                                          'carrot': {'count': 0, 'amounts': {}},
                                          'potato': {'count': 0, 'amounts': {}},
                                          'bread': {'count': 0, 'amounts': {}}},
                        'normal_farm': {'count': 0,
                                        'bread': {'count': 0, 'resources': 0},
                                        'carrot': {'count': 0, 'resources': 0},
                                        'potato': {'count': 0, 'resources': 0}},
                        'using_seed': {'count': 0,
                                       'bread': {'count': 0, 'resources': 0, 'seed_back': {}},
                                       'carrot': {'count': 0, 'resources': 0, 'seed_back': {}},
                                       'potato': {'count': 0, 'resources': 0, 'seed_back': {}}}}

    if response.embeds and is_farm__event_embed(response.embeds[0], message.author.name):
        data['farm']['special_event']['count'] += 1
        global_data['farm']['special_event']['count'] += 1

        def check_response(msg):
            return msg.author.id == message.author.id and msg.content.lower() in ('fight', 'plant another', 'cry')

        try:
            response = await client.wait_for('message', check=check_response, timeout=40)
        except asyncio.TimeoutError:
            pass
        else:
            if 'fight' in response.content.lower():
                def check_rpg_response(msg):
                    return msg.author.id == EPIC_RPG_ID and (
                            'Nothing happened' in msg.content or 'leveled up 20 times' in msg.content) and msg.channel.id == message.channel.id

                try:
                    response = await client.wait_for('message', check=check_rpg_response, timeout=15)
                except asyncio.TimeoutError:
                    pass
                else:
                    if 'leveled up 20 times' in response.content:
                        data['farm']['special_event']['won'][0] += 1
                        global_data['farm']['special_event']['won'][0] += 1
                    else:
                        data['farm']['special_event']['won'][1] += 1
                        global_data['farm']['special_event']['won'][1] += 1

    elif crop == 'none':
        data['farm']['normal_farm']['count'] += 1
        global_data['farm']['normal_farm']['count'] += 1
        lines = response.content.lower().split('\n')
        for line in lines:
            if line.startswith('earned '):
                amount = int(line.split('earned ')[1].split(' ')[0].replace(',', ''))
                data['farm']['xp_gained'] += amount

            elif 'carrot have grown' in line:
                amount = int(line.split(' ')[0].replace(',', ''))
                data['farm']['normal_farm']['carrot']['count'] += 1
                data['farm']['normal_farm']['carrot']['resources'] += amount
                global_data['farm']['normal_farm']['carrot']['count'] += 1
                global_data['farm']['normal_farm']['carrot']['resources'] += amount

            elif 'potato have grown' in line:
                amount = int(line.split(' ')[0].replace(',', ''))
                data['farm']['normal_farm']['potato']['count'] += 1
                data['farm']['normal_farm']['potato']['resources'] += amount
                global_data['farm']['normal_farm']['potato']['count'] += 1
                global_data['farm']['normal_farm']['potato']['resources'] += amount

            elif 'bread have grown' in line:
                amount = int(line.split(' ')[0].replace(',', ''))
                data['farm']['normal_farm']['bread']['count'] += 1
                data['farm']['normal_farm']['bread']['resources'] += amount
                global_data['farm']['normal_farm']['bread']['count'] += 1
                global_data['farm']['normal_farm']['bread']['resources'] += amount

            if f"**{message.author.name.lower()}** also got " in line:
                if 'carrot seed' in line:
                    amount = int(
                        line.split(f"**{message.author.name.lower()}** also got ")[1].split(' ')[0].replace(',', ''))
                    data['farm']['special_seeds']['count'] += 1
                    data['farm']['special_seeds']['carrot']['count'] += 1
                    global_data['farm']['special_seeds']['count'] += 1
                    global_data['farm']['special_seeds']['carrot']['count'] += 1
                    if amount < 4:
                        return

                    if amount not in data['farm']['special_seeds']['carrot']['amounts']:
                        data['farm']['special_seeds']['carrot']['amounts'][amount] = amount
                    else:
                        data['farm']['special_seeds']['carrot']['amounts'][amount] += amount

                    if amount not in global_data['farm']['special_seeds']['carrot']['amounts']:
                        global_data['farm']['special_seeds']['carrot']['amounts'][amount] = amount
                    else:
                        global_data['farm']['special_seeds']['carrot']['amounts'][amount] += amount

                elif 'bread seed' in line:
                    amount = int(
                        line.split(f"**{message.author.name.lower()}** also got ")[1].split(' ')[0].replace(',', ''))
                    data['farm']['special_seeds']['count'] += 1
                    data['farm']['special_seeds']['bread']['count'] += 1
                    global_data['farm']['special_seeds']['count'] += 1
                    global_data['farm']['special_seeds']['bread']['count'] += 1
                    if amount < 4:
                        return
                    if amount not in data['farm']['special_seeds']['bread']['amounts']:
                        data['farm']['special_seeds']['bread']['amounts'][amount] = amount
                    else:
                        data['farm']['special_seeds']['bread']['amounts'][amount] += amount

                    if amount not in global_data['farm']['special_seeds']['bread']['amounts']:
                        global_data['farm']['special_seeds']['bread']['amounts'][amount] = amount
                    else:
                        global_data['farm']['special_seeds']['bread']['amounts'][amount] += amount

                elif 'potato seed' in line:
                    amount = int(
                        line.split(f"**{message.author.name.lower()}** also got ")[1].split(' ')[0].replace(',', ''))
                    data['farm']['special_seeds']['count'] += 1
                    data['farm']['special_seeds']['potato']['count'] += 1
                    global_data['farm']['special_seeds']['count'] += 1
                    global_data['farm']['special_seeds']['potato']['count'] += 1
                    if amount < 4:
                        return
                    if amount not in data['farm']['special_seeds']['potato']['amounts']:
                        data['farm']['special_seeds']['potato']['amounts'][amount] = amount
                    else:
                        data['farm']['special_seeds']['potato']['amounts'][amount] += amount

                    if amount not in global_data['farm']['special_seeds']['potato']['amounts']:
                        global_data['farm']['special_seeds']['potato']['amounts'][amount] = amount
                    else:
                        global_data['farm']['special_seeds']['potato']['amounts'][amount] += amount

    elif crop == 'bread':
        data['farm']['using_seed']['count'] += 1
        data['farm']['using_seed']['bread']['count'] += 1
        global_data['farm']['using_seed']['count'] += 1
        global_data['farm']['using_seed']['bread']['count'] += 1

        lines = response.content.lower().split('\n')
        for line in lines:
            if line.startswith('earned '):
                amount = int(line.split('earned ')[1].split(' ')[0].replace(',', ''))
                data['farm']['xp_gained'] += amount
                global_data['farm']['xp_gained'] += amount

            elif 'bread have grown' in line:
                amount = int(line.split(' ')[0].replace(',', ''))
                data['farm']['using_seed']['bread']['resources'] += amount
                global_data['farm']['using_seed']['bread']['resources'] += amount

            if f"**{message.author.name.lower()}** also got " in line:
                amount = int(
                    line.split(f"**{message.author.name.lower()}** also got ")[1].split(' ')[0].replace(',', ''))
                if amount not in data['farm']['using_seed']['bread']['seed_back']:
                    data['farm']['using_seed']['bread']['seed_back'][amount] = 1
                else:
                    data['farm']['using_seed']['bread']['seed_back'][amount] += 1

                if amount not in global_data['farm']['using_seed']['bread']['seed_back']:
                    global_data['farm']['using_seed']['bread']['seed_back'][amount] = 1
                else:
                    global_data['farm']['using_seed']['bread']['seed_back'][amount] += 1

        if f"**{message.author.name.lower()}** also got " not in response.content.lower():
            amount = 0
            if amount not in data['farm']['using_seed']['bread']['seed_back']:
                data['farm']['using_seed']['bread']['seed_back'][amount] = 1
            else:
                data['farm']['using_seed']['bread']['seed_back'][amount] += 1

            if amount not in global_data['farm']['using_seed']['bread']['seed_back']:
                global_data['farm']['using_seed']['bread']['seed_back'][amount] = 1
            else:
                global_data['farm']['using_seed']['bread']['seed_back'][amount] += 1

    elif crop == 'potato':
        data['farm']['using_seed']['count'] += 1
        data['farm']['using_seed']['potato']['count'] += 1
        global_data['farm']['using_seed']['count'] += 1
        global_data['farm']['using_seed']['potato']['count'] += 1

        lines = response.content.lower().split('\n')
        for line in lines:
            if line.startswith('earned '):
                amount = int(line.split('earned ')[1].split(' ')[0].replace(',', ''))
                data['farm']['xp_gained'] += amount
                global_data['farm']['xp_gained'] += amount

            elif 'potato have grown' in line:
                amount = int(line.split(' ')[0].replace(',', ''))
                data['farm']['using_seed']['potato']['resources'] += amount
                global_data['farm']['using_seed']['potato']['resources'] += amount

            if f"**{message.author.name.lower()}** also got " in line:
                amount = int(
                    line.split(f"**{message.author.name.lower()}** also got ")[1].split(' ')[0].replace(',', ''))
                if amount not in data['farm']['using_seed']['potato']['seed_back']:
                    data['farm']['using_seed']['potato']['seed_back'][amount] = 1
                else:
                    data['farm']['using_seed']['potato']['seed_back'][amount] += 1

                if amount not in global_data['farm']['using_seed']['potato']['seed_back']:
                    global_data['farm']['using_seed']['potato']['seed_back'][amount] = 1
                else:
                    global_data['farm']['using_seed']['potato']['seed_back'][amount] += 1

        if f"**{message.author.name.lower()}** also got " not in response.content.lower():
            amount = 0
            if amount not in data['farm']['using_seed']['potato']['seed_back']:
                data['farm']['using_seed']['potato']['seed_back'][amount] = 1
            else:
                data['farm']['using_seed']['potato']['seed_back'][amount] += 1

            if amount not in global_data['farm']['using_seed']['potato']['seed_back']:
                global_data['farm']['using_seed']['potato']['seed_back'][amount] = 1
            else:
                global_data['farm']['using_seed']['potato']['seed_back'][amount] += 1

    elif crop == 'carrot':
        data['farm']['using_seed']['count'] += 1
        data['farm']['using_seed']['carrot']['count'] += 1
        global_data['farm']['using_seed']['count'] += 1
        global_data['farm']['using_seed']['carrot']['count'] += 1

        lines = response.content.lower().split('\n')
        for line in lines:
            if line.startswith('earned '):
                amount = int(line.split('earned ')[1].split(' ')[0].replace(',', ''))
                data['farm']['xp_gained'] += amount
                global_data['farm']['xp_gained'] += amount

            elif 'carrot have grown' in line:
                amount = int(line.split(' ')[0].replace(',', ''))
                data['farm']['using_seed']['carrot']['resources'] += amount
                global_data['farm']['using_seed']['carrot']['resources'] += amount

            if f"**{message.author.name.lower()}** also got " in line:
                amount = int(
                    line.split(f"**{message.author.name.lower()}** also got ")[1].split(' ')[0].replace(',', ''))
                if amount not in data['farm']['using_seed']['carrot']['seed_back']:
                    data['farm']['using_seed']['carrot']['seed_back'][amount] = 1
                else:
                    data['farm']['using_seed']['carrot']['seed_back'][amount] += 1

                if amount not in global_data['farm']['using_seed']['carrot']['seed_back']:
                    global_data['farm']['using_seed']['carrot']['seed_back'][amount] = 1
                else:
                    global_data['farm']['using_seed']['carrot']['seed_back'][amount] += 1

        if f"**{message.author.name.lower()}** also got " not in response.content.lower():
            amount = 0
            if amount not in data['farm']['using_seed']['carrot']['seed_back']:
                data['farm']['using_seed']['carrot']['seed_back'][amount] = 1
            else:
                data['farm']['using_seed']['carrot']['seed_back'][amount] += 1

            if amount not in global_data['farm']['using_seed']['carrot']['seed_back']:
                global_data['farm']['using_seed']['carrot']['seed_back'][amount] = 1
            else:
                global_data['farm']['using_seed']['carrot']['seed_back'][amount] += 1

    database[message.author.id] = data
    database[GLOBAL_USER] = global_data


def is_command_again(message, command):
    # Remove extra spaces from the command
    args = [i for i in message.content.lower().split(' ') if i != '']

    # We need at least 2 words
    if len(args) <= 1:
        return False

    # Make and verify the command
    command_used = args[0] + ' ' + args[1]
    return command_used.startswith(command)


def get_working_command_keywords(command):
    look_for = ''
    if command == 'chainsaw':
        look_for = ("is chopping with __**THREE CHAINSAW**__!!",)
    elif command == 'bowsaw':
        look_for = ("is chopping with **TWO BOW SAW**!",)
    elif command == 'axe':
        look_for = ("is chopping with an **AXE**!",)
    elif command == 'chop':
        look_for = (':woodenlog:', ':EPIClog:', ':SUPERlog:', ':MEGAlog:', ':HYPERlog:', ':ULTRAlog:', ':ULTIMATElog:')

    elif command == 'bigboat':
        look_for = ("is fishing with __**THREE NETS**__!!",)
    elif command == 'boat':
        look_for = ("is fishing with **TWO NETS**!",)
    elif command == 'net':
        look_for = ("is fishing with a **NET**!",)
    elif command == 'fish':
        look_for = (':normiefish:', ':goldenfish:', ':EPICfish:', ':SUPERfish:')

    elif command == 'dynamite':
        look_for = ("is mining with **FOUR DRILLS**!?",)
    elif command == 'drill':
        look_for = ("is mining with **TWO DRILLS**!",)
    elif command == 'pickaxe':
        look_for = ("is mining with **A PICKAXE**!",)
    elif command == 'mine':
        look_for = (':ruby:', ':coin:')

    elif command == 'greenhouse':
        look_for = ("is collecting fruits with **TWO TRACTORS**!!",)
    elif command == 'tractor':
        look_for = ("is collecting fruits with a **TRACTOR**??",)
    elif command == 'ladder':
        look_for = ("is collecting fruits with **BOTH HANDS**!",)
    elif command == 'pickup':
        look_for = (':Apple:', ':Banana:', ':Watermelon:')
    return look_for


async def add_working_commands(message, database, client, command):
    look_for = get_working_command_keywords(command)

    def check(msg: discord.Message):
        if msg.author.id == message.author.id and is_command_again(msg, 'rpg ' + command):
            return True

        if not msg.author.id == EPIC_RPG_ID:
            return False

        if msg.channel.id != message.channel.id:
            return False

        if message.author.name not in msg.content:
            return

        is_working_cmd = False
        for words in look_for:
            if words in msg.content:
                is_working_cmd = True
                break
        return is_working_cmd

    try:
        response = await client.wait_for('message', check=check, timeout=15)
    except asyncio.TimeoutError:
        return

    if is_command_again(response, 'rpg ' + command):
        return

    if "it seems like the river is frozen in this area lmao" in response.content:
        return

    data = database[message.author.id]

    if 'worker' not in data['info']:
        data['info']['worker'] = 99

    worker_level = data['info']['worker']
    if worker_level < 100:
        worker_level = 99

    if f'{GLOBAL_USER}{worker_level}' not in database:
        global_data = get_empty_working()
    else:
        global_data = database[f'{GLOBAL_USER}{worker_level}']

    # channel = client.get_channel(829123769083232276)
    # response = await channel.fetch_message(990505124092837909)
    # message = await channel.fetch_message(990505123300126780)
    # data = database[message.author.id]
    # global_data = database[f'{GLOBAL_USER}{worker_level}']

    if 'area' not in data['info']:
        data['info']['area'] = 0

    area = data['info']['area']

    update_global = True
    if command == 'chainsaw' and area < 9:
        update_global = False
    if command == 'bowsaw' and area < 6:
        update_global = False
    if command == 'axe' and area < 3:
        update_global = False
    if command == 'bigboat' and area < 9:
        update_global = False
    if command == 'boat' and area < 6:
        update_global = False
    if command == 'net' and area < 3:
        update_global = False

    if data['info']['area'] >= 16:
        if 'void_aura' not in global_data:
            global_data['void_aura'] = {}
        if data['info']['area'] not in global_data['void_aura']:
            global_data['void_aura'][area] = {'chop': {'count': 0, 'seen': 0},
                                              'fish': {'count': 0, 'seen': 0},
                                              'pickup': {'count': 0, 'seen': 0}}

        if 'void_aura' not in data['working_commands']:
            data['working_commands']['void_aura'] = {}
        if data['info']['area'] not in data['working_commands']['void_aura']:
            data['working_commands']['void_aura'][area] = {'chop': {'count': 0, 'seen': 0},
                                                           'fish': {'count': 0, 'seen': 0},
                                                           'pickup': {'count': 0, 'seen': 0}}

    if command in ('chainsaw', 'bowsaw', 'axe', 'chop'):
        if data['info']['area'] >= 16:
            data['working_commands']['void_aura'][area]['chop']['count'] += 1
            global_data['void_aura'][area]['chop']['count'] += 1

        data['working_commands'][command]['count'] += 1
        global_data[command]['count'] += 1
        lines = response.content.lower().split('\n')
        for line in lines:
            if 'normie fish in one of the leaves' in line:
                amount = int(line.split(f"the tree had ")[1].split(' ')[0])
                data['working_commands'][command]['bonus']['count'] += 1
                data['working_commands'][command]['bonus']['amount'] += amount

                global_data[command]['bonus']['count'] += 1
                global_data[command]['bonus']['amount'] += amount

            if data['info']['area'] >= 16:
                line = line.replace(f"{message.author.name.lower()}** also got", 'user** also got')
                if f"user** also got " in line:
                    if '__**ultimate log**__' in line:
                        data['working_commands']['void_aura'][area]['chop']['seen'] += 1
                        global_data['void_aura'][area]['chop']['seen'] += 1

            line = line.replace(f'{message.author.name.lower()}** got ', 'user** got ')

            if f"user** got" in line:
                if 'wooden log' in line:
                    amount = int(
                        line.split(f"**user** got ")[1].split(' ')[0].replace(',', ''))
                    data['working_commands'][command]['wooden']['count'] += 1
                    data['working_commands'][command]['wooden']['resources'] += amount

                    global_data[command]['wooden']['count'] += 1
                    global_data[command]['wooden']['resources'] += amount
                elif 'epic log' in line:
                    amount = int(line.split(f"**user** got ")[1].split(' ')[0].replace(',', ''))
                    data['working_commands'][command]['epic']['count'] += 1
                    data['working_commands'][command]['epic']['resources'] += amount
                    global_data[command]['epic']['count'] += 1
                    global_data[command]['epic']['resources'] += amount
                elif 'super log' in line:
                    amount = int(line.split(f"WOO! **user** got ".lower())[1].split(' ')[0].replace(',', ''))
                    data['working_commands'][command]['super']['count'] += 1
                    data['working_commands'][command]['super']['resources'] += amount
                    global_data[command]['super']['count'] += 1
                    global_data[command]['super']['resources'] += amount

                elif '**mega** log' in line:
                    amount = int(line.split(f"**WOOAAAA!! user** got ".lower())[1].split(' ')[0].replace(',', ''))
                    data['working_commands'][command]['mega']['count'] += 1
                    data['working_commands'][command]['mega']['resources'] += amount
                    global_data[command]['mega']['count'] += 1
                    global_data[command]['mega']['resources'] += amount
                elif '**hyper** log' in line:
                    amount = int(
                        line.split(f"**WwWOoOOoOAAa!!!1 user** got ".lower())[1].split(' ')[
                            0].replace(',', ''))
                    data['working_commands'][command]['hyper']['count'] += 1
                    data['working_commands'][command]['hyper']['resources'] += amount
                    global_data[command]['hyper']['count'] += 1
                    global_data[command]['hyper']['resources'] += amount
                elif '__**ultra log**__' in line:
                    amount = int(
                        line.split(f"IS THIS A **DREAM**????? **user** got ".lower())[1].split(
                            ' ')[0].replace(',', ''))
                    data['working_commands'][command]['ultra']['count'] += 1
                    data['working_commands'][command]['ultra']['resources'] += amount
                    global_data[command]['ultra']['count'] += 1
                    global_data[command]['ultra']['resources'] += amount
                elif '__**ultimate log**__' in line:
                    amount = int(line.split(
                        f"**__THIS MAY BE THE LUCKIEST MOMENT OF YOUR LIFE__**... **user** got ".lower())[
                                     1].split(' ')[0].replace(',', ''))
                    data['working_commands'][command]['ultimate']['count'] += 1
                    data['working_commands'][command]['ultimate']['resources'] += amount
                    global_data[command]['ultimate']['count'] += 1
                    global_data[command]['ultimate']['resources'] += amount

    elif command in ('dynamite', 'drill', 'pickaxe', 'mine'):
        data['working_commands'][command]['count'] += 1
        global_data[command]['count'] += 1
        lines = response.content.lower().split('\n')
        for line in lines:
            if 'mined with too much force' in line:
                line = line.replace(f'{message.author.name.lower()}** mined ', 'user** mined ')
                amount = int(line.split(
                    f"**user** mined with too much force, one of the nearby trees got **destroyed** and dropped ")[
                                 1].split(' ')[0].replace(',', ''))
                data['working_commands'][command]['bonus']['count'] += 1
                data['working_commands'][command]['bonus']['amount'] += amount
                global_data[command]['bonus']['count'] += 1
                global_data[command]['bonus']['amount'] += amount
                continue

            line = line.replace(f'{message.author.name.lower()}** got ', 'user** got ')

            if f"**user** got" in line:
                if 'ruby' in line:
                    amount = int(
                        line.split(f"OMG!! **user** got ".lower())[1].split(' ')[0].replace(
                            ',', ''))
                    data['working_commands'][command]['rubies']['count'] += 1
                    data['working_commands'][command]['rubies']['resources'] += amount
                    global_data[command]['rubies']['count'] += 1
                    global_data[command]['rubies']['resources'] += amount

                elif 'coins' in line:
                    amount = int(
                        line.split(f"**user** got ".lower())[1].split(' ')[0].replace(',', ''))
                    data['working_commands'][command]['coins']['count'] += 1
                    data['working_commands'][command]['coins']['resources'] += amount
                    global_data[command]['coins']['count'] += 1
                    global_data[command]['coins']['resources'] += amount

    elif command in ('bigboat', 'boat', 'net', 'fish'):
        if data['info']['area'] >= 16:
            data['working_commands']['void_aura'][area]['fish']['count'] += 1
            global_data['void_aura'][area]['fish']['count'] += 1

        data['working_commands'][command]['count'] += 1
        global_data[command]['count'] += 1

        lines = response.content.lower().split('\n')
        for line in lines:
            if 'for some reason, one of the fish was' in line:
                amount = int(
                    line.split(f"For some reason, one of the fish was carrying ".lower())[1].split(' ')[0].replace(',',
                                                                                                                   ''))
                data['working_commands'][command]['bonus']['count'] += 1
                data['working_commands'][command]['bonus']['amount'] += amount
                global_data[command]['bonus']['count'] += 1
                global_data[command]['bonus']['amount'] += amount

            if data['info']['area'] >= 16:
                line = line.replace(f'{message.author.name.lower()}** also got ', 'user** also got ')
                if f"user** also got " in line:
                    if '__**super fish**__' in line:
                        data['working_commands']['void_aura'][area]['fish']['seen'] += 1
                        global_data['void_aura'][area]['fish']['seen'] += 1

            line = line.replace(f'{message.author.name.lower()}** got ', 'user** got ')
            if f"**user** got" in line:
                if 'normie fish' in line:
                    amount = int(
                        line.split(f"**user** got ".lower())[1].split(' ')[0].replace(',', ''))
                    data['working_commands'][command]['normie']['count'] += 1
                    data['working_commands'][command]['normie']['resources'] += amount
                    global_data[command]['normie']['count'] += 1
                    global_data[command]['normie']['resources'] += amount

                elif 'golden fish' in line:
                    amount = int(
                        line.split(f"**user** got ".lower())[1].split(' ')[0].replace(',', ''))
                    data['working_commands'][command]['golden']['count'] += 1
                    data['working_commands'][command]['golden']['resources'] += amount
                    global_data[command]['golden']['count'] += 1
                    global_data[command]['golden']['resources'] += amount

                elif '**epic fish**' in line:
                    amount = int(
                        line.split(f"OOF! **user** got ".lower())[1].split(' ')[0].replace(',',
                                                                                           ''))
                    data['working_commands'][command]['epic']['count'] += 1
                    data['working_commands'][command]['epic']['resources'] += amount
                    global_data[command]['epic']['count'] += 1
                    global_data[command]['epic']['resources'] += amount

                elif '__**super fish**__' in line:
                    amount = int(
                        line.split(f"OOooOOFFF!! **user** got ".lower())[1].split(' ')[
                            0].replace(',', ''))
                    data['working_commands'][command]['super']['count'] += 1
                    data['working_commands'][command]['super']['resources'] += amount
                    global_data[command]['super']['count'] += 1
                    global_data[command]['super']['resources'] += amount

    elif command in ('greenhouse', 'tractor', 'ladder', 'pickup'):
        if data['info']['area'] >= 16:
            data['working_commands']['void_aura'][area]['pickup']['count'] += 1
            global_data['void_aura'][area]['pickup']['count'] += 1

        data['working_commands'][command]['count'] += 1
        global_data[command]['count'] += 1
        lines = response.content.lower().split('\n')
        for line in lines:
            if 'one of them had ' in line:
                amount = int(line.split(f"One of them had ".lower())[1].split(' ')[0].replace(',', ''))
                data['working_commands'][command]['bonus']['count'] += 1
                data['working_commands'][command]['bonus']['amount'] += amount
                global_data[command]['bonus']['count'] += 1
                global_data[command]['bonus']['amount'] += amount

            if data['info']['area'] >= 16:
                line = line.replace(f'{message.author.name.lower()}** also got ', 'user** also got ')
                if f"user** also got " in line:
                    if '**watermelon**' in line:
                        data['working_commands']['void_aura'][area]['pickup']['seen'] += 1
                        global_data['void_aura'][area]['pickup']['seen'] += 1

            line = line.replace(f'{message.author.name.lower()}** got ', 'user** got ')

            if f"**user** got" in line:
                if 'apple' in line:
                    amount = int(
                        line.split(f"**user** got ".lower())[1].split(' ')[0].replace(',', ''))
                    data['working_commands'][command]['apple']['count'] += 1
                    data['working_commands'][command]['apple']['resources'] += amount
                    global_data[command]['apple']['count'] += 1
                    global_data[command]['apple']['resources'] += amount
                elif 'banana' in line:
                    amount = int(
                        line.split(f"**user** got ".lower())[1].split(' ')[0].replace(',', ''))
                    data['working_commands'][command]['banana']['count'] += 1
                    data['working_commands'][command]['banana']['resources'] += amount
                    global_data[command]['banana']['count'] += 1
                    global_data[command]['banana']['resources'] += amount
                elif '**watermelon**' in line:
                    amount = int(
                        line.split(f"NICE! **user** got ".lower())[1].split(' ')[0].replace(
                            ',', ''))
                    data['working_commands'][command]['watermelon']['count'] += 1
                    data['working_commands'][command]['watermelon']['resources'] += amount
                    global_data[command]['watermelon']['count'] += 1
                    global_data[command]['watermelon']['resources'] += amount

    database[message.author.id] = data

    if update_global:
        database[f'{GLOBAL_USER}{worker_level}'] = global_data


def is_farm__event_embed(embed, name):
    EMBED = embed.to_dict()
    if 'author' in EMBED and f"{name} — farm" in EMBED['author']['name']:
        if 'description' in EMBED and "You planted a seed, but for some reason it's not growing up" in EMBED[
            'description']:
            return True
    return False


async def show_void_aura(channel, author, clean_txt_command, client, database, interaction=None, user=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    if not user:
        last_arg = clean_txt_command.split()[-1]
        if last_arg == 'global':
            userID = str(GLOBAL_USER)
        else:
            userID = str(author.id)

        if get_user(userID):
            try:
                user = await client.fetch_user(get_user(userID))
            except discord.HTTPException:
                user = author
        else:
            user = author

    if len(clean_txt_command.split()) == 6:
        area = clean_txt_command.split()[-2]
    else:
        area = clean_txt_command.split()[-1]

    if user.id not in agrees_to_track_db:
        await send_response(content=f"<@{author.id}> I didn't track anything for this user!")
        return

    try:
        if area[0] == 'a':
            area: int = int(area[1:])
        else:
            area: int = int(area)

    except (IndexError, TypeError, ValueError):
        await send_response(content=
                            f"<@{author.id}> Correct usage: `pog tr void aura <area>`.")
        return

    if user.id not in database:
        await send_response(content=
                            f"<@{author.id}> I don't have any data stored for that user or you used an invalid user ID")
        return

    data = {}
    if user.id == GLOBAL_USER:
        data = {'working_commands': get_empty_working()}
    else:
        data = database[user.id]

    if 'void_aura' not in data['working_commands']:
        data['working_commands']['void_aura'] = {}

    if area not in data['working_commands']['void_aura']:
        data['working_commands']['void_aura'][area] = {'chop': {'count': 0, 'seen': 0},
                                                       'fish': {'count': 0, 'seen': 0},
                                                       'pickup': {'count': 0, 'seen': 0}}

    if user.id == GLOBAL_USER:
        for i in range(99, 150):
            if f"{GLOBAL_USER}{i}" in database:
                add_data = database[f"{GLOBAL_USER}{i}"]

                if 'void_aura' in add_data:
                    for ar in add_data['void_aura']:
                        if ar != area:
                            continue
                        if ar == 21:
                            continue
                        for cmd in add_data['void_aura'][ar]:
                            data['working_commands']['void_aura'][ar][cmd]['count'] += add_data['void_aura'][ar][cmd][
                                'count']
                            data['working_commands']['void_aura'][ar][cmd]['seen'] += add_data['void_aura'][ar][cmd][
                                'seen']

    if not data['working_commands']['void_aura'][area]['pickup']['count']:
        data['working_commands']['void_aura'][area]['pickup']['count'] = 1
    if not data['working_commands']['void_aura'][area]['chop']['count']:
        data['working_commands']['void_aura'][area]['chop']['count'] = 1
    if not data['working_commands']['void_aura'][area]['fish']['count']:
        data['working_commands']['void_aura'][area]['fish']['count'] = 1

    description = f"""**VOID AURA STATS**
> Chop commands
Total commands tracked: {data['working_commands']['void_aura'][area]['chop']['count']}
{EMOJIS['ultimate']} found - {data['working_commands']['void_aura'][area]['chop']['seen']} → ({(data['working_commands']['void_aura'][area]['chop']['seen'] / data['working_commands']['void_aura'][area]['chop']['count']) * 100:.2f}%)

> Fish commands
Total commands tracked: {data['working_commands']['void_aura'][area]['fish']['count']}
{EMOJIS['super_fish']} found - {data['working_commands']['void_aura'][area]['fish']['seen']} → ({(data['working_commands']['void_aura'][area]['fish']['seen'] / data['working_commands']['void_aura'][area]['fish']['count']) * 100:.2f}%)

> Pickup commands
Total commands tracked: {data['working_commands']['void_aura'][area]['pickup']['count']}
{EMOJIS['watermelon']} found - {data['working_commands']['void_aura'][area]['pickup']['seen']} → ({(data['working_commands']['void_aura'][area]['pickup']['seen'] / data['working_commands']['void_aura'][area]['pickup']['count']) * 100:.2f}%)
"""
    embed = discord.Embed(colour=random.randint(0, 0xFFFFFF), description=description)
    embed.set_author(name=f"{user.name}'s void aura stats", icon_url=user.avatar)
    embed.set_footer(text='Use `pog help stats` for the list of stat commands | Pog <3')

    await send_response(embed=embed)


async def show_working_commnad(channel, author, command, clean_text_command, client, database, interaction=None,
                               user=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    worker_level = ''
    if not user:
        last_arg = clean_text_command.split()[-1]
        if last_arg == 'global':
            await send_response(content=
                                f"<@{author.id}> For global data you also need to specify the worker level. Example: `pog tr chainsaw global 105`")
            return
        data = {}

        if '+' in last_arg and 'global' in clean_text_command:
            worker_level = '+'
            try:
                levels = int(last_arg[:-1])
            except (IndexError, TypeError, ValueError):
                await send_response(content=
                                    f"<@{author.id}> Please use `level+` if you want to see the stats for this worker level and above. Example: `100+`, `105+`")
                return
            if levels < 99:
                levels = 99
            data = get_empty_working()
            for i in range(levels, levels + 50):
                if f"{GLOBAL_USER}{i}" in database:
                    add_data = database[f"{GLOBAL_USER}{i}"]
                    for cmd in data:
                        data[cmd]['count'] += add_data[cmd]['count']
                        for resource in data[cmd]:
                            if resource == 'count':
                                continue
                            if resource == 'bonus':
                                data[cmd][resource]['count'] += add_data[cmd][resource]['count']
                                data[cmd][resource]['amount'] += add_data[cmd][resource]['amount']
                            else:
                                data[cmd][resource]['count'] += add_data[cmd][resource]['count']
                                data[cmd][resource]['resources'] += add_data[cmd][resource]['resources']
            last_arg = str(GLOBAL_USER)

        elif last_arg.isnumeric() and 'global' in clean_text_command:
            worker_level = int(last_arg)
            if worker_level < 99:
                await send_response(content=
                                    f"<@{author.id}> Sorry, I only store data separately for worker levels above 100, for "
                                    f"all worker levels under 100 use `99`, and 101+ for all worker levels over 100 combined.")
                return
            worker_level = f"{worker_level}"
            last_arg = str(GLOBAL_USER)

        if get_user(last_arg):
            try:
                user = await client.fetch_user(get_user(last_arg))
            except discord.HTTPException:
                user = author
        else:
            user = author

    if user.id not in agrees_to_track_db:
        await send_response(content=f"<@{author.id}> I didn't track anything for this user!")
        return

    if user.id not in database:
        await send_response(content=
                            f"<@{author.id}> I don't have any data stored for that user or you used an invalid user ID")
        return

    if worker_level == '+':
        data = {'working_commands': data}

    elif user.id == GLOBAL_USER:
        if f"{GLOBAL_USER}{worker_level}" not in database:
            await send_response(content=
                                f"<@{author.id}> I don't have any data stored for that worker level yet!")
            return
        data = database[f"{GLOBAL_USER}{worker_level}"]
        data = {'working_commands': data}
    else:
        data = database[user.id]

    text = ''
    total = data['working_commands'][command]['count']
    if data['working_commands'][command]['count'] == 0:
        data['working_commands'][command]['count'] = 1
        total = '0'

    # total_count = 0
    # for item in data['working_commands'][command]:
    #     if item in ('bonus', 'count') :
    #         continue
    #     (data['working_commands'][command][item]['count'])
    #     total_count += data['working_commands'][command][item]['count']
    #
    # if total_count != total and total_count != 0:
    #     total = total_count
    #     data['working_commands'][command]['count'] = total_count

    if command in ('chainsaw', 'bowsaw', 'axe', 'chop'):
        text = f"""**{command.upper()} STATS**
        
🌲 **Total commands tracked:** {total}
> **You found**:
`x{data['working_commands'][command]['wooden']['count']}` {EMOJIS['wooden']} Wooden log - `col:` {data['working_commands'][command]['wooden']['resources']:,} → ({(data['working_commands'][command]['wooden']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
`x{data['working_commands'][command]['epic']['count']}` {EMOJIS['epic_log']} EPIC log - `col:` {data['working_commands'][command]['epic']['resources']:,} → ({(data['working_commands'][command]['epic']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
`x{data['working_commands'][command]['super']['count']}` {EMOJIS['super']} SUPER log - `col:` {data['working_commands'][command]['super']['resources']:,} → ({(data['working_commands'][command]['super']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
`x{data['working_commands'][command]['mega']['count']}` {EMOJIS['mega']} **MEGA** log - `col:` {data['working_commands'][command]['mega']['resources']:,} → ({(data['working_commands'][command]['mega']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
`x{data['working_commands'][command]['hyper']['count']}` {EMOJIS['hyper']} **HYPER** log - `col:` {data['working_commands'][command]['hyper']['resources']:,} → ({(data['working_commands'][command]['hyper']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
`x{data['working_commands'][command]['ultra']['count']}` {EMOJIS['ultra']} **ULTRA** log - `col:` {data['working_commands'][command]['ultra']['resources']:,} → ({(data['working_commands'][command]['ultra']['count'] / data['working_commands'][command]['count']) * 100}%)
`x{data['working_commands'][command]['ultimate']['count']}` {EMOJIS['ultimate']} __**ULTIMATE log**__ - `col:` {data['working_commands'][command]['ultimate']['resources']:,} → ({(data['working_commands'][command]['ultimate']['count'] / data['working_commands'][command]['count']) * 100}%)

> **Worker 101+ procs:**
`x{data['working_commands'][command]['bonus']['count']}` {EMOJIS['fish']} Normie fish - `col:` {data['working_commands'][command]['bonus']['amount']:,} → ({(data['working_commands'][command]['bonus']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
ㅤ
"""
    elif command in ('dynamite', 'drill', 'pickaxe', 'mine'):
        text = f"""**{command.upper()} STATS**

🌲 **Total commands tracked:** {total}
> **You found**:
`x{data['working_commands'][command]['rubies']['count']}` {EMOJIS['ruby']} Ruby - `col:` {data['working_commands'][command]['rubies']['resources']:,} → ({(data['working_commands'][command]['rubies']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
`x{data['working_commands'][command]['coins']['count']}` {EMOJIS['coin']} Coins - `col:` {data['working_commands'][command]['coins']['resources']:,} → ({(data['working_commands'][command]['coins']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)

> **Worker 101+ procs:**
`x{data['working_commands'][command]['bonus']['count']}` {EMOJIS['super']} SUPER log - `col:` {data['working_commands'][command]['bonus']['amount']:,} → ({(data['working_commands'][command]['bonus']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
ㅤ
"""
    elif command in ('bigboat', 'boat', 'net', 'fish'):
        text = f"""**{command.upper()} STATS**

🌲 **Total commands tracked:** {total}
> **You found**:
`x{data['working_commands'][command]['normie']['count']}` {EMOJIS['fish']} normie fish - `col:` {data['working_commands'][command]['normie']['resources']:,} → ({(data['working_commands'][command]['normie']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
`x{data['working_commands'][command]['golden']['count']}` {EMOJIS['golden']} Golden fish - `col:` {data['working_commands'][command]['golden']['resources']:,} → ({(data['working_commands'][command]['golden']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
`x{data['working_commands'][command]['epic']['count']}` {EMOJIS['epic_fish']} **EPIC** fish - `col:` {data['working_commands'][command]['epic']['resources']:,} → ({(data['working_commands'][command]['epic']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
`x{data['working_commands'][command]['super']['count']}` {EMOJIS['super_fish']} __**SUPER fish**__ - `col:` {data['working_commands'][command]['super']['resources']:,} → ({(data['working_commands'][command]['super']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)

> **Worker 101+ procs:**
`x{data['working_commands'][command]['bonus']['count']}` {EMOJIS['banana']} Banana - `col:` {data['working_commands'][command]['bonus']['amount']:,} → ({(data['working_commands'][command]['bonus']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
ㅤ
"""
    elif command in ('greenhouse', 'tractor', 'ladder', 'pickup'):
        text = f"""**{command.upper()} STATS**

🌲 **Total commands tracked:** {total}
> **You found**:
`x{data['working_commands'][command]['apple']['count']}` {EMOJIS['apple']} Apple - `col:` {data['working_commands'][command]['apple']['resources']:,} → ({(data['working_commands'][command]['apple']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
`x{data['working_commands'][command]['banana']['count']}` {EMOJIS['banana']} Banana - `col:` {data['working_commands'][command]['banana']['resources']:,} → ({(data['working_commands'][command]['banana']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
`x{data['working_commands'][command]['watermelon']['count']}` {EMOJIS['watermelon']} Watermelon - `col:` {data['working_commands'][command]['watermelon']['resources']:,} → ({(data['working_commands'][command]['watermelon']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)

> **Worker 101+ procs:**
`x{data['working_commands'][command]['bonus']['count']}` {EMOJIS['ruby']} Ruby - `col:` {data['working_commands'][command]['bonus']['amount']:,} → ({(data['working_commands'][command]['bonus']['count'] / data['working_commands'][command]['count']) * 100:.2f}%)
ㅤ
"""
    embed = discord.Embed(colour=random.randint(0, 0xFFFFFF), description=text)
    embed.set_author(name=f"{user.name}'s {command} stats", icon_url=user.avatar)
    embed.set_footer(text='Use `pog help stats` for the list of stat commands | Pog <3')

    await send_response(embed=embed)


def add_lbs_and_drops(command_type, data, split_hunt, hunt_type, lower_player_name):
    for line in split_hunt:
        if f"**{lower_player_name}** got" in line:
            amount = int(line.split(f"**{lower_player_name}** got ")[1].split(' ')[0])
            line = line.replace(f"**{lower_player_name}** got ", '')

            if 'wolf skin' in line:
                data[command_type][hunt_type]['mob_drops']['wolf_skin']['seen'] += 1
                data[command_type][hunt_type]['mob_drops']['total'] += 1
                data[command_type][hunt_type]['mob_drops']['wolf_skin']['found'] += amount
            elif 'zombie eye' in line:
                data[command_type][hunt_type]['mob_drops']['zombie_eye']['seen'] += 1
                data[command_type][hunt_type]['mob_drops']['total'] += 1
                data[command_type][hunt_type]['mob_drops']['zombie_eye']['found'] += amount
            elif 'unicorn horn' in line:
                data[command_type][hunt_type]['mob_drops']['unicorn_horn']['seen'] += 1
                data[command_type][hunt_type]['mob_drops']['total'] += 1
                data[command_type][hunt_type]['mob_drops']['unicorn_horn']['found'] += amount
            elif 'mermaid hair' in line:
                data[command_type][hunt_type]['mob_drops']['mermaid_hair']['seen'] += 1
                data[command_type][hunt_type]['mob_drops']['total'] += 1
                data[command_type][hunt_type]['mob_drops']['mermaid_hair']['found'] += amount
            elif 'chip' in line:
                data[command_type][hunt_type]['mob_drops']['chip']['seen'] += 1
                data[command_type][hunt_type]['mob_drops']['total'] += 1
                data[command_type][hunt_type]['mob_drops']['chip']['found'] += amount
            elif 'dragon scale' in line:
                data[command_type][hunt_type]['mob_drops']['dragon_scale']['seen'] += 1
                data[command_type][hunt_type]['mob_drops']['total'] += 1
                data[command_type][hunt_type]['mob_drops']['dragon_scale']['found'] += amount
            elif 'dark energy' in line:
                data[command_type][hunt_type]['mob_drops']['dark_energy']['seen'] += 1
                data[command_type][hunt_type]['mob_drops']['total'] += 1
                data[command_type][hunt_type]['mob_drops']['dark_energy']['found'] += amount

            elif 'uncommon lootbox' in line:
                data[command_type][hunt_type]['lootboxes']['uncommon']['seen'] += 1
                data[command_type][hunt_type]['lootboxes']['total'] += 1
                data[command_type][hunt_type]['lootboxes']['uncommon']['found'] += amount
            elif 'common lootbox' in line:
                data[command_type][hunt_type]['lootboxes']['common']['seen'] += 1
                data[command_type][hunt_type]['lootboxes']['total'] += 1
                data[command_type][hunt_type]['lootboxes']['common']['found'] += amount
            elif 'rare lootbox' in line:
                data[command_type][hunt_type]['lootboxes']['rare']['seen'] += 1
                data[command_type][hunt_type]['lootboxes']['total'] += 1
                data[command_type][hunt_type]['lootboxes']['rare']['found'] += amount
            elif 'epic lootbox' in line:
                data[command_type][hunt_type]['lootboxes']['epic']['seen'] += 1
                data[command_type][hunt_type]['lootboxes']['total'] += 1
                data[command_type][hunt_type]['lootboxes']['epic']['found'] += amount
            elif 'edgy lootbox' in line:
                data[command_type][hunt_type]['lootboxes']['edgy']['seen'] += 1
                data[command_type][hunt_type]['lootboxes']['total'] += 1
                data[command_type][hunt_type]['lootboxes']['edgy']['found'] += amount
            elif 'omega lootbox' in line:
                data[command_type][hunt_type]['lootboxes']['omega']['seen'] += 1
                data[command_type][hunt_type]['lootboxes']['total'] += 1
                data[command_type][hunt_type]['lootboxes']['omega']['found'] += amount
            elif 'godly lootbox' in line:
                data[command_type][hunt_type]['lootboxes']['godly']['seen'] += 1
                data[command_type][hunt_type]['lootboxes']['total'] += 1
                data[command_type][hunt_type]['lootboxes']['godly']['found'] += amount
            elif 'void lootbox' in line:
                data[command_type][hunt_type]['lootboxes']['void']['seen'] += 1
                data[command_type][hunt_type]['lootboxes']['total'] += 1
                data[command_type][hunt_type]['lootboxes']['void']['found'] += amount

            elif 'dark energy' in line:
                data[command_type][hunt_type]['dark_energy'] += 1

    return data


def get_player_area(mob) -> int:
    mob = mob.upper()
    if mob in ('WOLF', 'SLIME', 'GOBLIN'):
        return 1

    elif mob in ('WOLF', 'NYMPH', 'SKELETON'):
        return 2

    elif mob in ('ZOMBIE', 'GHOST', 'BABY DEMON'):
        return 3

    elif mob in ('ZOMBIE', 'WITCH', 'IMP'):
        return 4

    elif mob in ('UNICORN', 'GHOUL', 'GIANT SCORPION'):
        return 5

    elif mob in ('UNICORN', 'SORCERER', 'BABY ROBOT'):
        return 6

    elif mob in ('MERMAID', 'CECAELIA', 'GIANT PIRANHA'):
        return 7

    elif mob in ('MERMAID', 'NEREID', 'GIANT CROCODILE'):
        return 8

    elif mob in ('KILLER ROBOT', 'DEMON', 'HARPY'):
        return 9

    elif mob in ('MANTICORE', 'DULLAHAN'):
        return 10

    elif mob in ('SCALED BABY DRAGON', 'BABY DRAGON', 'YOUNG DRAGON'):
        return 11

    elif mob in ('KID DRAGON', 'SCALED KID DRAGON', 'NOT SO YOUNG DRAGON'):
        return 12

    elif mob in ('TEEN DRAGON', 'SCALED TEEN DRAGON', 'DEFINITELY NOT YOUNG DRAGON'):
        return 13

    elif mob in ('ADULT DRAGON', 'SCALED ADULT DRAGON', 'NOT YOUNG AT ALL DRAGON'):
        return 14

    elif mob in ('OLD DRAGON', 'SCALED OLD DRAGON', 'HOW DO YOU DARE CALL THIS DRAGON \"YOUNG\"???'):
        return 15

    elif mob == 'EPIC NPC':
        return 15.1

    elif mob in ('VOID FRAGMENT', 'VOID PARTICLES', 'VOID SHARD'):
        return 16

    elif mob in ('ABYSS BUG', 'NOTHING', 'SHADOW HANDS'):
        return 17

    return 0


def tier_10_add_lbs_and_drops(command_type, data, split_hunt, mode, lower_player_name):
    if data['tier_10']['has_t10']:
        data['tier_10'][command_type][mode]['count'] += 1

    for line in split_hunt:
        if f"**{lower_player_name}** got" in line:
            amount = int(line.split(f"**{lower_player_name}** got ")[1].split(' ')[0])
            line = line.replace(f"**{lower_player_name}** got ", '')

            if amount <= 1:
                continue

            if amount > 1 and not data['tier_10']['has_t10']:
                data['info']['horse_tier'] = 'T10'
                data['tier_10']['has_t10'] = True

            if 'wolf skin' in line:
                data['tier_10'][command_type][mode]['mob_drops']['total'] += 1
                if amount not in data['tier_10'][command_type][mode]['mob_drops']:
                    data['tier_10'][command_type][mode]['mob_drops'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['mob_drops'][amount] += 1

            elif 'zombie eye' in line:
                data['tier_10'][command_type][mode]['mob_drops']['total'] += 1
                if amount not in data['tier_10'][command_type][mode]['mob_drops']:
                    data['tier_10'][command_type][mode]['mob_drops'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['mob_drops'][amount] += 1

            elif 'unicorn horn' in line:
                data['tier_10'][command_type][mode]['mob_drops']['total'] += 1
                if amount not in data['tier_10'][command_type][mode]['mob_drops']:
                    data['tier_10'][command_type][mode]['mob_drops'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['mob_drops'][amount] += 1

            elif 'mermaid hair' in line:
                data['tier_10'][command_type][mode]['mob_drops']['total'] += 1
                if amount not in data['tier_10'][command_type][mode]['mob_drops']:
                    data['tier_10'][command_type][mode]['mob_drops'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['mob_drops'][amount] += 1

            elif 'chip' in line:
                data['tier_10'][command_type][mode]['mob_drops']['total'] += 1
                if amount not in data['tier_10'][command_type][mode]['mob_drops']:
                    data['tier_10'][command_type][mode]['mob_drops'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['mob_drops'][amount] += 1

            elif 'dragon scale' in line:
                data['tier_10'][command_type][mode]['mob_drops']['total'] += 1
                if amount not in data['tier_10'][command_type][mode]['mob_drops']:
                    data['tier_10'][command_type][mode]['mob_drops'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['mob_drops'][amount] += 1

            elif 'dark energy' in line:
                data['tier_10'][command_type][mode]['mob_drops']['total'] += 1
                if amount not in data['tier_10'][command_type][mode]['mob_drops']:
                    data['tier_10'][command_type][mode]['mob_drops'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['mob_drops'][amount] += 1

            elif 'uncommon lootbox' in line:
                data['tier_10'][command_type][mode]['lootboxes']['total'] += 1

                if amount not in data['tier_10'][command_type][mode]['lootboxes']['uncommon']:
                    data['tier_10'][command_type][mode]['lootboxes']['uncommon'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['lootboxes']['uncommon'][amount] += 1

            elif 'common lootbox' in line:
                data['tier_10'][command_type][mode]['lootboxes']['total'] += 1

                if amount not in data['tier_10'][command_type][mode]['lootboxes']['common']:
                    data['tier_10'][command_type][mode]['lootboxes']['common'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['lootboxes']['common'][amount] += 1

            elif 'rare lootbox' in line:
                data['tier_10'][command_type][mode]['lootboxes']['total'] += 1

                if amount not in data['tier_10'][command_type][mode]['lootboxes']['rare']:
                    data['tier_10'][command_type][mode]['lootboxes']['rare'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['lootboxes']['rare'][amount] += 1

            elif 'epic lootbox' in line:
                data['tier_10'][command_type][mode]['lootboxes']['total'] += 1

                if amount not in data['tier_10'][command_type][mode]['lootboxes']['epic']:
                    data['tier_10'][command_type][mode]['lootboxes']['epic'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['lootboxes']['epic'][amount] += 1

            elif 'edgy lootbox' in line:
                data['tier_10'][command_type][mode]['lootboxes']['total'] += 1

                if amount not in data['tier_10'][command_type][mode]['lootboxes']['edgy']:
                    data['tier_10'][command_type][mode]['lootboxes']['edgy'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['lootboxes']['edgy'][amount] += 1

            elif 'omega lootbox' in line:
                data['tier_10'][command_type][mode]['lootboxes']['total'] += 1

                if amount not in data['tier_10'][command_type][mode]['lootboxes']['omega']:
                    data['tier_10'][command_type][mode]['lootboxes']['omega'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['lootboxes']['omega'][amount] += 1

            elif 'godly lootbox' in line:
                data['tier_10'][command_type][mode]['lootboxes']['total'] += 1

                if amount not in data['tier_10'][command_type][mode]['lootboxes']['godly']:
                    data['tier_10'][command_type][mode]['lootboxes']['godly'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['lootboxes']['godly'][amount] += 1

            elif 'void lootbox' in line:
                data['tier_10'][command_type][mode]['lootboxes']['total'] += 1

                if amount not in data['tier_10'][command_type][mode]['lootboxes']['void']:
                    data['tier_10'][command_type][mode]['lootboxes']['void'][amount] = 1
                else:
                    data['tier_10'][command_type][mode]['lootboxes']['void'][amount] += 1

    return data


def add_per_mob_lbs_and_drops(command_type, data, split_hunt, mode, lower_player_name, mob_lower, is_global=False):
    if mob_lower not in data[command_type][mode]:
        if command_type == 'hunt':
            data[command_type][mode][mob_lower] = {
                'count': 0,
                'coins_gained': 0,
                'xp_gained': 0,
                'mob_drops': {'total': 0,
                              'wolf_skin': {'found': 0},
                              'zombie_eye': {'found': 0},
                              'unicorn_horn': {'found': 0},
                              'mermaid_hair': {'found': 0},
                              'chip': {'found': 0},
                              'dragon_scale': {'found': 0},
                              'dark_energy': {'found': 0}},

                'lootboxes': {'total': 0,
                              'common': {'found': 0},
                              'uncommon': {'found': 0},
                              'rare': {'found': 0},
                              'epic': {'found': 0},
                              'edgy': {'found': 0},
                              'omega': {'found': 0},
                              'godly': {'found': 0},
                              'void': {'found': 0}}}
        elif command_type == 'adventure':
            data[command_type][mode][mob_lower] = {
                'count': 0,
                'coins_gained': 0,
                'xp_gained': 0,
                'lootboxes': {'total': 0,
                              'common': {'found': 0},
                              'uncommon': {'found': 0},
                              'rare': {'found': 0},
                              'epic': {'found': 0},
                              'edgy': {'found': 0},
                              'omega': {'found': 0},
                              'godly': {'found': 0},
                              'void': {'found': 0}}}

    for line in split_hunt:
        if f"**{lower_player_name}** got" in line:
            amount = int(line.split(f"**{lower_player_name}** got ")[1].split(' ')[0])
            line = line.replace(f"**{lower_player_name}** got ", '')

            if 'uncommon lootbox' in line:
                if amount not in data[command_type][mode][mob_lower]['lootboxes']['uncommon']:
                    data[command_type][mode][mob_lower]['lootboxes']['uncommon'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['lootboxes']['uncommon'][amount] += 1

                data[command_type][mode][mob_lower]['lootboxes']['total'] += 1
                data[command_type][mode][mob_lower]['lootboxes']['uncommon']['found'] += amount
            elif 'common lootbox' in line:
                if amount not in data[command_type][mode][mob_lower]['lootboxes']['common']:
                    data[command_type][mode][mob_lower]['lootboxes']['common'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['lootboxes']['common'][amount] += 1

                data[command_type][mode][mob_lower]['lootboxes']['total'] += 1
                data[command_type][mode][mob_lower]['lootboxes']['common']['found'] += amount

            elif 'rare lootbox' in line:
                if amount not in data[command_type][mode][mob_lower]['lootboxes']['rare']:
                    data[command_type][mode][mob_lower]['lootboxes']['rare'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['lootboxes']['rare'][amount] += 1

                data[command_type][mode][mob_lower]['lootboxes']['total'] += 1
                data[command_type][mode][mob_lower]['lootboxes']['rare']['found'] += amount

            elif 'epic lootbox' in line:
                if amount not in data[command_type][mode][mob_lower]['lootboxes']['epic']:
                    data[command_type][mode][mob_lower]['lootboxes']['epic'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['lootboxes']['epic'][amount] += 1

                data[command_type][mode][mob_lower]['lootboxes']['total'] += 1
                data[command_type][mode][mob_lower]['lootboxes']['epic']['found'] += amount

            elif 'edgy lootbox' in line:
                if amount not in data[command_type][mode][mob_lower]['lootboxes']['edgy']:
                    data[command_type][mode][mob_lower]['lootboxes']['edgy'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['lootboxes']['edgy'][amount] += 1

                data[command_type][mode][mob_lower]['lootboxes']['total'] += 1
                data[command_type][mode][mob_lower]['lootboxes']['edgy']['found'] += amount

            elif 'omega lootbox' in line:
                if amount not in data[command_type][mode][mob_lower]['lootboxes']['omega']:
                    data[command_type][mode][mob_lower]['lootboxes']['omega'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['lootboxes']['omega'][amount] += 1

                data[command_type][mode][mob_lower]['lootboxes']['total'] += 1
                data[command_type][mode][mob_lower]['lootboxes']['omega']['found'] += amount

            elif 'godly lootbox' in line:
                if amount not in data[command_type][mode][mob_lower]['lootboxes']['godly']:
                    data[command_type][mode][mob_lower]['lootboxes']['godly'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['lootboxes']['godly'][amount] += 1

                data[command_type][mode][mob_lower]['lootboxes']['total'] += 1
                data[command_type][mode][mob_lower]['lootboxes']['godly']['found'] += amount

            elif 'void lootbox' in line:
                if amount not in data[command_type][mode][mob_lower]['lootboxes']['void']:
                    data[command_type][mode][mob_lower]['lootboxes']['void'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['lootboxes']['void'][amount] += 1

                data[command_type][mode][mob_lower]['lootboxes']['total'] += 1
                data[command_type][mode][mob_lower]['lootboxes']['void']['found'] += amount

            if mode == 'adventure':
                continue

            if 'wolf skin' in line:
                if amount not in data[command_type][mode][mob_lower]['mob_drops']['wolf_skin']:
                    data[command_type][mode][mob_lower]['mob_drops']['wolf_skin'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['mob_drops']['wolf_skin'][amount] += 1

                data[command_type][mode][mob_lower]['mob_drops']['total'] += 1
                data[command_type][mode][mob_lower]['mob_drops']['wolf_skin']['found'] += amount
            elif 'zombie eye' in line:
                if amount not in data[command_type][mode][mob_lower]['mob_drops']['zombie_eye']:
                    data[command_type][mode][mob_lower]['mob_drops']['zombie_eye'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['mob_drops']['zombie_eye'][amount] += 1

                data[command_type][mode][mob_lower]['mob_drops']['total'] += 1
                data[command_type][mode][mob_lower]['mob_drops']['zombie_eye']['found'] += amount
            elif 'unicorn horn' in line:
                if amount not in data[command_type][mode][mob_lower]['mob_drops']['unicorn_horn']:
                    data[command_type][mode][mob_lower]['mob_drops']['unicorn_horn'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['mob_drops']['unicorn_horn'][amount] += 1

                data[command_type][mode][mob_lower]['mob_drops']['total'] += 1
                data[command_type][mode][mob_lower]['mob_drops']['unicorn_horn']['found'] += amount
            elif 'mermaid hair' in line:
                if amount not in data[command_type][mode][mob_lower]['mob_drops']['mermaid_hair']:
                    data[command_type][mode][mob_lower]['mob_drops']['mermaid_hair'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['mob_drops']['mermaid_hair'][amount] += 1

                data[command_type][mode][mob_lower]['mob_drops']['total'] += 1
                data[command_type][mode][mob_lower]['mob_drops']['mermaid_hair']['found'] += amount
            elif 'chip' in line:
                if amount not in data[command_type][mode][mob_lower]['mob_drops']['chip']:
                    data[command_type][mode][mob_lower]['mob_drops']['chip'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['mob_drops']['chip'][amount] += 1

                data[command_type][mode][mob_lower]['mob_drops']['total'] += 1
                data[command_type][mode][mob_lower]['mob_drops']['chip']['found'] += amount

            elif 'dragon scale' in line:
                if amount not in data[command_type][mode][mob_lower]['mob_drops']['dragon_scale']:
                    data[command_type][mode][mob_lower]['mob_drops']['dragon_scale'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['mob_drops']['dragon_scale'][amount] += 1

                data[command_type][mode][mob_lower]['mob_drops']['total'] += 1
                data[command_type][mode][mob_lower]['mob_drops']['dragon_scale']['found'] += amount

            elif 'dark energy' in line:
                if amount not in data[command_type][mode][mob_lower]['mob_drops']['dark_energy']:
                    data[command_type][mode][mob_lower]['mob_drops']['dark_energy'][amount] = 1
                else:
                    data[command_type][mode][mob_lower]['mob_drops']['dark_energy'][amount] += 1

                data[command_type][mode][mob_lower]['mob_drops']['total'] += 1
                data[command_type][mode][mob_lower]['mob_drops']['dark_energy']['found'] += amount
    return data


def get_global_mob_data(command):
    if command == 'hunt':
        return {
            'count': 0,
            'coins_gained': 0,
            'xp_gained': 0,
            'mob_drops': {'total': 0,
                          'wolf_skin': {'found': 0},
                          'zombie_eye': {'found': 0},
                          'unicorn_horn': {'found': 0},
                          'mermaid_hair': {'found': 0},
                          'chip': {'found': 0},
                          'dragon_scale': {'found': 0},
                          'dark_energy': {'found': 0}},

            'lootboxes': {'total': 0,
                          'common': {'found': 0},
                          'uncommon': {'found': 0},
                          'rare': {'found': 0},
                          'epic': {'found': 0},
                          'edgy': {'found': 0},
                          'omega': {'found': 0},
                          'godly': {'found': 0},
                          'void': {'found': 0}}}
    elif command == 'adventure':
        return {
            'count': 0,
            'coins_gained': 0,
            'xp_gained': 0,
            'lootboxes': {'total': 0,
                          'common': {'found': 0},
                          'uncommon': {'found': 0},
                          'rare': {'found': 0},
                          'epic': {'found': 0},
                          'edgy': {'found': 0},
                          'omega': {'found': 0},
                          'godly': {'found': 0},
                          'void': {'found': 0}}}


def add_global_mob_data(split_hunt, lower_player_name, coins, xp, data):
    data['count'] += 1
    data['xp_gained'] += xp
    data['coins_gained'] += coins

    for line in split_hunt:
        if f"**{lower_player_name}** got" in line:
            amount = int(line.split(f"**{lower_player_name}** got ")[1].split(' ')[0])
            line = line.replace(f"**{lower_player_name}** got ", '')

            if 'uncommon lootbox' in line:
                if amount not in data['lootboxes']['uncommon']:
                    data['lootboxes']['uncommon'][amount] = 1
                else:
                    data['lootboxes']['uncommon'][amount] += 1

                data['lootboxes']['total'] += 1
                data['lootboxes']['uncommon']['found'] += amount
            elif 'common lootbox' in line:
                if amount not in data['lootboxes']['common']:
                    data['lootboxes']['common'][amount] = 1
                else:
                    data['lootboxes']['common'][amount] += 1

                data['lootboxes']['total'] += 1
                data['lootboxes']['common']['found'] += amount

            elif 'rare lootbox' in line:
                if amount not in data['lootboxes']['rare']:
                    data['lootboxes']['rare'][amount] = 1
                else:
                    data['lootboxes']['rare'][amount] += 1

                data['lootboxes']['total'] += 1
                data['lootboxes']['rare']['found'] += amount

            elif 'epic lootbox' in line:
                if amount not in data['lootboxes']['epic']:
                    data['lootboxes']['epic'][amount] = 1
                else:
                    data['lootboxes']['epic'][amount] += 1

                data['lootboxes']['total'] += 1
                data['lootboxes']['epic']['found'] += amount

            elif 'edgy lootbox' in line:
                if amount not in data['lootboxes']['edgy']:
                    data['lootboxes']['edgy'][amount] = 1
                else:
                    data['lootboxes']['edgy'][amount] += 1

                data['lootboxes']['total'] += 1
                data['lootboxes']['edgy']['found'] += amount

            elif 'omega lootbox' in line:
                if amount not in data['lootboxes']['omega']:
                    data['lootboxes']['omega'][amount] = 1
                else:
                    data['lootboxes']['omega'][amount] += 1

                data['lootboxes']['total'] += 1
                data['lootboxes']['omega']['found'] += amount

            elif 'godly lootbox' in line:
                if amount not in data['lootboxes']['godly']:
                    data['lootboxes']['godly'][amount] = 1
                else:
                    data['lootboxes']['godly'][amount] += 1

                data['lootboxes']['total'] += 1
                data['lootboxes']['godly']['found'] += amount

            elif 'void lootbox' in line:
                if amount not in data['lootboxes']['void']:
                    data['lootboxes']['void'][amount] = 1
                else:
                    data['lootboxes']['void'][amount] += 1

                data['lootboxes']['total'] += 1
                data['lootboxes']['void']['found'] += amount

            if 'wolf skin' in line:
                if amount not in data['mob_drops']['wolf_skin']:
                    data['mob_drops']['wolf_skin'][amount] = 1
                else:
                    data['mob_drops']['wolf_skin'][amount] += 1

                data['mob_drops']['total'] += 1
                data['mob_drops']['wolf_skin']['found'] += amount
            elif 'zombie eye' in line:
                if amount not in data['mob_drops']['zombie_eye']:
                    data['mob_drops']['zombie_eye'][amount] = 1
                else:
                    data['mob_drops']['zombie_eye'][amount] += 1

                data['mob_drops']['total'] += 1
                data['mob_drops']['zombie_eye']['found'] += amount
            elif 'unicorn horn' in line:
                if amount not in data['mob_drops']['unicorn_horn']:
                    data['mob_drops']['unicorn_horn'][amount] = 1
                else:
                    data['mob_drops']['unicorn_horn'][amount] += 1

                data['mob_drops']['total'] += 1
                data['mob_drops']['unicorn_horn']['found'] += amount
            elif 'mermaid hair' in line:
                if amount not in data['mob_drops']['mermaid_hair']:
                    data['mob_drops']['mermaid_hair'][amount] = 1
                else:
                    data['mob_drops']['mermaid_hair'][amount] += 1

                data['mob_drops']['total'] += 1
                data['mob_drops']['mermaid_hair']['found'] += amount
            elif 'chip' in line:
                if amount not in data['mob_drops']['chip']:
                    data['mob_drops']['chip'][amount] = 1
                else:
                    data['mob_drops']['chip'][amount] += 1

                data['mob_drops']['total'] += 1
                data['mob_drops']['chip']['found'] += amount

            elif 'dragon scale' in line:
                if amount not in data['mob_drops']['dragon_scale']:
                    data['mob_drops']['dragon_scale'][amount] = 1
                else:
                    data['mob_drops']['dragon_scale'][amount] += 1

                data['mob_drops']['total'] += 1
                data['mob_drops']['dragon_scale']['found'] += amount

            elif 'dark energy' in line:
                if amount not in data['mob_drops']['dark_energy']:
                    data['mob_drops']['dark_energy'][amount] = 1
                else:
                    data['mob_drops']['dark_energy'][amount] += 1

                data['mob_drops']['total'] += 1
                data['mob_drops']['dark_energy']['found'] += amount

    return data


async def add_adventure(message: discord.Message, database: sqlitedict.SqliteDict, client, mob_database):
    def check(msg: discord.Message):
        if msg.author.id == message.author.id and is_command_again(msg, 'rpg adv'):
            return True

        if not msg.author.id == EPIC_RPG_ID:
            return False

        if msg.channel.id != message.channel.id:
            return False

        is_adv = False
        for mob in ADV_MOB_NAMES:
            if mob in msg.content:
                is_adv = True
                break

        return message.author.name in msg.content and is_adv

    try:
        response = await client.wait_for('message', check=check, timeout=15)
    except asyncio.TimeoutError:
        return

    if is_command_again(response, 'rpg adv'):
        return

    data = database[message.author.id]
    mob_data = mob_database[message.author.id]

    global_data = database[GLOBAL_USER]
    key1, mob_data1 = '', {}
    if 'horse_tier' not in data['info']:
        data['info']['horse_tier'] = ''

    # channel = client.get_channel(842030586457489408)
    # message = await channel.fetch_message(879137072642945074)
    #
    # channel = client.get_channel(842030586457489408)
    # response = await channel.fetch_message(879137073406300230)

    split_hunt = response.content.lower().split('\n')
    if '(but stronger)' in response.content:
        """ ADV H """
        if 'but lost fighting' in response.content.lower():
            data = database[message.author.id]
            data['adventure']['hardmode']['count'] += 1
            data['adventure']['hardmode']['deaths'] += 1
            user_tier = data['info']['horse_tier']
            if user_tier:
                global_data[user_tier]['adventure']['hardmode']['count'] += 1
                global_data[user_tier]['adventure']['hardmode']['deaths'] += 1

        else:
            player_coins = int(split_hunt[1].split(' ')[1].replace(',', ''))
            player_XP = int(split_hunt[1].split(' ')[4].replace(',', ''))
            data['adventure']['hardmode']['count'] += 1
            data['adventure']['hardmode']['coins_gained'] += player_coins
            data['adventure']['hardmode']['xp_gained'] += player_XP
            data = add_lbs_and_drops('adventure', data, split_hunt, 'hardmode', message.author.name.lower())
            data = tier_10_add_lbs_and_drops('adventure', data, split_hunt, 'hardmode', message.author.name.lower())

            player_mob = split_hunt[0].replace(f"**{message.author.name.lower()}** found ", '').split('**')[1]
            mob_data = add_per_mob_lbs_and_drops('adventure', mob_data, split_hunt, 'hardmode',
                                                 message.author.name.lower(), player_mob)
            mob_data['adventure']['hardmode'][player_mob]['coins_gained'] += player_coins
            mob_data['adventure']['hardmode'][player_mob]['xp_gained'] += player_XP
            mob_data['adventure']['hardmode'][player_mob]['count'] += 1

            user_horse = data['info']['horse_tier']
            if user_horse:
                global_data[user_horse]['adventure']['hardmode']['count'] += 1
                global_data[user_horse]['adventure']['hardmode']['coins_gained'] += player_coins
                global_data[user_horse]['adventure']['hardmode']['xp_gained'] += player_XP
                global_data[user_horse] = add_lbs_and_drops('adventure', global_data[user_horse], split_hunt,
                                                            'hardmode',
                                                            message.author.name.lower())
                if user_horse == 'T10' or data['tier_10']['has_t10']:
                    global_data = tier_10_add_lbs_and_drops('adventure', global_data, split_hunt, 'hardmode',
                                                            message.author.name.lower())
                key1 = f"{user_horse}{player_mob}{'adventure'}{'hardmode'}"
                try:
                    global_mb_data = mob_database[key1]
                except KeyError:
                    global_mb_data = get_global_mob_data('hunt')

                mob_data1 = add_global_mob_data(split_hunt, message.author.name.lower(), player_coins, player_XP,
                                                global_mb_data)

    else:
        """NORMAL ADV"""
        split_hunt = response.content.lower().split('\n')
        if 'but lost fighting' in response.content.lower():
            data = database[message.author.id]
            data['adventure']['normal']['count'] += 1
            data['adventure']['normal']['deaths'] += 1

            user_tier = data['info']['horse_tier']
            if user_tier:
                global_data[user_tier]['adventure']['normal']['count'] += 1
                global_data[user_tier]['adventure']['normal']['deaths'] += 1
        else:
            player_coins = int(split_hunt[1].split(' ')[1].replace(',', ''))
            player_XP = int(split_hunt[1].split(' ')[4].replace(',', ''))
            data['adventure']['normal']['count'] += 1
            data['adventure']['normal']['coins_gained'] += player_coins
            data['adventure']['normal']['xp_gained'] += player_XP
            data = add_lbs_and_drops('adventure', data, split_hunt, 'normal', message.author.name.lower())
            data = tier_10_add_lbs_and_drops('adventure', data, split_hunt, 'normal', message.author.name.lower())

            player_mob = split_hunt[0].replace(f"**{message.author.name.lower()}** found ", '').split('**')[1]
            mob_data = add_per_mob_lbs_and_drops('adventure', mob_data, split_hunt, 'normal',
                                                 message.author.name.lower(), player_mob)
            mob_data['adventure']['normal'][player_mob]['coins_gained'] += player_coins
            mob_data['adventure']['normal'][player_mob]['xp_gained'] += player_XP
            mob_data['adventure']['normal'][player_mob]['count'] += 1

            user_horse = data['info']['horse_tier']
            if user_horse:
                global_data[user_horse]['adventure']['normal']['count'] += 1
                global_data[user_horse]['adventure']['normal']['coins_gained'] += player_coins
                global_data[user_horse]['adventure']['normal']['xp_gained'] += player_XP
                global_data[user_horse] = add_lbs_and_drops('adventure', global_data[user_horse], split_hunt,
                                                            'normal',
                                                            message.author.name.lower())
                if user_horse == 'T10' or data['tier_10']['has_t10']:
                    global_data = tier_10_add_lbs_and_drops('adventure', global_data, split_hunt, 'normal',
                                                            message.author.name.lower())
                key1 = f"{user_horse}{player_mob}{'adventure'}{'normal'}"
                try:
                    global_mb_data = mob_database[key1]
                except KeyError:
                    global_mb_data = get_global_mob_data('hunt')

                mob_data1 = add_global_mob_data(split_hunt, message.author.name.lower(), player_coins, player_XP,
                                                global_mb_data)

    database[message.author.id] = data
    database[GLOBAL_USER] = global_data

    mob_database[message.author.id] = mob_data
    if key1:
        mob_database[key1] = mob_data1


async def add_hunt(message: discord.Message, database, client, mob_database):
    def check(msg: discord.Message):
        if msg.author.id == message.author.id and is_command_again(msg, 'rpg hunt'):
            return True

        if not msg.author.id == EPIC_RPG_ID:
            return False

        if msg.channel.id != message.channel.id:
            return False

        is_hunt = False
        for mob in HUNT_MOB_NAMES:
            if mob in msg.content:
                is_hunt = True
                break

        return message.author.name in msg.content and is_hunt

    try:
        response = await client.wait_for('message', check=check, timeout=15)
    except asyncio.TimeoutError:
        return

    if is_command_again(response, 'rpg hunt'):
        return

    # =================================================================================================================

    data = database[message.author.id]
    mob_data = mob_database[message.author.id]
    global_data = database[GLOBAL_USER]

    # For global mob data
    key1, mob_data1 = '', {}

    try:
        partener_data = database[data['info']['partener_ID']]
    except KeyError:
        add_player_to_database(data['info']['partener_ID'], database)
        partener_data = database[data['info']['partener_ID']]

    try:
        partener_mob_data = mob_database[data['info']['partener_ID']]
    except KeyError:
        per_mob_add_player_to_database(data['info']['partener_ID'], mob_database)
        partener_mob_data = mob_database[data['info']['partener_ID']]

    if 'horse_tier' not in data['info']:
        data['info']['horse_tier'] = ''

    if 'area' not in data['info'] or 'max_hp' not in data['info']:
        data['info']['area'] = 0
        data['info']['max_hp'] = 0
    elif data['info']['area'] == 21:
        data['info']['area'] = 15.1

    # channel = client.get_channel(817518295271211039)
    # message = await channel.fetch_message(980945331560783942)
    #
    # channel = client.get_channel(817518295271211039)
    # response = await channel.fetch_message(980945332580024340)

    # =================================================================================================================
    # HUNT TOGETHER
    if 'together' in response.content:
        split_hunt = response.content.lower().split('\n')
        if 'lost fighting, but they saved each other' in response.content:
            # =========================================================================================================
            # BOTH PLAYERS DIE

            if data['info']['partener_ID']:

                partener_data['hunt']['partener']['count'] += 1
                partener_data['hunt']['partener']['deaths'] += 1

                if 'horse_tier' not in partener_data['info']:
                    partener_data['info']['horse_tier'] = ''

                partener_tier = partener_data['info']['horse_tier']
                if partener_tier:
                    global_data[partener_tier]['hunt']['partener']['count'] += 1
                    global_data[partener_tier]['hunt']['partener']['deaths'] += 1

            data['hunt']['hardmode']['count'] += 1
            data['hunt']['hardmode']['deaths'] += 1

            user_tier = data['info']['horse_tier']
            if user_tier:
                global_data[user_tier]['hunt']['hardmode']['count'] += 1
                global_data[user_tier]['hunt']['hardmode']['deaths'] += 1

        # =============================================================================================================
        # HUNT HARDMODE T
        elif '(but stronger)' in split_hunt[1]:
            """HUNT HARD TOGETHER"""
            if 'just in time!' in split_hunt[1]:
                if f"**{message.author.name}** earned" in response.content:
                    # =================================================================================================
                    # PARTNER DIED

                    if data['info']['partener_ID']:
                        partener_data['hunt']['partener']['count'] += 1
                        partener_data['hunt']['partener']['deaths'] += 1

                        if 'horse_tier' not in partener_data['info']:
                            partener_data['info']['horse_tier'] = ''
                        partener_tier = partener_data['info']['horse_tier']
                        if partener_tier:
                            global_data[partener_tier]['hunt']['partener']['count'] += 1
                            global_data[partener_tier]['hunt']['partener']['deaths'] += 1

                    partener_name = split_hunt[0].split('** and **')[1].replace('** are hunting together!', '')
                    player_XP = int(
                        split_hunt[2].replace(f"**{message.author.name.lower()}** earned ", '').split(' ')[0].replace(
                            ',', ''))
                    player_coins = int(
                        split_hunt[2].replace(f"**{message.author.name.lower()}** earned ", '').split(' ')[3].replace(
                            ',', ''))

                    data['info']['partener_name'] = partener_name
                    data['hunt']['hardmode']['count'] += 1
                    data['hunt']['hardmode']['coins_gained'] += player_coins
                    data['hunt']['hardmode']['xp_gained'] += player_XP
                    data = add_lbs_and_drops('hunt', data, split_hunt, 'hardmode', message.author.name.lower())
                    data = tier_10_add_lbs_and_drops('hunt', data, split_hunt, 'hardmode', message.author.name.lower())

                    player_mob = split_hunt[1].replace(f"**{message.author.name.lower()}** found ", '').replace(
                        f"**{partener_name}** found ", '').split('**')[1]
                    mob_data = add_per_mob_lbs_and_drops('hunt', mob_data, split_hunt, 'hardmode',
                                                         message.author.name.lower(), player_mob)

                    max_hp = int(split_hunt[3].split(f"remaining hp is ")[1].split('/')[1])
                    area = get_player_area(player_mob)
                    if max_hp * 2 < data['info']['max_hp']:
                        data['info']['max_hp'] = 0
                        data['info']['area'] = 0

                    if max_hp > data['info']['max_hp']:
                        data['info']['max_hp'] = max_hp

                    if area > data['info']['area']:
                        data['info']['area'] = area

                    mob_data['hunt']['hardmode'][player_mob]['coins_gained'] += player_coins
                    mob_data['hunt']['hardmode'][player_mob]['xp_gained'] += player_XP
                    mob_data['hunt']['hardmode'][player_mob]['count'] += 1

                    user_horse = data['info']['horse_tier']
                    if user_horse:
                        global_data[user_horse]['hunt']['hardmode']['count'] += 1
                        global_data[user_horse]['hunt']['hardmode']['coins_gained'] += player_coins
                        global_data[user_horse]['hunt']['hardmode']['xp_gained'] += player_XP
                        global_data[user_horse] = add_lbs_and_drops('hunt', global_data[user_horse], split_hunt,
                                                                    'hardmode', message.author.name.lower())
                        if user_horse == 'T10':
                            global_data = tier_10_add_lbs_and_drops('hunt', global_data, split_hunt, 'hardmode',
                                                                    message.author.name.lower())

                        key1 = f"{user_horse}{player_mob}{'hunt'}{'hardmode'}"
                        try:
                            global_mb_data = mob_database[key1]
                        except KeyError:
                            global_mb_data = get_global_mob_data('hunt')

                        mob_data1 = add_global_mob_data(split_hunt, message.author.name.lower(), player_coins,
                                                        player_XP, global_mb_data)
                else:
                    # =================================================================================================
                    # PLAYER DIED

                    if data['info']['partener_ID']:
                        partener_data['hunt']['partener']['count'] += 1

                        partener_XP = int(
                            split_hunt[2].replace(f"**{data['info']['partener_name'].lower()}** earned ", '').split(
                                ' ')[
                                0].replace(',', ''))
                        partener_coins = int(
                            split_hunt[2].replace(f"**{data['info']['partener_name'].lower()}** earned ", '').split(
                                ' ')[
                                3].replace(',', ''))

                        partener_data['hunt']['partener']['coins_gained'] += partener_coins
                        partener_data['hunt']['partener']['xp_gained'] += partener_XP

                        partener_data = add_lbs_and_drops('hunt', partener_data, split_hunt, 'partener',
                                                          data['info']['partener_name'])
                        partener_data = tier_10_add_lbs_and_drops('hunt', partener_data, split_hunt, 'partener',
                                                                  data['info']['partener_name'])

                        if 'epic npc' in split_hunt[1].replace(f"**{message.author.name.lower()}** found ", '').replace(
                                f"**{data['info']['partener_name']}** found ", ''):
                            partener_mob = \
                                split_hunt[1].replace(f"**{message.author.name.lower()}** found ", '').replace(
                                    f"**{data['info']['partener_name']}** found ", '').split('**')[5]
                        else:
                            partener_mob = \
                                split_hunt[1].replace(f"**{message.author.name.lower()}** found ", '').replace(
                                    f"**{data['info']['partener_name']}** found ", '').split('**')[3]

                        partener_mob_data = add_per_mob_lbs_and_drops('hunt', partener_mob_data, split_hunt, 'partener',
                                                                      data['info']['partener_name'].lower(),
                                                                      partener_mob)
                        partener_mob_data['hunt']['partener'][partener_mob]['count'] += 1
                        partener_mob_data['hunt']['partener'][partener_mob]['coins_gained'] += partener_coins
                        partener_mob_data['hunt']['partener'][partener_mob]['xp_gained'] += partener_XP

                        if 'horse_tier' not in partener_data['info']:
                            partener_data['info']['horse_tier'] = ''
                        user_horse = partener_data['info']['horse_tier']
                        if user_horse:
                            global_data[user_horse]['hunt']['partener']['count'] += 1
                            global_data[user_horse]['hunt']['partener']['coins_gained'] += partener_coins
                            global_data[user_horse]['hunt']['partener']['xp_gained'] += partener_XP
                            global_data[user_horse] = add_lbs_and_drops('hunt', global_data[user_horse], split_hunt,
                                                                        'partener',
                                                                        data['info']['partener_name'])
                            if user_horse == 'T10' or partener_data['tier_10']['has_t10']:
                                global_data = tier_10_add_lbs_and_drops('hunt', global_data, split_hunt, 'partener',
                                                                        data['info']['partener_name'])

                    data['hunt']['hardmode']['count'] += 1
                    data['hunt']['hardmode']['deaths'] += 1
                    user_tier = data['info']['horse_tier']
                    if user_tier:
                        global_data[user_tier]['hunt']['hardmode']['count'] += 1
                        global_data[user_tier]['hunt']['hardmode']['deaths'] += 1
            else:
                # =================================================================================================
                # BOTH SURVIVED

                partener_name = split_hunt[0].split('** and **')[1].replace('** are hunting together!', '')
                try:
                    player_coins = int(split_hunt[2].replace(f"**{message.author.name.lower()}** earned ", '').replace(
                        f"**{partener_name}**", 'pog').split(' ')[0].replace(',', ''))
                except ValueError:
                    return

                player_XP = int(split_hunt[2].replace(f"**{message.author.name.lower()}** earned ", '').replace(
                    f"**{partener_name}**", 'pog').split(' ')[3].replace(',', ''))

                partener_coins = int(split_hunt[2].replace(f"**{message.author.name.lower()}** earned ", '').replace(
                    f"**{partener_name}**", 'pog').split(' ')[8].replace(',', ''))
                partener_XP = int(split_hunt[2].replace(f"**{message.author.name.lower()}** earned ", '').replace(
                    f"**{partener_name}**", 'pog').split(' ')[11].replace(',', ''))

                player_mob = split_hunt[1].replace(f"**{message.author.name.lower()}** found ", '').replace(
                    f"**{partener_name}** found ", '').split('**')[1]

                if player_mob == 'epic npc':
                    partener_mob = split_hunt[1].replace(f"**{message.author.name.lower()}** found ", '').replace(
                        f"**{partener_name}** found ", '').split('**')[5]
                else:
                    partener_mob = split_hunt[1].replace(f"**{message.author.name.lower()}** found ", '').replace(
                        f"**{partener_name}** found ", '').split('**')[3]

                mob_data = add_per_mob_lbs_and_drops('hunt', mob_data, split_hunt, 'hardmode',
                                                     message.author.name.lower(), player_mob)
                mob_data['hunt']['hardmode'][player_mob]['coins_gained'] += player_coins
                mob_data['hunt']['hardmode'][player_mob]['xp_gained'] += player_XP
                mob_data['hunt']['hardmode'][player_mob]['count'] += 1

                max_hp = int(split_hunt[3].split(f"remaining hp is ")[1].split('/')[1])
                area = get_player_area(player_mob)
                if max_hp * 2 < data['info']['max_hp']:
                    data['info']['max_hp'] = 0
                    data['info']['area'] = 0

                if max_hp > data['info']['max_hp']:
                    data['info']['max_hp'] = max_hp

                if area > data['info']['area']:
                    data['info']['area'] = area

                data['info']['partener_name'] = partener_name
                data['hunt']['hardmode']['count'] += 1
                data['hunt']['hardmode']['coins_gained'] += player_coins
                data['hunt']['hardmode']['xp_gained'] += player_XP
                data = add_lbs_and_drops('hunt', data, split_hunt, 'hardmode', message.author.name.lower())
                data = tier_10_add_lbs_and_drops('hunt', data, split_hunt, 'hardmode', message.author.name.lower())

                user_horse = data['info']['horse_tier']
                if user_horse:
                    global_data[user_horse]['hunt']['hardmode']['count'] += 1
                    global_data[user_horse]['hunt']['hardmode']['coins_gained'] += player_coins
                    global_data[user_horse]['hunt']['hardmode']['xp_gained'] += player_XP
                    global_data[user_horse] = add_lbs_and_drops('hunt', global_data[user_horse], split_hunt, 'hardmode',
                                                                message.author.name.lower())

                    if user_horse == 'T10' or data['tier_10']['has_t10']:
                        global_data = tier_10_add_lbs_and_drops('hunt', global_data, split_hunt, 'hardmode',
                                                                message.author.name.lower())

                    key1 = f"{user_horse}{player_mob}{'hunt'}{'hardmode'}"
                    try:
                        global_mb_data = mob_database[key1]
                    except KeyError:
                        global_mb_data = get_global_mob_data('hunt')

                    mob_data1 = add_global_mob_data(split_hunt, message.author.name.lower(), player_coins, player_XP,
                                                    global_mb_data)

                if data['info']['partener_ID']:
                    partener_data['hunt']['partener']['count'] += 1
                    partener_data['hunt']['partener']['coins_gained'] += partener_coins
                    partener_data['hunt']['partener']['xp_gained'] += partener_XP

                    partener_data = add_lbs_and_drops('hunt', partener_data, split_hunt, 'partener', partener_name)
                    partener_data = tier_10_add_lbs_and_drops('hunt', partener_data, split_hunt, 'partener',
                                                              partener_name)

                    partener_mob_data = add_per_mob_lbs_and_drops('hunt', partener_mob_data, split_hunt, 'partener',
                                                                  partener_name, partener_mob)
                    partener_mob_data['hunt']['partener'][partener_mob]['count'] += 1
                    partener_mob_data['hunt']['partener'][partener_mob]['coins_gained'] += partener_coins
                    partener_mob_data['hunt']['partener'][partener_mob]['xp_gained'] += partener_XP

                    if 'horse_tier' not in partener_data['info']:
                        partener_data['info']['horse_tier'] = ''
                    user_horse = partener_data['info']['horse_tier']
                    if user_horse:
                        global_data[user_horse]['hunt']['partener']['count'] += 1
                        global_data[user_horse]['hunt']['partener']['coins_gained'] += partener_coins
                        global_data[user_horse]['hunt']['partener']['xp_gained'] += partener_XP
                        global_data[user_horse] = add_lbs_and_drops('hunt', global_data[user_horse], split_hunt,
                                                                    'partener', partener_name)
                        if user_horse == 'T10' or partener_data['tier_10']['has_t10']:
                            global_data = tier_10_add_lbs_and_drops('hunt', global_data, split_hunt, 'partener',
                                                                    partener_name)

        else:
            # =================================================================================================
            # NORMAL HUNT TOGETHER

            if 'just in time!' in split_hunt[1]:
                if f"**{message.author.name}** earned" in response.content:
                    """ PARTNER DIED """
                    if data['info']['partener_ID']:
                        partener_data['hunt']['partener']['count'] += 1
                        partener_data['hunt']['partener']['deaths'] += 1

                        if 'horse_tier' not in partener_data['info']:
                            partener_data['info']['horse_tier'] = ''
                        partener_tier = partener_data['info']['horse_tier']
                        if partener_tier:
                            global_data[partener_tier]['hunt']['partener']['count'] += 1
                            global_data[partener_tier]['hunt']['partener']['deaths'] += 1

                    partener_name = split_hunt[0].split('** and **')[1].replace('** are hunting together!', '')
                    player_XP = int(
                        split_hunt[2].replace(f"**{message.author.name.lower()}** earned ", '').split(' ')[0].replace(
                            ',', ''))
                    player_coins = int(
                        split_hunt[2].replace(f"**{message.author.name.lower()}** earned ", '').split(' ')[3].replace(
                            ',', ''))

                    data['info']['partener_name'] = partener_name
                    data['hunt']['normal']['count'] += 1
                    data['hunt']['normal']['coins_gained'] += player_coins
                    data['hunt']['normal']['xp_gained'] += player_XP
                    data = add_lbs_and_drops('hunt', data, split_hunt, 'normal', message.author.name.lower())
                    data = tier_10_add_lbs_and_drops('hunt', data, split_hunt, 'normal', message.author.name.lower())

                    player_mob = split_hunt[1].replace(f"**{message.author.name.lower()}** found ", '').replace(
                        f"**{partener_name}** found ", '').split('**')[1]
                    mob_data = add_per_mob_lbs_and_drops('hunt', mob_data, split_hunt, 'normal',
                                                         message.author.name.lower(), player_mob)
                    mob_data['hunt']['normal'][player_mob]['coins_gained'] += player_coins
                    mob_data['hunt']['normal'][player_mob]['xp_gained'] += player_XP
                    mob_data['hunt']['normal'][player_mob]['count'] += 1

                    max_hp = int(split_hunt[3].split(f"remaining hp is ")[1].split('/')[1])
                    area = get_player_area(player_mob)
                    if max_hp * 2 < data['info']['max_hp']:
                        data['info']['max_hp'] = 0
                        data['info']['area'] = 0

                    if max_hp > data['info']['max_hp']:
                        data['info']['max_hp'] = max_hp

                    if area > data['info']['area']:
                        data['info']['area'] = area

                    user_horse = data['info']['horse_tier']
                    if user_horse:
                        global_data[user_horse]['hunt']['normal']['count'] += 1
                        global_data[user_horse]['hunt']['normal']['coins_gained'] += player_coins
                        global_data[user_horse]['hunt']['normal']['xp_gained'] += player_XP
                        global_data[user_horse] = add_lbs_and_drops('hunt', global_data[user_horse], split_hunt,
                                                                    'normal', message.author.name.lower())
                        if user_horse == 'T10' or data['tier_10']['has_t10']:
                            global_data = tier_10_add_lbs_and_drops('hunt', global_data, split_hunt, 'normal',
                                                                    message.author.name.lower())

                        key1 = f"{user_horse}{player_mob}{'hunt'}{'normal'}"
                        try:
                            global_mb_data = mob_database[key1]
                        except KeyError:
                            global_mb_data = get_global_mob_data('hunt')

                        mob_data1 = add_global_mob_data(split_hunt, message.author.name.lower(), player_coins,
                                                        player_XP, global_mb_data)

                else:
                    # =================================================================================================
                    # PLAYER DIED
                    if data['info']['partener_ID']:
                        partener_data['hunt']['partener']['count'] += 1

                        partener_XP = int(
                            split_hunt[2].replace(f"**{data['info']['partener_name'].lower()}** earned ", '').split(
                                ' ')[0].replace(',', ''))
                        partener_coins = int(
                            split_hunt[2].replace(f"**{data['info']['partener_name'].lower()}** earned ", '').split(
                                ' ')[
                                3].replace(',', ''))

                        partener_data['hunt']['partener']['coins_gained'] += partener_coins
                        partener_data['hunt']['partener']['xp_gained'] += partener_XP
                        partener_data = add_lbs_and_drops('hunt', partener_data, split_hunt, 'partener',
                                                          data['info']['partener_name'])
                        partener_data = tier_10_add_lbs_and_drops('hunt', partener_data, split_hunt, 'partener',
                                                                  data['info']['partener_name'])

                        partener_mob = split_hunt[1].replace(f"**{message.author.name.lower()}** found ", '').replace(
                            f"**{data['info']['partener_name'].lower()}** found ", '').split('**')[3]
                        partener_mob_data = add_per_mob_lbs_and_drops('hunt', partener_mob_data, split_hunt, 'partener',
                                                                      data['info']['partener_name'].lower(),
                                                                      partener_mob)

                        partener_mob_data['hunt']['partener'][partener_mob]['count'] += 1
                        partener_mob_data['hunt']['partener'][partener_mob]['coins_gained'] += partener_coins
                        partener_mob_data['hunt']['partener'][partener_mob]['xp_gained'] += partener_XP

                        if 'horse_tier' not in partener_data['info']:
                            partener_data['info']['horse_tier'] = ''
                        user_horse = partener_data['info']['horse_tier']
                        if user_horse:
                            global_data[user_horse]['hunt']['partener']['count'] += 1
                            global_data[user_horse]['hunt']['partener']['coins_gained'] += partener_coins
                            global_data[user_horse]['hunt']['partener']['xp_gained'] += partener_XP
                            global_data[user_horse] = add_lbs_and_drops('hunt', global_data[user_horse], split_hunt,
                                                                        'partener',
                                                                        data['info']['partener_name'])
                            if user_horse == 'T10' or partener_data['tier_10']['has_t10']:
                                global_data = tier_10_add_lbs_and_drops('hunt', global_data, split_hunt, 'partener',
                                                                        data['info']['partener_name'])

                    data['hunt']['normal']['count'] += 1
                    data['hunt']['normal']['deaths'] += 1
                    user_tier = data['info']['horse_tier']
                    if user_tier:
                        global_data[user_tier]['hunt']['normal']['count'] += 1
                        global_data[user_tier]['hunt']['normal']['deaths'] += 1
            else:
                # =================================================================================================
                # BOTH SURVIVED

                partener_name = split_hunt[0].split('** and **')[1].replace('** are hunting together!', '')
                player_coins = int(
                    split_hunt[2].replace(f"**{message.author.name.lower()}** earned ", '').replace(
                        f"**{partener_name}**", 'pog').split(' ')[0].replace(',', ''))
                player_XP = int(
                    split_hunt[2].replace(f"**{message.author.name.lower()}** earned ", '').replace(
                        f"**{partener_name}**", 'pog').split(' ')[3].replace(',', ''))

                partener_coins = int(
                    split_hunt[2].replace(f"**{message.author.name.lower()}** earned ", '').replace(
                        f"**{partener_name}**", 'pog').split(' ')[8].replace(',', ''))
                partener_XP = int(
                    split_hunt[2].replace(f"**{message.author.name.lower()}** earned ", '').replace(
                        f"**{partener_name}**", 'pog').split(' ')[11].replace(',', ''))

                player_mob = split_hunt[1].replace(f"**{message.author.name.lower()}** found ", '').replace(
                    f"**{partener_name}** found ", '').split('**')[1]

                if player_mob == 'epic npc':
                    partener_mob = split_hunt[1].replace(f"**{message.author.name.lower()}** found ", '').replace(
                        f"**{partener_name}** found ", '').split('**')[5]
                else:
                    partener_mob = split_hunt[1].replace(f"**{message.author.name.lower()}** found ", '').replace(
                        f"**{partener_name}** found ", '').split('**')[3]

                max_hp = int(split_hunt[3].split(f"remaining hp is ")[1].split('/')[1])
                area = get_player_area(player_mob)
                if max_hp * 2 < data['info']['max_hp']:
                    data['info']['max_hp'] = 0
                    data['info']['area'] = 0

                if max_hp > data['info']['max_hp']:
                    data['info']['max_hp'] = max_hp

                if area > data['info']['area']:
                    data['info']['area'] = area

                mob_data = add_per_mob_lbs_and_drops('hunt', mob_data, split_hunt, 'normal',
                                                     message.author.name.lower(), player_mob)
                mob_data['hunt']['normal'][player_mob]['coins_gained'] += player_coins
                mob_data['hunt']['normal'][player_mob]['xp_gained'] += player_XP
                mob_data['hunt']['normal'][player_mob]['count'] += 1

                data['info']['partener_name'] = partener_name
                data['hunt']['normal']['count'] += 1
                data['hunt']['normal']['coins_gained'] += player_coins
                data['hunt']['normal']['xp_gained'] += player_XP
                data = add_lbs_and_drops('hunt', data, split_hunt, 'normal', message.author.name.lower())
                data = tier_10_add_lbs_and_drops('hunt', data, split_hunt, 'normal', message.author.name.lower())

                user_horse = data['info']['horse_tier']
                if user_horse:
                    global_data[user_horse]['hunt']['normal']['count'] += 1
                    global_data[user_horse]['hunt']['normal']['coins_gained'] += player_coins
                    global_data[user_horse]['hunt']['normal']['xp_gained'] += player_XP
                    global_data[user_horse] = add_lbs_and_drops('hunt', global_data[user_horse], split_hunt, 'normal',
                                                                message.author.name.lower())

                    if user_horse == 'T10' or data['tier_10']['has_t10']:
                        global_data = tier_10_add_lbs_and_drops('hunt', global_data, split_hunt, 'normal',
                                                                message.author.name.lower())
                    key1 = f"{user_horse}{player_mob}{'hunt'}{'normal'}"
                    try:
                        global_mb_data = mob_database[key1]
                    except KeyError:
                        global_mb_data = get_global_mob_data('hunt')

                    mob_data1 = add_global_mob_data(split_hunt, message.author.name.lower(), player_coins, player_XP,
                                                    global_mb_data)

                if data['info']['partener_ID']:
                    partener_data['hunt']['partener']['count'] += 1
                    partener_data['hunt']['partener']['coins_gained'] += partener_coins
                    partener_data['hunt']['partener']['xp_gained'] += partener_XP
                    partener_data = add_lbs_and_drops('hunt', partener_data, split_hunt, 'partener', partener_name)
                    partener_data = tier_10_add_lbs_and_drops('hunt', partener_data, split_hunt, 'partener',
                                                              partener_name)

                    partener_mob_data = add_per_mob_lbs_and_drops('hunt', partener_mob_data, split_hunt, 'partener',
                                                                  partener_name, partener_mob)
                    partener_mob_data['hunt']['partener'][partener_mob]['count'] += 1
                    partener_mob_data['hunt']['partener'][partener_mob]['coins_gained'] += partener_coins
                    partener_mob_data['hunt']['partener'][partener_mob]['xp_gained'] += partener_XP

                    if 'horse_tier' not in partener_data['info']:
                        partener_data['info']['horse_tier'] = ''
                    user_horse = partener_data['info']['horse_tier']
                    if user_horse:
                        global_data[user_horse]['hunt']['partener']['count'] += 1
                        global_data[user_horse]['hunt']['partener']['coins_gained'] += partener_coins
                        global_data[user_horse]['hunt']['partener']['xp_gained'] += partener_XP
                        global_data[user_horse] = add_lbs_and_drops('hunt', global_data[user_horse], split_hunt,
                                                                    'partener', partener_name)
                        if user_horse == 'T10' or partener_data['tier_10']['has_t10']:
                            global_data = tier_10_add_lbs_and_drops('hunt', global_data, split_hunt, 'partener',
                                                                    partener_name)

    else:
        split_hunt = response.content.lower().split('\n')
        if '(but stronger)' in response.content.lower():
            # =========================================================================================================
            # HUNT HARDMODE

            if 'but lost fighting' in response.content.lower():
                data['hunt']['hardmode']['count'] += 1
                data['hunt']['hardmode']['deaths'] += 1

            else:
                player_coins = int(split_hunt[1].split(' ')[1].replace(',', ''))
                player_XP = int(split_hunt[1].split(' ')[4].replace(',', ''))
                data['hunt']['hardmode']['count'] += 1
                data['hunt']['hardmode']['coins_gained'] += player_coins
                data['hunt']['hardmode']['xp_gained'] += player_XP
                data = add_lbs_and_drops('hunt', data, split_hunt, 'hardmode', message.author.name.lower())
                data = tier_10_add_lbs_and_drops('hunt', data, split_hunt, 'hardmode', message.author.name.lower())

                player_mob = split_hunt[0].replace(f"**{message.author.name.lower()}** found ", '').split('**')[1]
                mob_data = add_per_mob_lbs_and_drops('hunt', mob_data, split_hunt, 'hardmode',
                                                     message.author.name.lower(), player_mob)
                max_hp = int(split_hunt[2].split(f"remaining hp is ")[1].split('/')[1])
                area = get_player_area(player_mob)
                if max_hp * 2 < data['info']['max_hp']:
                    data['info']['max_hp'] = 0
                    data['info']['area'] = 0

                if max_hp > data['info']['max_hp']:
                    data['info']['max_hp'] = max_hp

                if area > data['info']['area']:
                    data['info']['area'] = area

                mob_data['hunt']['hardmode'][player_mob]['coins_gained'] += player_coins
                mob_data['hunt']['hardmode'][player_mob]['xp_gained'] += player_XP
                mob_data['hunt']['hardmode'][player_mob]['count'] += 1

                user_horse = data['info']['horse_tier']
                if user_horse:
                    global_data[user_horse]['hunt']['hardmode']['count'] += 1
                    global_data[user_horse]['hunt']['hardmode']['coins_gained'] += player_coins
                    global_data[user_horse]['hunt']['hardmode']['xp_gained'] += player_XP
                    global_data[user_horse] = add_lbs_and_drops('hunt', global_data[user_horse], split_hunt, 'hardmode',
                                                                message.author.name.lower())
                    if user_horse == 'T10' or data['tier_10']['has_t10']:
                        global_data = tier_10_add_lbs_and_drops('hunt', global_data, split_hunt, 'hardmode',
                                                                message.author.name.lower())
                    key1 = f"{user_horse}{player_mob}{'hunt'}{'hardmode'}"
                    try:
                        global_mb_data = mob_database[key1]
                    except KeyError:
                        global_mb_data = get_global_mob_data('hunt')

                    mob_data1 = add_global_mob_data(split_hunt, message.author.name.lower(), player_coins, player_XP,
                                                    global_mb_data)

        else:
            # =========================================================================================================
            # NORMAL HUNT

            if 'but lost fighting' in response.content.lower():
                data['hunt']['normal']['count'] += 1
                data['hunt']['normal']['deaths'] += 1

            else:
                player_coins = int(split_hunt[1].split(' ')[1].replace(',', ''))
                player_XP = int(split_hunt[1].split(' ')[4].replace(',', ''))
                data['hunt']['normal']['count'] += 1
                data['hunt']['normal']['coins_gained'] += player_coins
                data['hunt']['normal']['xp_gained'] += player_XP
                data = add_lbs_and_drops('hunt', data, split_hunt, 'normal', message.author.name.lower())
                data = tier_10_add_lbs_and_drops('hunt', data, split_hunt, 'normal', message.author.name.lower())

                player_mob = split_hunt[0].replace(f"**{message.author.name.lower()}** found ", '').split('**')[1]
                mob_data = add_per_mob_lbs_and_drops('hunt', mob_data, split_hunt, 'normal',
                                                     message.author.name.lower(), player_mob)
                mob_data['hunt']['normal'][player_mob]['coins_gained'] += player_coins
                mob_data['hunt']['normal'][player_mob]['xp_gained'] += player_XP
                mob_data['hunt']['normal'][player_mob]['count'] += 1

                if 'horse_tier' not in data['info']:
                    data['info']['horse_tier'] = ''

                max_hp = int(split_hunt[2].split(f"remaining hp is ")[1].split('/')[1])
                area = get_player_area(player_mob)
                if max_hp * 2 < data['info']['max_hp']:
                    data['info']['max_hp'] = 0
                    data['info']['area'] = 0

                if max_hp > data['info']['max_hp']:
                    data['info']['max_hp'] = max_hp

                if area > data['info']['area']:
                    data['info']['area'] = area
                user_horse = data['info']['horse_tier']
                if user_horse:
                    global_data[user_horse]['hunt']['normal']['count'] += 1
                    global_data[user_horse]['hunt']['normal']['coins_gained'] += player_coins
                    global_data[user_horse]['hunt']['normal']['xp_gained'] += player_XP
                    global_data[user_horse] = add_lbs_and_drops('hunt', global_data[user_horse], split_hunt, 'normal',
                                                                message.author.name.lower())
                    if user_horse == 'T10' or data['tier_10']['has_t10']:
                        global_data = tier_10_add_lbs_and_drops('hunt', global_data, split_hunt, 'normal',
                                                                message.author.name.lower())
                    key1 = f"{user_horse}{player_mob}{'hunt'}{'normal'}"
                    try:
                        global_mb_data = mob_database[key1]
                    except KeyError:
                        global_mb_data = get_global_mob_data('hunt')

                    mob_data1 = add_global_mob_data(split_hunt, message.author.name.lower(), player_coins, player_XP,
                                                    global_mb_data)

    database[message.author.id] = data
    database[GLOBAL_USER] = global_data

    mob_database[message.author.id] = mob_data
    if key1:
        mob_database[key1] = mob_data1

    if data['info']['partener_ID']:
        database[data['info']['partener_ID']] = partener_data
        mob_database[data['info']['partener_ID']] = partener_mob_data


async def show_profile(channel, author, clean_text_command, database, client, interaction=None, user=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    if not user:
        last_arg = clean_text_command.split()[-1]
        if get_user(last_arg):
            try:
                user = await client.fetch_user(get_user(last_arg))
            except discord.HTTPException:
                user = author
        else:
            user = author

        if user.id not in database:
            await send_response(content=
                                f"<@{author.id}> I don't have any data stored for that user or you used an invalid user ID")
            return

        if user.id not in agrees_to_track_db:
            await send_response(content=f"<@{author.id}> I didn't track anything for this user!")
            return

    data = database[user.id]
    if not data['info']['partener_ID']:
        data['info']['partener_name'] = "Please use `pog tr marry @user`"
    if 'area' not in data['info']:
        data['info']['area'] = 0
        data['info']['max_hp'] = 0
    if 'worker' not in data['info']:
        data['info']['worker'] = '`use `rpg pr`'
    if 'horse_tier' not in data['info'] or not data['info']['horse_tier']:
        data['info']['horse_tier'] = 'Use `rpg horse`'
    if 'tt' not in data['info']:
        data['info']['tt'] = 'Use `rpg pet`'
    if 'max_hp' not in data['info']:
        data['info']['max_hp'] = 'unknown'
    description = f"""> **USER PROFILE**
💬 **Name:** {user.name}
🌀 **Time travel:** {data['info']['tt']}
:heart: **Married to:** {data['info']['partener_name']} 
:camping:  **Area:** {data['info']['area']}
:anatomical_heart: **Max hp:** {data['info']['max_hp']}
:horse: **Horse tier:** {data['info']['horse_tier']}
:evergreen_tree: **Worker pr level**: {data['info']['worker']}
:bookmark_tabs: **Has disabled tracking:** {data['info']['disabled_tracking']}
"""
    embed = discord.Embed(colour=random.randint(0, 0xffffff), description=description)
    embed.set_author(name=f"{user.name}'s profile", icon_url=user.avatar)
    embed.set_footer(text="Use [pog help stats] to learn more about command tracking")
    await send_response(embed=embed)


async def show_farm_stats(channel, author, clean_text_command, client, database, interaction=None, user=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    if not user:
        last_arg = clean_text_command.split()[-1]
        if last_arg == 'global':
            last_arg = str(GLOBAL_USER)

        if get_user(last_arg):
            try:
                user = await client.fetch_user(get_user(last_arg))
            except discord.HTTPException:
                user = author
        else:
            user = author

    if user.id not in database:
        await send_response(content=
                            f"<@{author.id}> I don't have any data stored for that user or you used an invalid user ID")
        return

    if user.id not in agrees_to_track_db:
        await send_response(content=f"<@{author.id}> I didn't track anything for this user!")
        return

    data = database[user.id]
    if 'farm' not in data or 'special_event' not in data['farm']:
        if 'farm' in data['working_commands']:
            del data['working_commands']['farm']
        data['farm'] = {'xp_gained': 0,
                        'special_event': {'count': 0, 'won': [0, 0]},
                        'special_seeds': {'count': 0,
                                          'carrot': {'count': 0, 'amounts': {}},
                                          'potato': {'count': 0, 'amounts': {}},
                                          'bread': {'count': 0, 'amounts': {}}},
                        'normal_farm': {'count': 0,
                                        'bread': {'count': 0, 'resources': 0},
                                        'carrot': {'count': 0, 'resources': 0},
                                        'potato': {'count': 0, 'resources': 0}},
                        'using_seed': {'count': 0,
                                       'bread': {'count': 0, 'resources': 0, 'seed_back': {}},
                                       'carrot': {'count': 0, 'resources': 0, 'seed_back': {}},
                                       'potato': {'count': 0, 'resources': 0, 'seed_back': {}}}}
        database[user.id] = data

    total_txt = data['farm']['normal_farm']['count'] + data['farm']['using_seed']['count']
    normal_total_txt = data['farm']['normal_farm']['count']
    special_total_txt = data['farm']['using_seed']['count']
    special_seed_total_txt = data['farm']['special_seeds']['count']

    if not special_seed_total_txt:
        special_seed_total_txt = 0
        data['farm']['special_seeds']['count'] = 1

    if not special_total_txt:
        special_total_txt = 0
        data['farm']['special_seeds']['count'] = 1

    if not normal_total_txt:
        normal_total_txt = 0
        data['farm']['normal_farm']['count'] = 1
    bread_seed_text = ""
    for amount in data['farm']['special_seeds']['bread']['amounts']:
        bread_seed_text += f"— {amount} at once `x{data['farm']['special_seeds']['bread']['amounts'][amount] // amount}` times → ({(data['farm']['special_seeds']['bread']['amounts'][amount] // amount / data['farm']['special_seeds']['bread']['count']) * 100:.2f}%)\n"

    carrot_seed_text = ""
    for amount in data['farm']['special_seeds']['carrot']['amounts']:
        carrot_seed_text += f"— {amount} at once `x{data['farm']['special_seeds']['carrot']['amounts'][amount] // amount}` times → ({(data['farm']['special_seeds']['carrot']['amounts'][amount] // amount / data['farm']['special_seeds']['carrot']['count']) * 100:.2f}%)\n"

    potato_seed_text = ""
    for amount in data['farm']['special_seeds']['potato']['amounts']:
        potato_seed_text += f"— {amount} at once `x{data['farm']['special_seeds']['potato']['amounts'][amount] // amount}` times → ({(data['farm']['special_seeds']['potato']['amounts'][amount] // amount / data['farm']['special_seeds']['potato']['count']) * 100:.2f}%)\n"
    if not bread_seed_text:
        bread_seed_text = "— none"
    if not carrot_seed_text:
        carrot_seed_text = "— none"
    if not potato_seed_text:
        potato_seed_text = "— none"

    bread_count = data['farm']['using_seed']['bread']['count']
    if not data['farm']['using_seed']['bread']['count']:
        data['farm']['using_seed']['bread']['count'] = 1
        bread_count = 0

    carrot_count = data['farm']['using_seed']['carrot']['count']
    if not data['farm']['using_seed']['carrot']['count']:
        data['farm']['using_seed']['carrot']['count'] = 1
        carrot_count = 0

    potato_count = data['farm']['using_seed']['potato']['count']
    if not data['farm']['using_seed']['potato']['count']:
        data['farm']['using_seed']['potato']['count'] = 1
        potato_count = 0

    gained_back_bread = ""
    for amount in sorted(data['farm']['using_seed']['bread']['seed_back']):
        gained_back_bread += f"— `x{data['farm']['using_seed']['bread']['seed_back'][amount]}` times **{amount}** back → ({(data['farm']['using_seed']['bread']['seed_back'][amount] / sum(data['farm']['using_seed']['bread']['seed_back'].values())) * 100:.2f}%)\n"

    gained_back_carrot = ""
    for amount in sorted(data['farm']['using_seed']['carrot']['seed_back']):
        gained_back_carrot += f"— `x{data['farm']['using_seed']['carrot']['seed_back'][amount]}` times **{amount}** back → ({(data['farm']['using_seed']['carrot']['seed_back'][amount] / sum(data['farm']['using_seed']['carrot']['seed_back'].values())) * 100:.2f}%)\n"

    gained_back_potato = ""
    for amount in sorted(data['farm']['using_seed']['potato']['seed_back']):
        gained_back_potato += f"— `x{data['farm']['using_seed']['potato']['seed_back'][amount]}` times **{amount}** back → ({(data['farm']['using_seed']['potato']['seed_back'][amount] / sum(data['farm']['using_seed']['potato']['seed_back'].values())) * 100:.2f}%)\n"

    if not data['farm']['special_event']['won'][0]:
        data['farm']['special_event']['won'][0] = 1

    description = F"""
> **FARM STATS**
:corn: **Total commands tracked:** {total_txt}
{EMOJIS['xp']} **XP gained:** {data['farm']['xp_gained']:,}
> **Normal farm:**
**Total commands:** {normal_total_txt}
`x{data['farm']['normal_farm']['bread']['count']}` {EMOJIS['bread']} - `col:` {data['farm']['normal_farm']['bread']['resources']:,} → ({(data['farm']['normal_farm']['bread']['count'] / data['farm']['normal_farm']['count']) * 100:.2f}%)
`x{data['farm']['normal_farm']['carrot']['count']}` {EMOJIS['carrot']} - `col:` {data['farm']['normal_farm']['carrot']['resources']:,} → ({(data['farm']['normal_farm']['carrot']['count'] / data['farm']['normal_farm']['count']) * 100:.2f}%)
`x{data['farm']['normal_farm']['potato']['count']}` {EMOJIS['potato']} - `col:` {data['farm']['normal_farm']['potato']['resources']:,} → ({(data['farm']['normal_farm']['potato']['count'] / data['farm']['normal_farm']['count']) * 100:.2f}%)

You found special seeds in **{special_seed_total_txt}** cmds → ({(data['farm']['special_seeds']['count'] / data['farm']['normal_farm']['count']) * 100:.2f}%)
`x{data['farm']['special_seeds']['bread']['count']}` {EMOJIS['seed_bread']} - `col:` {sum(data['farm']['special_seeds']['bread']['amounts'].values())} → ({(data['farm']['special_seeds']['bread']['count'] / data['farm']['special_seeds']['count']) * 100:.2f}%)
**Drop amounts**: 
{bread_seed_text}
`x{data['farm']['special_seeds']['carrot']['count']}` {EMOJIS['seed_carrot']} - `col:` {sum(data['farm']['special_seeds']['carrot']['amounts'].values())} → ({(data['farm']['special_seeds']['carrot']['count'] / data['farm']['special_seeds']['count']) * 100:.2f}%)
**Drop amounts**: 
{carrot_seed_text}
`x{data['farm']['special_seeds']['potato']['count']}` {EMOJIS['seed_potato']} - `col:` {sum(data['farm']['special_seeds']['potato']['amounts'].values())} → ({(data['farm']['special_seeds']['potato']['count'] / data['farm']['special_seeds']['count']) * 100:.2f}%)
**Drop amounts**: 
{potato_seed_text}
> **Farm using a special seed:**
**Total commands:** {special_total_txt}
`x{bread_count}` {EMOJIS['bread']} - `col:` {data['farm']['using_seed']['bread']['resources']:,}
`x{carrot_count}` {EMOJIS['carrot']} - `col:` {data['farm']['using_seed']['carrot']['resources']:,}
`x{potato_count}` {EMOJIS['potato']} - `col:` {data['farm']['using_seed']['potato']['resources']:,}
> **{EMOJIS['seed_bread']} gained back:**
{gained_back_bread}
> **{EMOJIS['seed_carrot']} gained back:**
{gained_back_carrot}
> **{EMOJIS['seed_potato']} gained back:**
{gained_back_potato}
"""
    # > **Special event:**
    # Total occurrences: {data['farm']['special_event']['count']} → ({(data['farm']['special_event']['count']/(data['farm']['normal_farm']['count']+data['farm']['special_seeds']['count'])) * 100:.2f}%)
    # Event succesful: {data['farm']['special_event']['won'][0]} → ({(data['farm']['special_event']['won'][0]/(data['farm']['special_event']['won'][0]+data['farm']['special_event']['won'][1]))*100:.2f}%)
    # Event failed: {data['farm']['special_event']['won'][1]} → ({(data['farm']['special_event']['won'][1]/(data['farm']['special_event']['won'][0]+data['farm']['special_event']['won'][1]))*100:.2f}%)

    embed = discord.Embed(colour=random.randint(0, 0xffffff), description=description)
    embed.set_author(name=f"{user.name}'s farm stats", icon_url=user.avatar)
    embed.set_footer(text="Use [pog help stats] to learn more about command tracking")
    await send_response(embed=embed)


async def rest_tracking(channel, author, clean_text_command, client, command_tracking_database, interaction=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    if clean_text_command == 'pog tr reset' or clean_text_command == f'{client.user.id} tr reset':
        await send_response(content=
                            f"<@{author.id}> Correct usage: `pog tr reset <tracking command>`. \nExample: `pog tr reset hunt`")
        return

    command = clean_text_command.replace('pog tr reset ', '')

    if command not in ('hunt', 'adv', 't10', 'chainsaw', 'all', 'work',
                       'bowsaw', 'axe', 'chop', 'dynamite', 'drill', 'pickaxe', 'mine', 'bigboat', 'boat', 'net',
                       'fish',
                       'greenhouse', 'tractor', 'ladder', 'pickup', 'farm', 'partner'):
        if command.startswith('hunt'):
            await send_response(content=
                                f"<@{author.id}> Correct usage: `pog tr reset hunt`. You can only reset all hunt stats for all modes at once!")

        elif command.startswith('adv'):
            if command.startswith('hunt'):
                await send_response(content=
                                    f"<@{author.id}> Correct usage: `pog tr reset adv`. You can only reset all adv stats for all modes at once!")
        else:
            await send_response(content=
                                f"<@{author.id}> \nCorrect usage: `pog tr reset <tracking command>`. \nExample: `pog tr reset hunt`\n"
                                f"Please just use the stuff you type after pog tr, except don't add the modes!")
        return

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Yes", style=discord.ButtonStyle.green, custom_id="yes_reset"))
    view.add_item(discord.ui.Button(label="No", style=discord.ButtonStyle.red, custom_id="no_reset"))

    message = await send_response(view=view,
                                  content=f"<@{author.id}> Are you sure that you want to reset your data for the command specified?"
                                          f" Answer with `yes`/`no`.\n You will receive a file with your data after the reset, and you can load this data back in at any time!")

    def check(inter: discord.Interaction):
        return inter.message and inter.message.id == message.id

    while True:
        try:
            interaction = await client.wait_for('interaction', timeout=120, check=check)
        except asyncio.TimeoutError:
            for child in view.children:
                child.disabled = True

            view.stop()
            await interaction.message.edit(view=view)
            return

        if interaction.user.id != author.id:
            await interaction.response.send_message(
                content="This is not your command! Use `val recipes` to browse recipes yourself!", ephemeral=True)
            continue

        if interaction.data['custom_id'] == "yes_reset":
            data = command_tracking_database[author.id]
            empty_data = get_empty_db()

            if command.startswith('hunt') or command.startswith('adv'):
                if command == 'adv':
                    command = 'adventure'
                file_name = f"""{command} {datetime.date.today().strftime("%d-%b-%Y")}.pog"""
                with open(file_name, 'w+') as file:
                    string_data = f"{command}\n" + f"{author.id}\n" + dumps(data[command])
                    encoded_data = string_data
                    file.write(str(encoded_data))

                await interaction.response.send_message(
                    f"<@{author.id}> I have successfully reset your data for `{command}`!\n"
                    f"Here is your file", file=discord.File(file_name))
                os.remove(file_name)
                data[command] = empty_data[command]

            elif command.startswith('partner'):
                hunt_data = data['hunt']['partener']
                file_name = f"""partener {datetime.date.today().strftime("%d-%b-%Y")}.pog"""
                with open(file_name, 'w+') as file:
                    string_data = f"partener\n" + f"{author.id}\n" + dumps(hunt_data)
                    encoded_data = string_data
                    file.write(str(encoded_data))

                await interaction.response.send_message(
                    f"<@{author.id}> I have successfully reset your data for partner hunt stats!\n"
                    f"Here is your file", file=discord.File(file_name))
                os.remove(file_name)
                data['hunt']['partener'] = get_empty_partener()

            elif command == 't10':
                file_name = f"""{command} {datetime.date.today().strftime("%d-%b-%Y")}.pog"""
                with open(file_name, 'w+') as file:
                    string_data = f"{command}\n" + f"{author.id}\n" + dumps(data['tier_10'])
                    encoded_data = string_data
                    file.write(str(encoded_data))

                await interaction.response.send_message(
                    f"<@{author.id}> I have successfully reset your data for `{command}`!\n"
                    f"Here is your file", file=discord.File(file_name))
                os.remove(file_name)
                data['tier_10'] = empty_data['tier_10']

            elif command == 'farm':
                file_name = f"""{command} {datetime.date.today().strftime("%d-%b-%Y")}.pog"""
                with open(file_name, 'w+') as file:
                    string_data = f"{command}\n" + f"{author.id}\n" + dumps(data['farm'])
                    encoded_data = string_data
                    file.write(str(encoded_data))

                await interaction.response.send_message(
                    f"<@{author.id}> I have successfully reset your data for `{command}`!\n"
                    f"Here is your file", file=discord.File(file_name))
                os.remove(file_name)
                data['farm'] = empty_data['farm']

            elif command == 'work':
                command = 'working commands'
                file_name = f"""{command} {datetime.date.today().strftime("%d-%b-%Y")}.pog"""
                with open(file_name, 'w+') as file:
                    string_data = f"{command}\n" + f"{author.id}\n" + dumps(data['working_commands'])
                    encoded_data = string_data
                    file.write(str(encoded_data))

                await interaction.response.send_message(
                    f"<@{author.id}> I have successfully reset your data for `{command}`!\n"
                    f"Here is your file", file=discord.File(file_name))
                os.remove(file_name)
                data['working_commands'] = empty_data['working_commands']

            elif command in (
                    'chainsaw', 'bowsaw', 'axe', 'chop', 'dynamite', 'drill', 'pickaxe', 'mine', 'bigboat', 'boat',
                    'net',
                    'fish',
                    'greenhouse', 'tractor', 'ladder', 'pickup'):

                file_name = f"""{command} {datetime.date.today().strftime("%d-%b-%Y")}.pog"""
                with open(file_name, 'w+') as file:
                    string_data = f"{command}\n" + f"{author.id}\n" + dumps(data['working_commands'][command])
                    encoded_data = string_data
                    file.write(str(encoded_data))

                await interaction.response.send_message(
                    f"<@{author.id}> I have successfully reset your data for `{command}`!\n"
                    f"Here is your file", file=discord.File(file_name))
                os.remove(file_name)

                data['working_commands'][command] = empty_data['working_commands'][command]

            elif command == 'all':
                command = 'everything'
                file_name = f"""{command} {datetime.date.today().strftime("%d-%b-%Y")}.pog"""
                with open(file_name, 'w+') as file:
                    string_data = f"{command}\n" + f"{author.id}\n" + dumps(data)
                    encoded_data = string_data
                    file.write(str(encoded_data))

                await interaction.response.send_message(
                    f"<@{author.id}> I have successfully reset your data for `{command}`!\n"
                    f"Here is your file", file=discord.File(file_name))
                os.remove(file_name)
                data = empty_data

            command_tracking_database[author.id] = data

            for child in view.children:
                child.disabled = True

            view.stop()
            await interaction.message.edit(view=view)
            return

        else:
            await interaction.response.send_message(f"<@{author.id}> I didn't reset your data.")
            for child in view.children:
                child.disabled = True

            view.stop()
            await interaction.message.edit(view=view)
            return


async def load_data(channel, author, attachments, database, client, interaction=None, filename=""):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    if not filename:
        if not attachments:
            embed = discord.Embed(colour=random.randint(0, 0xffffff), title="Example:")
            embed.set_image(url="https://i.postimg.cc/kgJBfs6N/image.png")

            await send_response(
                content=f"<@{author.id}> Please send the file with your data at the same time as the command! Just like you send a picture\n",
                embed=embed)
            return

    else:
        if not filename.isnumeric():
            message = None
        else:
            message = await channel.fetch_message(filename)

        if not message or not message.attachments:
            embed = discord.Embed(colour=random.randint(0, 0xffffff), title="Example:")
            embed.set_image(url="https://i.postimg.cc/Y28cQx7B/image.png")
            await send_response(content=
                                f"<@{author.id}> Please add the ID of the message with your file! Send it in the same channel as the one where you do the command!",
                                embed=embed)
            return

        attachments = message.attachments

    data = attachments[0]
    if not str(data).endswith('.pog'):
        await send_response(content=f"<@{author.id}> Please send the `.pog` file only!")
        return

    filename = f"{time.time()}{random.randint(0, 100)}.pog"

    try:
        await attachments[0].save(filename)
        with open(filename, 'r') as file:
            data = file.read()
            data = data.split('\n')
            command, userID, dictionary = data[0], int(data[1]), loads(data[2])
        os.remove(filename)

    except (IndexError, ValueError, AttributeError, TypeError):
        await send_response(content=
                            f"<@{author.id}> An error occurred! Make sure the file provided was given by me and was never edited!\n"
                            f"If this persists please report it in the support server, join with `/invite`.")
        return

    if userID != author.id:
        await send_response(content=f"<@{author.id}> Sorry, you can only load your own data!")
        return

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Yes", style=discord.ButtonStyle.green, custom_id="yes_reset"))
    view.add_item(discord.ui.Button(label="No", style=discord.ButtonStyle.red, custom_id="no_reset"))

    message = await send_response(view=view,
                                  content=
                                  f"<@{author.id}> Are you sure that you want to load this data for `{command}`?"
                                  f"Your current data will be overwritten! Make sure to reset it to get a backup first.")

    def check(inter: discord.Interaction):
        return inter.message and inter.message.id == message.id

    while True:
        try:
            interaction = await client.wait_for('interaction', timeout=120, check=check)
        except asyncio.TimeoutError:
            for child in view.children:
                child.disabled = True

            view.stop()
            await interaction.message.edit(view=view)
            return

        if interaction.user.id != author.id:
            await interaction.response.send_message(
                content="This is not your command! Use `val recipes` to browse recipes yourself!", ephemeral=True)
            continue

        if interaction.data['custom_id'] == "yes_reset":
            current_data = database[author.id]
            if command.startswith('hunt') or command.startswith('adventure'):
                current_data[command] = dictionary
            elif command.startswith('partener'):
                current_data['hunt']['partener'] = dictionary
            elif command.startswith('t10'):
                current_data['tier_10'] = dictionary
            elif command.startswith('farm'):
                current_data['farm'] = dictionary
            elif command.startswith('working commands'):
                current_data['working_commands'] = dictionary

            elif command in (
                    'chainsaw', 'bowsaw', 'axe', 'chop', 'dynamite', 'drill', 'pickaxe', 'mine', 'bigboat', 'boat',
                    'net', 'fish', 'greenhouse', 'tractor', 'ladder', 'pickup'):
                current_data['working_commands'][command] = dictionary

            elif command.startswith('everything'):
                current_data = dictionary

            await interaction.response.send_message(content=f"<@{author.id}> Data loaded successfully!")
            database[author.id] = current_data

        else:
            await interaction.response.send_message(f"<@{author.id}> I didn't load the data.")
            for child in view.children:
                child.disabled = True

            view.stop()
            await interaction.message.edit(view=view)
            return


async def show_hunt_or_adv_stats(channel, author, mode, command_given, client, database, interaction=None, user=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    title = ""
    command = ""
    if mode == 'hunt h':
        mode = 'hardmode'
        command = 'hunt'
        title = "HUNT HARDMODE STATS"
    elif mode == 'hunt n':
        mode = 'normal'
        command = "hunt"
        title = "NORMAL HUNT STATS"
    elif mode == 'hunt p':
        mode = 'partener'
        command = "hunt"
        title = "FROM PARTNER HUNT STATS"
    elif mode == 'adv h':
        mode = 'hardmode'
        command = "adventure"
        title = "ADVENTURE HARDMODE STATS"
    elif mode == 'adv n':
        mode = 'normal'
        command = "adventure"
        title = "NORMAL ADVENTURE STATS"

    tier = ''
    if not user:

        last_arg = command_given.split()[-1]
        if last_arg == 'global':
            await send_response(content=
                                f"<@{author.id}> For global data you also need to specify a horse tier at the end. Example: "
                                f"`pog tr hunt h global T9`.")
            return

        if last_arg.startswith('t') and last_arg[1:].isnumeric() and 'global' in command_given.lower():
            horse_tier = int(last_arg[1:])

            if 5 >= horse_tier > 10:
                await send_response(content=f"<@{author.id}> Sorry, I only store data for the T6 - T10 horses")
                return

            tier = f"T{horse_tier}"
            last_arg = str(GLOBAL_USER)

        is_user = get_user(last_arg)
        if is_user:
            try:
                user = await client.fetch_user(is_user)
            except discord.HTTPException:
                user = author
        else:
            user = author

    if user.id not in database:
        await send_response(
            content=f"<@{author.id}> I don't have any data stored for that user or you used an invalid user ID")
        return

    marry = ""
    if user.id == GLOBAL_USER:
        data = database[GLOBAL_USER][tier]
    else:
        if user.id not in agrees_to_track_db:
            await send_response(content=f"<@{author.id}> I didn't track anything for this user!")
            return

        data = database[user.id]
        marry = data['info']['partener_ID']
        if not marry:
            marry = 'Use `pog tr marry @user` to marry someone'
        else:
            marry = data['info']['partener_name']

    description = f"""🔹 dropped - how many times you got this type in a hunt
🔹 collected - how many you found in total (because T10 horse can give more than 1)\n"""

    hunt_val = ""
    lb_val = ""

    total_txt = data[command][mode]['count']
    if data[command][mode]['count'] == 0:
        data[command][mode]['count'] = 1
        total_txt = 0

    mob_total_txt = data['hunt'][mode]['mob_drops']['total']
    if data['hunt'][mode]['mob_drops']['total'] == 0:
        data['hunt'][mode]['mob_drops']['total'] = 1
        mob_total_txt = 0

    lb_total_txt = data[command][mode]['lootboxes']['total']
    if data[command][mode]['lootboxes']['total'] == 0:
        data[command][mode]['lootboxes']['total'] = 1
        lb_total_txt = 0

    description += f"""
> **{title}**\n"""

    if user.id == GLOBAL_USER and mode == 'partener':
        description += f"**Married to:** everyone lmao"
    elif mode == 'partener':
        description += f"**Married to:** {marry}"

    description += f"""\n
:dart: **Total commands tracked:** {total_txt:,}
:skull: **Deaths:** {data[command][mode]['deaths']:,}
{EMOJIS['coin']} **Coins gained:** {data[command][mode]['coins_gained']:,}
{EMOJIS['xp']} **XP gained:**  {data[command][mode]['xp_gained']:,}
ㅤ
"""

    if command == 'hunt' and data['hunt'][mode]['mob_drops']['total']:
        hunt_val = f"""You got a mob drop in **{mob_total_txt:,}** cmds → ({((data['hunt'][mode]['mob_drops']['total'] / data['hunt'][mode]['count'] * 100.0)):.2f}%)\n"""

        for drop in data['hunt'][mode]['mob_drops']:
            if drop == 'total':
                continue
            if not data['hunt'][mode]['mob_drops'][drop]['seen']:
                continue
            hunt_val += f"""{EMOJIS[drop]} > `dropped:` {data['hunt'][mode]['mob_drops'][drop]['seen']:,}"""

            if data['hunt'][mode]['mob_drops'][drop]['found'] != data['hunt'][mode]['mob_drops'][drop]['seen']:
                hunt_val += f""", `collected:` {data['hunt'][mode]['mob_drops'][drop]['found']:,}"""
            hunt_val += '\n'

    if data[command][mode]['lootboxes']['total']:
        lb_val = f"""You got a lootbox in **{lb_total_txt:,}** cmds → ({((data[command][mode]['lootboxes']['total'] / data[command][mode]['count'] * 100.0)):.2f}%)\n"""

        for lootbox in data[command][mode]['lootboxes']:
            if lootbox == 'total':
                continue
            if not data[command][mode]['lootboxes'][lootbox]['seen']:
                continue
            lb_val += f"""{EMOJIS[lootbox]} > `dropped: `{data[command][mode]['lootboxes'][lootbox]['seen']:,}"""
            if data[command][mode]['lootboxes'][lootbox]['seen'] != data[command][mode]['lootboxes'][lootbox]['found']:
                lb_val += f""", `collected:` {data[command][mode]['lootboxes'][lootbox]['found']:,}"""
            lb_val += f""" → ({(data[command][mode]['lootboxes'][lootbox]['seen'] / data[command][mode]['lootboxes']['total']) * 100:.2f}%)\n"""

    embed = discord.Embed(colour=random.randint(0, 0xFFFFFF), description=description)
    if hunt_val:
        embed.add_field(name='Mob drops', value=hunt_val, inline=False)
    if lb_val:
        embed.add_field(name='Lootboxes', value=lb_val, inline=False)

    if (command == 'hunt' and len(embed.fields) < 2) or (command == 'adventure' and not len(embed.fields)):
        embed.description += """Your mob drops and lootboxes will appear here after you obtain at least 1 specimen.\nㅤ"""
    embed.set_author(name=f"{user.name}'s stats", icon_url=user.avatar)
    embed.set_footer(text='Use `pog help stats` for the list of stat commands | Pog <3')

    await send_response(embed=embed)


async def show_tier10_stats(channel, author, hunt_or_adv, command, client, database, interaction=None, user=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    if not user:
        last_arg = command.split()[-1]

        if last_arg == 'global':
            last_arg = str(GLOBAL_USER)

        if get_user(last_arg):
            try:
                user = await client.fetch_user(get_user(last_arg))
            except discord.HTTPException:
                user = author
        else:
            user = author

    if user.id not in database:
        await send_response(content=
                            f"<@{author.id}> I don't have any data stored for that user or you used an invalid user ID")
        return

    if user.id not in agrees_to_track_db:
        await send_response(content=f"<@{author.id}> I didn't track anything for this user!")
        return

    data = database[user.id]
    if not data['tier_10']['has_t10']:
        if user.id == author.id:
            await send_response(content=
                                f"<@{author.id}>This command will be unlocked after you get more than 1 lootbox or monster item at once in hunt or adventure. "
                                f"You can still check the data of other people.")
        else:
            await send_response(content=
                                f"<@{author.id}> That user doesn't have a T10 horse or never got more than 1 lootbox or monster item at once in hunt or adventure. ")
        return

    name = ''
    command_type = ''
    mode = ''

    if hunt_or_adv == 'hunt h':
        name = 'TIER 10 - HUNT HARDMODE STATS'
        command_type = 'hunt'
        mode = 'hardmode'
    elif hunt_or_adv == 'hunt n':
        name = 'TIER 10 - NORMAL HUNT STATS'
        command_type = 'hunt'
        mode = 'normal'
    elif hunt_or_adv == 'hunt p':
        name = 'TIER 10 - HUNTS BY PARTNER STATS'
        command_type = 'hunt'
        mode = 'partener'
    elif hunt_or_adv == 'adv h':
        name = 'TIER 10 - ADVENTURE HARDMODE STATS'
        command_type = 'adventure'
        mode = 'hardmode'
    elif hunt_or_adv == 'adv n':
        name = 'TIER 10 - NORMAL ADVENTURE STATS'
        command_type = 'adventure'
        mode = 'normal'

    total_count = data['tier_10'][command_type][mode]['count']
    if total_count == 0:
        data['tier_10'][command_type][mode]['count'] = 1
        total_count = 0

    description = f"""🔹 dropped - how many times you got this type in a hunt
🔹 collected - how many you found in total (because T10 horse can give more than 1)

> **{name}**

:dart: **Total commands tracked:** {total_count:,}"""

    embed = discord.Embed(colour=random.randint(0, 0xFFFFFF), description=description)
    embed.set_author(name=f"{user.name}'s t10 proc stats", icon_url=user.avatar)
    embed.set_footer(text='Use `pog help stats` for the list of stat commands | Pog <3')
    if data['tier_10'][command_type][mode]['count'] == 0:
        data['tier_10'][command_type][mode]['count'] = 1
    if command_type == 'hunt':
        mob_drop_text = f"""You got more than 1 mob drop in {data['tier_10'][command_type][mode]['mob_drops']['total']:,} cmds → ({((data['tier_10'][command_type][mode]['mob_drops']['total'] / data['tier_10'][command_type][mode]['count'] * 100.0)):.2f} %)\n"""

        if len(data['tier_10'][command_type][mode]['mob_drops']) == 1:
            mob_drop_text += "The amount of times you get x2, x3... will show up here once you drop them"

        mob_drop_keys = [i for i in list(data['tier_10'][command_type][mode]['mob_drops'].keys()) if isinstance(i, int)]
        for amount in sorted(mob_drop_keys):
            mob_drop_text += f"`x{amount:,}` at once - {data['tier_10'][command_type][mode]['mob_drops'][amount]:,} times ({(data['tier_10'][command_type][mode]['mob_drops'][amount] / data['tier_10'][command_type][mode]['mob_drops']['total']) * 100:.3f} %)\n"
        embed.add_field(name=f"🌽 Mob Drops", value=mob_drop_text, inline=False)

    if data['tier_10'][command_type][mode]['lootboxes']['total'] == 0:
        data['tier_10'][command_type][mode]['lootboxes']['total'] = 1
    lootbox_drop_text = f"""You got more than 1 lootbox in {data['tier_10'][command_type][mode]['lootboxes']['total']:,} cmds → ({((data['tier_10'][command_type][mode]['lootboxes']['total'] / data['tier_10'][command_type][mode]['count'] * 100.0)):.2f} %)\n"""

    drop_amounts = {}
    for lootbox_type in data['tier_10'][command_type][mode]['lootboxes']:
        if lootbox_type == 'total':
            continue

        if not data['tier_10'][command_type][mode]['lootboxes'][lootbox_type]:
            continue

        for amount in data['tier_10'][command_type][mode]['lootboxes'][lootbox_type]:
            if amount not in drop_amounts:
                drop_amounts[amount] = data['tier_10'][command_type][mode]['lootboxes'][lootbox_type][amount]
            else:
                drop_amounts[amount] += data['tier_10'][command_type][mode]['lootboxes'][lootbox_type][amount]

    for amount in sorted(drop_amounts.keys()):
        lootbox_drop_text += f"`x{amount:,}` at once - {drop_amounts[amount]:,} times ({(drop_amounts[amount] / data['tier_10'][command_type][mode]['lootboxes']['total']) * 100:.2f} %)\n"

    embed.add_field(name=f"🥡 Lootboxes", value=lootbox_drop_text, inline=False)
    for lootbox_type in data['tier_10'][command_type][mode]['lootboxes']:
        if lootbox_type == 'total':
            continue

        if not data['tier_10'][command_type][mode]['lootboxes'][lootbox_type]:
            continue

        text = ""
        for amount in data['tier_10'][command_type][mode]['lootboxes'][lootbox_type]:
            text += f"`x{amount:,}` at once - {data['tier_10'][command_type][mode]['lootboxes'][lootbox_type][amount]:,} times"

        embed.add_field(name=f"{lootbox_type.title()} lootbox", value=text, inline=False)

    await send_response(embed=embed)


async def dump_mobs(channel, author, command, client, mob_database, interaction=None, user=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    try:
        splits = command.split()
        command = splits[4]
        mode = splits[5]
        if not mode.startswith(('h', 'n', 'p')):
            raise ValueError
        if command not in ('hunt', 'adv'):
            raise ValueError
        elif command == 'adv' and mode == 'p':
            raise ValueError

    except (TypeError, IndexError, ValueError):
        await send_response(content=F"<@{author.id}> Correct usage: `pog tr mob dump <command> <mode>`.\n"
                                    F"Commands can be `hunt`, `adv`\n."
                                    F" Mode can be `h`, `n`, `p`.")
        return

    last_arg = command.split()[-1]
    if last_arg == 'global':
        await send_response(content=
                            f"<@{author.id}> Sorry, it's not possible to check the global mobs dumps. Try using the mob names"
                            f" from `pog dex` if you are looking for a specific mob.")
        return

    if not user:
        if get_user(last_arg):
            try:
                user = await client.fetch_user(get_user(last_arg))
            except discord.HTTPException:
                user = author
        else:
            user = author

    if user.id not in agrees_to_track_db:
        await send_response(content=f"<@{author.id}> I didn't track anything for this user!")
        return

    if user.id not in mob_database:
        await send_response(content=
                            f"<@{author.id}> I don't have any data stored for that user or you used an invalid user ID")
        return

    if user.id == GLOBAL_USER:
        await send_response(content=
                            f"<@{author.id}> Sorry, it's not possible to check the global mobs dumps. Try using the mob names"
                            f" from `pog dex` if you are looking for a specific mob.")
        return

    if mode == 'h':
        mode = 'hardmode'

    elif mode == 'p':
        mode = 'partener'
    elif mode == 'n':
        mode = 'normal'
    if command == 'adv':
        command = 'adventure'

    data = mob_database[user.id]
    text = ""
    for mob in data[command][mode]:
        text += f"{mob}\n"

    if not text:
        text = "No mobs stored?!"

    add = "Here are the mobs stored for you. Use `pog tr mob <mob name> <command>` to access the data.\n\n" \
          "—————————————————————\n"
    embed = discord.Embed(colour=random.randint(0, 0xFFFFFF), description=add + text + '—————————————————————')
    embed.set_author(name=f"{user.name}'s mob dump", icon_url=user.avatar)
    embed.set_footer(text='Use `pog help stats` for the list of stat commands | Pog <3')

    await send_response(embed=embed)


async def show_per_mob_data(channel, author, clean_text_command, client, mob_database, interaction=None, user=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    mob = ''
    command = ''
    mode = ''
    for arg in clean_text_command.split()[3:]:
        if arg in ('hunt', 'adv'):
            break
        mob += f"{arg} "

    mob = mob.strip()

    for arg in clean_text_command.split()[3:]:
        if arg == 'hunt':
            command = 'hunt'
        elif arg == 'adv':
            command = 'adventure'
        elif arg in ('h', 'hardmode'):
            mode = 'hardmode'
        elif arg in ('n', 'normal'):
            mode = 'normal'
        elif arg in ('p', 'partener'):
            mode = 'partener'

    tier = ''
    if not user:
        last_arg = clean_text_command.split()[-1]
        if last_arg == 'global':
            await send_response(content=
                                f"<@{author.id}> For global data you also need to specify a horse tier at the and, like "
                                f"`pog tr hunt h global T9`.")
            return

        if last_arg.startswith('t') and last_arg[1:].isnumeric():
            horse_tier = int(last_arg[1:])
            if 5 >= horse_tier > 10:
                await send_response(content=f"<@{author.id}> Sorry, I only store data for the T6 - T10 horses")
                return
            tier = f"T{horse_tier}"
            last_arg = str(GLOBAL_USER)

        if get_user(last_arg):
            try:
                user = await client.fetch_user(get_user(last_arg))
            except discord.HTTPException:
                user = author
        else:
            user = author

    if user.id not in agrees_to_track_db:
        await send_response(content=f"<@{author.id}> I didn't track anything for this user!")
        return

    if user.id not in mob_database and user.id != GLOBAL_USER:
        await send_response(content=
                            f"<@{author.id}> I don't have any data stored for that user or you used an invalid user ID")
        return

    if user.id == GLOBAL_USER:
        key = f"{tier}{mob}{command}{mode}"
        if key not in mob_database:
            await send_response(content=
                                f"""<@{author.id}> Looks like I didn't track any global data for that mob yet.
Check `pog dex` to get the mob names you should use when searching.""")
            return
        data = mob_database[key]
        data = {command: {mode: {mob: data}}}
    else:
        data = mob_database[user.id]

    if mob not in data[command][mode]:
        if author.id != user.id:
            await send_response(content=
                                f"""<@{author.id}> Looks like I didn't track any data for that mob yet, for that user.
Check `pog tr mob dump <command> <mode> @user/userID` to see what I have stored for them and the correct mob names!""")
        else:
            await send_response(content=
                                f"""<@{author.id}> Looks like I didn't track any data for that mob yet.
Check `pog tr mob dump <command> <mode>` to see what I have stored for you and the correct mob names!""")
        return

    if not command or not mode:
        await send_response(content=
                            F"<@{author.id}> What are you trying to do? Correct usage: `pog tr mob <mob name> <command>`.")
        return

    emoji = ''
    if mob.upper() in HUNT_MOB_EMOJIS:
        emoji = HUNT_MOB_EMOJIS[mob.upper()]
    elif mob.upper() in ADV_MOB_EMOJIS:
        emoji = ADV_MOB_EMOJIS[mob.upper()]

    description = f"""🔹 dropped - how many times you got this type in a hunt
🔹 collected - how many you found in total (because T10 horse can give more than 1)

> {emoji} **{mob.title()} stats for {command.upper()} {mode.upper()}**

:dart: **Total encounters:** {data[command][mode][mob]['count']}
{EMOJIS['coin']} **Coins gained:** {data[command][mode][mob]['coins_gained']:,}
{EMOJIS['xp']} **XP gained:**  {data[command][mode][mob]['xp_gained']:,}
ㅤ
"""
    embed = discord.Embed(colour=random.randint(0, 0xffffff))
    embed.set_author(name=f"{user.name}'s mob stats", icon_url=user.avatar)
    embed.set_footer(text='Use `pog help stats` for the list of stat commands | Pog <3')
    if command == 'hunt':
        if data[command][mode][mob]['mob_drops']['total']:
            text = ""
            for drop in data[command][mode][mob]['mob_drops']:
                if drop == 'total':
                    continue
                if not data[command][mode][mob]['mob_drops'][drop]['found']:
                    continue

                found = data[command][mode][mob]['mob_drops'][drop]['found']
                del data[command][mode][mob]['mob_drops'][drop]['found']

                total_dropped = sum(data[command][mode][mob]['mob_drops'][drop].values())

                text += f"\n{EMOJIS[drop]} > `dropped:` {total_dropped}"
                if total_dropped != found:
                    text += f""", `collected:` {found:,}"""
                if not data[command][mode][mob]['count']:
                    data[command][mode][mob]['count'] = 1
                text += f""" ({(total_dropped / data[command][mode][mob]['count']) * 100:.2f}%)\n"""

                for amount in sorted(data[command][mode][mob]['mob_drops'][drop].keys()):
                    text += f"`x{amount}` at once - {data[command][mode][mob]['mob_drops'][drop][amount]} times → ({(data[command][mode][mob]['mob_drops'][drop][amount] / total_dropped) * 100:.2f}%)\n"

            embed.add_field(name='Mob drops', value=text + 'ㅤ', inline=False)

    if data[command][mode][mob]['lootboxes']['total']:
        drop_amounts = {}
        grand_total_dropped = 0
        grand_total_found = 0
        embed.add_field(name=':takeout_box: Lootboxes', value='', inline=False)
        for drop in data[command][mode][mob]['lootboxes']:
            if drop == 'total':
                continue
            if not data[command][mode][mob]['lootboxes'][drop]['found']:
                continue

            text = ""
            found = data[command][mode][mob]['lootboxes'][drop]['found']
            del data[command][mode][mob]['lootboxes'][drop]['found']

            grand_total_found += found

            total_dropped = sum(data[command][mode][mob]['lootboxes'][drop].values())
            grand_total_dropped += total_dropped

            text += f"\n{EMOJIS[drop]} > dropped: {total_dropped}, collected: {found:,} → ({(total_dropped / data[command][mode][mob]['lootboxes']['total']) * 100:.2f}%)\n"
            for amount in sorted(data[command][mode][mob]['lootboxes'][drop].keys()):
                if amount not in drop_amounts:
                    drop_amounts[amount] = data[command][mode][mob]['lootboxes'][drop][amount]
                else:
                    drop_amounts[amount] += data[command][mode][mob]['lootboxes'][drop][amount]

                text += f"`x{amount}` at once - {data[command][mode][mob]['lootboxes'][drop][amount]} times → ({(data[command][mode][mob]['lootboxes'][drop][amount] / total_dropped) * 100:.2f}%)\n"

            embed.add_field(name=f"{drop.title()} lootbox", value=text, inline=False)

        lootbox_text = f"**Total dropped:** {grand_total_dropped}. **Total collected:** {grand_total_found} → ({(grand_total_dropped / data[command][mode][mob]['count']) * 100:.2f}%)\n"
        for amount in sorted(drop_amounts.keys()):
            lootbox_text += f"`x{amount}` at once - {drop_amounts[amount]} times → ({(drop_amounts[amount] / sum(drop_amounts.values())) * 100:.2f}%)\n"

        for i, field in enumerate(embed.fields):
            if field.name == ':takeout_box: Lootboxes':
                embed.set_field_at(index=i, name=':takeout_box: Lootboxes', value=lootbox_text + 'ㅤ', inline=False)
                break

    embed.description = description

    await send_response(embed=embed)


def per_mob_add_player_to_database(userID, database):
    database[userID] = {'hunt': {'hardmode': {}, 'normal': {}, 'partener': {}},
                        'adventure': {'hardmode': {}, 'normal': {}}}


def add_player_to_database(userID, database):
    database[userID] = get_empty_db()


async def mob_dex(channel, author, command, interaction=None, area=0):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    if not area:
        try:
            area = int(command.split()[-1])
        except (TypeError, ValueError, IndexError):
            await send_response(content=F"<@{author.id}> Correct usage: `pog dex <area>`")
            return

    area_1 = F"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['SLIME']} Slime
{HUNT_MOB_EMOJIS['GOBLIN']} Goblin
{HUNT_MOB_EMOJIS['WOLF']} Wolf
> **Adventure mobs:**
{ADV_MOB_EMOJIS['MUTANT WATER BOTTLE']} Mutant Water Bottle
{ADV_MOB_EMOJIS['GIANT SPIDER']} Giant Spider
{ADV_MOB_EMOJIS['BUNCH OF BEES']} Bunch of Bees
ㅤ"""

    area_2 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['WOLF']} Wolf
{HUNT_MOB_EMOJIS['NYMPH']} Nymph
{HUNT_MOB_EMOJIS['SKELETON']} Skeleton
> **Adventure mobs:**
{ADV_MOB_EMOJIS['OGRE']} Ogre
{ADV_MOB_EMOJIS['DARK KNIGHT']} Dark Knight
{ADV_MOB_EMOJIS['HYPER GIANT BOWL']} Hyper Giant Bowl"""

    area_3 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['ZOMBIE']} Zombie
{HUNT_MOB_EMOJIS['GHOST']} Ghost
{HUNT_MOB_EMOJIS['BABY DEMON']} Baby Demon
> **Adventure mobs:**
{ADV_MOB_EMOJIS['MUTANT SHOE']} Mutant Shoe
{ADV_MOB_EMOJIS['WEREWOLF']} Werewolf
{ADV_MOB_EMOJIS['CENTAUR']} Centaur"""

    area_4 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['ZOMBIE']} Zombie
{HUNT_MOB_EMOJIS['WITCH']} Witch
{HUNT_MOB_EMOJIS['IMP']} Imp
> **Adventure mobs:**
{ADV_MOB_EMOJIS['CHIMERA']} Chimera
{ADV_MOB_EMOJIS['HYPER GIANT AERONAUTICAL ENGINE']} Hyper Giant Aeronautical Engine
{ADV_MOB_EMOJIS['GOLEM']} Golem
"""

    area_5 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['UNICORN']} Unicorn
{HUNT_MOB_EMOJIS['GHOUL']} Ghoul
{HUNT_MOB_EMOJIS['GIANT SCORPION']} Giant Scorpion
> **Adventure mobs:**
{ADV_MOB_EMOJIS['MAMMOTH']} Mammoth
{ADV_MOB_EMOJIS["MUTANT 'ESC' KEY"]} Mutant 'Esc' Key
{ADV_MOB_EMOJIS['ENT']} Ent"""
    area_6 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['UNICORN']} Unicorn
{HUNT_MOB_EMOJIS['SORCERER']} Sorcerer
{HUNT_MOB_EMOJIS['BABY ROBOT']} Baby Robot
> **Adventure mobs:**
{ADV_MOB_EMOJIS['DINOSAUR']} Dinosaur
{ADV_MOB_EMOJIS['HYPER GIANT DOOR']} Hyper Giant Door
{ADV_MOB_EMOJIS['CYCLOPS']} Cyclops
"""
    area_7 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['MERMAID']} Mermaid
{HUNT_MOB_EMOJIS['CECAELIA']} Cecaelia
{HUNT_MOB_EMOJIS['GIANT PIRANHA']} Giant Piranha
> **Adventure mobs:**
{ADV_MOB_EMOJIS['ATTACK HELICOPTER']} Attack Helicopter
{ADV_MOB_EMOJIS['MUTANT BOOK']} Mutant Book
{ADV_MOB_EMOJIS['HYDRA']} Hydra
"""
    area_8 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['MERMAID']} Mermaid
{HUNT_MOB_EMOJIS['NEREID']} Nereid
{HUNT_MOB_EMOJIS['GIANT CROCODILE']} Giant Cocodrile
> **Adventure mobs:**
{ADV_MOB_EMOJIS['KRAKEN']} Kraken
{ADV_MOB_EMOJIS['HYPER GIANT CHEST']} Hyper Giant Chest
{ADV_MOB_EMOJIS['LEVIATHAN']} Leviathan
"""
    area_9 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['KILLER ROBOT']} Killer Robot
{HUNT_MOB_EMOJIS['DEMON']} Demon
{HUNT_MOB_EMOJIS['HARPY']} Harpy
> **Adventure mobs:**
{ADV_MOB_EMOJIS['WAR TANK']} War Tank
{ADV_MOB_EMOJIS['MUTANT BACKPACK']} Mutant Backpack
{ADV_MOB_EMOJIS['WYRM']} Wyrm
"""
    area_10 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['KILLER ROBOT']} Killer Robot
{HUNT_MOB_EMOJIS['MANTICORE']} Manticore
{HUNT_MOB_EMOJIS['DULLAHAN']} Dullahan
> **Adventure mobs:**
{ADV_MOB_EMOJIS['HYPER GIANT TOILET']} Hyper Giant Toilet
{ADV_MOB_EMOJIS['TITAN']} Titan
{ADV_MOB_EMOJIS['TYPHON']} Typhon
"""
    area_11 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['SCALED BABY DRAGON']} Scaled Baby Dragon
{HUNT_MOB_EMOJIS['BABY DRAGON']} Baby Dragon
{HUNT_MOB_EMOJIS['YOUNG DRAGON']} Young Dragon
> **Adventure mobs:**
{ADV_MOB_EMOJIS['ANCIENT DRAGON']} Ancient Dragon
{ADV_MOB_EMOJIS['MUTANT DRAGON']} Mutant Dragon
"""
    area_12 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['KID DRAGON']} Kid Dragon
{HUNT_MOB_EMOJIS['SCALED KID DRAGON']} Scaled Kid Dragon
{HUNT_MOB_EMOJIS['NOT SO YOUNG DRAGON']} Not so Young Dragon
> **Adventure mobs:**
{ADV_MOB_EMOJIS['HYPER GIANT DRAGON']} Hyper Giant Dragon
{ADV_MOB_EMOJIS['EVEN MORE ANCIENT DRAGON']} Even more Ancient Dragon
"""
    area_13 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['TEEN DRAGON']} Teen Dragon
{HUNT_MOB_EMOJIS['SCALED TEEN DRAGON']} Scaled Teen Dragon
{HUNT_MOB_EMOJIS['DEFINITELY NOT YOUNG DRAGON']} Definitely Not Young Dragon
> **Adventure mobs:**
{ADV_MOB_EMOJIS['ANCIENTEST DRAGON']} Ancientest Dragon
{ADV_MOB_EMOJIS['ANOTHER MUTANT DRAGON LIKE IN AREA 11 BUT STRONGER']} ANOTHER MUTANT DRAGON LIKE IN AREA 11 BUT STRONGER
"""
    area_14 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['ADULT DRAGON']} Adult Dragon
{HUNT_MOB_EMOJIS['SCALED ADULT DRAGON']} Scaled Adult Dragon
{HUNT_MOB_EMOJIS['NOT SO YOUNG DRAGON']} Not Young at all Dragon
> **Adventure mobs:**
{ADV_MOB_EMOJIS['just purple DRAGON']} Just Purple Dragon
{ADV_MOB_EMOJIS['YES, AS YOU EXPECTED, ANOTHER HYPER GIANT DRAGON BUT OP ETC']} YES, AS YOU EXPECTED, ANOTHER HYPER GIANT DRAGON BUT OP ETC
"""
    area_15 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['OLD DRAGON']} Old Dragon
{HUNT_MOB_EMOJIS['SCALED OLD DRAGON']} Scaled Old Dragon
{HUNT_MOB_EMOJIS['HOW DO YOU DARE CALL THIS DRAGON "YOUNG"???']} How do you dare to call this Dragon "Young"
> **Adventure mobs:**
{ADV_MOB_EMOJIS['i have no more ideas DRAGON']} I have no more ideas dragon
{ADV_MOB_EMOJIS['MUTANTEST DRAGON']} MUTANTEST DRAGON
"""
    area_16 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['VOID FRAGMENT']} Void Fragment 
{HUNT_MOB_EMOJIS['VOID PARTICLES']} Void Particles
{HUNT_MOB_EMOJIS['VOID SHARD']} Void Shard
> **Adventure mobs:**
{ADV_MOB_EMOJIS['VOID CONE']} Void Cone
{ADV_MOB_EMOJIS['VOID CUBE']} Void Cube
{ADV_MOB_EMOJIS['VOID SPHERE']} Void Sphere
"""
    area_17 = f"""
> **Hunt mobs:**
{HUNT_MOB_EMOJIS['ABYSS BUG']} Abyss Bug
{HUNT_MOB_EMOJIS['NOTHING']} Nothing
{HUNT_MOB_EMOJIS['SHADOW HANDS']} Shadow Hands
> **Adventure mobs:**
{ADV_MOB_EMOJIS['ABYSS WORM']} Abyss Worm
{ADV_MOB_EMOJIS['SHADOW CREATURE']} Shadow Creature
{ADV_MOB_EMOJIS['SHADOW ENTITY']} Shadow Entity
"""

    embed = discord.Embed(colour=random.randint(0, 0xffffff))
    embed.set_author(name=f"{author.name}'s dex command", icon_url=author.avatar)
    embed.set_footer(text="Use [pog tr mob <monster> <command>] to view your stats for that mob")

    if area == 1:
        embed.add_field(name='——— AREA 1 ———', value=area_1)
    elif area == 2:
        embed.add_field(name=' ——— AREA 2 ———', value=area_2)
    elif area == 3:
        embed.add_field(name='——— AREA 3 ———', value=area_3)
    elif area == 4:
        embed.add_field(name='——— AREA 4 ———', value=area_4)
    elif area == 5:
        embed.add_field(name='——— AREA 5 ———', value=area_5)
    elif area == 6:
        embed.add_field(name='——— AREA 6 ———', value=area_6)
    elif area == 7:
        embed.add_field(name='——— AREA 7 ———', value=area_7)
    elif area == 8:
        embed.add_field(name='——— AREA 8 ———', value=area_8)
    elif area == 9:
        embed.add_field(name='——— AREA 9 ———', value=area_9)
    elif area == 10:
        embed.add_field(name='——— AREA 10 ———', value=area_10)
    elif area == 11:
        embed.add_field(name='——— AREA 11 ———', value=area_11)
    elif area == 12:
        embed.add_field(name='——— AREA 12 ———', value=area_12)
    elif area == 13:
        embed.add_field(name='——— AREA 13 ———', value=area_13)
    elif area == 14:
        embed.add_field(name='——— AREA 14 ———', value=area_14)
    elif area == 15:
        embed.add_field(name='——— AREA 15 ———', value=area_15)
    elif area == 16:
        embed.add_field(name='——— AREA 16 ———', value=area_16)
    elif area == 17:
        embed.add_field(name='——— AREA 17 ———', value=area_17)
    else:
        embed.add_field(name='IDK', value="I don't have data for this area yet (i was too lazy too add it)")

    await send_response(embed=embed)


async def add_partener(channel, author, command, database, client, interaction=None, user=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    if not user:
        try:
            partener = int(command.split()[-1][2:-1])
        except (IndexError, ValueError, TypeError):
            await send_response(content=f"<@{author.id}> Correct usage: `pog tr marry @user`.")
            return
    else:
        partener = user.id

    if author.id == partener:
        await send_response(content=f"<@{author.id}> You can't marry yourself lmao")
        return

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Yes", emoji="💝", style=discord.ButtonStyle.green, custom_id="yes_reset"))
    view.add_item(discord.ui.Button(label="Yucky no", emoji="💔", style=discord.ButtonStyle.red, custom_id="no_reset"))

    message = await send_response(view=view, content=f"<@{partener}> is **{author.name}** really your partner in EPIC RPG?")
    await (await channel.send(f"<@{partener}>")).delete()

    def check(inter: discord.Interaction):
        return inter.message and inter.message.id == message.id

    while True:
        try:
            interaction = await client.wait_for('interaction', timeout=120, check=check)
        except asyncio.TimeoutError:
            for child in view.children:
                child.disabled = True

            view.stop()
            await interaction.message.edit(view=view)
            return

        if interaction.user.id != partener:
            await interaction.response.send_message(ontent="This is not your command!", ephemeral=True)
            continue

        if interaction.data['custom_id'] == "yes_reset":
            data = database[author.id]
            old_partener = data['info']['partener_ID']
            if old_partener:
                old = database[old_partener]
                old['info']['partener_ID'] = 0
                old['info']['partener_name'] = ''
                database[old_partener] = old

            other_person = database[partener]

            data['info']['partener_name'] = interaction.user.name
            data['info']['partener_ID'] = partener

            other_person['info']['partener_name'] = author.name
            other_person['info']['partener_ID'] = author.id

            await interaction.response.send_message(
                f":heart: <@{author.id}> <@{partener}> So cute! From now on all of the drops you get "
                f"for your partner will show up in their `partner / p` command mode! :heart:")

            database[author.id] = data
            database[partener] = other_person
        else:
            await interaction.response.send_message(content=f"Alright! Make sure to ping your real partner next time.")
            for child in view.children:
                child.disabled = True

            view.stop()
            await interaction.message.edit(view=view)
            return


async def divorce(channel, author, database, interaction=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    data = database[author.id]
    partener_ID = data['info']['partener_ID']
    if not partener_ID:
        await send_response(content=f"<@{author.id}> You are not married lol, use `/marry-for-tracking`")
        return

    other_person = database[partener_ID]

    data['info']['partener_ID'] = 0
    data['info']['partener_name'] = ''

    other_person['info']['partener_ID'] = 0
    other_person['info']['partener_name'] = ''

    database[author.id] = data
    database[partener_ID] = other_person
    await send_response(content=
                        f"💔 Noooo! I have removed your partner. I hope you will find someone who loves you next time!")


async def disable_tracking(channel, author, database, mode, agree_db, interaction=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    data = database[author.id]

    if mode == 'enable':
        data['info']['disabled_tracking'] = False
        await send_response(content=
                            f"<@{author.id}> Thank you! From now on I will track all of your commands. Use `/help` to learn more.")
    elif mode == 'disable':
        data['info']['disabled_tracking'] = True
        await send_response(content=
                            f"<@{author.id}> Welp. From this point on, I will no longer track any of your commands. Your older data will remain though.")
        del agree_db[author.id]
        agree_db.commit()

    database[author.id] = data


async def tracking_help(message):
    text = """> **COMMAND TRACKING**
This feature will track all of your commands, in almost every possible way, then show you the data gathered.
To check the data for another users just ping them after the commands
To check global data, just add `global` at the end of any command

> **Possible modes for hunt and adv:**
🔸 `h` - hardmode ┃ `n` - normal hunt ┃ `p` - partner hunt

> **🌲 WORKING COMMANDS**
🔹 `pog tr <working command>` - shows the stats for any working command provided
🔹 `pog tr void aura <area>` - shows stats related to the void aura

> **<:unicorn:979027505702920192> HUNTS**
🔹 `pog tr hunt <mode>` - shows the hunt data
🔹 `pog tr mob <full mob name> hunt <mode>` - shows all data gathered for a specific mob in a specific command in hunt

> **<:Lindorei_helped_me:979034794501476352> ADVENTURES**
🔹 `pog tr adv <mode>` - shows the adventure data
🔹 `pog tr mob <full mob name> adv <mode>` - shows all data gathered for a specific mob in a specific command in adv

> **<:godly:977508095678877706> LOOTBOXES**
🔹 `pog tr <lootbox type>` - example: `pog tr uncommon`
🔹 add `one` at the end of the command to see any useful stats - example: `pog tr godly one`

> <:cat:951188235814572052> **PET ADVENTURE REWARDS**:
🔹 `pog tr petadv <pet_tier>` - shows the data for the pet adventure rewards, if no tier is specified, shows for all tiers at once

> 🤼 **TRAINING**
🔹 `pog tr tr <command_amount_used_to_catch_pet>` - shows the stats for training, if no command amount is specified, shows the stats \
for all trainings. Use `globalt10`, `globalt9`... for seeing the data for specific horse tiers

> **<:t10_horse:985611263432335370> T10 HORSE EXTRA LOOT**
🔹 `pog tr t10 hunt <mode>` - shows extra drops from a tier 10 horse in hunt
🔹 `pog tr t10 adv <mode>` - shows extra drops from a tier 10 horse in adventure


> **⚙ HELPFUL COMMANDS**
🔹 `pog dex <area>` - shows all mobs in this area
🔹 `pog tr mob dump <command> <mode>` - shows you all the mobs stored for this type of command. Use this name when searching for a mob

> **<:green_arrow_right:968808534181576714> RESET AND SAVE DATA:**
🔹 `pog tr reset <command>` - resets the data and gives you a backup of it. Use `all` to reset everything and `work` to reset \
all working commands. For the rest use the command name, like `hunt`, `farm`, `chainsaw`, etc
🔹 `pog tr load` + attachment - loads the data from the attachment, use only `.pog` files. Your current data will be overwritten!

> **🍄 MISC:**
🔹 `pog tr marry @user` - set this person as your EPIC RPG partner
🔹 `pog tr divorce` - remove your partner
🔹 `pog tr disable` - stop the bot from tracking your commands
🔹 `pog tr enable` - reverses the previous command
"""
    embed = discord.Embed(colour=random.randint(0, 0xffffff), description=text)
    embed.set_author(name=f"{message.author.name}'s stats help command", icon_url=message.author.avatar)
    embed.set_footer(text="If you have suggestions let me know!")

    await message.channel.send(embed=embed)


def get_empty_db():
    return {
        'info': {'partener_name': '',
                 'partener_ID': 0,
                 'disabled_tracking': False,
                 'verified_user': False},

        'hunt': {
            'hardmode': {
                'count': 0,
                'deaths': 0,
                'coins_gained': 0,
                'xp_gained': 0,
                'mob_drops': {'total': 0,
                              'wolf_skin': {'seen': 0, 'found': 0},
                              'zombie_eye': {'seen': 0, 'found': 0},
                              'unicorn_horn': {'seen': 0, 'found': 0},
                              'mermaid_hair': {'seen': 0, 'found': 0},
                              'chip': {'seen': 0, 'found': 0},
                              'dragon_scale': {'seen': 0, 'found': 0},
                              'dark_energy': {'seen': 0, 'found': 0}},

                'lootboxes': {'total': 0,
                              'common': {'seen': 0, 'found': 0},
                              'uncommon': {'seen': 0, 'found': 0},
                              'rare': {'seen': 0, 'found': 0},
                              'epic': {'seen': 0, 'found': 0},
                              'edgy': {'seen': 0, 'found': 0},
                              'omega': {'seen': 0, 'found': 0},
                              'godly': {'seen': 0, 'found': 0},
                              'void': {'seen': 0, 'found': 0}}},

            'normal': {
                'count': 0,
                'deaths': 0,
                'coins_gained': 0,
                'xp_gained': 0,
                'mob_drops': {'total': 0,
                              'wolf_skin': {'seen': 0, 'found': 0},
                              'zombie_eye': {'seen': 0, 'found': 0},
                              'unicorn_horn': {'seen': 0, 'found': 0},
                              'mermaid_hair': {'seen': 0, 'found': 0},
                              'chip': {'seen': 0, 'found': 0},
                              'dragon_scale': {'seen': 0, 'found': 0},
                              'dark_energy': {'seen': 0, 'found': 0}},

                'lootboxes': {'total': 0,
                              'common': {'seen': 0, 'found': 0},
                              'uncommon': {'seen': 0, 'found': 0},
                              'rare': {'seen': 0, 'found': 0},
                              'epic': {'seen': 0, 'found': 0},
                              'edgy': {'seen': 0, 'found': 0},
                              'omega': {'seen': 0, 'found': 0},
                              'godly': {'seen': 0, 'found': 0},
                              'void': {'seen': 0, 'found': 0}}},

            'partener': {
                'count': 0,
                'deaths': 0,
                'coins_gained': 0,
                'xp_gained': 0,
                'mob_drops': {'total': 0,
                              'wolf_skin': {'seen': 0, 'found': 0},
                              'zombie_eye': {'seen': 0, 'found': 0},
                              'unicorn_horn': {'seen': 0, 'found': 0},
                              'mermaid_hair': {'seen': 0, 'found': 0},
                              'chip': {'seen': 0, 'found': 0},
                              'dragon_scale': {'seen': 0, 'found': 0},
                              'dark_energy': {'seen': 0, 'found': 0}},

                'lootboxes': {'total': 0,
                              'common': {'seen': 0, 'found': 0},
                              'uncommon': {'seen': 0, 'found': 0},
                              'rare': {'seen': 0, 'found': 0},
                              'epic': {'seen': 0, 'found': 0},
                              'edgy': {'seen': 0, 'found': 0},
                              'omega': {'seen': 0, 'found': 0},
                              'godly': {'seen': 0, 'found': 0},
                              'void': {'seen': 0, 'found': 0}}}},

        'adventure': {'hardmode': {'count': 0,
                                   'deaths': 0,
                                   'coins_gained': 0,
                                   'xp_gained': 0,
                                   'lootboxes': {'total': 0,
                                                 'common': {'seen': 0, 'found': 0},
                                                 'uncommon': {'seen': 0, 'found': 0},
                                                 'rare': {'seen': 0, 'found': 0},
                                                 'epic': {'seen': 0, 'found': 0},
                                                 'edgy': {'seen': 0, 'found': 0},
                                                 'omega': {'seen': 0, 'found': 0},
                                                 'godly': {'seen': 0, 'found': 0},
                                                 'void': {'seen': 0, 'found': 0}}},
                      'normal': {'count': 0,
                                 'deaths': 0,
                                 'coins_gained': 0,
                                 'xp_gained': 0,
                                 'lootboxes': {'total': 0,
                                               'common': {'seen': 0, 'found': 0},
                                               'uncommon': {'seen': 0, 'found': 0},
                                               'rare': {'seen': 0, 'found': 0},
                                               'epic': {'seen': 0, 'found': 0},
                                               'edgy': {'seen': 0, 'found': 0},
                                               'omega': {'seen': 0, 'found': 0},
                                               'godly': {'seen': 0, 'found': 0},
                                               'void': {'seen': 0, 'found': 0}}}},

        'tier_10': {'has_t10': False,
                    'adventure': {'hardmode': {'count': 0,
                                               'lootboxes': {'total': 0,
                                                             'common': {},
                                                             'uncommon': {},
                                                             'rare': {},
                                                             'epic': {},
                                                             'edgy': {},
                                                             'omega': {},
                                                             'godly': {},
                                                             'void': {}}},
                                  'normal': {'count': 0,
                                             'lootboxes': {'total': 0,
                                                           'common': {},
                                                           'uncommon': {},
                                                           'rare': {},
                                                           'epic': {},
                                                           'edgy': {},
                                                           'omega': {},
                                                           'godly': {},
                                                           'void': {}}}},
                    'hunt': {'hardmode': {'count': 0,
                                          'mob_drops': {'total': 0},
                                          'lootboxes': {'total': 0,
                                                        'common': {},
                                                        'uncommon': {},
                                                        'rare': {},
                                                        'epic': {},
                                                        'edgy': {},
                                                        'omega': {},
                                                        'godly': {},
                                                        'void': {}}},
                             'normal': {'count': 0,
                                        'mob_drops': {'total': 0},
                                        'lootboxes': {'total': 0,
                                                      'common': {},
                                                      'uncommon': {},
                                                      'rare': {},
                                                      'epic': {},
                                                      'edgy': {},
                                                      'omega': {},
                                                      'godly': {},
                                                      'void': {}}},
                             'partener': {'count': 0,
                                          'mob_drops': {'total': 0},
                                          'lootboxes': {'total': 0,
                                                        'common': {},
                                                        'uncommon': {},
                                                        'rare': {},
                                                        'epic': {},
                                                        'edgy': {},
                                                        'omega': {},
                                                        'godly': {},
                                                        'void': {}}}}},
        'working_commands': {
            'chop': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                     'wooden': {'count': 0, 'resources': 0},
                     'epic': {'count': 0, 'resources': 0},
                     'super': {'count': 0, 'resources': 0},
                     'mega': {'count': 0, 'resources': 0},
                     'hyper': {'count': 0, 'resources': 0},
                     'ultra': {'count': 0, 'resources': 0},
                     'ultimate': {'count': 0, 'resources': 0}},

            'axe': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                    'wooden': {'count': 0, 'resources': 0},
                    'epic': {'count': 0, 'resources': 0},
                    'super': {'count': 0, 'resources': 0},
                    'mega': {'count': 0, 'resources': 0},
                    'hyper': {'count': 0, 'resources': 0},
                    'ultra': {'count': 0, 'resources': 0},
                    'ultimate': {'count': 0, 'resources': 0}},

            'bowsaw': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                       'wooden': {'count': 0, 'resources': 0},
                       'epic': {'count': 0, 'resources': 0},
                       'super': {'count': 0, 'resources': 0},
                       'mega': {'count': 0, 'resources': 0},
                       'hyper': {'count': 0, 'resources': 0},
                       'ultra': {'count': 0, 'resources': 0},
                       'ultimate': {'count': 0, 'resources': 0}},

            'chainsaw': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                         'wooden': {'count': 0, 'resources': 0},
                         'epic': {'count': 0, 'resources': 0},
                         'super': {'count': 0, 'resources': 0},
                         'mega': {'count': 0, 'resources': 0},
                         'hyper': {'count': 0, 'resources': 0},
                         'ultra': {'count': 0, 'resources': 0},
                         'ultimate': {'count': 0, 'resources': 0}},

            'fish': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                     'normie': {'count': 0, 'resources': 0},
                     'golden': {'count': 0, 'resources': 0},
                     'epic': {'count': 0, 'resources': 0},
                     'super': {'count': 0, 'resources': 0}},

            'net': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                    'normie': {'count': 0, 'resources': 0},
                    'golden': {'count': 0, 'resources': 0},
                    'epic': {'count': 0, 'resources': 0},
                    'super': {'count': 0, 'resources': 0}},

            'boat': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                     'normie': {'count': 0, 'resources': 0},
                     'golden': {'count': 0, 'resources': 0},
                     'epic': {'count': 0, 'resources': 0},
                     'super': {'count': 0, 'resources': 0}},

            'bigboat': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                        'normie': {'count': 0, 'resources': 0},
                        'golden': {'count': 0, 'resources': 0},
                        'epic': {'count': 0, 'resources': 0},
                        'super': {'count': 0, 'resources': 0}},

            'mine': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                     'coins': {'count': 0, 'resources': 0},
                     'rubies': {'count': 0, 'resources': 0}},

            'pickaxe': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                        'coins': {'count': 0, 'resources': 0},
                        'rubies': {'count': 0, 'resources': 0}},

            'drill': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                      'coins': {'count': 0, 'resources': 0},
                      'rubies': {'count': 0, 'resources': 0}},

            'dynamite': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                         'coins': {'count': 0, 'resources': 0},
                         'rubies': {'count': 0, 'resources': 0}},

            'pickup': {'count': 0,
                       'bonus': {'count': 0, 'amount': 0},
                       'apple': {'count': 0, 'resources': 0},
                       'banana': {'count': 0, 'resources': 0},
                       'watermelon': {'count': 0, 'resources': 0}},

            'tractor': {'count': 0,
                        'bonus': {'count': 0, 'amount': 0},
                        'apple': {'count': 0, 'resources': 0},
                        'banana': {'count': 0, 'resources': 0},
                        'watermelon': {'count': 0, 'resources': 0}},

            'greenhouse': {'count': 0,
                           'bonus': {'count': 0, 'amount': 0},
                           'apple': {'count': 0, 'resources': 0},
                           'banana': {'count': 0, 'resources': 0},
                           'watermelon': {'count': 0, 'resources': 0}},

            'ladder': {'count': 0,
                       'bonus': {'count': 0, 'amount': 0},
                       'apple': {'count': 0, 'resources': 0},
                       'banana': {'count': 0, 'resources': 0},
                       'watermelon': {'count': 0, 'resources': 0}}},

        'farm': {'xp_gained': 0,
                 'special_event': {'count': 0, 'won': [0, 0]},
                 'special_seeds': {'count': 0,
                                   'carrot': {'count': 0, 'amounts': {}},
                                   'potato': {'count': 0, 'amounts': {}},
                                   'bread': {'count': 0, 'amounts': {}}},
                 'normal_farm': {'count': 0,
                                 'bread': {'count': 0, 'resources': 0},
                                 'carrot': {'count': 0, 'resources': 0},
                                 'potato': {'count': 0, 'resources': 0}},
                 'using_seed': {'count': 0,
                                'bread': {'count': 0, 'resources': 0, 'seed_back': {}},
                                'carrot': {'count': 0, 'resources': 0, 'seed_back': {}},
                                'potato': {'count': 0, 'resources': 0, 'seed_back': {}}}}}


def get_empty_hunt():
    return {
        'hardmode': {
            'count': 0,
            'deaths': 0,
            'coins_gained': 0,
            'xp_gained': 0,
            'mob_drops': {'total': 0,
                          'wolf_skin': {'seen': 0, 'found': 0},
                          'zombie_eye': {'seen': 0, 'found': 0},
                          'unicorn_horn': {'seen': 0, 'found': 0},
                          'mermaid_hair': {'seen': 0, 'found': 0},
                          'chip': {'seen': 0, 'found': 0},
                          'dragon_scale': {'seen': 0, 'found': 0},
                          'dark_energy': {'seen': 0, 'found': 0}},

            'lootboxes': {'total': 0,
                          'common': {'seen': 0, 'found': 0},
                          'uncommon': {'seen': 0, 'found': 0},
                          'rare': {'seen': 0, 'found': 0},
                          'epic': {'seen': 0, 'found': 0},
                          'edgy': {'seen': 0, 'found': 0},
                          'omega': {'seen': 0, 'found': 0},
                          'godly': {'seen': 0, 'found': 0},
                          'void': {'seen': 0, 'found': 0}}},

        'normal': {
            'count': 0,
            'deaths': 0,
            'coins_gained': 0,
            'xp_gained': 0,
            'mob_drops': {'total': 0,
                          'wolf_skin': {'seen': 0, 'found': 0},
                          'zombie_eye': {'seen': 0, 'found': 0},
                          'unicorn_horn': {'seen': 0, 'found': 0},
                          'mermaid_hair': {'seen': 0, 'found': 0},
                          'chip': {'seen': 0, 'found': 0},
                          'dragon_scale': {'seen': 0, 'found': 0},
                          'dark_energy': {'seen': 0, 'found': 0}},

            'lootboxes': {'total': 0,
                          'common': {'seen': 0, 'found': 0},
                          'uncommon': {'seen': 0, 'found': 0},
                          'rare': {'seen': 0, 'found': 0},
                          'epic': {'seen': 0, 'found': 0},
                          'edgy': {'seen': 0, 'found': 0},
                          'omega': {'seen': 0, 'found': 0},
                          'godly': {'seen': 0, 'found': 0},
                          'void': {'seen': 0, 'found': 0}}},

        'partener': {
            'count': 0,
            'deaths': 0,
            'coins_gained': 0,
            'xp_gained': 0,
            'mob_drops': {'total': 0,
                          'wolf_skin': {'seen': 0, 'found': 0},
                          'zombie_eye': {'seen': 0, 'found': 0},
                          'unicorn_horn': {'seen': 0, 'found': 0},
                          'mermaid_hair': {'seen': 0, 'found': 0},
                          'chip': {'seen': 0, 'found': 0},
                          'dragon_scale': {'seen': 0, 'found': 0},
                          'dark_energy': {'seen': 0, 'found': 0}},

            'lootboxes': {'total': 0,
                          'common': {'seen': 0, 'found': 0},
                          'uncommon': {'seen': 0, 'found': 0},
                          'rare': {'seen': 0, 'found': 0},
                          'epic': {'seen': 0, 'found': 0},
                          'edgy': {'seen': 0, 'found': 0},
                          'omega': {'seen': 0, 'found': 0},
                          'godly': {'seen': 0, 'found': 0},
                          'void': {'seen': 0, 'found': 0}}}}


def get_empty_partener():
    return {
        'count': 0,
        'deaths': 0,
        'coins_gained': 0,
        'xp_gained': 0,
        'mob_drops': {'total': 0,
                      'wolf_skin': {'seen': 0, 'found': 0},
                      'zombie_eye': {'seen': 0, 'found': 0},
                      'unicorn_horn': {'seen': 0, 'found': 0},
                      'mermaid_hair': {'seen': 0, 'found': 0},
                      'chip': {'seen': 0, 'found': 0},
                      'dragon_scale': {'seen': 0, 'found': 0},
                      'dark_energy': {'seen': 0, 'found': 0}},

        'lootboxes': {'total': 0,
                      'common': {'seen': 0, 'found': 0},
                      'uncommon': {'seen': 0, 'found': 0},
                      'rare': {'seen': 0, 'found': 0},
                      'epic': {'seen': 0, 'found': 0},
                      'edgy': {'seen': 0, 'found': 0},
                      'omega': {'seen': 0, 'found': 0},
                      'godly': {'seen': 0, 'found': 0},
                      'void': {'seen': 0, 'found': 0}}}


def get_empty_adv():
    return {'hardmode': {'count': 0,
                         'deaths': 0,
                         'coins_gained': 0,
                         'xp_gained': 0,
                         'lootboxes': {'total': 0,
                                       'common': {'seen': 0, 'found': 0},
                                       'uncommon': {'seen': 0, 'found': 0},
                                       'rare': {'seen': 0, 'found': 0},
                                       'epic': {'seen': 0, 'found': 0},
                                       'edgy': {'seen': 0, 'found': 0},
                                       'omega': {'seen': 0, 'found': 0},
                                       'godly': {'seen': 0, 'found': 0},
                                       'void': {'seen': 0, 'found': 0}}},
            'normal': {'count': 0,
                       'deaths': 0,
                       'coins_gained': 0,
                       'xp_gained': 0,
                       'lootboxes': {'total': 0,
                                     'common': {'seen': 0, 'found': 0},
                                     'uncommon': {'seen': 0, 'found': 0},
                                     'rare': {'seen': 0, 'found': 0},
                                     'epic': {'seen': 0, 'found': 0},
                                     'edgy': {'seen': 0, 'found': 0},
                                     'omega': {'seen': 0, 'found': 0},
                                     'godly': {'seen': 0, 'found': 0},
                                     'void': {'seen': 0, 'found': 0}}}}


def get_empty_working():
    return {
        'chop': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                 'wooden': {'count': 0, 'resources': 0},
                 'epic': {'count': 0, 'resources': 0},
                 'super': {'count': 0, 'resources': 0},
                 'mega': {'count': 0, 'resources': 0},
                 'hyper': {'count': 0, 'resources': 0},
                 'ultra': {'count': 0, 'resources': 0},
                 'ultimate': {'count': 0, 'resources': 0}},

        'axe': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                'wooden': {'count': 0, 'resources': 0},
                'epic': {'count': 0, 'resources': 0},
                'super': {'count': 0, 'resources': 0},
                'mega': {'count': 0, 'resources': 0},
                'hyper': {'count': 0, 'resources': 0},
                'ultra': {'count': 0, 'resources': 0},
                'ultimate': {'count': 0, 'resources': 0}},

        'bowsaw': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                   'wooden': {'count': 0, 'resources': 0},
                   'epic': {'count': 0, 'resources': 0},
                   'super': {'count': 0, 'resources': 0},
                   'mega': {'count': 0, 'resources': 0},
                   'hyper': {'count': 0, 'resources': 0},
                   'ultra': {'count': 0, 'resources': 0},
                   'ultimate': {'count': 0, 'resources': 0}},

        'chainsaw': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                     'wooden': {'count': 0, 'resources': 0},
                     'epic': {'count': 0, 'resources': 0},
                     'super': {'count': 0, 'resources': 0},
                     'mega': {'count': 0, 'resources': 0},
                     'hyper': {'count': 0, 'resources': 0},
                     'ultra': {'count': 0, 'resources': 0},
                     'ultimate': {'count': 0, 'resources': 0}},

        'fish': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                 'normie': {'count': 0, 'resources': 0},
                 'golden': {'count': 0, 'resources': 0},
                 'epic': {'count': 0, 'resources': 0},
                 'super': {'count': 0, 'resources': 0}},

        'net': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                'normie': {'count': 0, 'resources': 0},
                'golden': {'count': 0, 'resources': 0},
                'epic': {'count': 0, 'resources': 0},
                'super': {'count': 0, 'resources': 0}},

        'boat': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                 'normie': {'count': 0, 'resources': 0},
                 'golden': {'count': 0, 'resources': 0},
                 'epic': {'count': 0, 'resources': 0},
                 'super': {'count': 0, 'resources': 0}},

        'bigboat': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                    'normie': {'count': 0, 'resources': 0},
                    'golden': {'count': 0, 'resources': 0},
                    'epic': {'count': 0, 'resources': 0},
                    'super': {'count': 0, 'resources': 0}},

        'mine': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                 'coins': {'count': 0, 'resources': 0},
                 'rubies': {'count': 0, 'resources': 0}},

        'pickaxe': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                    'coins': {'count': 0, 'resources': 0},
                    'rubies': {'count': 0, 'resources': 0}},

        'drill': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                  'coins': {'count': 0, 'resources': 0},
                  'rubies': {'count': 0, 'resources': 0}},

        'dynamite': {'count': 0, 'bonus': {'count': 0, 'amount': 0},
                     'coins': {'count': 0, 'resources': 0},
                     'rubies': {'count': 0, 'resources': 0}},

        'pickup': {'count': 0,
                   'bonus': {'count': 0, 'amount': 0},
                   'apple': {'count': 0, 'resources': 0},
                   'banana': {'count': 0, 'resources': 0},
                   'watermelon': {'count': 0, 'resources': 0}},

        'tractor': {'count': 0,
                    'bonus': {'count': 0, 'amount': 0},
                    'apple': {'count': 0, 'resources': 0},
                    'banana': {'count': 0, 'resources': 0},
                    'watermelon': {'count': 0, 'resources': 0}},

        'greenhouse': {'count': 0,
                       'bonus': {'count': 0, 'amount': 0},
                       'apple': {'count': 0, 'resources': 0},
                       'banana': {'count': 0, 'resources': 0},
                       'watermelon': {'count': 0, 'resources': 0}},

        'ladder': {'count': 0,
                   'bonus': {'count': 0, 'amount': 0},
                   'apple': {'count': 0, 'resources': 0},
                   'banana': {'count': 0, 'resources': 0},
                   'watermelon': {'count': 0, 'resources': 0}}}


def get_empty_global_db():
    return {
        'T10': {'hunt': get_empty_hunt(), 'adventure': get_empty_adv()},
        'T9': {'hunt': get_empty_hunt(), 'adventure': get_empty_adv()},
        'T8': {'hunt': get_empty_hunt(), 'adventure': get_empty_adv()},
        'T7': {'hunt': get_empty_hunt(), 'adventure': get_empty_adv()},
        'T6': {'hunt': get_empty_hunt(), 'adventure': get_empty_adv()},

        'tier_10': {'has_t10': True,
                    'adventure': {'hardmode': {'count': 0,
                                               'lootboxes': {'total': 0,
                                                             'common': {},
                                                             'uncommon': {},
                                                             'rare': {},
                                                             'epic': {},
                                                             'edgy': {},
                                                             'omega': {},
                                                             'godly': {},
                                                             'void': {}}},
                                  'normal': {'count': 0,
                                             'lootboxes': {'total': 0,
                                                           'common': {},
                                                           'uncommon': {},
                                                           'rare': {},
                                                           'epic': {},
                                                           'edgy': {},
                                                           'omega': {},
                                                           'godly': {},
                                                           'void': {}}}},
                    'hunt': {'hardmode': {'count': 0,
                                          'mob_drops': {'total': 0},
                                          'lootboxes': {'total': 0,
                                                        'common': {},
                                                        'uncommon': {},
                                                        'rare': {},
                                                        'epic': {},
                                                        'edgy': {},
                                                        'omega': {},
                                                        'godly': {},
                                                        'void': {}}},
                             'normal': {'count': 0,
                                        'mob_drops': {'total': 0},
                                        'lootboxes': {'total': 0,
                                                      'common': {},
                                                      'uncommon': {},
                                                      'rare': {},
                                                      'epic': {},
                                                      'edgy': {},
                                                      'omega': {},
                                                      'godly': {},
                                                      'void': {}}},
                             'partener': {'count': 0,
                                          'mob_drops': {'total': 0},
                                          'lootboxes': {'total': 0,
                                                        'common': {},
                                                        'uncommon': {},
                                                        'rare': {},
                                                        'epic': {},
                                                        'edgy': {},
                                                        'omega': {},
                                                        'godly': {},
                                                        'void': {}}}}},
        'farm': {'xp_gained': 0,
                 'special_event': {'count': 0, 'won': [0, 0]},
                 'special_seeds': {'count': 0,
                                   'carrot': {'count': 0, 'amounts': {}},
                                   'potato': {'count': 0, 'amounts': {}},
                                   'bread': {'count': 0, 'amounts': {}}},
                 'normal_farm': {'count': 0,
                                 'bread': {'count': 0, 'resources': 0},
                                 'carrot': {'count': 0, 'resources': 0},
                                 'potato': {'count': 0, 'resources': 0}},
                 'using_seed': {'count': 0,
                                'bread': {'count': 0, 'resources': 0, 'seed_back': {}},
                                'carrot': {'count': 0, 'resources': 0, 'seed_back': {}},
                                'potato': {'count': 0, 'resources': 0, 'seed_back': {}}}}}


async def info(database, channel, author, client, interaction=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    text = f":small_blue_diamond: Pong! Bot's latency: {round(client.latency * 1000)} ms\n"
    delta_uptime = datetime.datetime.utcnow() - client.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")

    text += f":small_blue_diamond: The bot has been online for **{days}d, {hours}h, {minutes}m and {seconds}s**\n"
    text += f":small_blue_diamond:The bot is currently in **{str(len(client.guilds))}** servers!\n"
    text += f":small_blue_diamond: Tracked data for: **{len(database)} users**\n"
    text += f":small_blue_diamond: Actively tracking data for: **{len(agrees_to_track_db)} users**"

    title = str(author).split("#")[0] + "'s info"
    embed = discord.Embed(color=random.randint(0, 0xFFFFFF))
    embed.add_field(name="Here is the bot's info:", value=text)
    embed.set_author(name=title, icon_url=author.avatar)
    embed.set_footer(text=f"Today at {current_time} | Poggers")
    await send_response(embed=embed)


def get_user(arg: str):
    if arg.isnumeric():
        return int(arg)
    if arg.startswith('<@') and arg.endswith('>'):
        if arg[2:-1].isnumeric():
            return int(arg[2:-1])

    return False


async def add_manual_loot(message, database, mob_database, client):
    last_arg = message.content.lower().split(' ')[-1]
    if get_user(last_arg):
        try:
            user = await client.fetch_user(get_user(last_arg))
        except discord.HTTPException:
            user = message.author
    else:
        user = message.author

    if user.id not in database or user.id not in mob_database:
        await message.channel.send(
            f"<@{message.author.id}> I don't have any data stored for that user or you used an invalid user ID")
        return

    command = message.content.lower().replace('pog tr add ', '').split(' ')

    data = database[user.id]
    if command[0] == 'hunt':
        data['hunt'][command[1]]['lootboxes'][command[2]]['seen'] += 1
        data['hunt'][command[1]]['lootboxes']['total'] += 1
        data['hunt'][command[1]]['lootboxes'][command[2]]['found'] += int(command[3])
        data['hunt'][command[1]]['count'] += 1

    await message.channel.send(f"Loot added **SUCESSFULLY** to **{user.name}**.")
    database[user.id] = data


async def reset_global_data(message, mob_db):
    key = message.content.replace('pog tr del global ', '')
    if key not in mob_db:
        await message.channel.send(
            f"<@{message.author.id}> Correct format for reset: HORSE TIER + MOB NAME + COMMAND + MODE.\n"
            f"Example: `T10well idk... mutantest mutant dragonadventurehardmode`")
        return

    del mob_db[key]
    await message.channel.send(f"<@{message.author.id}> Successfully deleted `{key}`")


async def reset__data(message, cmd_db):
    key = message.content.replace('pog tr del ', '')
    horse, command, mode = key.split(' ')

    for i in range(0, 150):
        if f"{GLOBAL_USER}{i}" in cmd_db:
            del cmd_db[f"{GLOBAL_USER}{i}"]

    empty = {}
    if command == 'hunt':
        empty = get_empty_hunt()
    else:
        empty = get_empty_adv()

    global_data = cmd_db[GLOBAL_USER]

    try:
        global_data[horse][command][mode] = empty
    except KeyError:
        await message.channel.send(f"<@{message.author.id}> BAD: `{horse}, {command}, {mode}`."
                                   f"HORSE + COMMAND + MODE!")
        return

    cmd_db[GLOBAL_USER] = global_data
    await message.channel.send(f"<@{message.author.id}> Successfully deleted `{horse}, {command}, {mode}`")


async def ask_for_permission(channel, author, agree_db, interaction=None):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    embed = discord.Embed(description="""Before running any EPIC RPG tracking command, do you want and agree that from now on \
    Utility Necrobot will watch ALL of your epic rpg commands and log information about them (how likely is for something to happen, \
    the amount of times you used the command, etc) and to keep a list with your time travel, HP, area, marry partner, horse, etc?

    Do you also agree that anyone will be able to check your tracked information and for it to count towards global statistics?

    :warning: This will only look at your EPIC RPG commands and will not store any messages, you can always disable this using `pog tr disable`!""",
                          colour=random.randint(0, 0xffffff))

    embed.set_author(name=f"{author.name}'s agreement", icon_url=author.avatar)

    view = discord.ui.View()
    view.add_item(agree_btn := discord.ui.Button(label="I agree", style=discord.ButtonStyle.green))
    view.add_item(disagree_btn := discord.ui.Button(label="I disagree", style=discord.ButtonStyle.red))

    async def agree(inter: discord.Interaction):
        if inter.user.id != author.id:
            return

        await inter.response.send_message(
            "You agreed, thank you! You can now use the command tracking functions of the bot!")
        agree_db[author.id] = 1

        for child in view.children:
            child.disabled = True

        view.stop()
        await inter.message.edit(view=view)

    async def disagree(inter: discord.Interaction):
        if inter.user.id != author.id:
            return

        await inter.response.send_message("You denied! If you change your mind feel free to try and register again")

        for child in view.children:
            child.disabled = True

        view.stop()
        await inter.message.edit(view=view)

    agree_btn.callback = agree
    disagree_btn.callback = disagree

    await send_response(f"<@{author.id}> Do you agree with these terms?", embed=embed, view=view)
