import discord
from discord.ext import commands
import aiohttp
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Lade die beiden Webhook-URLs aus der .env-Datei
SERVER_WEBHOOK_URL = os.getenv("SERVER_WEBHOOK_URL")  # Für neue Server
COMMAND_WEBHOOK_URL = os.getenv("COMMAND_WEBHOOK_URL")  # Für Commands

class LogsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_webhook_url = SERVER_WEBHOOK_URL
        self.command_webhook_url = COMMAND_WEBHOOK_URL

        # Überprüfe, ob die Webhook-URLs definiert sind
        if not self.server_webhook_url:
            raise ValueError("SERVER_WEBHOOK_URL ist in der .env-Datei nicht definiert!")
        if not self.command_webhook_url:
            raise ValueError("COMMAND_WEBHOOK_URL ist in der .env-Datei nicht definiert!")

    async def send_to_server_webhook(self, embed):
        """Sendet ein Embed an den Webhook für neue Server."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(self.server_webhook_url, session=session)
            await webhook.send(embed=embed)

    async def send_to_command_webhook(self, embed):
        """Sendet ein Embed an den Webhook für Commands."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(self.command_webhook_url, session=session)
            await webhook.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Loggt, wenn der Bot einem neuen Server beitritt (an den Server-Webhook)."""
        # Stelle sicher, dass der Owner geladen ist
        owner = guild.owner
        if owner is None:
            try:
                owner = await guild.fetch_member(guild.owner_id)
            except discord.errors.NotFound:
                owner = None

        embed = discord.Embed(title="New Server Added", color=discord.Color.red())
        embed.add_field(name="THE BOT HAS BEEN ADDED TO A NEW SERVER:", value="", inline=False)
        embed.add_field(name="Server Name", value=f"✨ {guild.name} ✨", inline=False)
        embed.add_field(name="Server ID", value=str(guild.id), inline=False)
        embed.add_field(name="Total Members", value=str(guild.member_count), inline=False)

        if owner:
            embed.add_field(name="Owner", value=f"{owner} (ID: {owner.id})", inline=False)
        else:
            embed.add_field(name="Owner", value="Unbekannt (Owner konnte nicht geladen werden)", inline=False)

        try:
            invite = await guild.text_channels[0].create_invite(max_uses=1, unique=True)
            embed.add_field(name="Invite Link", value=invite.url, inline=False)
        except Exception as e:
            embed.add_field(name="Invite Link", value=f"Konnte keinen Invite-Link erstellen! Fehler: {str(e)}", inline=False)

        await self.send_to_server_webhook(embed)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        """Loggt, wenn ein Befehl verwendet wird (an den Command-Webhook)."""
        if not ctx.guild:  # Ignoriere DMs
            return
        embed = discord.Embed(title="Command Used", color=discord.Color.blue())
        embed.add_field(name="Command", value=f"✨ {ctx.command} ✨", inline=False)
        embed.add_field(name="User", value=f"{ctx.author} (ID: {ctx.author.id})", inline=False)
        embed.add_field(name="Server", value=f"{ctx.guild.name} (ID: {ctx.guild.id})", inline=False)
        embed.add_field(name="Channel", value=f"{ctx.channel.name} (ID: {ctx.channel.id})", inline=False)
        embed.add_field(name="Timestamp", value=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'), inline=False)

        await self.send_to_command_webhook(embed)

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        """Loggt, wenn ein Slash-Command verwendet wird (an den Command-Webhook)."""
        # Prüfe, ob es eine Interaktion mit einem Slash-Command ist
        if not interaction.guild:  # Ignoriere DMs
            return
        if interaction.type == discord.InteractionType.application_command:
            embed = discord.Embed(title="Slash Command Used", color=discord.Color.green())
            embed.add_field(name="Command", value=f"`` {interaction.command.name} ``", inline=False)
            embed.add_field(name="User", value=f"{interaction.user} (ID: {interaction.user.id})", inline=False)
            embed.add_field(name="Server", value=f"{interaction.guild.name} (ID: {interaction.guild.id})", inline=False)
            embed.add_field(name="Channel", value=f"{interaction.channel.name} (ID: {interaction.channel.id})", inline=False)
            embed.add_field(name="Timestamp", value=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'), inline=False)

            print(f"Slash-Command geloggt: {interaction.command.name} von {interaction.user}")  # Debugging
            await self.send_to_command_webhook(embed)

async def setup(bot):
    await bot.add_cog(LogsCog(bot))