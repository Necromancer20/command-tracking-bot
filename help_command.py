import asyncio
import datetime

import discord.ui

new_commands = f""""""


def get_formatted_cool_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time


def get_help_empty_embed(author):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    embed = discord.Embed(color=0xFF0000)
    embed.set_author(name="Here is a list of my commands:", icon_url=author.avatar)
    embed.set_footer(text=f"Today at {current_time} | Poggers <3")
    return embed


async def pog_help_prefix(bot,
                          channel,
                          author: discord.User,
                          command: str,
                          interaction: discord.Interaction = None, topic=""):
    if interaction:
        send_response = interaction.edit_original_response
    else:
        send_response = channel.send

    embed_start = get_help_empty_embed(author)
    view = discord.ui.View()

    tracking = """**Please pick an EPIC RPG command from below to display help for how to check it's stats!**"""
    view.clear_items()
    embed_start.description = tracking
    embed_start.set_image(
        url='https://cdn.discordapp.com/attachments/951775683108036608/1013700274528997386/Untitled.png')
    options = [discord.SelectOption(label='Helpful Commands', emoji='⚙',
                                    description='Resetting your data, check all tracked mobs, etc'),
               discord.SelectOption(label='Miscellaneous', emoji='🍄',
                                    description='Marry another user, diable the tracking, etc'),
               discord.SelectOption(label='Global & Other Users', emoji='🌍',
                                    description='How to check global data and other user\'s data'),
               discord.SelectOption(label='Working Commands', emoji='🌲',
                                    description="Commands like chop, fish, bigboat, chainsaw..."),
               discord.SelectOption(label="Hunt", emoji='<:unicorn:979027505702920192>',
                                    description="How to check the hunt stats"),
               discord.SelectOption(label='Adventure', emoji='<:Lindorei_helped_me:979034794501476352>',
                                    description="How to check the adventure stats"),
               discord.SelectOption(label='Lootboxes', emoji='<:godly:977508095678877706>',
                                    description='How to check lootbox loot data'),
               discord.SelectOption(label='Pet adventure rewards', emoji='<:cat:951188235814572052>',
                                    description='The stuff pets found in adventure'),
               discord.SelectOption(label='Training', emoji='🤼',
                                    description='The xp, pets, etc you got from training'),
               discord.SelectOption(label='T10 Extra', emoji='<:t10_horse:985611263432335370>',
                                    description='The times you got more than 1 item in hunt because of T10')]
    select = discord.ui.Select(custom_id='track_dropdown', placeholder="Please select an EPIC RPG command",
                               options=options)
    view.add_item(select)
    help_embed_msg = await send_response(embed=embed_start, view=view)

    def check(inter):
        return inter.message and inter.message.id == help_embed_msg.id

    while True:
        try:
            interaction = await bot.wait_for('interaction', check=check, timeout=120)
        except asyncio.TimeoutError:
            for button in view.children:
                button.disabled = True
            await help_embed_msg.edit(view=view)
            return

        if interaction.user.id != author.id:
            await interaction.response.send_message(
                content="This is not your help! Use `pog help` to do this yourself!", ephemeral=True)
            continue

        embed = get_help_empty_embed(author)

        if interaction.data['custom_id'] == 'track_dropdown':
            if interaction.data['values'][0] == 'Helpful Commands':
                embed.description = """> **⚙ HELPFUL COMMANDS**
🔹 `pog dex [area]` - shows all mobs in this area
🔹 `pog tr mob dump [command] [mode]` - shows you all the mobs stored for this type of command. Use these mob names when searching for a mob

> **<:green_arrow_right:968808534181576714> RESET AND SAVE DATA:**
🔹 `pog tr reset [command]` - resets the data and gives you a backup of it. Use `all` to reset everything and `work` to reset \
all working commands. For the rest use the command name, like `hunt`, `farm`, `chainsaw`, etc
🔹 `pog tr load` + attachment - loads the data from the attachment, use only `.pog` files. Your current data will be overwritten!
"""
            elif interaction.data['values'][0] == 'Miscellaneous':
                embed.description = """> **🍄 MISC:**
🔹 `pog tr marry [@user]` - set this person as your EPIC RPG partner
🔹 `pog tr divorce` - remove your partner
🔹 `pog tr disable` - stop the bot from tracking your commands
🔹 `pog tr enable` - reverses the previous command"""
            elif interaction.data['values'][0] == 'Working Commands':
                embed.description = """> **🌲 WORKING COMMANDS**
🔹 `pog tr [working_command_name]` - shows the stats for any working command provided
Examples: `pog tr chainsaw`, `pog tr ladder`, `pog tr axe`

🔹 `pog tr void aura [area]` - shows stats related to the void aura"""
            elif interaction.data['values'][0] == 'Hunt':
                embed.description = """> **Possible modes for hunt:**
🔸 `h` - hardmode ┃ `n` - normal hunt ┃ `p` - partner hunt

> **<:unicorn:979027505702920192> HUNTS**
🔹 `pog tr hunt [mode]` - shows the hunt data
Examples: `pog tr hunt h`, `pog tr hunt p`

🔹 `pog tr mob [full_mob_name] hunt [mode]` - shows all data gathered for a specific mob in a specific command in hunt
Examples: `pog tr wolf hunt h`, `pog tr scaled kid dragon hunt h`"""
            elif interaction.data['values'][0] == 'Adventure':
                embed.description = """> **Possible modes for adventure:**
🔸 `h` - hardmode ┃ `n` - normal hunt 

> **<:Lindorei_helped_me:979034794501476352> ADVENTURES**
🔹 `pog tr adv [mode]` - shows the adventure data
Examples: `pog tr adv h`, `pog tr adv n`

🔹 `pog tr mob [full_mob_name] adv [mode]` - shows all data gathered for a specific mob in a specific command in adv
Example: `pog tr bunch of bees adv h`"""

            elif interaction.data['values'][0] == 'Lootboxes':
                embed.description = """> **<:godly:977508095678877706> LOOTBOXES**
🔹 `pog tr [lootbox type]` - example: `pog tr uncommon`
🔹 add `one` at the end of the command to see any useful stats - example: `pog tr godly one`
"""
            elif interaction.data['values'][0] == 'Pet adventure rewards':
                embed.description = """> <:cat:951188235814572052> **PET ADVENTURE REWARDS**:
🔹 `pog tr petadv [pet_tier]` - shows the data for the pets adventure rewards, if no tier is specified, shows for all tiers at once
"""
            elif interaction.data['values'][0] == 'Training':
                embed.description = """> 🤼 **TRAINING**
🔹 `pog tr tr [command_amount_used_to_catch_pet]` - shows the stats for training, if no command amount is specified, shows the stats \
for all trainings. Use `globalt10`, `globalt9`... for seeing the data for specific horse tiers
"""
            elif interaction.data['values'][0] == 'T10 Extra':
                embed.description = """> **<:t10_horse:985611263432335370> T10 HORSE EXTRA LOOT**
🔹 `pog tr t10 hunt [mode]` - shows extra drops from a tier 10 horse in hunt
🔹 `pog tr t10 adv [mode]` - shows extra drops from a tier 10 horse in adventure

Example: `pog tr t10 hunt h`. Modes can be h, n, p.
"""
            elif interaction.data['values'][0] == 'Global & Other Users':
                embed.description = """> 🌎 **Global Data and Checking other users:**

To check the global data in the bot add `global` at the end of any command! Note that some commands need more info, they will specify it when used.
To check the data for another user simply @mention or put his USER_ID at the end of the command.

Examples: `pog tr hunt h global`, `pog tr mob wolf hunt h @necromancer20`"""

        await interaction.response.edit_message(embed=embed, view=view)
