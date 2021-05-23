import sys
import os
import logging
import argparse
from bs4 import BeautifulSoup
import requests

# Output data to stdout instead of stderr
log = logging.getLogger()
log.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

log.addHandler(handler)

# Parse the argument for user specification files
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--website",
                    type=str,
                    required=True,
                    help="Website file for downloading a pack of icons")
parser.add_argument("-o", "--output",
                    type=str,
                    required=True,
                    help="Output directory for the download")
args = parser.parse_args()

# Check directory is exist or not
os.makedirs(f"{args.output}",
            exist_ok=True)

# Create the fake headers to cheat the website
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/56.0.2924.87 Safari/537.36 "
}

# Save the category files
buffer_information = open(args.website, "r").readlines()

for cur_information in buffer_information:
    # Remove "\n"
    cur_website, categories = cur_information.strip().split(",")

    # Know the current category
    logging.info(categories)

    # End line
    if cur_website == "":
        sys.exit()

    count = 0
   
   
    # Get the html and parse the tags
    response = requests.get(f"{cur_website}",
                            headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    find_ul = soup.find("section", {"class": "search-result"}).find("ul", {"class": "icons"})
    find_li = find_ul.findAll("li", {"class": "icon--item"})

    # Run through all the image section
    for li in find_li:
        try:
            img = li.find("img", {"class": "lzy"})

            img_url = img.get("data-src")

            # Check the url is valid for saving image file
            if not img_url.endswith(".png"):
                continue

            # Save the data
            img_data = requests.get(img_url).content

            # Save the image and text file
            with open(f"{args.output}/{categories}_{count+1}.png", "wb") as img_file, \
                    open(f"{args.output}/{categories}_{count+1}.txt", "w") as text_file:
                img_file.write(img_data)
                text_file.write(f"{categories}\n")

            count += 1
        except Exception:
            break


