#!/usr/bin/env python
# -*- coding: utf-8 -*-

# created by: Raps
# updated: 7/1/2022
# title: AccelPlotter txt_error module
# description: detect any OCR recognition errors or inconsistencies

def initial_check(result, old_result, frame_diff):
    duplicate_speed = False
    checks = [False, False] # speedometer and timer text checks
    potential_speed_error = False

    # search for potential timestamps
    timestamp_loc = []
    for i in range(len(result)):
        if ":" in result[i] and "." in result[i] and len(result[i]) == 9:
            timestamp_loc.append(i)

    # save timestamp if only one is detected
    if len(timestamp_loc) == 1:
        timestamp = result.pop(timestamp_loc[0])
        checks[1] = True
    # recognition error if more than one timestamps are detected
    else:
        timestamp = None

    old_speed = int(old_result[0])
    # if only one potential speed is detected
    if len(result) == 1 and result[0].isdigit():
        speed = result[0]
        checks[0] = True

        speed_difference = abs(int(speed)-old_speed)
        # # check if the speed is the same as the previous error-less frame
        if speed_difference == 0:
            duplicate_speed = True
        # check if the speed is inconsistent with the previous error-less frame
        elif speed_difference > frame_diff+1:
            potential_speed_error = True

    # if more than one potential speed is detected
    elif len(result) > 1:
        speed_differences = []
        # find the closest speed to the previous error-less frame
        for i in result:
            if i.isdigit():
                speed_differences.append(abs(int(i) - old_speed))
            else:
                speed_differences.append(None)
        ideal_speed_dif = min(x for x in speed_differences if x is not None)
        speed = result[speed_differences.index(ideal_speed_dif)]
        checks[0] = True

        # check if the speed is the same or inconsistent
        if ideal_speed_dif == 0:
            duplicate_speed = True
        elif ideal_speed_dif > 2:
            potential_speed_error = True

    # if no speed text is detected
    else:
        speed = None

    # format result and return to main.py
    if duplicate_speed == False:
        check_result = ([speed, timestamp], checks, potential_speed_error)
    else:
        check_result = (None, [True, True], False)

    return check_result
