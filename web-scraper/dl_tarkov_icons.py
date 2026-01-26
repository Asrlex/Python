import os
import logging
import requests
from bs4 import BeautifulSoup

# Configure the logger
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

urls = [
    "https://escapefromtarkov.fandom.com/wiki/7.62x25mm_Tokarev",
    "https://escapefromtarkov.fandom.com/wiki/9x18mm_Makarov",
    "https://escapefromtarkov.fandom.com/wiki/9x19mm_Parabellum",
    "https://escapefromtarkov.fandom.com/wiki/9x21mm_Gyurza",
    "https://escapefromtarkov.fandom.com/wiki/.357_Magnum",
    "https://escapefromtarkov.fandom.com/wiki/.45_ACP",
    "https://escapefromtarkov.fandom.com/wiki/20x1mm",
    "https://escapefromtarkov.fandom.com/wiki/4.6x30mm_HK",
    "https://escapefromtarkov.fandom.com/wiki/5.7x28mm_FN",
    "https://escapefromtarkov.fandom.com/wiki/5.45x39mm",
    "https://escapefromtarkov.fandom.com/wiki/5.56x45mm_NATO",
    "https://escapefromtarkov.fandom.com/wiki/6.8x51mm",
    "https://escapefromtarkov.fandom.com/wiki/.300_Blackout",
    "https://escapefromtarkov.fandom.com/wiki/7.62x39mm",
    "https://escapefromtarkov.fandom.com/wiki/7.62x51mm_NATO",
    "https://escapefromtarkov.fandom.com/wiki/7.62x54mmR",
    "https://escapefromtarkov.fandom.com/wiki/.338_Lapua_Magnum",
    "https://escapefromtarkov.fandom.com/wiki/9x39mm",
    "https://escapefromtarkov.fandom.com/wiki/.366_TKM",
    "https://escapefromtarkov.fandom.com/wiki/12.7x55mm_STs-130",
    "https://escapefromtarkov.fandom.com/wiki/12.7x108mm",
    "https://escapefromtarkov.fandom.com/wiki/12/70",
    "https://escapefromtarkov.fandom.com/wiki/20/70",
    "https://escapefromtarkov.fandom.com/wiki/23x75mm",
    "https://escapefromtarkov.fandom.com/wiki/30x29mm",
    "https://escapefromtarkov.fandom.com/wiki/40x46mm",
    "https://escapefromtarkov.fandom.com/wiki/40x53mm",
    "https://escapefromtarkov.fandom.com/wiki/26x75mm"
]

# Loop through each URL
for url in urls:
    logging.info(f"Downloading images from {url}")

    # Folder to save the downloaded images
    folder_path = f"./output/ammunition/{url.split('/')[-1].lower()}"
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Send a GET request to the website
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    # Find all the img tags inside th components
    img_tags = soup.select("th a img")
    if not img_tags:
        img_tags = soup.select("td a img")

    # Download and save each image with the images default name
    for img_tag in img_tags:
        try:
            img_src = img_tag["src"] if img_tag["src"].startswith("http") else img_tag["data-src"]
            img_url = url + img_src if not img_src.startswith("http") else img_src
            # The name of the file is 3 slashes after the word "images" in the URL
            img_name = img_url.split("/images/")[1].split("/")[2][:-4] + ".webp"
            img_path = os.path.join(folder_path, img_name)

            # Send a GET request to download the image
            img_response = requests.get(img_url)

            # Save the image to the specified folder
            with open(img_path, "wb") as img_file:
                img_file.write(img_response.content)

            # Log the downloaded image
            logging.info(f"Downloaded: {img_name}")
        except Exception as e:
            # Log the error
            logging.error(f"Error downloading image {img_name} from {img_src}: {e}")