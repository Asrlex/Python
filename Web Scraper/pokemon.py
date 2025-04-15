import os
import re
import logging
import csv
import requests
from bs4 import BeautifulSoup

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

urls = [
    "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number",
]
pokemon_types = [
    "Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison", "Ground", "Flying",
    "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"
]
class Pokemon:
    def __init__(self, name, number, img_name, type1, type2, generation):
        self.name = name
        self.number = number
        self.img_name = img_name
        self.type1 = type1
        self.type2 = type2
        self.generation = generation

pokemon_collection = []

def download_pokemon(url):
    logging.info(f"Downloading images from {url}")

    folder_path = "./output/pokemon"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    generation = 0
    tables = soup.select(".roundy")
    for table in tables:
        pokemon_rows = table.select("tbody tr")[1:]
        generation += 1
        for row in pokemon_rows:
            columns = row.select("td")
            if len(columns) < 3:
                continue
            logging.info(f"Downloading {row.select('td')[2].text.strip()}")
            
            if re.match(r"#\d{4}", columns[0].text.strip()):
                number = columns[0].text.strip().split("#")[-1]
                img_url = columns[1].select_one("img")["src"]
                img_name = img_url.split("/")[-1]
                img_data = requests.get(img_url).content
                name = columns[2].text.strip()
                type1 = columns[3].text.strip()
                if len(columns) > 4 and columns[4].text.strip() in pokemon_types:
                    type2 = columns[4].text.strip()
                else:
                    type2 = ""
            else:
                number = pokemon_collection[-1].number if pokemon_collection else "0000"
                img_url = columns[0].select_one("img")["src"]
                img_name = img_url.split("/")[-1]
                img_data = requests.get(img_url).content
                name = row.select_one("a").get("title").strip() + " - " + row.select_one("small").text.strip()
                type1 = columns[2].text.strip()
                if len(columns) > 3 and columns[3].text.strip() in pokemon_types:
                    type2 = columns[3].text.strip()
                else:
                    type2 = ""

            pokemon = Pokemon(name, number, img_name, type1, type2, generation)
            pokemon_collection.append(pokemon)

            if os.path.exists(f"{folder_path}/{img_name}"):
                logging.info(f"Image {img_name} already exists, skipping download")
                continue
            with open(f"{folder_path}/{img_name}", "wb") as img_file:
                img_file.write(img_data)

        logging.info("Download completed")

def save_pokemon():
    with open('pokemon.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Number", "Image", "Type1", "Type2"])
        for pokemon in pokemon_collection:
            logging.info(f"Saving {pokemon.name}")
            writer.writerow([pokemon.name, pokemon.number, pokemon.img_name, pokemon.type1, pokemon.type2])

def main():
    for url in urls:
        download_pokemon(url)
    save_pokemon()

if __name__ == "__main__":
    main()
        