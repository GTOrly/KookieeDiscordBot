import discord
import re
from urllib.parse import urlparse

# ==== Embeds con estilos ====

def crear_embed_info(titulo: str, descripcion: str, usuario: discord.User, color: discord.Color = discord.Color.blurple()) -> discord.Embed:
    embed = discord.Embed(title=titulo, description=descripcion, color=color)
    embed.set_footer(
        text=f"Solicitado por {usuario.display_name}",
        icon_url=usuario.avatar.url if usuario.avatar else discord.Embed.Empty
    )
    return embed

def crear_embed_exito(titulo: str, descripcion: str, usuario: discord.User) -> discord.Embed:
    return crear_embed_info(titulo, descripcion, usuario, color=discord.Color.green())

def crear_embed_error(titulo: str, descripcion: str, usuario: discord.User) -> discord.Embed:
    return crear_embed_info(titulo, descripcion, usuario, color=discord.Color.red())

# ==== Utilidades auxiliares ====

def hex_a_rgb(hex_color: str) -> tuple[int, int, int] | None:
    match = re.fullmatch(r"#?([0-9a-fA-F]{6})", hex_color)
    if not match:
        return None
    hex_value = match.group(1)
    r = int(hex_value[0:2], 16)
    g = int(hex_value[2:4], 16)
    b = int(hex_value[4:6], 16)
    return (r, g, b)

def url_valida(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)

async def resolver_menciones(texto: str, guild: discord.Guild) -> tuple[str, bool]:
    nombres = [nombre.strip().lstrip("@") for nombre in texto.split(",")]
    menciones = []
    hay_menciones = False

    for nombre in nombres:
        miembro = discord.utils.find(lambda m: m.name == nombre or m.display_name == nombre, guild.members)
        rol = discord.utils.find(lambda r: r.name == nombre, guild.roles)

        if miembro:
            menciones.append(f"👤 **{miembro.mention}**")
            hay_menciones = True
        elif rol:
            menciones.append(f"🛡️ **{rol.mention}**")
            hay_menciones = True
        else:
            menciones.append(f"❓ `{nombre}`")  # No encontrado

    return "\n".join(menciones), hay_menciones

# ==== Modal personalizado para embeds ====

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

    color_hex = discord.ui.TextInput(
        label="Color (hex o nombre)",
        placeholder="#7289da / red / blue...",
        required=False
    )

    imagen_url = discord.ui.TextInput(
        label="URL de imagen (opcional)",
        placeholder="https://...",
        required=False
    )

    menciones = discord.ui.TextInput(
        label="Menciones (@nombre o nombre de rol)",
        placeholder="Ej: @Juan, @Moderadores",
        required=False
    )

    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        # Resolución de menciones
        menciones_str, hay_menciones = ("", False)
        if self.menciones.value:
            menciones_str, hay_menciones = await resolver_menciones(self.menciones.value, interaction.guild)

        # Color personalizado
        color_input = self.color_hex.value.lower().strip()
        colores_predefinidos = {
            "red": discord.Color.red(),
            "blue": discord.Color.blue(),
            "green": discord.Color.green(),
            "yellow": discord.Color.gold(),
            "random": discord.Color.random(),
        }

        color_embed = discord.Color.blurple()
        if color_input in colores_predefinidos:
            color_embed = colores_predefinidos[color_input]
        else:
            rgb = hex_a_rgb(color_input)
            if rgb:
                color_embed = discord.Color.from_rgb(*rgb)

        # Construcción del embed
        embed = discord.Embed(
            title=self.titulo.value,
            description=self.descripcion.value,
            color=color_embed
        )

        embed.set_footer(
            text=f"Creado por {interaction.user.display_name}",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else discord.Embed.Empty
        )

        if self.imagen_url.value and url_valida(self.imagen_url.value):
            embed.set_image(url=self.imagen_url.value)

        # Campo separado para menciones
        if menciones_str.strip():
            embed.add_field(
                name="🔔 Menciones",
                value=menciones_str,
                inline=False
            )

        await interaction.response.send_message(embed=embed)
