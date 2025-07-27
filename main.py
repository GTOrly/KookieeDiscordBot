import discord
from discord.ext import commands
from discord import app_commands
import requests
import os
import webserver  # Esto asume que tienes este archivo en tu proyecto

Discord_Token = os.getenv('Discord_Token')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=873266970764669009))  # Reemplaza con tu ID
    print(f'Bot conectado como {bot.user}')

# 👇 Slash command: /test
@tree.command(name="test", description="Recibe un mensaje de prueba")
@app_commands.describe(mensaje="Escribe el mensaje de prueba")
async def slash_test(interaction: discord.Interaction, mensaje: str):
    await interaction.response.send_message(f'Test command received: {mensaje}')

# 👇 Prefijo: .test
@bot.command()
async def test(ctx, *args):
    response = ' '.join(args)
    await ctx.send(f'Test command received: {response}')

# 👇 Slash command: /poke
@tree.command(name="poke", description="Busca un Pokémon y muestra su imagen")
@app_commands.describe(nombre="Nombre del Pokémon a buscar")
async def slash_poke(interaction: discord.Interaction, nombre: str):
    try:
        result = requests.get(f'https://pokeapi.co/api/v2/pokemon/{nombre.lower()}')
        if result.status_code == 404:
            await interaction.response.send_message(f'Pokémon \"{nombre}\" no encontrado.')
        else:
            image_url = result.json()['sprites']['front_default']
            await interaction.response.send_message(f'Imagen de {nombre}: {image_url}')
    except Exception as e:
        print(f'Error en slash poke: {e}')
        await interaction.response.send_message('Error al buscar el Pokémon.')

# 👇 Prefijo: .poke
@bot.command()
async def poke(ctx, arg):
    try:
        pokemon = arg.split(" ", 1)[0]
        result = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}')
        if result.status_code == 404:
            await ctx.send(f'Pokémon \"{pokemon}\" no encontrado.')
        else:
            image_url = result.json()['sprites']['front_default']
            await ctx.send(f'Poke recibido: {pokemon}\nImagen: {image_url}')
    except Exception as e:
        print(f'Error en poke: {e}')

@poke.error
async def poke_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Por favor, proporciona el nombre del Pokémon.')
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send('Ocurrió un error. Intenta de nuevo más tarde.')

# 👇 Slash command: /clean
@tree.command(name="clean", description="Borra los últimos 100 mensajes del canal")
async def slash_clean(interaction: discord.Interaction):
    channel = interaction.channel
    messages = [msg async for msg in channel.history(limit=100)]
    await channel.delete_messages(messages)
    await interaction.response.send_message("Mensajes eliminados.", ephemeral=True)

# 👇 Prefijo: .clean
@bot.command()
async def clean(ctx):
    await ctx.channel.purge(limit=100)
    await ctx.send('Mensajes eliminados correctamente.', delete_after=3)

# Mantén vivo el bot en Render
webserver.keep_alive()
bot.run(Discord_Token)

