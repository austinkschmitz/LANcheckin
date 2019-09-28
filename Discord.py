# https://discordpy.readthedocs.io/en/latest/api.html?highlight=change%20nickname#discord.Permissions.change_nickname
# https://discordpy.readthedocs.io/en/latest/api.html#discord.Permissions.manage_roles
# https://discordpy.readthedocs.io/en/latest/api.html#discord.Guild.get_member

# TODO:
#   Create dynamic variables for packaging.


import csv
import discord
from discord.ext import commands

TOKEN = ''


def pull_csv(number_query):
    with open('datatest.csv') as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for row in read_csv:
            card_number = row[0]
            real_name = row[1]
            screen_name = row[2]
            seat_number = row[3]
            if number_query == int(card_number):
                this_tuple = (card_number, real_name, screen_name, seat_number)
                return this_tuple


client = discord.Client()
bot = commands.Bot(command_prefix='!')


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$help'):
        await message.channel.send("Declare your input channel: $in_ctx. \nDeclare your output channel: $out_ctx. \n"
                                   "Declare user's new role: $new_role. ex: $new_role|EXAMPLE \nPurge output channel: "
                                   "$purge")

    if message.content.startswith('$in_ctx'):
        globals()['Input_Channel'] = message.channel.id
        await message.channel.send("This is now your input channel")

    if message.content.startswith('$out_ctx'):
        globals()['Output_Channel'] = message.channel.id
        await message.channel.send("This is now your output channel")

    if message.content.startswith('$new_role|'):
        temp_str = message.content
        temp_str = temp_str[10:]
        globals()['New_Role'] = temp_str
        # globals()['New_Role'] = discord.utils.get(guild.roles, name="moved")
        await message.channel.send("{0} is now your user role".format(temp_str))

    if message.content.startswith('$purge'):
        channel_out = client.get_channel(globals()['Output_Channel'])
        await message.channel.send("Starting the purge of $Output_Channel")
        deleted = await channel_out.purge(limit=100)
        await message.channel.send('Deleted {} message(s)'.format(len(deleted)))

    if message.content.startswith('0'):
        channel_out = client.get_channel(globals()['Output_Channel'])

        if message.channel == channel_out:
            deleted = await message.delete()
            await channel_out.send("Is this your output channel?")

        server = message.guild.members
        Bar_code = int(message.content)
        New_Name = (pull_csv(Bar_code))
        screen_name = New_Name[2]
        seat_number = New_Name[3]
        for member in server:
            if member.name == screen_name:
                await member.edit(nick=(seat_number + ":" + str(screen_name)))  # Editing Nick name for the server
                role = discord.utils.get(member.guild.roles, name=(globals()['New_Role']))   # name="moved"
                await member.add_roles(role)
                await channel_out.send("@here  Welcome to the Party {0}! You sit at {1}.".format(str(screen_name), str(seat_number)))


client.run(TOKEN)
