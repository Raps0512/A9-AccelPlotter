#!/usr/bin/env python
# -*- coding: utf-8 -*-

# created by: Raps
# updated: 7/1/2022
# title: AccelPlotter data_visualisation module
# description: format text and graph data

import os
from datetime import datetime, timedelta
import pandas as pd # https://pypi.org/project/pandas/
import matplotlib.pyplot as plt # https://pypi.org/project/matplotlib/

# format time text and convert to float
def time_convert(time_str):
    # convert to datetime object
    time_str_formatted = f"{time_str}000"
    time_datetime = datetime.strptime(time_str_formatted,'%M:%S.%f') - datetime(1900,1,1)
    time_datetime_ms = time_datetime // timedelta(milliseconds=1)

    # convert to milliseconds
    time_int = int(time_datetime_ms)
    time_float = time_int / 1000
    return time_float

# export data to Excel
def export_to_excel(checked_text):
    df = pd.DataFrame(data=checked_text)
    df_formatted = df.T # invert DataFrame axes
    df_formatted.columns = ["Speed", "Timestamp"]
    df_formatted.index.name = "Frame"
    return df_formatted

# plot graph
def plot_graph(df, projname, projpath):
    df.plot(x="Timestamp", y="Speed")
    plt.title(projname)
    plt.xlabel('Time (s)')
    plt.ylabel('Speed (km/h)')
    plt.savefig(os.path.join(projpath, "output.png"))
