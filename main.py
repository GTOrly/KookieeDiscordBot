import discord
from discord.ext import commands
import requests
import os
import webserver

Discord_Token = os.getenv('Discord_Token')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.tree.command(name="ping", description="Responde con Pong y muestra la latencia")
async def slash_ping(interaction: discord.Interaction):
    latency_ms = round(bot.latency * 1000)

    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latencia actual: `{latency_ms} ms`",
        color=discord.Color.blue()
    )
    embed.set_footer(
        text=f"Solicitado por {interaction.user.display_name}",
        icon_url=interaction.user.avatar.url if interaction.user.avatar else discord.Embed.Empty
    )

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="poke", description="Busca información sobre un Pokémon")
async def slash_poke(interaction: discord.Interaction, nombre: str):
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{nombre.lower()}'
        result = requests.get(url)

        if result.status_code != 200:
            await interaction.response.send_message(f'Pokémon \"{nombre}\" no encontrado.', ephemeral=True)
            return

        data = result.json()
        name = data['name'].capitalize()
        types = [t['type']['name'].capitalize() for t in data['types']]
        abilities = [a['ability']['name'].capitalize() for a in data['abilities']]
        sprite_url = data['sprites']['front_default']
        weight = data['weight'] / 10
        height = data['height'] / 10
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}

        atk = stats.get('attack', 'N/A')
        defn = stats.get('defense', 'N/A')
        speed = stats.get('speed', 'N/A')

        embed = discord.Embed(
            title=f"{name} 🐾",
            description=f"Altura: `{height} m`  |  Peso: `{weight} kg`\nTipo(s): {', '.join(types)}",
            color=discord.Color.random()
        )
        embed.set_thumbnail(url=sprite_url)
        embed.add_field(name="✨ Habilidades", value=', '.join(abilities), inline=False)
        embed.add_field(name="📊 Stats", value=f"Ataque: `{atk}`\nDefensa: `{defn}`\nVelocidad: `{speed}`", inline=False)

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        print(f'Error en slash_poke: {e}')
        await interaction.response.send_message('Ocurrió un error al procesar tu solicitud.')

@bot.tree.command(name="clean", description="Elimina mensajes del canal")
async def slash_clean(interaction: discord.Interaction, cantidad: int = 100):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(
            "🚫 No tienes permisos para usar este comando.",
            ephemeral=True
        )
        return

    try:
        await interaction.response.defer(ephemeral=False)
        await interaction.channel.purge(limit=cantidad)

        embed = discord.Embed(
            title="🧼 Limpieza completada",
            description=f"Se eliminaron `{cantidad}` mensajes.",
            color=discord.Color.green()
        )
        embed.set_footer(
            text=f"Solicitado por {interaction.user.display_name}",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else discord.Embed.Empty
        )

        await interaction.followup.send(embed=embed, delete_after=5)

    except Exception as e:
        print(f'Error en slash_clean: {e}')
        await interaction.followup.send("⚠️ Ocurrió un error al intentar limpiar los mensajes.")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()

webserver.keep_alive()
bot.run(Discord_Token)

