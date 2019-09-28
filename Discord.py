# https://discordpy.readthedocs.io/en/latest/api.html?highlight=change%20nickname#discord.Permissions.change_nickname
# https://discordpy.readthedocs.io/en/latest/api.html#discord.Permissions.manage_roles
# https://discordpy.readthedocs.io/en/latest/api.html#discord.Guild.get_member

# TODO:
#   Message Everyone that varuser checkedin in new channel
#   Combine Barcode to discord

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

member_check = ''
seat_number = 0
screen_name = ''


def set_globvar():
    global member_check  # Needed to modify global copy of globvar
    global seat_number
    global screen_name


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

    if message.content.startswith('$hello'):
        await message.channel.send('Hello! ' + str(message.author))


    if message.content.startswith('0'):
        server = message.guild.members
        guild = message.guild
        Bar_code = int(message.content)
        New_Name = (pull_csv(Bar_code))
        screen_name = New_Name[2]
        seat_number = New_Name[3]
        for member in server:
            if member.name == screen_name:
                print(str(seat_number) + ':' + member.name)
                print(member.roles)
                print(member.guild_permissions)
                print(member.nick)
                await member.edit(nick=(seat_number + ":" + str(screen_name)))
                role = discord.utils.get(member.guild.roles, name="moved")
                await member.add_roles(role)
                await message.delete()
                await message.channel.send('@here  Welcome to the LAN ' + str(screen_name) + "!")




client.run(TOKEN)

