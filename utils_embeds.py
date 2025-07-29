import discord

def crear_embed_info(titulo: str, descripcion: str, usuario: discord.User, color: discord.Color = discord.Color.blurple()):
    embed = discord.Embed(title=titulo, description=descripcion, color=color)
    embed.set_footer(
        text=f"Solicitado por {usuario.display_name}",
        icon_url=usuario.avatar.url if usuario.avatar else discord.Embed.Empty
    )
    return embed

def crear_embed_exito(titulo: str, descripcion: str, usuario: discord.User):
    return crear_embed_info(titulo, descripcion, usuario, color=discord.Color.green())

def crear_embed_error(titulo: str, descripcion: str, usuario: discord.User):
    return crear_embed_info(titulo, descripcion, usuario, color=discord.Color.red())

async def resolver_menciones(texto: str, guild: discord.Guild) -> str:
    nombres = [nombre.strip().lstrip("@") for nombre in texto.split(",")]
    menciones = []

    for nombre in nombres:
        miembro = discord.utils.find(lambda m: m.name == nombre or m.display_name == nombre, guild.members)
        rol = discord.utils.find(lambda r: r.name == nombre, guild.roles)

        if miembro:
            menciones.append(miembro.mention)
        elif rol:
            menciones.append(rol.mention)
        else:
            menciones.append(f"`{nombre}`")  # No encontrado

    return " ".join(menciones)

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
        placeholder="#7289da / red / blue",
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
        # Color personalizado
        color_input = self.color_hex.value.lower().strip()
        colores_predefinidos = {
            "red": discord.Color.red(),
            "blue": discord.Color.blue(),
            "green": discord.Color.green(),
            "yellow": discord.Color.gold(),
            "random": discord.Color.random(),
        }

        color_embed = discord.Color.blurple()  # Por defecto

        if color_input in colores_predefinidos:
            color_embed = colores_predefinidos[color_input]
        elif color_input.startswith("#") and len(color_input) == 7:
            try:
                color_embed = discord.Color.from_str(color_input)
            except:
                pass  # Color inválido, usa por defecto

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

        if self.imagen_url.value:
            embed.set_image(url=self.imagen_url.value)

        await interaction.response.send_message(embed=embed)

        # Resolución de menciones
        if self.menciones.value:
            menciones_str = await resolver_menciones(self.menciones.value, interaction.guild)
            await interaction.followup.send(content=menciones_str)
