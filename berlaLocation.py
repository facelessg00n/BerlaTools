"""
facelessg00n 2020
Made in Australia

Normalises Berla time data to allow use with other analysis platforms.
Also outputs a second set of CSV files with blank values dropped i.e only events / points with a
timestamp are shown.

Time format is compatible with software such as IBM i2 and ESRI Arc GIS
"""

# TODO - Work in progress. Needs some more testing.
# TODO - Tidy up  events export columns


import os
import pandas as pd
import tqdm

# More decimal places
pd.set_option("display.precision", 8)

fileList = os.listdir(os.getcwd())

for x in tqdm.tqdm(fileList, desc="Loading data from files in directory"):

    if x.endswith("Trackpoint.csv"):
        trackpointPD = pd.read_csv(x)
        trackPointFilename = x.split(".")[0]

    elif x.endswith("Event.csv"):
        eventPD = pd.read_csv(x)
        eventFilename = x.split(".")[0]
    else:
        pass

# Fix timestamps in trackpoint data
# Formatted dates and times are in the DateTime column which ARC GIS searches for.
try:
    trackpointPD.rename(columns={"DateTime": "Orig_Timestamp"}, inplace=True)
    trackpointPD["DateTime"] = pd.to_datetime(
        trackpointPD["Orig_Timestamp"],
        errors="ignore",
        format="%m/%d/%Y %I:%M:%S.%f %p",
    )

    trackpointPD = trackpointPD[
        [
            "Longitude",
            "Latitude",
            "Orig_Timestamp",
            "DateTime",
            "strSpeed",
            "TrackName",
            "UniqueString",
            "TimestampType",
            "TimestampConfidence",
            "TimestampConfidenceString",
            "NetOffset",
            "NetOffsetDisplayString",
            "OffsetsAppliedDisplayString",
            "OffsetApplied",
        ]
    ]
    # Generate second dataframe with only points with time data
    trackpointTimePD = trackpointPD.copy()
    trackpointTimePD.dropna(subset=["DateTime"], inplace=True)

except NameError:
    print("\nTrackPoint CSV not loaded. File must end in Trackpoint.csv to be loaded\n")
    pass
except:
    pass


# Fix timestamps in events data.
# Formatted dates and times are in the DateTime column which ARC GIS searches for.

try:
    eventPD.rename(columns={"DateTime": "Orig_Timestamp"}, inplace=True)
    eventPD["DateTime"] = pd.to_datetime(
        eventPD["Orig_Timestamp"],
        errors="ignore",
        format="%m/%d/%Y %I:%M:%S.%f %p",
    )
    # Generate second dataframe with only points with time data
    eventTimePD = eventPD.copy()
    eventTimePD.dropna(subset=["DateTime"], inplace=True)


except NameError:
    print("\nEvent CSV not loaded. File must end in Event.csv to be loaded\n")
    pass

except:
    pass

# ------Export Files-----------------------------------------------------------------

print("Writing output files.\n")
try:
    trackpointPD.to_csv(
        trackPointFilename + "_All.csv", index=False, date_format="%Y/%m/%d %H:%M:%S"
    )
    trackpointTimePD.to_csv(
        trackPointFilename + "_Time.csv", index=False, date_format="%Y/%m/%d %H:%M:%S"
    )
except:
    pass

try:
    eventPD.to_csv(
        eventFilename + "_All.csv", index=False, date_format="%Y/%m/%d %H:%M:%S"
    )
    eventTimePD.to_csv(
        eventFilename + "_Time.csv", index=False, date_format="%Y/%m/%d %H:%M:%S"
    )
except:
    pass
