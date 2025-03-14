import discord
from discord import app_commands
import aiohttp
import random
from datetime import datetime
import asyncio

# Bot initialisieren
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Liste von Capybara-API-Endpunkten
CAPYBARA_API_ENDPOINTS = [
    "https://api.capy.lol/v1/capybara?json=true",
]

# Liste von Dog-API-Endpunkten
DOG_API_ENDPOINTS = [
    "https://dog.ceo/api/breeds/image/random",
]

# Getrennte Listen für Beschreibungen
CAPYBARA_DESCRIPTIONS = [
    "Ein süßes Capybara genießt den Tag!",
    "Schau mal, wie entspannt dieses Capybara ist!",
    "Capybara-Chill-Level: Weltmeister!",
    "Ein flauschiges Capybara nur für dich!",
    "Dieses Capybara sagt: Alles wird gut!",
    "Ein Capybara, das dein Herz erobert!",
    "So süß, dass du es knuddeln möchtest!",
    "Capybara-Vibes: Pures Glück!",
    "Dieses Capybara ist bereit für ein Abenteuer!",
    "Ein Capybara, das dir den Tag versüßt!",
    "Chillen wie ein Capybara – unschlagbar!",
    "Ein Capybara, das einfach nur süß ist!",
    "Capybara-Liebe auf den ersten Blick!",
    "Dieses Capybara bringt Sonne in dein Leben!",
    "Ein Capybara, das dir ein Lächeln schenkt!",
    "Capybara-Magie: Einfach unwiderstehlich!",
    "Dieses Capybara hat den Entspannungsmodus aktiviert!",
    "Ein Capybara, das dich zum Träumen bringt!",
    "Capybara-Freunde machen den Tag besser!",
    "Dieses Capybara ist der Star des Tages!",
    "Ein Capybara, das dir die Welt erklärt!",
    "Capybara-Zeit: Entspannung pur!",
    "Dieses Capybara hat einen entspannten Tag!",
    "Ein Capybara, das dich zum Lachen bringt!",
    "Capybara-Liebe: Einfach unendlich süß!"
]

DOG_DESCRIPTIONS = [
    "Ein treuer Hund genießt den Tag!",
    "Schau dir diesen verspielten Hund an!",
    "Hund-Charm: Unwiderstehlich!",
    "Ein flauschiger Hund nur für dich!",
    "Dieser Hund bringt Freude ins Leben!",
    "Ein Hund, der dein Herz stiehlt!",
    "So süß, dass du ihn streicheln willst!",
    "Hund-Vibes: Volle Energie!",
    "Dieser Hund ist bereit für Spaß!",
    "Ein Hund, der deinen Tag erhellt!",
    "Spielen wie ein Hund – unvergesslich!",
    "Ein Hund, der einfach liebenswert ist!",
    "Hund-Liebe auf den ersten Blick!",
    "Dieser Hund strahlt Glück aus!",
    "Ein Hund, der dich zum Lächeln bringt!",
    "Hund-Magie: Einfach wunderbar!",
    "Dieser Hund hat den Spielmodus an!",
    "Ein Hund, der dich begeistert!",
    "Hund-Freunde machen alles besser!",
    "Dieser Hund ist der Star des Tages!",
    "Ein Hund, der die Welt erobert!",
    "Hund-Zeit: Freude pur!",
    "Dieser Hund hat einen tollen Tag!",
    "Ein Hund, der dich zum Lachen bringt!"
]

# Funktion für Aktivitäten (Statusmeldungen)
def get_activities():
    return [
        discord.Activity(type=discord.ActivityType.watching, name="created by Jonesyyy"),
        discord.Activity(type=discord.ActivityType.watching, name="Capybaras"),
        discord.Activity(type=discord.ActivityType.watching, name="Capycord 💕"),
        discord.Activity(type=discord.ActivityType.watching, name="Hunde 🐶")
    ]

# Funktion zum zyklischen Wechseln des Status
async def update_status():
    activities = get_activities()
    while True:
        for activity in activities:
            await client.change_presence(activity=activity)
            await asyncio.sleep(30)

@client.event
async def on_ready():
    print(f'Eingeloggt als {client.user}')
    try:
        synced = await tree.sync()
        print(f"Befehle synchronisiert: {len(synced)}")
    except Exception as e:
        print(f"Fehler bei der Synchronisierung: {e}")

    client.loop.create_task(update_status())

# Funktion zum Abrufen eines Capybara-Bildes von der API
async def get_capybara_image():
    api_url = random.choice(CAPYBARA_API_ENDPOINTS)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    if "data" in data and "url" in data["data"]:
                        return data["data"]["url"]
                    return None
                return None
        except Exception as e:
            print(f"Fehler bei API-Aufruf {api_url}: {e}")
            return None

# Funktion zum Abrufen eines Hundebildes von der API
async def get_dog_image():
    api_url = random.choice(DOG_API_ENDPOINTS)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    if "message" in data:
                        return data["message"]
                    return None
                return None
        except Exception as e:
            print(f"Fehler bei API-Aufruf {api_url}: {e}")
            return None

# Slash-Command für Capybara-Bilder
@tree.command(
    name="capybara",
    description="Zeigt ein süßes Capybara!"
)
async def capybara(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("Du nutzt den Bot in einer DM! Hier ist dein Capybara:", ephemeral=False)
    else:
        if not interaction.channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.response.send_message(
                "Ich habe keine Berechtigung, in diesem Kanal Nachrichten zu senden. Bitte gib mir die entsprechenden Berechtigungen!",
                ephemeral=True
            )
            return
        await interaction.response.defer()

    image_url = await get_capybara_image()
    
    if image_url:
        random_desc = random.choice(CAPYBARA_DESCRIPTIONS)  # Nur Capybara-Beschreibungen
        embed = discord.Embed(
            title="Süßes Capybara! 🦫",
            description=random_desc,
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_image(url=image_url)
        embed.set_footer(text="Powered by Jonesyyy ✘ Capycord")
        await interaction.followup.send(embed=embed) if interaction.response.is_done() else await interaction.response.send_message(embed=embed)
    else:
        await interaction.followup.send("Sorry, konnte kein Capybara-Bild von capy.lol laden! Versuche es nochmal.", ephemeral=True) if interaction.response.is_done() else await interaction.response.send_message("Sorry, konnte kein Capybara-Bild von capy.lol laden! Versuche es nochmal.", ephemeral=True)

# Slash-Command für Hundebilder
@tree.command(
    name="dog",
    description="Zeigt ein süßes Hundebild!"
)
async def dog(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("Du nutzt den Bot in einer DM! Hier ist dein Hund:", ephemeral=False)
    else:
        if not interaction.channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.response.send_message(
                "Ich habe keine Berechtigung, in diesem Kanal Nachrichten zu senden. Bitte gib mir die entsprechenden Berechtigungen!",
                ephemeral=True
            )
            return
        await interaction.response.defer()

    image_url = await get_dog_image()
    
    if image_url:
        random_desc = random.choice(DOG_DESCRIPTIONS)  # Nur Hund-Beschreibungen
        embed = discord.Embed(
            title="Süßer Hund! 🐶",
            description=random_desc,
            color=discord.Color.from_rgb(139, 69, 19),  # Braune Farbe für Hunde
            timestamp=discord.utils.utcnow()
        )
        embed.set_image(url=image_url)
        embed.set_footer(text="Powered by Jonesyyy ✘ Capycord")
        await interaction.followup.send(embed=embed) if interaction.response.is_done() else await interaction.response.send_message(embed=embed)
    else:
        await interaction.followup.send("Sorry, konnte kein Hundebild von dog.ceo laden! Versuche es nochmal.", ephemeral=True) if interaction.response.is_done() else await interaction.response.send_message("Sorry, konnte kein Hundebild von dog.ceo laden! Versuche es nochmal.", ephemeral=True)

# Slash-Command für Bot-Informationen
@tree.command(
    name="info",
    description="Zeigt Informationen über den Capybara Bot!"
)
async def info(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("Du nutzt den Bot in einer DM! Hier sind die Infos:", ephemeral=False)
    else:
        if not interaction.channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.response.send_message(
                "Ich habe keine Berechtigung, in diesem Kanal Nachrichten zu senden. Bitte gib mir die entsprechenden Berechtigungen!",
                ephemeral=True
            )
            return
        await interaction.response.defer()

    embed = discord.Embed(
        title="Über den Capybara Bot 🦫",
        description=(
            "Ein Discordbot, der dir zufällige Capybarabilder und Hundebilder zeigt! "
            "Die Capybarabilder stammen aus der [Capycord-API](https://capy.lol) und die Hundebilder aus der [Dog CEO API](https://dog.ceo). "
            "Der Bot wurde von Jonesyyy speziell für Capycord entwickelt.\n\n"
            "Nutze `/capybara` für Capybaras, `/dog` für Hunde!\n"
            f"**Einladungslink**: [Hier klicken](https://discord.com/oauth2/authorize?client_id={client.user.id}&scope=bot+applications.commands&permissions=2147483648)"
        ),
        color=discord.Color.orange(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(text="Powered by Jonesyyy ✘ Capycord")
    
    await interaction.followup.send(embed=embed) if interaction.response.is_done() else await interaction.response.send_message(embed=embed)


# Bot starten
client.run('MTM1MDExNzM2NzEzMjQ1NDkyNg.G1RNSx.UdH4UO1nfbLA89hEAFHtq3rvXkAt1pDSraDmu0')