# ImperturbableGainboroAgent

from dotenv import load_dotenv
import datetime
import os
import random
import typing

import discord
from discord import app_commands

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD = os.getenv('GUILD_ID')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(
  activity = discord.Game(name='Pokémon Red', start=datetime.datetime.now()),
  intents=intents
)
tree = app_commands.CommandTree(client)

def now() -> str:
  #returns current timestamp
  time = datetime.datetime.now()
  date = [time.month, time.day, time.year, (time.hour-7)%24, time.minute, time.second]
  for i in range(len(date)):
    date[i] = str(date[i])
    if len(date[i])==1: date[i] = '0' + date[i]
  return f'[{date[0]}-{date[1]}-{date[2]} {date[3]}:{date[4]}:{date[5]}]'
def error(message):
  #prints an error message
  print('\n' + f'{now()} [ERROR] {message}')

@client.event
async def on_ready():
  for guild in client.guilds:
    tree.copy_global_to(guild=guild)
    await tree.sync(guild=guild)
  guilds = '\n - '.join([f'{guild.name} (id: {guild.id})' for guild in client.guilds])
  print(f'{client.user} is active in the following guilds:')
  print(f' - {guilds}\n')
  me = client.get_user(587040390603866122)
  await me.send("Koduck.")
  print('Eric sent a DM to doduodrio (id: 587040390603866122) upon activating!')

# @tree.command(description='Echo user input')
# @app_commands.describe(input='Say something')
# async def echo(i: discord.Interaction, input: str):
#   await i.response.send_message(input)

@tree.command(description='Ping Eric')
async def ping(i: discord.Interaction):
  await i.response.send_message(f'Pong! Latency is {client.latency*100} ms.')
  print('\n' + f'{now()} Eric was pinged by {i.user.name}.')

@tree.command(description='Say hello to Eric')
async def hello(i: discord.Interaction):
  await i.response.send_message('👋 Koduck.')
  print('\n' + f'{now()} Eric said hello to {i.user.name}.')

@tree.command(name='8ball', description='Ask Eric a question')
@app_commands.describe(q='Ask a yes/no question')
@app_commands.rename(q='question')
async def eightball(i: discord.Interaction, q: str):
  replies = [
    'It is certain',
    'It is decidedly so',
    'Without a doubt',
    'Yes definitely',
    'You may rely on it',
    'Reply hazy, try again',
    'Ask again later',
    'Better not tell you now',
    'Cannot predict now',
    'Concentrate and ask again',
    'Don\'t count on it',
    'My reply is no',
    'My sources say no',
    'Outlook not so good',
    'Very doubtful'
  ]
  r = random.choice(replies)
  await i.response.send_message(f'Question: {q}\nReply: {r}')
  print('\n' + f'{now()} {i.user.name} asked "{q}" and Eric replied "{r}".')

@tree.context_menu(name='account creation date')
async def accountCreationDate_user(i: discord.Interaction, user: discord.Member):
  created = discord.utils.format_dt(user.created_at)
  await i.response.send_message(f'{user.name}\'s account was created on {created}!')
  print('\n' + f'{now()} {i.user.name} used the account creation date command (user) on {user.name} (Created on {user.created_at})')

@tree.context_menu(name='account creation date')
async def accountCreationDate_message(i: discord.Interaction, message: discord.Message):
  user = message.author
  created = discord.utils.format_dt(user.created_at)
  await i.response.send_message(f'{user.name}\'s account was created on {created}!')
  print('\n' + f'{now()} {i.user.name} used the account creation date command (message) on {user.name} (Created on {user.created_at})')

@tree.command(description='Send something in a specified channel and server')
@app_commands.describe(
  message='Send something',
  server='The name of the server to send it in',
  channel='The name of the channel to send it in'
)
async def send(i: discord.Interaction, message: str, server: str, channel: str):
  guild = discord.utils.get(client.guilds, name=server)
  if guild is None:
    error(f'[{i.user.name}] Eric could not send "{message}" in channel {channel} in guild {server}')
    await i.response.send_message(f'There was an error in delivering your message. Server "{server}" not found.', ephemeral=True)
    return
  c = discord.utils.get(guild.channels, name=channel)
  if c is None:
    error(f'[{i.user.name}] Eric could not send "{message}" in channel {channel} in guild {server}')
    await i.response.send_message(f'There was an error in delivering your message. Channel "{channel}" not found.', ephemeral=True)
    return
  await c.send(message)
  await i.response.send_message('Message delivered.', ephemeral=True)
  print('\n' + f'{now()} [{i.user.name}] Eric sent "{message}" in channel {channel} in guild {server}')

@send.autocomplete("channel")
async def sendAutocomplete_channel(i: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
  ns = i.namespace
  guild = discord.utils.get(client.guilds, name=ns.server)
  if guild is None:
    return []
  choices = []
  for category in guild.categories:
    for channel in category.channels:
      if not isinstance(channel, discord.ForumChannel) and current.lower() in channel.name:
        choices.append(app_commands.Choice(name=channel.name, value=channel.name))
  return choices[slice(25)]
  
@send.autocomplete("server")
async def sendAutocomplete_server(i: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
  mutual_guilds = i.user.mutual_guilds
  choices = []
  for guild in mutual_guilds:
    if current.lower() in guild.name.lower():
      choices.append(app_commands.Choice(name=guild.name, value=guild.name))
  return choices

@tree.command(description='Display a list of all of Eric\'s commands')
async def help(i: discord.Interaction):
  c = '''```
Slash Commands:
help:    Display a list of all of Eric\'s commands
hello:   Say hello to Eric
ping:    Ping Eric
8ball:   Ask Eric a question
send:    Send something in a specified channel and server
(type / to get a list of these commands)
```
```
Context Menu Commands:
account created on: Get when an account was created
(click on a user > Apps to run these commands)
```'''
  await i.response.send_message(c, ephemeral=True)
  print('\n' + f'{now()} Eric\'s help command was ran by {i.user.name}.')

# To-do:
# fetch channel history
# dm users (fetch dmchannel history)
# make commands useable in dms
# factor in permissions when generating channel choices in /send

client.run(TOKEN)