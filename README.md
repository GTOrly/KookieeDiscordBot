# OrlyLearn Bot

OrlyLearn Bot es un bot de Discord creado en Python utilizando discord.py. Está diseñado para ofrecer comandos útiles, moderación básica, y respuestas visuales con embeds personalizados. Ideal para comunidades que valoran organización y funcionalidad.

## Comandos Disponibles

- /ping: Muestra la latencia actual del bot
- /poke nombre: Busca información sobre un Pokémon
- /clean cantidad: Elimina mensajes en el canal (solo moderadores)
- /active: Envía el enlace para activar la insignia de desarrollador (solo visible para quien lo ejecuta)

## Tecnologías Utilizadas

- Python 3.11+
- discord.py con app_commands
- Render.com para despliegue automático
- utils_embeds.py para embeds personalizados
- Webserver de keep alive para mantener activo el bot en hosting gratuito

## Estructura del Proyecto (sugerida)

orlylearn-bot/
├── main.py
├── webserver.py
├── utils_embeds.py
├── requirements.txt
├── README.md

## Moderación y Seguridad

- Verificación de permisos para comandos administrativos
- Mensajes de error claros y visuales
- Interacciones privadas con respuestas ephemeral

## Próximas Mejoras

- Comando /help con menú interactivo
- Comandos /kick, /ban, /userinfo
- Integración de botones y select menus
- Separación en cogs para modularidad

