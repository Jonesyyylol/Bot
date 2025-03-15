import discord
from discord.ext import commands
import requests
import asyncio
import os
import random
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class AskCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.GEMINI_API_KEY = GEMINI_API_KEY
        # Farben für das Embed (zufällige Auswahl)
        self.embed_colors = [
            discord.Color.blue(),
            discord.Color.green(),
            discord.Color.orange(),
            discord.Color.purple(),
            discord.Color.gold()
        ]

    @discord.app_commands.command(name="ask", description="Stelle der KI eine Frage!")
    async def ask(self, interaction: discord.Interaction, question: str):
        if not self.GEMINI_API_KEY:
            await interaction.response.send_message("Fehler: Google Gemini API-Schlüssel fehlt! Bitte in der .env-Datei konfigurieren.", ephemeral=True)
            return

        await interaction.response.send_message("🧠 Denke nach... Bitte warte einen Moment! ⏳")

        try:
            # Hole die KI-Antwort
            ai_response = await self.get_ai_response(question)

            if ai_response:
                # Erstelle ein hübsches Embed
                embed = discord.Embed(
                    title="🤖 KI-Antwort",
                    description=ai_response,
                    color=random.choice(self.embed_colors),  # Zufällige Farbe
                    timestamp=discord.utils.utcnow()
                )
                embed.set_author(name="Capybara Bot", icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None)
                embed.set_footer(text="Powered by Jonesyyy", icon_url="https://i.postimg.cc/DySD5hG5/purple-egirl-ok.gif")  # Google-Icon als Fußzeile (falls verfügbar)
                # Optional: Füge ein Thumbnail hinzu (z. B. ein Capybara-Bild)
                embed.set_thumbnail(url="https://api.capy.lol/v1/capybara?json=true")  # Zufälliges Capybara-Bild

                await interaction.edit_original_response(content="", embed=embed)
            else:
                await interaction.edit_original_response(content="😕 Sorry, konnte keine Antwort finden! Versuche es später nochmal.")
        except Exception as e:
            await interaction.edit_original_response(content=f"❌ Fehler: {str(e)}")

    async def get_ai_response(self, question: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.GEMINI_API_KEY}"

        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": f"Antworte auf folgende Frage in einem lockeren, freundlichen Ton auf Deutsch: '{question}'"
                                }
                            ]
                        }
                    ]
                }
            )

            if response.status_code == 200:
                data = response.json()
                ai_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text")
                return ai_text if ai_text else "Keine Antwort gefunden! 😅"
            else:
                print(f"Fehler bei der Gemini API: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            print(f"Fehler beim Abrufen der KI-Antwort: {e}")
            return None

async def setup(bot):
    await bot.add_cog(AskCog(bot))