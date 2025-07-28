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
