#!/usr/bin/env python
# -*- coding: utf-8 -*-

# created by: Raps
# updated: 7/1/2022
# title: AccelPlotter split_frames module
# description: split and filter video frames

# adapted from https://stackoverflow.com/a/33399711

import os
import cv2 # https://pypi.org/project/opencv-python/
import imagehash # https://pypi.org/project/ImageHash/
from PIL import Image # https://pypi.org/project/Pillow/

import remove_bg # local file to remove image backgrounds

# crop and save speed and time image
def full_crop(image, count, projpath):
    full_crop = image[20:182, 1587:1818] # speedometer and time counter area
    full_filtered = remove_bg.black_bg(full_crop) # remove background
    cv2.imwrite(os.path.join(f"{projpath}/", "frame%d.png" % count), full_filtered)

# split video frames and filter out same speed frames
def split_frames(projpath, vidname):
    # read video
    vidcap = cv2.VideoCapture(vidname)
    success,image = vidcap.read()

    count = 0 # frame count
    cutoff = 2 # image difference threshold
    frames = [] # list of saved frame ids

    while success: # iterate through each video frame
        success,image = vidcap.read()

        if count % 5 == 0: # iterate through every 5th frame to increase efficiency; more information: https://stackoverflow.com/a/22706622
            image = cv2.resize(image, (1920, 886), interpolation=cv2.INTER_LINEAR) # resize image to fit crop parameters
            speed_crop = image[18:118, 1587:1818] # speedometer area

            # if not the first frame, save the previous frame for comparison
            if count != 0:
                prev_filtered = speed_filtered

            speed_filtered = remove_bg.black_bg(speed_crop) # remove speedometer background

            # save the first frame
            if count == 0:
                full_crop(image, count, projpath)
                frames.append(count)
            # if not the first frame, compare previous speedometer and current speedometer images to detect speed change
            else:
                img1 = Image.fromarray(prev_filtered)
                img2 = Image.fromarray(speed_filtered)

                # get the image hash of the speedometer frames
                hash0 = imagehash.average_hash(img1)
                hash1 = imagehash.average_hash(img2)

                # if the speed is the same, discard the frame
                if hash0 - hash1 < cutoff:
                    print('images are similar', count, hash0 - hash1)
                # if the speed has changed, save the new frame
                else:
                    print('images are not similar', count, hash0 - hash1)
                    full_crop(image, count, projpath)
                    frames.append(count)

        count += 1 # frame count
    return frames # return list of frame ids for OCR
