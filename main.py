import discord
from discord.ext import commands
import requests
import os
import webserver
from utils_embeds import crear_embed_info, crear_embed_exito, crear_embed_error

Discord_Token = os.getenv('Discord_Token')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

def es_admin(interaction: discord.Interaction) -> bool:
    return interaction.user.guild_permissions.administrator

@bot.tree.command(name="active", description="Muestra el enlace para activar tu insignia de desarrollador")
async def slash_active(interaction: discord.Interaction):
    if not es_admin(interaction):
        embed_error = crear_embed_error(
            titulo="🚫 Solo administradores",
            descripcion="No tienes permisos para usar este comando.",
            usuario=interaction.user
        )
        await interaction.response.send_message(embed=embed_error, ephemeral=True)
        return

    embed = crear_embed_info(
        titulo="🎓 ¡Activa tu insignia de desarrollador!",
        descripcion=(
            "Si ya has usado el Portal para desarrolladores de Discord y tienes una aplicación activa, "
            "puedes activar tu insignia aquí:\n\n"
            "[🔗 Enlace de activación](https://discord.com/developers/active-developer)"
        ),
        usuario=interaction.user
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="ping", description="Responde con Pong y muestra la latencia")
async def slash_ping(interaction: discord.Interaction):
    latency_ms = round(bot.latency * 1000)
    embed = crear_embed_info(
        titulo="🏓 Pong!",
        descripcion=f"Latencia actual: `{latency_ms} ms`",
        usuario=interaction.user,
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="poke", description="Busca información sobre un Pokémon")
async def slash_poke(interaction: discord.Interaction, nombre: str):
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{nombre.lower()}'
        result = requests.get(url)

        if result.status_code != 200:
            embed_error = crear_embed_error(
                titulo="🧐 Pokémon no encontrado",
                descripcion=f"El Pokémon \"{nombre}\" no existe o está mal escrito.",
                usuario=interaction.user
            )
            await interaction.response.send_message(embed=embed_error, ephemeral=True)
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

        embed = crear_embed_info(
            titulo=f"{name} 🐾",
            descripcion=f"Altura: `{height} m` | Peso: `{weight} kg`\nTipo(s): {', '.join(types)}",
            usuario=interaction.user,
            color=discord.Color.random()
        )
        embed.set_thumbnail(url=sprite_url)
        embed.add_field(name="✨ Habilidades", value=', '.join(abilities), inline=False)
        embed.add_field(name="📊 Stats", value=f"Ataque: `{atk}`\nDefensa: `{defn}`\nVelocidad: `{speed}`", inline=False)

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        print(f'Error en slash_poke: {e}')
        embed_error = crear_embed_error(
            titulo="❌ Error interno",
            descripcion="Ocurrió un problema al buscar el Pokémon.",
            usuario=interaction.user
        )
        await interaction.response.send_message(embed=embed_error)

@bot.tree.command(name="clean", description="Elimina mensajes del canal")
async def slash_clean(interaction: discord.Interaction, cantidad: int = 100):
    if not interaction.user.guild_permissions.manage_messages:
        embed_error = crear_embed_error(
            titulo="🚫 Permisos insuficientes",
            descripcion="No tienes permisos para eliminar mensajes.",
            usuario=interaction.user
        )
        await interaction.response.send_message(embed=embed_error, ephemeral=True)
        return

    try:
        await interaction.response.defer(ephemeral=False)
        await interaction.channel.purge(limit=cantidad)

        embed = crear_embed_exito(
            titulo="🧼 Limpieza completada",
            descripcion=f"Se eliminaron `{cantidad}` mensajes.",
            usuario=interaction.user
        )
        await interaction.followup.send(embed=embed, delete_after=5)

    except Exception as e:
        print(f'Error en slash_clean: {e}')
        embed_error = crear_embed_error(
            titulo="❌ Error",
            descripcion="Ocurrió un problema al ejecutar la limpieza.",
            usuario=interaction.user
        )
        await interaction.followup.send(embed=embed_error)

@bot.tree.command(name="embed", description="Crea un embed con reacciones para seguimiento")
async def slash_embed(
    interaction: discord.Interaction,
    titulo: str = commands.Param(description="Título del mensaje"),
    descripcion: str = commands.Param(description="Contenido principal del mensaje"),
    color_hex: str = commands.Param(default="#5865F2", description="Color del embed"),
    privado: bool = commands.Param(default=False, description="Si el mensaje es solo para ti")
):
    if not interaction.user.guild_permissions.manage_messages:
        embed_error = crear_embed_error(
            titulo="🚫 Permisos insuficientes",
            descripcion="Necesitas el permiso `Manage Messages` para usar este comando.",
            usuario=interaction.user
        )
        await interaction.response.send_message(embed=embed_error, ephemeral=True)
        return

    try:
        COLORES_NOMBRES = {
            "red": 0xFF0000, "green": 0x00FF00, "blue": 0x0000FF,
            "yellow": 0xFFFF00, "purple": 0x800080, "orange": 0xFFA500,
            "grey": 0x808080, "white": 0xFFFFFF, "black": 0x000000
        }
        color_hex = color_hex.strip().lower()
        color = discord.Color(COLORES_NOMBRES.get(color_hex, int(color_hex.strip("#"), 16)))

        embed = discord.Embed(title=titulo, description=descripcion, color=color)
        embed.set_footer(
            text=f"Creado por {interaction.user.display_name}",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else discord.Embed.Empty
        )

        await interaction.response.send_message(embed=embed, ephemeral=privado)

        if not privado:
            msg = await interaction.original_response()
            await msg.add_reaction("👁️")   # Leído
            await msg.add_reaction("📥")   # No leído / pendiente

    except Exception as e:
        print(f"Error en slash_embed: {e}")
        await interaction.response.send_message("❌ Error al crear el embed. Revisa el color o los argumentos.", ephemeral=True)6

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    await bot.tree.sync()

webserver.keep_alive()
bot.run(Discord_Token)

