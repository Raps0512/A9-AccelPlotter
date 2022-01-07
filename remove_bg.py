#!/usr/bin/env python
# -*- coding: utf-8 -*-

# created by: Raps
# updated: 7/1/2022
# title: AccelPlotter remove_bg module
# description: remove backgrounds of individual images

# adapted from https://stackoverflow.com/a/63003020

import cv2 # https://pypi.org/project/opencv-python/
import numpy as np # https://pypi.org/project/numpy/

# convert background to black
def black_bg(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to graky
    mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)[1] # threshold input image as mask

    # apply morphology to remove isolated extraneous noise
    # use borderconstant of black since foreground touches the edges
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # anti-alias the mask -- blur then stretch
    # blur alpha channel
    mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)

    # linear stretch so that 127.5 goes to 0, but 255 stays 255
    mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

    return mask

# convert background to transparent
def remove_bg(img):
    mask = black_bg(img) # get image mask

    # put mask into alpha channel
    result = img.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask

    return result
