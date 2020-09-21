###################
# imports data from CSV files output from BERLA iVE
# Outputs files for contact, calls and SMS data
# Device name and details added to contact, call and SMS files
# for easier analysis
# timestamps normalised
####################

# Formatted with Black


import os
import pandas as pd
import tqdm

print("Berla format conversion\n")

# --- Functions---


def timeConversion(inputPD):
    z = inputPD.keys().tolist()
    if "StartTime" in z:
        inputPD.rename(columns={"StartTime": "Orig_Timestamp"}, inplace=True)
        inputPD["StartTime"] = pd.to_datetime(
            inputPD["Orig_Timestamp"], errors="ignore", format="%m/%d/%Y %I:%M:%S.%f %p"
        )
        return inputPD

    elif "DateTime" in z:
        inputPD.rename(columns={"DateTime": "Orig_Timestamp"}, inplace=True)

        inputPD["DateTime"] = pd.to_datetime(
            inputPD["Orig_Timestamp"], errors="ignore", format="%m/%d/%Y %I:%M:%S.%f %p"
        )
        return inputPD

    else:
        print("else")
        raise invalidFile("Invalid input file")


class invalidFile(Exception):
    pass


# --- Import Files----
fileList = os.listdir(os.getcwd())

for x in tqdm.tqdm(fileList, desc="Loading files"):
    if x.endswith("Contact.csv"):
        contactPD = pd.read_csv(x)

    elif x.endswith("Attached Device.csv"):
        devicePD = pd.read_csv(x)

    elif x.endswith("Call Log.csv"):
        callLogPD = pd.read_csv(x)

    elif x.endswith("SMS.csv"):
        smsPD = pd.read_csv(x)

    else:
        pass

outputFiles = []


# ----Format Contacts---
try:
    contactConvert = pd.merge(
        devicePD,
        contactPD,
        left_on=["UniqueNumber"],
        right_on=["DeviceIdentifier"],
        how="inner",
    )
    contactConvert = contactConvert[
        [
            "UniqueString_x",
            "DeviceName",
            "DeviceIdentifier",
            "DeviceType",
            "Manufacturer",
            "Model",
            "UniqueString_y",
            "FirstName",
            "LastName",
            "Company",
            "PhoneNumber",
            "WorkNumber",
            "HomeNumber",
            "MobileNumber",
            "Email",
        ]
    ]
    outputFiles.append([contactConvert, "contactConvert"])
except:
    pass

# -----Format calls----
try:
    callConvert = pd.merge(
        devicePD,
        callLogPD,
        left_on=["UniqueNumber"],
        right_on=["DeviceIdentifier"],
        how="inner",
    )
    callConvert = timeConversion(callConvert)
    callConvert = callConvert[
        [
            "UniqueString_x",
            "DeviceName",
            "DeviceIdentifier",
            "DeviceType",
            "UniqueString_y",
            "OffsetApplied_x",
            "StartTime",
            "Orig_Timestamp",
            "PhoneNumber",
            "ContactName",
            "FlagsString_y",
            "TimestampType_y",
        ]
    ]
    outputFiles.append([callConvert, "callConvert"])
except:
    pass

# ---Format SMS messages-----
try:
    smsConvert = pd.merge(
        devicePD,
        smsPD,
        left_on=["UniqueNumber"],
        right_on=["DeviceIdentifier"],
        how="inner",
    )
    smsConvert = timeConversion(smsConvert)
    smsConvert = smsConvert[
        [
            "UniqueString_x",
            "DeviceName",
            "DeviceType",
            "UniqueNumber",
            "Manufacturer",
            "InterfaceType",
            "OffsetApplied_x",
            "Orig_Timestamp",
            "DateTime",
            "To",
            "From",
            "Name",
            "Body",
            "ReadStatus",
            "UniqueString_y",
            "TimestampType_y",
            "TimestampConfidence_y",
            "NetOffset_y",
        ]
    ]
    smsConvert.rename(columns={"UniqueString_y": "UniqueString_SMS"}, inplace=True)
    outputFiles.append([smsConvert, "smsConvert"])

except:
    pass


# Write out CSV files.
for x in tqdm.tqdm(outputFiles, desc="Writing files"):
    x[0].to_csv("%s.csv" % x[1], index=False, date_format="%Y/%m/%d %H:%M:%S")

print("\nComplete")
