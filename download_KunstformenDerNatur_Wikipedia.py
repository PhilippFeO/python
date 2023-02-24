"""
This script downloads all plates of Ernst Haeckels "Kunstformen der Natur" from <url>
and saves the images under <image_dir>.
"""


import requests
import re
from subprocess import run
from time import sleep
from bs4 import BeautifulSoup
from os import makedirs


# url with all 100 "Kunstformen der Natur - Erich Haeckel" plates
url = "https://commons.wikimedia.org/wiki/Kunstformen_der_Natur?uselang=de"
r = requests.get(url=url, timeout=2000)
soup = BeautifulSoup(r.text, features="html.parser")

# target directory
image_dir = "./Wikipedia/"
makedirs(image_dir, exist_ok=True)

# Pattern for matching the Titles
#   Some thumbnails on the Wikipedia page habe two <img>-tags in the corresponding HTML-li-section
#   but one <img> has an <alt>-attribute with the title and titles start with a number.
regex = re.compile(r'^\d')
titles = [] # Titles are saved to file because they are necessray for GIMP manipulation later on

# Iterate over the HTML elements to retrieve the information for downloading images
for ul in soup.find_all('ul'):
    try:
        if ul['class']==["gallery", "mw-gallery-packed-hover"]:
            for li in ul.find_all('li'):
                for p in li.find_all('p'):
                    title = p.get_text().strip() # remove newline and whitespace characters
                    # Cover image is not marked with a (plate) number
                    if "Cover" in title:
                        title = f"0. {title}"
                    titles.append(title)
                    for img in li.find_all('img'):
                        # Regex-Matching because comparison with title was not possible
                        #   <img.alt> and <p> contain only(!) on first glance the same string
                        match = regex.match(img['alt'])
                        if match or title == "0. Cover":
                            # format "thumbnail url" to get url of high resolution image
                            img_src: str = img['src']
                            img_src = img_src.replace("/thumb", "")
                            img_src = img_src.rsplit('/', 1)[0]
                            # Download high resolution images using <wget>
                            #   ...was not able to get it working with <requests>
                            run(["wget", "-O", f"{image_dir}/{title}", img_src])
                            # Delay, otherwise Wikipedia blocks some requests
                            sleep(1)
    except KeyError as ke:
        print("E: Attribute 'class' non existent in current <ul>-tag.")

print("\nBilder gespeichert.")

# Save titles in file (are necessray for manipulation in GIMP)
with open(image_dir + "Titel.txt", "w") as title_file:
    title_file.writelines(title + "\n" for title in titles)

print("\nTitel gespeichert.")
print()
