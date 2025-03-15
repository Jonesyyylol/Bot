import discord
from discord import app_commands
from discord.ext import commands  # Importiere commands
import aiohttp
import random
from datetime import datetime

class AnimalCog(commands.Cog):  # Verwendet jetzt den korrekt importierten commands
    def __init__(self, bot):
        self.bot = bot
        self.CAPYBARA_API_ENDPOINTS = [
            "https://api.capy.lol/v1/capybara?json=true",
        ]
        self.DOG_API_ENDPOINTS = [
            "https://dog.ceo/api/breeds/image/random",
        ]
        self.CAPYBARA_DESCRIPTIONS = [
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
        self.DOG_DESCRIPTIONS = [
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

    async def get_capybara_image(self):
        api_url = random.choice(self.CAPYBARA_API_ENDPOINTS)
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

    async def get_dog_image(self):
        api_url = random.choice(self.DOG_API_ENDPOINTS)
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
    @app_commands.command(name="capybara", description="Zeigt ein süßes Capybara!")
    async def capybara(self, interaction: discord.Interaction):
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

        image_url = await self.get_capybara_image()
        if image_url:
            random_desc = random.choice(self.CAPYBARA_DESCRIPTIONS)
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
    @app_commands.command(name="dog", description="Zeigt ein süßes Hundebild!")
    async def dog(self, interaction: discord.Interaction):
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

        image_url = await self.get_dog_image()
        if image_url:
            random_desc = random.choice(self.DOG_DESCRIPTIONS)
            embed = discord.Embed(
                title="Süßer Hund! 🐶",
                description=random_desc,
                color=discord.Color.from_rgb(139, 69, 19),
                timestamp=discord.utils.utcnow()
            )
            embed.set_image(url=image_url)
            embed.set_footer(text="Powered by Jonesyyy ✘ Capycord")
            await interaction.followup.send(embed=embed) if interaction.response.is_done() else await interaction.response.send_message(embed=embed)
        else:
            await interaction.followup.send("Sorry, konnte kein Hundebild von dog.ceo laden! Versuche es nochmal.", ephemeral=True) if interaction.response.is_done() else await interaction.response.send_message("Sorry, konnte kein Hundebild von dog.ceo laden! Versuche es nochmal.", ephemeral=True)

    # Slash-Command für Bot-Informationen
    @app_commands.command(name="info", description="Zeigt Informationen über den Capybara Bot!")
    async def info(self, interaction: discord.Interaction):
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
                f"**Einladungslink**: [Hier klicken](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot+applications.commands&permissions=2147483648)"
            ),
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text="Powered by Jonesyyy ✘ Capycord")
        await interaction.followup.send(embed=embed) if interaction.response.is_done() else await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(AnimalCog(bot))