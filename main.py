import discord
from discord.ext import commands
import requests
import os
import webserver
Discord_Token = os.getenv('Discord_Token')

# Initialize the bot with the specified command prefix and intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.command()
async def test(ctx,*args):
    response = ' '.join(args)
    await ctx.send(f'Test command received: {response}')

@bot.command()
async def poke(ctx, arg):
    try:
        pokemon = arg.split(" ", 1)[0]
        result = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}')
        if result.text == 'Not Found':
            await ctx.send(f'Pokemon "{pokemon}" not found.')
        else:
            iamge_url = result.json()['sprites']['front_default']
            print(iamge_url)
            await ctx.send(f'Poke command received for: {pokemon})
       
    except Exception as e:
        print(f'Error in poke command: {e}')

@poke.error
async def poke_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please provide a Pokemon name.')
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send('An error occurred while processing your request. Please try again later.')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
@bot.command()
async def clean(ctx):
    await ctx.channel.purge(limit=1000)
    await ctx.send('Mensanges deleted successfully.', delete_after=3)

webserver.keep_alive()
bot.run(Discord_Token)

