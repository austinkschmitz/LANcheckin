# https://discordpy.readthedocs.io/en/latest/api.html?highlight=change%20nickname#discord.Permissions.change_nickname
# https://discordpy.readthedocs.io/en/latest/api.html#discord.Permissions.manage_roles
# https://discordpy.readthedocs.io/en/latest/api.html#discord.Guild.get_member

import csv
import discord
from discord.ext import commands

TOKEN = 'str'


def pull_csv(number_query):
    with open('datatest.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        CardNumbers = []
        ScreenNames = []
        RealNames = []
        for row in readCSV:
            CardNumber = row[0]
            RealName = row[1]
            ScreenName = row[2]

            if number_query == int(CardNumber):
                this_tuple = (RealName, ScreenName, CardNumber)
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

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello! ' + str(message.author))

    if message.content.startswith('!!'):
        x = message.guild.members
        for member in x:
            if member.name == screen_name:
                print(str(seat_number) + ':' + member.name)
                print(member.roles)
                print(member.guild_permissions)
                print(member.nick)
                await member.edit(nick='boom')
                role = discord.utils.get(member.guild.roles, name="moved")
                await member.add_roles(role)


client.run(TOKEN)
