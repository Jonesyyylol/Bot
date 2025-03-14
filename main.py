import discord
from discord import app_commands
import aiohttp
import random

# Bot initialisieren
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Liste von Capybara-APIs
CAPYBARA_APIS = [
    "https://capybara-api.xyz/image",  # API 1
    "https://api.capy.lol/v1/capybara",  # API 2
]

# Zufällige Beschreibungen
DESCRIPTIONS = [
    "Ein süßes Capybara genießt den Tag!",
    "Schau mal, wie entspannt dieses Capybara ist!",
    "Capybara-Chill-Level: Weltmeister!",
    "Ein flauschiges Capybara nur für dich!",
    "Dieses Capybara sagt: Alles wird gut!",
]

@client.event
async def on_ready():
    print(f'Eingeloggt als {client.user}')
    try:
        synced = await tree.sync()
        print(f"Befehle synchronisiert: {len(synced)}")
    except Exception as e:
        print(e)

# Funktion zum Abrufen eines Capybara-Bildes von einer zufälligen API
async def get_capybara_image():
    api_url = random.choice(CAPYBARA_APIS)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    # Unterschiedliche API-Strukturen behandeln
                    if "url" in data:
                        return data["url"]  # Für capybara-api.xyz
                    elif "data" in data and "image" in data["data"]:
                        return data["data"]["image"]  # Für api.capy.lol
                return None
        except Exception as e:
            print(f"Fehler bei API-Aufruf {api_url}: {e}")
            return None

# Slash-Command für Capybara-Bilder
@tree.command(
    name="capybara",
    description="Zeigt ein süßes Capybara-Bild von verschiedenen Quellen!"
)
async def capybara(interaction: discord.Interaction):
    # Bild von einer zufälligen API abrufen
    image_url = await get_capybara_image()
    
    if image_url:
        # Zufällige Beschreibung auswählen
        random_desc = random.choice(DESCRIPTIONS)
        
        # Embed erstellen
        embed = discord.Embed(
            title="Süßes Capybara! 🦫",
            description=random_desc,
            color=discord.Color.orange()
        )
        embed.set_image(url=image_url)
        embed.set_footer(text="Powered by Jonesyyy")
        
        # Embed senden
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(
            "Sorry, konnte kein Capybarabild laden! Versuche es nochmal.",
            ephemeral=True
        )

# Bot starten
client.run('MTM1MDExNzM2NzEzMjQ1NDkyNg.G1RNSx.UdH4UO1nfbLA89hEAFHtq3rvXkAt1pDSraDmu0')