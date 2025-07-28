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

class EmbedModal(discord.ui.Modal, title="Crear un Embed Personalizado"):
    titulo = discord.ui.TextInput(
        label="Título del embed",
        placeholder="Escribe el título aquí...",
        max_length=256
    )
    descripcion = discord.ui.TextInput(
        label="Descripción",
        style=discord.TextStyle.paragraph,
        placeholder="Puedes usar saltos de línea libremente",
        max_length=2000,
        required=True
    )

    def __init__(self, interaction: discord.Interaction, color=discord.Color.blurple()):
        super().__init__()
        self.interaction = interaction
        self.color = color

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.titulo.value,
            description=self.descripcion.value,
            color=self.color
        )
        embed.set_footer(
            text=f"Creado por {interaction.user.display_name}",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else discord.Embed.Empty
        )

        await interaction.response.send_message(embed=embed)

        msg = await interaction.original_response()
        await msg.add_reaction("👁️")
        await msg.add_reaction("📥")

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

class EmbedModal(discord.ui.Modal, title="Crear un Embed Personalizado"):
    titulo = discord.ui.TextInput(
        label="Título del embed",
        placeholder="Escribe el título aquí...",
        max_length=256
    )
    descripcion = discord.ui.TextInput(
        label="Descripción",
        style=discord.TextStyle.paragraph,
        placeholder="Puedes usar saltos de línea libremente",
        max_length=2000,
        required=True
    )
    imagen_url = discord.ui.TextInput(
        label="URL de imagen (opcional)",
        placeholder="https://i.imgur.com/ejemplo.png",
        required=False
    )

    def __init__(self, interaction: discord.Interaction, color=discord.Color.blurple()):
        super().__init__()
        self.interaction = interaction
        self.color = color

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.titulo.value,
            description=self.descripcion.value,
            color=self.color
        )

        # Solo agregar imagen si se especifica
        if self.imagen_url.value.strip():
            embed.set_image(url=self.imagen_url.value.strip())

        embed.set_footer(
            text=f"Creado por {interaction.user.display_name}",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else discord.Embed.Empty
        )

        await interaction.response.send_message(embed=embed)

        msg = await interaction.original_response()
        await msg.add_reaction("👁️")
        await msg.add_reaction("📥")

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    await bot.tree.sync()

webserver.keep_alive()
bot.run(Discord_Token)

