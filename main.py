import asyncio
import datetime
import os
from enum import Enum

import discord
from sqlitedict import SqliteDict

import command_tracking
from help_command import pog_help_prefix
from settings import BOT_TOKEN

command_tracking_db = SqliteDict("./databases/command_tracking.sqlite")
mob_tracking_db = SqliteDict("./databases/mob_tracking_db.sqlite")
agrees_to_track_db = SqliteDict("./databases/agreements.sqlite", autocommit=True)

NECROMANCER_ID = 557841939375063068
EPIC_RPG_ID = 555955826880413696

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = discord.Client(intents=intents)

command_tree = discord.app_commands.CommandTree(bot)

bot.launch_time = datetime.datetime.utcnow()


@bot.event
async def on_ready():
    # option = input("Do you want to sync: ")
    # if option.upper() == 'Y':
    #     await command_tree.sync(guild=discord.Object(id=944233364787965982))

    global command_tracking_db, mob_tracking_db
    pet_adv_db = command_tracking.get_pet_adventure_rewards_db()

    print(f'Logged in as {bot.user}')

    while True:
        command_tracking_db.commit()
        mob_tracking_db.commit()
        pet_adv_db.commit()
        await asyncio.sleep(300)


@bot.event
async def on_message(message: discord.Message):
    # =================================================================================================================
    # Filtering
    if message.author.bot and message.author.id != EPIC_RPG_ID:
        return

    command = " ".join(message.content.lower().split())

    # if command == "pog sync" and message.author.id == NECROMANCER_ID:
    #     await command_tree.sync()
    #     await message.channel.send(f"{message.author.mention} Sync complete!")
    #     return

    # ===================================================================================================
    # Add to db

    if message.author.id not in agrees_to_track_db:
        if command.startswith('pog tr '):
            await command_tracking.ask_for_permission(message.channel, message.author, agrees_to_track_db)
            if message.author.id not in agrees_to_track_db:
                return

    if message.author.id not in command_tracking_db:
        command_tracking.add_player_to_database(message.author.id, command_tracking_db)

    if message.author.id not in mob_tracking_db:
        command_tracking.per_mob_add_player_to_database(message.author.id, mob_tracking_db)

    # data = command_tracking_db[950107553470226443]
    # data['T10']['adventure'] = command_tracking.get_empty_adv()
    # data['T9']['adventure'] = command_tracking.get_empty_adv()
    # data['T8']['adventure'] = command_tracking.get_empty_adv()
    # data['T7']['adventure'] = command_tracking.get_empty_adv()
    # data['T6']['adventure'] = command_tracking.get_empty_adv()
    # del data['adventure']
    #
    # command_tracking_db[950107553470226443] = data
    # command_tracking_db.commit()
    # exit()

    # if message.channel.id != 951775683108036608:
    #     return

    # for user in command_tracking_db:
    #     data = command_tracking_db[user]
    #     if 'training' in data:
    #         del data['training']
    #         command_tracking_db[user] = data
    # command_tracking_db.commit()
    # exit()

    # channel = bot.get_channel(824505092056285186)
    # message = await channel.fetch_message(997872784782934016)
    # print(message.id)
    #
    # if message.embeds:
    #     print(command_tracking.get_pet_rewards_from_embed(message.embeds[0].to_dict()))
    #     print('---------------------------------\n')
    # exit()

    # for user in command_tracking_db:
    #     data = command_tracking_db[user]
    #     if 'training' in data:
    #         del data['training']
    #     if 'lootboxes' in data:
    #         del data['lootboxes']
    #     if 'lootboxes_one' in data:
    #         del data['lootboxes_one']
    #
    #     print(user)
    #     command_tracking_db[user] = data
    #
    # command_tracking_db.commit()
    # exit()

    # ===================================================================================================
    # TRACK IT!
    if not command.startswith(('pog ', f"{bot.user.mention} ")):
        await command_tracking.track_command(message, command_tracking_db, bot, mob_tracking_db)

    # ===================================================================================================
    # HUNT & ADV
    elif command.startswith(("pog help", f"{bot.user.mention} help")):
        await pog_help_prefix(bot, message.channel, message.author, command)

    elif command.startswith(("pog tr hunt h", f"{bot.user.mention} tr hunt h")):
        await command_tracking.show_hunt_or_adv_stats(message.channel, message.author, "hunt h", command, bot,
                                                      command_tracking_db)
    elif command.startswith(("pog tr hunt n", f"{bot.user.mention} tr hunt n")):
        await command_tracking.show_hunt_or_adv_stats(message.channel, message.author, "hunt n", command, bot,
                                                      command_tracking_db)
    elif command.startswith(("pog tr hunt p", f"{bot.user.mention} tr hunt p")):
        await command_tracking.show_hunt_or_adv_stats(message.channel, message.author, "hunt p", command, bot,
                                                      command_tracking_db)

    elif command.startswith(("pog tr adv h", f"{bot.user.mention} tr adv h")):
        await command_tracking.show_hunt_or_adv_stats(message.channel, message.author, "adv h", command, bot,
                                                      command_tracking_db)
    elif command.startswith(("pog tr adv n", f"{bot.user.mention} tr adv n")):
        await command_tracking.show_hunt_or_adv_stats(message.channel, message.author, "adv n", command, bot,
                                                      command_tracking_db)

    # ===================================================================================================
    # T10 stuff
    elif command.startswith(("pog tr t10 hunt h", f"{bot.user.mention} tr t10 hunt h")):
        await command_tracking.show_tier10_stats(message.channel, message.author, 'hunt h', command, bot,
                                                 command_tracking_db)
    elif command.startswith(("pog tr t10 hunt n", f"{bot.user.mention} tr t10 hunt n")):
        await command_tracking.show_tier10_stats(message.channel, message.author, 'hunt n', command, bot,
                                                 command_tracking_db)
    elif command.startswith(("pog tr t10 hunt p", f"{bot.user.mention} tr t10 hunt p")):
        await command_tracking.show_tier10_stats(message.channel, message.author, 'hunt p', command, bot,
                                                 command_tracking_db)

    elif command.startswith(("pog tr t10 adv h", f"{bot.user.mention} tr t10 adv h")):
        await command_tracking.show_tier10_stats(message.channel, message.author, 'adv h', command, bot,
                                                 command_tracking_db)
    elif command.startswith(("pog tr t10 adv n", f"{bot.user.mention} tr t10 adv n")):
        await command_tracking.show_tier10_stats(message.channel, message.author, 'adv n', command, bot,
                                                 command_tracking_db)

    # ===================================================================================================
    # PER MOB
    elif command.startswith(("pog tr mob dump", f"{bot.user.mention} tr mob dump")):
        await command_tracking.dump_mobs(message.channel, message.author, command, bot, mob_tracking_db)

    elif command.startswith(("pog tr mob", f"{bot.user.mention} tr mob")):
        await command_tracking.show_per_mob_data(message.channel, message.author, command, bot, mob_tracking_db)

    # ===================================================================================================
    # PET ADVENTURE REWARDS
    elif command.startswith(('pog tr petadv', f'{bot.user.mention} tr petadv')):
        await command_tracking.show_pet_reward(message.channel, message.author, command, bot)

    # ===================================================================================================
    # WORKING COMMANDS
    elif command.startswith(('pog tr chainsaw', f'{bot.user.mention} tr chainsaw')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'chainsaw', command, bot,
                                                    command_tracking_db)
    elif command.startswith(('pog tr bowsaw', f'{bot.user.mention} tr bowsaw')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'bowsaw', command, bot,
                                                    command_tracking_db)
    elif command.startswith(('pog tr axe', f'{bot.user.mention} tr axe')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'axe', command, bot,
                                                    command_tracking_db)
    elif command.startswith(('pog tr chop', f'{bot.user.mention} tr chop')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'chop', command, bot,
                                                    command_tracking_db)

    elif command.startswith(('pog tr dynamite', f'{bot.user.mention} tr dynamite')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'dynamite', command, bot,
                                                    command_tracking_db)
    elif command.startswith(('pog tr drill', f'{bot.user.mention} tr drill')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'drill', command, bot,
                                                    command_tracking_db)
    elif command.startswith(('pog tr pickaxe', f'{bot.user.mention} tr pickaxe')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'pickaxe', command, bot,
                                                    command_tracking_db)
    elif command.startswith(('pog tr mine', f'{bot.user.mention} tr mine')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'mine', command, bot,
                                                    command_tracking_db)

    elif command.startswith(('pog tr bigboat', f'{bot.user.mention} tr bigboat')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'bigboat', command, bot,
                                                    command_tracking_db)
    elif command.startswith(('pog tr boat', f'{bot.user.mention} tr boat')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'boat', command, bot,
                                                    command_tracking_db)
    elif command.startswith(('pog tr net', f'{bot.user.mention} tr net')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'net', command, bot,
                                                    command_tracking_db)
    elif command.startswith(('pog tr fish', f'{bot.user.mention} tr fish')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'fish', command, bot,
                                                    command_tracking_db)

    elif command.startswith(('pog tr greenhouse', f'{bot.user.mention} tr greenhouse')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'greenhouse', command, bot,
                                                    command_tracking_db)
    elif command.startswith(('pog tr tractor', f'{bot.user.mention} tr tractor')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'tractor', command, bot,
                                                    command_tracking_db)
    elif command.startswith(('pog tr ladder', f'{bot.user.mention} tr ladder')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'ladder', command, bot,
                                                    command_tracking_db)
    elif command.startswith(('pog tr pickup', f'{bot.user.mention} tr pickup')):
        await command_tracking.show_working_commnad(message.channel, message.author, 'pickup', command, bot,
                                                    command_tracking_db)

    elif command.startswith(('pog tr void aura', f'{bot.user.mention} tr void aura')):
        await command_tracking.show_void_aura(message.channel, message.author, command, bot, command_tracking_db)
    # ===================================================================================================
    # FARM
    elif command.startswith(('pog tr farm', f'{bot.user.mention} tr farm')):
        await command_tracking.show_farm_stats(message.channel, message.author, command, bot, command_tracking_db)

    # ===================================================================================================
    # TRAINING
    elif command.startswith(
            ('pog tr training', 'pog tr tr', f'{bot.user.mention} tr training', f'{bot.user.mention} tr tr')):
        await command_tracking.show_training(message.channel, message.author, command, bot, command_tracking_db)

    # ===================================================================================================
    # LOOTBOXES
    elif command.startswith(('pog tr common', f'{bot.user.mention} tr common')):
        await command_tracking.show_lootbox(message.channel, message.author, 'common', command, bot,
                                            command_tracking_db)
    elif command.startswith(('pog tr uncommon', f'{bot.user.mention} tr uncommon')):
        await command_tracking.show_lootbox(message.channel, message.author, 'uncommon', command, bot,
                                            command_tracking_db)
    elif command.startswith(('pog tr rare', f'{bot.user.mention} tr rare')):
        await command_tracking.show_lootbox(message.channel, message.author, 'rare', command, bot, command_tracking_db)
    elif command.startswith(('pog tr epic', f'{bot.user.mention} tr epic')):
        await command_tracking.show_lootbox(message.channel, message.author, 'epic', command, bot, command_tracking_db)
    elif command.startswith(('pog tr edgy', f'{bot.user.mention} tr edgy')):
        await command_tracking.show_lootbox(message.channel, message.author, 'edgy', command, bot, command_tracking_db)
    elif command.startswith(('pog tr omega', f'{bot.user.mention} tr omega')):
        await command_tracking.show_lootbox(message.channel, message.author, 'omega', command, bot, command_tracking_db)
    elif command.startswith(('pog tr godly', f'{bot.user.mention} tr godly')):
        await command_tracking.show_lootbox(message.channel, message.author, 'godly', command, bot, command_tracking_db)
    elif command.startswith(('pog tr void', f'{bot.user.mention} tr void')):
        await command_tracking.show_lootbox(message.channel, message.author, 'void', command, bot, command_tracking_db)

    # ===================================================================================================
    # RESET & LOAD
    elif command.startswith(('pog tr reset', f'{bot.user.mention} tr reset')):
        await command_tracking.rest_tracking(message.channel, message.author, command, bot, command_tracking_db)

    elif command.startswith(('pog tr load', f'{bot.user.mention} tr load')):
        await command_tracking.load_data(message.channel, message.author, message.attachments, command_tracking_db, bot)

    # elif message.author.id == NECROMANCER_ID and message_lower.startswith('pog tr del global'):
    #     await command_tracking.reset_global_data(message, mob_tracking_db)
    # elif message.author.id == NECROMANCER_ID and message_lower.startswith('pog tr del'):
    #     await command_tracking.reset__data(message, command_tracking_db)

    elif command.startswith(('pog dex', f'{bot.user.mention} dex')):
        await command_tracking.mob_dex(message.channel, message.author, command)
        return

    # ===================================================================================================
    # MARRY
    elif command.startswith(('pog tr marry', f'{bot.user.mention} tr marry')):
        await command_tracking.add_partener(message.channel, message.author, command, command_tracking_db, bot)
    elif command.startswith(('pog tr divorce', f'{bot.user.mention} tr divorce')):
        await command_tracking.divorce(message.channel, message.author, command_tracking_db)

    # ===================================================================================================
    # DISABLE
    elif command.startswith(('pog tr disable', f'{bot.user.mention} tr disable')):
        await command_tracking.disable_tracking(message.channel, message.author, command_tracking_db, 'disable',
                                                agrees_to_track_db)
    elif command.startswith(('pog tr enable', f'{bot.user.mention} tr enable')):
        await command_tracking.disable_tracking(message.channel, message.author, command_tracking_db, 'enable',
                                                agrees_to_track_db)

    # ===================================================================================================
    # OTHER
    elif command.startswith(('pog tr info', f'{bot.user.mention} tr info')):
        await command_tracking.info(command_tracking_db, message.channel, message.author, bot)

    elif command.startswith(('pog tr profile', f'{bot.user.mention} tr profile')):
        await command_tracking.show_profile(message.channel, message.author, command, command_tracking_db, bot)

    elif command.startswith(('pog tr add', f'{bot.user.mention} tr add')) and message.author.id == NECROMANCER_ID:
        await command_tracking.add_manual_loot(message, command_tracking_db, mob_tracking_db, bot)
    elif command.startswith(('pog tr add', f'{bot.user.mention} tr add')):
        pet_adv_db = command_tracking.get_pet_adventure_rewards_db()
        command_tracking_db.commit()
        mob_tracking_db.commit()
        pet_adv_db.commit()
        await message.channel.send("All data has been **SAVED** to disk.")

    if command.startswith(('pog tr del lootboxes all',
                           f'{bot.user.mention} tr del lootboxes all')) and message.author.id == NECROMANCER_ID:
        for user in command_tracking_db:
            data = command_tracking_db[user]
            if 'lootboxes' in data:
                del data['lootboxes']
                command_tracking_db[user] = data

        command_tracking_db.commit()
        await message.channel.send("DONE!")


class HuntModes(Enum):
    hardmode = 'h'
    normal = 'n'
    partner = 'p'


@command_tree.command(name='hunt-tracking', description="View the data gathered by the bot for the hunt command",
                      guild=discord.Object(id=944233364787965982))
@discord.app_commands.choices(global_data=[
    discord.app_commands.Choice(name='T6 horse global data', value='global t6'),
    discord.app_commands.Choice(name='T7 horse global data', value='global t7'),
    discord.app_commands.Choice(name='T8 horse global data', value='global t8'),
    discord.app_commands.Choice(name='T9 horse global data', value='global t9'),
    discord.app_commands.Choice(name='T10 horse global data', value='global t10'),
])
async def hunt_tr(interaction: discord.Interaction, mode: HuntModes, global_data: discord.app_commands.Choice[str] = "",
                  user: discord.User = None):
    await interaction.response.defer()

    global_data = global_data.value if global_data else ""

    await command_tracking.show_hunt_or_adv_stats(interaction.channel, interaction.user, f"hunt {mode.value}",
                                                  f"pog {global_data}", bot, command_tracking_db, user=user,
                                                  interaction=interaction)
    return


@command_tree.command(name='adventure-tracking',
                      description="View the data gathered by the bot for the adventure command",
                      guild=discord.Object(id=944233364787965982))
@discord.app_commands.choices(global_data=[
    discord.app_commands.Choice(name='T6 horse global data', value='global t6'),
    discord.app_commands.Choice(name='T7 horse global data', value='global t7'),
    discord.app_commands.Choice(name='T8 horse global data', value='global t8'),
    discord.app_commands.Choice(name='T9 horse global data', value='global t9'),
    discord.app_commands.Choice(name='T10 horse global data', value='global t10'),
])
async def adv_tr(interaction: discord.Interaction, mode: HuntModes, global_data: discord.app_commands.Choice[str] = "",
                 user: discord.User = None):
    await interaction.response.defer()

    global_data = global_data.value if global_data else ""

    await command_tracking.show_hunt_or_adv_stats(interaction.channel, interaction.user, f"adv {mode.value}",
                                                  f"pog {global_data}", bot, command_tracking_db, user=user,
                                                  interaction=interaction)
    return


@command_tree.command(name='t10-drop-tracking',
                      description="View the data gathered by the bot for the extra items you got by having a t10 horse",
                      guild=discord.Object(id=944233364787965982))
@discord.app_commands.choices(mode=[
    discord.app_commands.Choice(name='hunt hardmode', value='hunt h'),
    discord.app_commands.Choice(name='hunt normal', value='hunt n'),
    discord.app_commands.Choice(name='hunt partner', value='hunt p'),
    discord.app_commands.Choice(name='adv hardmode', value='adv h'),
    discord.app_commands.Choice(name='adv normal', value='adv n'),
])
async def t10_tr(interaction: discord.Interaction, mode: discord.app_commands.Choice[str], global_data: bool = False,
                 user: discord.User = None):
    await interaction.response.defer()

    global_data = "global" if global_data else ""

    await command_tracking.show_tier10_stats(interaction.channel, interaction.user, mode.value, f"pog {global_data}",
                                             bot, command_tracking_db, interaction=interaction, user=user)
    return


@command_tree.command(name='dump-mobs', description="Shows a list of all the mobs you have data tracked for",
                      guild=discord.Object(id=944233364787965982))
@discord.app_commands.choices(mode=[
    discord.app_commands.Choice(name='hunt hardmode', value='hunt h'),
    discord.app_commands.Choice(name='hunt normal', value='hunt n'),
    discord.app_commands.Choice(name='hunt partner', value='hunt p'),
    discord.app_commands.Choice(name='adv hardmode', value='adv h'),
    discord.app_commands.Choice(name='adv normal', value='adv n'),
])
async def mob_dumps(interaction: discord.Interaction, mode: discord.app_commands.Choice[str],
                    user: discord.User = None):
    await interaction.response.defer()

    await command_tracking.dump_mobs(interaction.channel, interaction.user, f"pog tr mob dump {mode.value}", bot,
                                     mob_tracking_db,
                                     interaction=interaction, user=user)
    return


@command_tree.command(name='pet-adventure-tracking',
                      description="Shows a list of all the rewards given by claiming pet adventures",
                      guild=discord.Object(id=944233364787965982))
async def pet_adv_tr(interaction: discord.Interaction, tier: int = 0, global_data: bool = False,
                     user: discord.User = None):
    await interaction.response.defer()

    global_data = "global" if global_data else ""

    await command_tracking.show_pet_reward(interaction.channel, interaction.user,
                                           f"pog tr petadv {'' if not tier else tier} {global_data}", bot,
                                           interaction=interaction, user=user)
    return


@command_tree.command(name='working-command-tracking', description="Shows all working command tracked data",
                      guild=discord.Object(id=944233364787965982))
@discord.app_commands.choices(command=[
    discord.app_commands.Choice(name='chainsaw', value='chainsaw'),
    discord.app_commands.Choice(name='bowsaw', value='bowsaw'),
    discord.app_commands.Choice(name='axe', value='axe'),
    discord.app_commands.Choice(name='chop', value='chop'),
    discord.app_commands.Choice(name='bigboat', value='bigboat'),
    discord.app_commands.Choice(name='boat', value='boat'),
    discord.app_commands.Choice(name='net', value='net'),
    discord.app_commands.Choice(name='fish', value='fish'),
    discord.app_commands.Choice(name='greenhouse', value='greenhouse'),
    discord.app_commands.Choice(name='tractor', value='tractor'),
    discord.app_commands.Choice(name='ladder', value='ladder'),
    discord.app_commands.Choice(name='pickup', value='pickup'),
    discord.app_commands.Choice(name='dynamite', value='dynamite'),
    discord.app_commands.Choice(name='drill', value='drill'),
    discord.app_commands.Choice(name='pickaxe', value='pickaxe'),
    discord.app_commands.Choice(name='mine', value='mine'),
])
async def working_tr(interaction: discord.Interaction, command: discord.app_commands.Choice[str],
                     global_data: bool = False, worker_level: int = 0,
                     user: discord.User = None):
    await interaction.response.defer()

    global_data = "global" if global_data else ""
    worker_level = worker_level if worker_level else ""

    await command_tracking.show_working_commnad(interaction.channel, interaction.user, 'chainsaw',
                                                f"pog tr {command.value} {global_data} {worker_level}", bot,
                                                command_tracking_db, interaction=interaction, user=user)

    return


@command_tree.command(name='mob-tracking', description="View the data gathered by the bot for all mobs separately",
                      guild=discord.Object(id=944233364787965982))
@discord.app_commands.choices(mode=[
    discord.app_commands.Choice(name='hunt hardmode', value='hunt h'),
    discord.app_commands.Choice(name='hunt normal', value='hunt n'),
    discord.app_commands.Choice(name='hunt partner', value='hunt p'),
    discord.app_commands.Choice(name='adv hardmode', value='adv h'),
    discord.app_commands.Choice(name='adv normal', value='adv n'),
],
    global_data=[
        discord.app_commands.Choice(name='T6 horse global data', value='global t6'),
        discord.app_commands.Choice(name='T7 horse global data', value='global t7'),
        discord.app_commands.Choice(name='T8 horse global data', value='global t8'),
        discord.app_commands.Choice(name='T9 horse global data', value='global t9'),
        discord.app_commands.Choice(name='T10 horse global data', value='global t10'),
    ]
)
async def mob_tr(interaction: discord.Interaction,
                 mode: discord.app_commands.Choice[str],
                 mob: str,
                 global_data: discord.app_commands.Choice[str] = "",
                 user: discord.User = None):
    await interaction.response.defer()

    global_data = global_data.value if global_data else ""

    await command_tracking.show_per_mob_data(interaction.channel, interaction.user,
                                             f"pog tr mob {mob} {mode.value} {global_data}",
                                             bot, mob_tracking_db, interaction=interaction, user=user)
    return


@command_tree.command(name='void-aura-tracking',
                      description="View the data gathered by the bot for the void aura drops",
                      guild=discord.Object(id=944233364787965982))
async def void_aura(interaction: discord.Interaction, area: int, global_data: bool = False, user: discord.User = None):
    await interaction.response.defer()

    global_data = "global" if global_data else ""

    await command_tracking.show_void_aura(interaction.channel, interaction.user,
                                          f"pog tr void aura {area} {global_data}", bot, command_tracking_db,
                                          interaction=interaction, user=user)
    return


@command_tree.command(name='farm-tracking', description="View the data gathered by the bot for the farm command",
                      guild=discord.Object(id=944233364787965982))
async def farm_tr(interaction: discord.Interaction, global_data: bool = False, user: discord.User = None):
    await interaction.response.defer()

    global_data = "global" if global_data else ""

    await command_tracking.show_farm_stats(interaction.channel, interaction.user, f"pog tr farm {global_data}", bot,
                                           command_tracking_db, interaction=interaction, user=user)
    return


@command_tree.command(name='training-tracking',
                      description="View the data gathered by the bot for the training command",
                      guild=discord.Object(id=944233364787965982))
@discord.app_commands.choices(global_data=[
    discord.app_commands.Choice(name='T6 horse global data', value='globalt6'),
    discord.app_commands.Choice(name='T7 horse global data', value='globalt7'),
    discord.app_commands.Choice(name='T8 horse global data', value='globalt8'),
    discord.app_commands.Choice(name='T9 horse global data', value='globalt9'),
    discord.app_commands.Choice(name='T10 horse global data', value='globalt10')])
async def tr_tr(interaction: discord.Interaction, commands_used_to_catch_pet: int = 0,
                global_data: discord.app_commands.Choice[str] = None, user: discord.User = None):
    await interaction.response.defer()

    global_data = global_data.value if global_data else ""
    commands_used_to_catch_pet = commands_used_to_catch_pet if commands_used_to_catch_pet else ""

    await command_tracking.show_training(interaction.channel, interaction.user,
                                         f"pog tr tr {commands_used_to_catch_pet} {global_data}", bot,
                                         command_tracking_db, interaction=interaction, user=user)
    return


@command_tree.command(name='lootbox-tracking',
                      description="View the data gathered by the bot for the lootboxes you opened",
                      guild=discord.Object(id=944233364787965982))
@discord.app_commands.choices(lootbox=[
    discord.app_commands.Choice(name='common', value='common'),
    discord.app_commands.Choice(name='uncommon', value='uncommon'),
    discord.app_commands.Choice(name='rare', value='rare'),
    discord.app_commands.Choice(name='epic', value='epic'),
    discord.app_commands.Choice(name='edgy', value='edgy'),
    discord.app_commands.Choice(name='omega', value='omega'),
    discord.app_commands.Choice(name='godly', value='godly'),
    discord.app_commands.Choice(name='void', value='void')])
async def lb_tr(interaction: discord.Interaction, lootbox: discord.app_commands.Choice[str],
                show_only_lbs_opened_one_by_one: bool = False, global_data: bool = False, user: discord.User = None):
    await interaction.response.defer()

    global_data = "global" if global_data else ""
    show_only_lbs_opened_one_by_one = "one" if show_only_lbs_opened_one_by_one else ""

    await command_tracking.show_lootbox(interaction.channel, interaction.user, lootbox.value,
                                        f"pog tr lootbox {lootbox.value} {global_data} {show_only_lbs_opened_one_by_one}",
                                        bot, command_tracking_db, interaction=interaction, user=user)
    return


@command_tree.command(name='reset-tracking-data', description="Reset the data for a tracked command",
                      guild=discord.Object(id=944233364787965982))
async def reset_tr(interaction: discord.Interaction, command: str):
    await interaction.response.defer()

    await command_tracking.rest_tracking(interaction.channel, interaction.user, f"pog tr reset {command}", bot,
                                         command_tracking_db, interaction=interaction)
    return


@command_tree.command(name='load-tracking-data', description="Load the data for a tracked command using a pog file",
                      guild=discord.Object(id=944233364787965982))
async def load_tr(interaction: discord.Interaction, message_id: str):
    await interaction.response.defer()
    await command_tracking.load_data(interaction.channel, interaction.user, [], command_tracking_db, bot,
                                     interaction=interaction, filename=message_id)
    return


@command_tree.command(name='rpg-mob-dex', description="View the mobs from any rpg area!",
                      guild=discord.Object(id=944233364787965982))
async def dex_tr(interaction: discord.Interaction, area: int):
    await interaction.response.defer()
    await command_tracking.mob_dex(interaction.channel, interaction.user, '', interaction=interaction, area=area)
    return


@command_tree.command(name='marry-for-tracking', description="Set your partner for tracking!",
                      guild=discord.Object(id=944233364787965982))
async def part_tr(interaction: discord.Interaction, user: discord.User):
    await interaction.response.defer()
    await command_tracking.add_partener(interaction.channel, interaction.user, "", command_tracking_db, bot,
                                        interaction=interaction, user=user)
    return


@command_tree.command(name='divorce-for-tracking', description="Unset your partner for tracking!",
                      guild=discord.Object(id=944233364787965982))
async def div_tra(interaction: discord.Interaction):
    await interaction.response.defer()
    await command_tracking.divorce(interaction.channel, interaction.user, command_tracking_db, interaction=interaction)
    return


@command_tree.command(name='disable-or-enable-tracking', description="Stop the bot from tracking your commands!",
                      guild=discord.Object(id=944233364787965982))
@discord.app_commands.choices(what_to_do=[
    discord.app_commands.Choice(name='enable', value='enable'),
    discord.app_commands.Choice(name='disable', value='disable'), ])
async def enab_tr(interaction: discord.Interaction, what_to_do: discord.app_commands.Choice[str]):
    await interaction.response.defer()
    await command_tracking.disable_tracking(interaction.channel, interaction.user, command_tracking_db,
                                            what_to_do.value,
                                            agrees_to_track_db, interaction=interaction)

    return


@command_tree.command(name='info-tr', description="See info about the bot's uptime!",
                      guild=discord.Object(id=944233364787965982))
async def info_tr(interaction: discord.Interaction):
    await interaction.response.defer()
    await command_tracking.info(command_tracking_db, interaction.channel, interaction.user, bot,
                                interaction=interaction)


@command_tree.command(name='profile-tracking', description="See general data tracked for you",
                      guild=discord.Object(id=944233364787965982))
async def part_tr(interaction: discord.Interaction, user: discord.User = None):
    await interaction.response.defer()
    await command_tracking.show_profile(interaction.channel, interaction.user, 'pog tr profile', command_tracking_db,
                                        bot,
                                        interaction=interaction, user=user)


# ======================================================================================================================
if __name__ == '__main__':
    if not os.path.exists("./databases"):
        os.mkdir("./databases")

    bot.run(BOT_TOKEN)
