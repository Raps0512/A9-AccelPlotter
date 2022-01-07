#!/usr/bin/env python
# -*- coding: utf-8 -*-

# created by: Raps
# updated: 7/1/2022
# title: AccelPlotter ocr module
# description: detect speed and time text from images with OCR

# adapted from https://cloud.google.com/vision/docs/ocr

import io
import re
from google.cloud import vision # https://pypi.org/project/google-cloud/

client = vision.ImageAnnotatorClient() # OCR instance

def detect_text(path):
    # open image file
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    # read image file and recognise characters
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # parse text and remove a-Z characters, in particular to remove "KM/H"
    RESULT = []
    for i in range(len(texts)):
        texts[i].description = re.sub(r'[^0-9:.]','',texts[i].description)
        if len(texts[i].description) != 0:
            RESULT.append(texts[i].description)
    del RESULT[0]

    # return OCR result
    return(RESULT)

    # OCR error
    if response.error.message:
        raise Exception(response.error.message)
