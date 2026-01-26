# Comunidad de Madrid Appointment Checker

This Python script automates the process of checking for available appointments on the Comunidad de Madrid website. It uses Selenium WebDriver to interact with the website and Telegram Bot API to send notifications to users.

## Features
- Automates the process of navigating the Comunidad de Madrid appointment system.
- Sends notifications to specified Telegram users when appointments are available or retries are exhausted.
- Handles user confirmation via Telegram to continue or terminate the process.
- Configurable retry intervals and maximum retry attempts.

## Requirements
- Python 3.8+
- Selenium WebDriver
- BeautifulSoup4
- Requests
- Google Chrome and ChromeDriver

## Setup
1. Clone this repository.
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up a Telegram bot and obtain the bot token. Add the token and user chat IDs to the `TELEGRAM_BOT_TOKEN` and `TELEGRAM_USERS` variables in `main.py`.
4. Ensure Google Chrome and ChromeDriver are installed and compatible with each other.

## Usage
1. Activate your virtual environment:
   ```bash
   source venv/Scripts/activate
   ```
2. Run the script:
   ```bash
   python main.py
   ```
3. The script will notify you via Telegram about the status of appointment availability.

## Configuration
- `BASE_URL`: The URL of the Comunidad de Madrid appointment system.
- `RETRY_INTERVAL`: Time (in seconds) between retries.
- `MAX_RETRY_COUNT`: Maximum number of retries before asking for user confirmation.

## Notes
- Ensure the Telegram bot has access to the specified chat IDs.
- The script runs in headless mode by default. You can modify the `init_driver` function to disable headless mode for debugging.

## License
This project is licensed under the MIT License.