# 🐾 Kookiee Bot

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![discord.py](https://img.shields.io/badge/discord.py-app_commands-green)
![Render](https://img.shields.io/badge/Deployment-Render.com-purple)
![Status](https://img.shields.io/badge/Project-Active-brightgreen)

**Kookiee Bot** es un bot de Discord desarrollado en **Python** utilizando `discord.py`. Su objetivo es ofrecer comandos visuales y funcionales con respuestas mediante embeds personalizados, moderación integrada (en desarrollo), y soporte para interfaces como formularios, botones y menús. Está pensado para comunidades que valoran organización, seguridad y una experiencia visual atractiva.

Su entorno secundario de desarrollo es **OrlyLearn**, donde se experimentan nuevas funciones antes de su implementación oficial en Kookiee.

---

## 🧪 Comandos Disponibles

- `/ping` → Muestra la latencia actual del bot.
- `/poke nombre` → Busca información sobre un Pokémon.
- `/clean cantidad` → Elimina mensajes del canal (requiere permisos de moderación).
- `/active` → Envía enlace para activar la insignia de desarrollador (respuesta privada).
- `/embed` → Crea un embed personalizado desde formulario interactivo.

---

## 🔧 Tecnologías Utilizadas

- **Python 3.11+**
- **discord.py** con `app_commands` y componentes `discord.ui`
- **Render.com** para despliegue automático y persistente
- `utils_embeds.py` para manejo estandarizado de estilos visuales
- **Sistema uptime (keep alive)**:  
  El archivo `webserver.py` ejecuta una instancia web mínima para evitar que el bot se duerma en servicios gratuitos como Replit. Es útil como complemento cuando el despliegue no garantiza persistencia continua.

---

## 🚀 Próximas Integraciones

- Comando `/help` con menú interactivo por categorías.
- Comandos administrativos: `/kick`, `/ban`, `/userinfo`.
- Moderación y seguridad:
  - Verificación de permisos (`Manage Messages`, `Administrator`)
  - Embeds visuales para errores y advertencias
  - Respuestas privadas con `ephemeral`
- Select menus y botones para navegación y confirmaciones.
- Refactorización en `cogs` modulares por categoría (`mod`, `info`, `fun`, `ui`).
- Base de datos opcional para persistencia (usuarios, estadísticas, configuraciones).

---

## 🤝 Contribuciones

Este proyecto está en evolución constante. Si deseas aportar, puedes hacerlo mediante:

- Sugerencias en los issues del repositorio.
- Forks y Pull Requests con mejoras o nuevos comandos.
- Pruebas en entorno de desarrollo utilizando **OrlyLearn** como sandbox.

> Tu participación ayuda a que Kookiee sea más completo, modular y útil para distintas comunidades. 🧩
