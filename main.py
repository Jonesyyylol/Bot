import discord
from discord import app_commands
import aiohttp
import random
from datetime import datetime
import asyncio

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# List of Capybara API endpoints
CAPYBARA_API_ENDPOINTS = [
    "https://api.capy.lol/v1/capybara?json=true",
]

# List of Dog API endpoints
DOG_API_ENDPOINTS = [
    "https://dog.ceo/api/breeds/image/random",
]

# Separate lists for descriptions
CAPYBARA_DESCRIPTIONS = [
    "A cute capybara enjoying the day!",
    "Look how relaxed this capybara is!",
    "Capybara chill level: World champion!",
    "A fluffy capybara just for you!",
    "This capybara says: Everything will be fine!",
    "A capybara that captures your heart!",
    "So cute you’ll want to cuddle it!",
    "Capybara vibes: Pure happiness!",
    "This capybara is ready for an adventure!",
    "A capybara that sweetens your day!",
    "Chilling like a capybara – unbeatable!",
    "A capybara that’s simply adorable!",
    "Capybara love at first sight!",
    "This capybara brings sunshine into your life!",
    "A capybara that gives you a smile!",
    "Capybara magic: Simply irresistible!",
    "This capybara has relaxation mode activated!",
    "A capybara that makes you dream!",
    "Capybara friends make the day better!",
    "This capybara is the star of the day!",
    "A capybara that explains the world to you!",
    "Capybara time: Pure relaxation!",
    "This capybara is having a chill day!",
    "A capybara that makes you laugh!",
    "Capybara love: Endlessly cute!"
]

DOG_DESCRIPTIONS = [
    "A loyal dog enjoying the day!",
    "Check out this playful dog!",
    "Dog charm: Irresistible!",
    "A fluffy dog just for you!",
    "This dog brings joy to life!",
    "A dog that steals your heart!",
    "So cute you’ll want to pet it!",
    "Dog vibes: Full of energy!",
    "This dog is ready for fun!",
    "A dog that brightens your day!",
    "Playing like a dog – unforgettable!",
    "A dog that’s simply lovable!",
    "Dog love at first sight!",
    "This dog radiates happiness!",
    "A dog that makes you smile!",
    "Dog magic: Simply wonderful!",
    "This dog has play mode on!",
    "A dog that excites you!",
    "Dog friends make everything better!",
    "This dog is the star of the day!",
    "A dog that conquers the world!",
    "Dog time: Pure joy!",
    "This dog is having a great day!",
    "A dog that makes you laugh!"
]

# Function for activities (status messages)
def get_activities():
    return [
        discord.Activity(type=discord.ActivityType.watching, name="created by Jonesyyy"),
        discord.Activity(type=discord.ActivityType.watching, name="Capybaras"),
        discord.Activity(type=discord.ActivityType.watching, name="Capycord 💕"),
        discord.Activity(type=discord.ActivityType.watching, name="Dogs 🐶")
    ]

# Function to cycle through status updates
async def update_status():
    activities = get_activities()
    while True:
        for activity in activities:
            await client.change_presence(activity=activity)
            await asyncio.sleep(30)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    try:
        synced = await tree.sync()
        print(f"Commands synchronized: {len(synced)}")
    except Exception as e:
        print(f"Error during synchronization: {e}")

    client.loop.create_task(update_status())

# Function to fetch a capybara image from the API
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
            print(f"Error calling API {api_url}: {e}")
            return None

# Function to fetch a dog image from the API
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
            print(f"Error calling API {api_url}: {e}")
            return None

# Slash command for capybara images
@tree.command(
    name="capybara",
    description="Shows a cute capybara!"
)
async def capybara(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("You're using the bot in a DM! Here's your capybara:", ephemeral=False)
    else:
        if not interaction.channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.response.send_message(
                "I don’t have permission to send messages in this channel. Please give me the appropriate permissions!",
                ephemeral=True
            )
            return
        await interaction.response.defer()

    image_url = await get_capybara_image()
    
    if image_url:
        random_desc = random.choice(CAPYBARA_DESCRIPTIONS)  # Only capybara descriptions
        embed = discord.Embed(
            title="Cute Capybara! 🦫",
            description=random_desc,
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_image(url=image_url)
        embed.set_footer(text="Powered by Jonesyyy ✘ Capycord")
        await interaction.followup.send(embed=embed) if interaction.response.is_done() else await interaction.response.send_message(embed=embed)
    else:
        await interaction.followup.send("Sorry, couldn’t load a capybara image from capy.lol! Try again.", ephemeral=True) if interaction.response.is_done() else await interaction.response.send_message("Sorry, couldn’t load a capybara image from capy.lol! Try again.", ephemeral=True)

# Slash command for dog images
@tree.command(
    name="dog",
    description="Shows a cute dog image!"
)
async def dog(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("You're using the bot in a DM! Here's your dog:", ephemeral=False)
    else:
        if not interaction.channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.response.send_message(
                "I don’t have permission to send messages in this channel. Please give me the appropriate permissions!",
                ephemeral=True
            )
            return
        await interaction.response.defer()

    image_url = await get_dog_image()
    
    if image_url:
        random_desc = random.choice(DOG_DESCRIPTIONS)  # Only dog descriptions
        embed = discord.Embed(
            title="Cute Dog! 🐶",
            description=random_desc,
            color=discord.Color.from_rgb(139, 69, 19),  # Brown color for dogs
            timestamp=discord.utils.utcnow()
        )
        embed.set_image(url=image_url)
        embed.set_footer(text="Powered by Jonesyyy ✘ Capycord")
        await interaction.followup.send(embed=embed) if interaction.response.is_done() else await interaction.response.send_message(embed=embed)
    else:
        await interaction.followup.send("Sorry, couldn’t load a dog image from dog.ceo! Try again.", ephemeral=True) if interaction.response.is_done() else await interaction.response.send_message("Sorry, couldn’t load a dog image from dog.ceo! Try again.", ephemeral=True)

# Slash command for bot information
@tree.command(
    name="info",
    description="Shows information about the Capybara Bot!"
)
async def info(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("You're using the bot in a DM! Here’s the info:", ephemeral=False)
    else:
        if not interaction.channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.response.send_message(
                "I don’t have permission to send messages in this channel. Please give me the appropriate permissions!",
                ephemeral=True
            )
            return
        await interaction.response.defer()

    embed = discord.Embed(
        title="About the Capybara Bot 🦫",
        description=(
            "A Discord bot that shows you random capybara and dog images! "
            "The capybara images come from the [Capycord API](https://capy.lol) and the dog images from the [Dog CEO API](https://dog.ceo). "
            "The bot was developed by Jonesyyy specifically for Capycord.\n\n"
            "Use `/capybara` for capybaras, `/dog` for dogs!\n"
            f"**Invite Link**: [Click here](https://discord.com/oauth2/authorize?client_id={client.user.id}&scope=bot+applications.commands&permissions=2147483648)"
        ),
        color=discord.Color.orange(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(text="Powered by Jonesyyy ✘ Capycord")
    
    await interaction.followup.send(embed=embed) if interaction.response.is_done() else await interaction.response.send_message(embed=embed)

# Start the bot
client.run('YOUR_BOT_TOKEN')  # It would be better to create a .env file for safety standards