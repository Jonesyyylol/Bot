# Capybara Bot

A fun and simple Discord bot that fetches random images of capybaras and dogs using public APIs. Built with Python and the `discord.py` library, this bot brings cute animal vibes to your Discord server!

- **Capybara Images**: Sourced from the [Capycord API](https://capy.lol).
- **Dog Images**: Sourced from the [Dog CEO API](https://dog.ceo).
- **Developed by**: Jonesyyy for Capycord.

## Features
- **Slash Commands**:
  - `/capybara`: Displays a random capybara image with a fun description.
  - `/dog`: Displays a random dog image with a playful description.
  - `/info`: Shows information about the bot, including an invite link.
- **Dynamic Status**: Cycles through various status messages (e.g., "Watching Capybaras").
- **Embed Support**: Images are presented in stylish Discord embeds with timestamps and footers.

## Prerequisites
- Python 3.8 or higher
- A Discord account and a bot token (create one via the [Discord Developer Portal](https://discord.com/developers/applications))
- Required Python libraries (see [Installation](#installation))

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jonesyyylol/bot.git
   cd capybara-bot
   ```

2. **Install Dependencies**:
   Install the required Python libraries using `pip`:
   ```bash
   pip install -r requirements.txt
   ```
   If there’s no `requirements.txt` yet, install these manually:
   ```bash
   pip install discord.py aiohttp
   ```

3. **Set Up Your Bot Token**:
   - Create a `.env` file in the project root:
     ```bash
     touch .env
     ```
   - Add your Discord bot token to the `.env` file:
     ```
     DISCORD_TOKEN=your_bot_token_here
     ```
   - **Note**: Never commit your `.env` file to GitHub. Add it to `.gitignore` for safety.

4. **Run the Bot**:
   ```bash
   python bot.py
   ```

## Usage
1. Invite the bot to your Discord server using the invite link provided by the `/info` command.
2. Use the following slash commands in your server:
   - `/capybara` – Get a cute capybara image.
   - `/dog` – Get an adorable dog image.
   - `/info` – Learn more about the bot.

### Example Output
- **Command**: `/capybara`
  - **Response**: An embed with a capybara image and a random description like "A cute capybara enjoying the day!"

## Configuration
- **API Endpoints**: Modify `CAPYBARA_API_ENDPOINTS` or `DOG_API_ENDPOINTS` in `bot.py` to use different APIs if desired.
- **Descriptions**: Customize the `CAPYBARA_DESCRIPTIONS` and `DOG_DESCRIPTIONS` lists to change the text displayed with images.
- **Status Messages**: Edit the `get_activities()` function to adjust the bot’s rotating status.

## Contributing
Feel free to fork this repository, submit pull requests, or open issues for bugs and feature requests! Contributions are welcome.

1. Fork the repo.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License
This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for details.

## Credits
- **Developer**: Jonesyyy
- **APIs Used**:
  - [Capycord API](https://capy.lol)
  - [Dog CEO API](https://dog.ceo)
- **Powered by**: Capycord

## Contact
For questions or support, reach out via Discord (add your Discord handle here) or open an issue on GitHub.

---
