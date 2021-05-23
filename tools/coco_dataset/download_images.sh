#!/usr/bin/env bash

# Download everything
wget --directory-prefix=downloads http://images.cocodataset.org/zips/train2017.zip
wget --directory-prefix=downloads http://images.cocodataset.org/zips/val2017.zip
wget --directory-prefix=downloads http://images.cocodataset.org/annotations/annotations_trainval2017.zip

# Unpack everything
mkdir -p dataset/images
mkdir -p dataset/annotations
unzip -q downloads/train2017.zip -d dataset/images/
unzip -q downloads/val2017.zip -d dataset/images/
unzip -q downloads/annotations_trainval2017.zip -d dataset/annotations/
