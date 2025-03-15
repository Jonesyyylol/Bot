import discord
from discord.ext import commands, tasks
import asyncio
import os
import random
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Liste der Aktivitäten
ACTIVITIES = [
    discord.Activity(type=discord.ActivityType.watching, name="created by Jonesyyy"),
    discord.Activity(type=discord.ActivityType.watching, name="Hunde 🐶"),
    discord.Activity(type=discord.ActivityType.watching, name="Capybaras 🦦"),
    discord.Activity(type=discord.ActivityType.watching, name="Capycord 💕"),
]

@bot.event
async def on_ready():
    print(f'Eingeloggt als {bot.user}')
    
    # Lade alle Cogs und zähle sie
    loaded_cogs = 0
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                loaded_cogs += 1
                print(f"Cog geladen: {filename}")
                # Liste alle Slash-Commands der geladenen Cog auf
                for command in bot.tree.get_commands():
                    print(f"  Gefundener Befehl: {command.name}")
            except Exception as e:
                print(f"Fehler beim Laden von {filename}: {e}")
    
    # Synchronisiere Slash-Commands für einen spezifischen Server
    try:
        guild_id = 123456789012345678  # Ersetze mit deiner Server-ID
        guild = discord.Object(id=guild_id)
        synced = await bot.tree.sync(guild=guild)
        print(f"Slash-Commands für Guild {guild_id} synchronisiert: {len(synced)} Befehle")
        print("Synchronisierte Befehle:", [command.name for command in synced])
        # Synchronisiere auch global
        global_synced = await bot.tree.sync()
        print(f"Globale Slash-Commands synchronisiert: {len(global_synced)} Befehle")
        print("Globale synchronisierte Befehle:", [command.name for command in global_synced])
    except Exception as e:
        print(f"Fehler bei der Synchronisation der Slash-Commands: {e}")
    
    print(f"Anzahl der geladenen Cogs: {loaded_cogs}")
    print(f"Befehle und Cogs geladen. Bot ist bereit!")

    # Starte die Status-Wechsel-Schleife
    if not change_status.is_running():
        change_status.start()

# Hintergrundaufgabe zum Wechseln des Status
@tasks.loop(seconds=30)
async def change_status():
    activity = random.choice(ACTIVITIES)  # Wähle eine zufällige Aktivität
    await bot.change_presence(activity=activity)

bot.run(DISCORD_TOKEN)