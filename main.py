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
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}'
        result = requests.get(url)

        if result.status_code != 200:
            await ctx.send(f'Pokémon "{pokemon}" no encontrado.')
            return

        data = result.json()
        name = data['name'].capitalize()
        types = [t['type']['name'].capitalize() for t in data['types']]
        abilities = [a['ability']['name'].capitalize() for a in data['abilities']]
        sprite_url = data['sprites']['front_default']
        weight = data['weight'] / 10  # en kilogramos
        height = data['height'] / 10  # en metros

        # Extraer estadísticas base
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        atk = stats.get('attack', 'N/A')
        defn = stats.get('defense', 'N/A')
        speed = stats.get('speed', 'N/A')

        response = (
            f"**{name}**\n"
            f"📏 Altura: {height} m | ⚖️ Peso: {weight} kg\n"
            f"🔰 Tipo(s): {', '.join(types)}\n"
            f"✨ Habilidades: {', '.join(abilities)}\n"
            f"📊 Stats: Ataque {atk}, Defensa {defn}, Velocidad {speed}\n"
            f"🖼️ Imagen: {sprite_url}"
        )

        await ctx.send(response)

    except Exception as e:
        print(f'Error en el comando poke: {e}')
        await ctx.send('Ocurrió un error al procesar tu solicitud.')


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

