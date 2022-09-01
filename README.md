<h1 align="center">
  Textmage
</h1>

<h4 align="center">
  Website for generating images from text
</h4>

![](https://i.imgur.com/pcVrK6v.jpg)

## Discription
**Textmage** is a website that generate images from text using generative model called - **DALLE**. **DALLE** is released from **OpenAI**. Here is the [paper link](https://arxiv.org/abs/2102.12092). The model was built from the [
Phil Wang](https://github.com/lucidrains) repository - [DALLE-pytorch](https://github.com/lucidrains/DALLE-pytorch).


## Install and deploy
1. Create an virtual environment using **conda** or **virtualenv**.
2. Install **requirement.txt**
    ```shell
    $ pip install -r requirements.txt
    ```
    Used package are shown [here](https://github.com/JoyPang123/Textmage/blob/main/requirements.txt).
3. Download the pretrained weight  
    Users can download the weight from [here](https://drive.google.com/file/d/1sRinsRKxKaWHhRJ3ayT60BTHDANTQuQg/view?usp=sharing). Or using `gdown` to download the file (recommend). Download file should be placed in the **root** of the project folder.
    ```shell
    $ cd Textmage
    $ gdown https://drive.google.com/uc?id=1sRinsRKxKaWHhRJ3ayT60BTHDANTQuQg
    $ unzip -q weight.zip && rm weight.zip
    ```
5. Deploy
    ```shell
    $ python app.py
    ```
    
## Dataset

> Note: Training images and text should be placed in the same folder


### COCO Dataset
To train on COCO dataset, run the following command:
```shell
$ ./tools/coco_dataset/download_images.sh
```
All the downloaded files will be placed in `tools/coco_dataset/dataset`:
```
tools/coco_dataset/dataset
|
|--train2017
|
|--val2017
|
|--annotations
```

To download text, run the `tools/coco_dataset/download_text.py`. Usage is shown below
```shell
usage: download_text.py [-h] [-c COCO] [-d DOWNLOAD] [-t IMAGE_TYPE] -p PLACE

optional arguments:
  -h, --help            show this help message and exit
  -c COCO, --coco COCO  Root dir for the coco json files
  -d DOWNLOAD, --download DOWNLOAD
                        Download the annotation files
  -t IMAGE_TYPE, --image_type IMAGE_TYPE
                        Types for the image - train and val
  -p PLACE, --place PLACE
                        Place for download files
```
For example
```shell
$ cd tool/coco_dataset
$ python download_text.py \
    --coco dataset/annotations/ \
    --downlaod false \
    --image_type train \
    --place dataset/train2017
```

### Icon
> Warning: The icon were downloaded from the [flaticon](https://www.flaticon.com). Please follow their rules to avoid any legal dispute. In our examples and our project, we only download their free icons


Users can first find the [icon packs](https://www.flaticon.com/packs) you like and copy the **url** into `tools/crawler/categories.txt` and use `,` to seperate text. For example, I downloaded cat icons and expect all the icons to be labeled to `cat`:
```
https://...,cat
```

See [categories.txt](https://github.com/JoyPang123/Textmage/blob/main/tools/crawler/categroies.txt) for more example.

Afterwards, run `tools/crawler/get-icon.py` to download the text-image pairs. Usage of `get-icon.py` is shown below
```
usage: get-icon.py [-h] -w WEBSITE -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -t TXT, --txt TXT
                        Txt file for downloading a pack of icons
  -o OUTPUT, --output OUTPUT
                        Output directory for the download
```

For instance:

```shell
$ cd tools/crawler
$ python get-icon.py \
    --txt categories.txt \
    --output dataset
```

## Training
For training custom model, please refer to the [DALLE-pytorch](https://github.com/lucidrains/DALLE-pytorch). Above dataset can be used in training.

## Demonstration
### 1. On COCO dataset
```
Two dogs are standing on the surf board
```
![](https://i.imgur.com/l578bnr.jpg)

```
Sheep is flying in the air
```
![](https://i.imgur.com/ngm244j.jpg)


> Well, our model is not good enough...

### 2. On Icon dataset
```
dog
```
![](https://i.imgur.com/JMRukj2.jpg)

```
cat
```
![](https://i.imgur.com/osC7TqS.jpg)

> It learned only on the training dataset... Because we only collect 566 icons...

What if we tried dog + cat?

```
dog cat
```
![](https://i.imgur.com/VazokKs.jpg)

> Bad thing...


## Contribution
Opening, just pull request 🤩

## Citation
```bibtex
@misc{ramesh2021zeroshot,
    title   = {Zero-Shot Text-to-Image Generation}, 
    author  = {Aditya Ramesh and Mikhail Pavlov and Gabriel Goh and Scott Gray and Chelsea Voss and Alec Radford and Mark Chen and Ilya Sutskever},
    year    = {2021},
    eprint  = {2102.12092},
    archivePrefix = {arXiv},
    primaryClass = {cs.CV}
}
```


```bibtex
@misc{radford2021learning,
      title={Learning Transferable Visual Models From Natural Language Supervision}, 
      author={Alec Radford and Jong Wook Kim and Chris Hallacy and Aditya Ramesh and Gabriel Goh and Sandhini Agarwal and Girish Sastry and Amanda Askell and Pamela Mishkin and Jack Clark and Gretchen Krueger and Ilya Sutskever},
      year={2021},
      eprint={2103.00020},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

```bibtex
@misc{esser2021taming,
    title   = {Taming Transformers for High-Resolution Image Synthesis},
    author  = {Patrick Esser and Robin Rombach and Björn Ommer},
    year    = {2021},
    eprint  = {2012.09841},
    archivePrefix = {arXiv},
    primaryClass = {cs.CV}
}
```
