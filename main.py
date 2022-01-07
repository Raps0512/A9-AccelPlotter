#!/usr/bin/env python
# -*- coding: utf-8 -*-

# created by: Raps
# updated: 7/1/2022
# title: AccelPlotter
# description: Python script to plot the acceleration of cars in the mobile racing game Asphalt 9: Legends

import os
import pandas as pd # https://pypi.org/project/pandas/

# local files
import split_frames
import remove_bg
import ocr
import txt_error
import data_visualisation

# file information
path = input("Folder path: ")
vidname = input("Video filename: ")
projname = input("Project name: ")

# create folders
projpath = os.path.join(path, projname)
os.mkdir(projpath)

framesdirpath = os.path.join(projpath, 'Frames')
os.mkdir(framesdirpath)

# split and filter video frames
frames = split_frames.split_frames(framesdirpath, vidname)

# detect and filter text with OCR
initial_text = {}
checked_text = {}
initial_errors = []
duplicate_frames = []
potential_speed_errors = []

for i in range(len(frames)): # iterate through each saved frame
    file_name = os.path.join(framesdirpath, f"frame{frames[i]}.png") # get image filename
    result = ocr.detect_text(file_name) # recognise characters
    initial_text[frames[i]] = result # save initial result

    if i != 0: # if not the first frame, complete error detection
        # if no errors were detected in the previous frame, use it for frame comparison
        if None not in checked_text[frames[i-1]] and frames[i-1] not in potential_speed_errors:
            last_checked_text = checked_text[frames[i-1]]
            frame_diff = 1
        # if errors were detected, use the last frame with no detected errors (first frame will always be accurate)
        else:
            checked_frames = sorted(list(set(frames)-set(initial_errors)-set(potential_speed_errors)-set(duplicate_frames)))
            cur_frame_index = checked_frames.index(frames[i])
            del checked_frames[cur_frame_index:]

            last_full_checked_loc = checked_frames[-1]
            last_checked_text = checked_text[last_full_checked_loc]

            frame_diff = i-frames.index(checked_frames[-1]) # get the frame increment to compare the detected speeds

        # compare the previous error-less frame with the current frame to detect errors or inconsistencies
        checked_results = txt_error.initial_check(initial_text[frames[i]], last_checked_text, frame_diff)

        # if no serious errors are detected, append to checked_text dict
        if checked_results[0] != None:
            checked_text[frames[i]] = checked_results[0]
            if checked_results[2] == True: # note if there is a speed inconsistency
                potential_speed_errors.append(frames[i])
        # note any duplicate speed frames to be removed later
        else:
            checked_text[frames[i]] = [None, None]
            duplicate_frames.append(frames[i])

        # note any serious errors
        if False in checked_results[1]:
            initial_errors.append(frames[i])
    else: # if the first frame, verify text recognition accuracy
        if input(f"\nPlease manually verify if the following information is correct regarding the first frame \nSpeed: {result[0]} \nTimestamp: {result[1]} \n(y/n) ") != "y":
            # if the text is incorrect, ask the user to input the correct information
            result[0] = input("Correct speed: ")
            result[1] = input("Correct timestamp (eg: 00:00.001): ")
        print("")
        checked_text[frames[i]] = result

    # print out frame information
    print(f"Frame: {frames[i]}")
    if frames[i] in duplicate_frames:
        print("Duplicate speed, frame skipped")
    print(f"Frame text: {checked_text[frames[i]]} \n")

# remove duplicate speed frames
for i in duplicate_frames:
    del checked_text[i]

# convert checked_text dict to Pandas DataFrame and export to Excel for human verification
df = data_visualisation.export_to_excel(checked_text)
excelpath = os.path.join(projpath, "output.xlsx")
df.to_excel(excelpath)

input(f"""
The video analysis is complete
Confirmed errors: {initial_errors}
Potential errors: {potential_speed_errors}
Removed duplicate frames: {duplicate_frames}

Please review and edit the generated spreadsheet and press ENTER to plot the data. Press Ctrl + C to stop this process
""")

# after errors are corrected, read Excel and clean data
df_reviewed = pd.read_excel(excelpath, sheet_name='Sheet1')
df_reviewed = df_reviewed.dropna()

# graph data
for index in df_reviewed.index:
    df_reviewed.loc[index, "Speed"] = int(df_reviewed.loc[index, "Speed"])
    df_reviewed.loc[index, "Timestamp"] = data_visualisation.time_convert(df_reviewed.loc[index, "Timestamp"])
data_visualisation.plot_graph(df_reviewed, projname, projpath)
