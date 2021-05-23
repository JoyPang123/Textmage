import os
import logging
import zipfile
import requests
from pycocotools.coco import COCO
from tqdm import tqdm
import argparse

# Set to info level for prompting in terminal
logging.getLogger().setLevel(logging.INFO)

# Add the argument parse
arg_p = argparse.ArgumentParser()
arg_p.add_argument("-c", "--coco",
                   type=str,
                   default=".",
                   help="Root dir for the coco json files")
arg_p.add_argument("-d", "--download",
                   type=str,
                   default="false",
                   help="Download the annotation files")
arg_p.add_argument("-t", "--image_type",
                   type=str,
                   default="train",
                   help="Types for the image - train and val")
arg_p.add_argument("-p", "--place",
                   type=str,
                   required=True,
                   help="Place for download files")
args = vars(arg_p.parse_args())

# Check saving folder is exist or not
if not os.path.isdir(args["place"]):
    logging.info(f"Creating an folder for users called {args['place']}")
    os.makedirs(args["place"])

data_dir = f"{args['coco']}"

if args["download"] == "true":
    # Download json zip file
    url_json = "http://images.cocodataset.org/annotations/annotations_trainval2017.zip"
    r = requests.get(url_json, allow_redirects=True)
    open('train.zip', 'wb').write(r.content)

    # Unzip file
    with zipfile.ZipFile("train.zip", 'r') as zip_ref:
        zip_ref.extractall(data_dir)

# Coco image folder
data_type = f"{args['image_type']}2017"
image_file = f"{data_dir}/annotations/instances_{data_type}.json"
caption_file = f"{data_dir}/annotations/captions_{data_type}.json"

# Initialize COCO api for instance annotations
coco_images = COCO(image_file)
coco_captions = COCO(caption_file)

# Get images id in coco
images_ids = list(coco_images.anns.keys())

# Saving path
save_path = f"{args['place']}/"
count = 1
running_id = tqdm(images_ids, leave=False)

# Start download and saving files
for idx in running_id:
    running_id.set_description(f"Downloading text {count}", refresh=True)

    # Load image url
    img_id = coco_images.anns[idx]['image_id']
    img = coco_images.loadImgs(img_id)[0]

    # Load captions
    file_name = img["file_name"].split(".")[0]
    captions_id = coco_captions.getAnnIds(imgIds=img['id'])
    captions_list = coco_captions.loadAnns(captions_id)

    # Write the captions to file
    captions_txt = ""
    for caption in captions_list:
        captions_txt = captions_txt + caption["caption"] + "\n"
    with open(f"{save_path}/{file_name}.txt", "w") as text_file:
        text_file.write(captions_txt)

    # Increase images number
    count += 1
