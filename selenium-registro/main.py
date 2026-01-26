import signal
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

BASE_URL = "https://gestiona.comunidad.madrid/ctac_cita/registro#"
RETRY_INTERVAL = 300
MAX_RETRY_COUNT = 20
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_POST_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
TELEGRAM_GET_UPDATES_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
TELEGRAM_USERS = [
    {
        "chat_id": "",
        "name": "Chat 1"
    },
    {
        "chat_id": "",
        "name": "Chat 2"
    }
]

driver = None

def sigint_handler(signum, frame):
    """Handle SIGINT (Ctrl+C) to gracefully exit the application."""
    print("\nSIGINT received. Exiting gracefully...")
    if driver:
        send_telegram_notification("Bot is shutting down due to manual termination.")
        print("Closing WebDriver...")
        driver.quit()
        send_telegram_notification("Bot manually terminated.")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

def main():
    """
    Automated script to check for available appointments on the Comunidad de Madrid website
    and send notifications via Telegram when appointments may be available.
    """
    global driver
    driver = init_driver()
    try:
        run_complete_process(driver)
    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        if driver:
            driver.quit()

def init_driver():
    """Initialize the Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    return driver

def start_session(driver, url):
    """Start a session and load the initial page."""
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    if soup.title:
        print("Page Title:", soup.title.string)
        send_telegram_notification(f"Bot started. Accessed page title: {soup.title.string}")
    else:
        print("Page Title: None")

def click_appointment_option(driver):
    """Click on the 'SOLICITAR CITA' link to start the appointment process."""
    link = driver.find_element(By.LINK_TEXT, "SOLICITAR CITA")
    link.click()
    time.sleep(1)

def select_options(driver):
    """Select the appropriate options from dropdown menus."""
    dropdown = driver.find_element(By.ID, "combo1")
    print("Interacting with dropdown menu...")
    for option in dropdown.find_elements(By.TAG_NAME, "option"):
        if option.text == "Registro Civil de Torrejón de Ardoz":
            print("Selecting option:", option.text)
            option.click()
            break
    time.sleep(1)
    
    dropdown = driver.find_element(By.ID, "comboServicios")
    print("Selecting service from dropdown...")
    for option in dropdown.find_elements(By.TAG_NAME, "option"):
        if option.text == "Apertura de Expediente de Matrimonio":
            print("Selecting option:", option.text)
            option.click()
            break
    time.sleep(1)

def click_continue_button(driver):
    """Click the 'Continuar' button to proceed."""
    continue_button = driver.find_element(By.XPATH, "//input[@class='boton' and @value='Continuar']")
    print("Clicking Continuar button...")
    continue_button.click()
    time.sleep(2)

def check_for_dialog(driver):
    """Check if the dialog indicating no appointments is present."""
    try:
        dialog = driver.find_element(By.CLASS_NAME, "ui-dialog")
        return dialog.is_displayed()
    except:
        return False

def close_dialog(driver):
    """Close the dialog box."""
    close_button = driver.find_element(By.XPATH, "//button[contains(@class, 'ui-dialog-titlebar-close')]")
    close_button.click()
    time.sleep(1)

def run_complete_process(driver):
    """Run the complete appointment checking process."""
    start_session(driver, BASE_URL)

    click_appointment_option(driver)
    
    select_options(driver)
    
    tries = 0
    while tries < MAX_RETRY_COUNT:
        run_main_block(driver, tries)
        tries += 1
        if tries < MAX_RETRY_COUNT:
            time.sleep(RETRY_INTERVAL)

    handle_confirmation(driver)

def run_main_block(driver, tries):
    """Main block to check for appointments and send notifications."""
    click_continue_button(driver)

    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    retry = "Attempt {}/{}".format(tries + 1, MAX_RETRY_COUNT)
    if check_for_dialog(driver):
        message = f"[{timestamp}] {retry} - ❌ No available appointments found, retrying in {RETRY_INTERVAL // 60} minutes..."
        send_telegram_notification(message)
        print(message)
        close_dialog(driver)
    else:
        message = f"[{timestamp}] {retry} - ✅ Appointments may be available. Please check the website manually."
        send_telegram_notification(message)
        print(message)
        tries = MAX_RETRY_COUNT

def send_telegram_notification(message):
    """Send a notification message via Telegram bot."""
    url = TELEGRAM_POST_URL
    for user in TELEGRAM_USERS:
        payload = {
            "chat_id": user["chat_id"],
            "text": message
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print("Message sent successfully to chat ID", user["name"])
            else:
                print("Failed to send message to chat ID", user["name"], "Status Code:", response.status_code)
        except Exception as e:
            print("Error sending message to chat ID", user["name"], "Error:", str(e))

def handle_confirmation(driver):
    """Handle the confirmation process."""
    send_confirmation_request()
    response, chat_id = poll_for_response()
    name = next((user["name"] for user in TELEGRAM_USERS if user["chat_id"] == str(chat_id)), None)
    if response == "yes":
        message = f"User {name} confirmed to continue. Restarting the process..."
        print(message)
        driver.quit()
        send_telegram_notification(message)
        main()
    elif response == "no":
        message = f"User {name} declined to continue. Terminating the process."
        print(message)
        send_telegram_notification(message)
        driver.quit()
        exit()

def send_confirmation_request():
    """Send a confirmation request to Telegram chat IDs."""
    message = "All retry attempts have been exhausted. Do you want to continue? Reply 'yes' to continue or 'no' to stop."
    send_telegram_notification(message)

def poll_for_response():
    """Poll the Telegram Bot API for a response."""
    url = TELEGRAM_GET_UPDATES_URL
    last_update_id = None
    print("Polling for user response...")
    while True:
        try:
            params = {"offset": last_update_id + 1} if last_update_id is not None else {}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                updates = response.json().get("result", [])
                for update in updates:
                    last_update_id = update["update_id"]
                    message = update.get("message", {})
                    chat_id = message.get("chat", {}).get("id")
                    text = message.get("text", "").strip().lower()
                    date = message.get("date", 0)
                    current_time = int(time.time())

                    if chat_id in map(int, [user["chat_id"] for user in TELEGRAM_USERS]) and current_time - date <= 300:
                        if text.lower() in ["yes", "no"]:
                            return text.lower(), chat_id
            else:
                print("Failed to poll for updates. Status Code:", response.status_code)
        except Exception as e:
            print("Error polling for updates:", str(e))
        time.sleep(5)

if __name__ == "__main__":
    main()