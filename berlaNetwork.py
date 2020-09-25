"""
facelessg00n 2020
Made in Australia

Relational analysis tool for files output by Berla iVe
Determines if phone numbers are common between devices allowing relationships between devices to be quickly analysed.

Formatted with Black
"""
# TODO - Clean up phone numbers for better matching. i.e country codes etc.

import os
import tqdm
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# ------------------------Settings---------------------------------------------
# Demo Mode
# Loads the sample dataset for testing.
demo_mode = True
demo_file = "samples/Contact1.csv"

# ---- Do we want to filter out common numbers
filters_on = True

# Save image to working directory
save_image = False

# Draw clean chart with only common entities
simple_chart = True


# Data to ignore
# Common phone numbers
ignoreNumbers = [
    "101",
    "000",
    "1234",
    "1800737732",
    "1800551800",
    "911",
    "1223",
    "124937",
    "555",
    "321",
    "",
    "#101#",
    "555",
    "321",
    "NaN",
]


# -----------------------Load data--------------------------------------------
if demo_mode:
    df = pd.read_csv(demo_file)
    # if Phone number field is blank bring in number from Mobile Number or home number column
    df.loc[df["PhoneNumber"].isnull(), "PhoneNumber"] = df["MobileNumber"]
    df.loc[df["PhoneNumber"].isnull(), "PhoneNumber"] = df["HomeNumber"]
    # Remove blank rows
    df.dropna(subset=["PhoneNumber"], inplace=True)
    # if device name is missing use device identifier.
    df.loc[df["DeviceName"].isnull(), "DeviceName"] = df["DeviceIdentifier"]


else:
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
        
        # if Phone number field is blank bring in number from Mobile Number or home number column
        contactConvert.loc[
            contactConvert["PhoneNumber"].isnull(), "PhoneNumber"
        ] = contactConvert["MobileNumber"]
        contactConvert.loc[
            contactConvert["PhoneNumber"].isnull(), "PhoneNumber"
        ] = contactConvert["HomeNumber"]
        # Remove blank rows
        contactConvert.dropna(subset=["PhoneNumber"], inplace=True)
        # if device name is missing use device identifier.
        contactConvert.loc[
            contactConvert["DeviceName"].isnull(), "DeviceName"
        ] = contactConvert["DeviceIdentifier"]
        df = contactConvert
        # print(df)

    except:
        pass


# ---- Filter out common numbers to reduce false positives
if filters_on:
    filtered_frame = ~df.PhoneNumber.isin(ignoreNumbers)
    df = df[filtered_frame]


# --- Create lists of unique entities.
devices = list(df.DeviceName.unique())
phoneNumbers = list(df.PhoneNumber.unique())

print("Drawing chart")
# -----------------------Draw relationship chart-----------------------------
g = nx.from_pandas_edgelist(df, source="DeviceName", target="PhoneNumber")
common_numbers = [pNumber for pNumber in phoneNumbers if g.degree(pNumber) > 1]
# Extract connected numbers for simple chart
filtered_frame2 = df.PhoneNumber.isin(common_numbers)
df1 = df[filtered_frame2]
# contactConvert.to_csv("frame1.csv")


if not simple_chart:
    contact_size = [g.degree(device) * 10 for device in devices]
    layout = nx.spring_layout(g, iterations=20, scale=0.2)
    plt.figure(figsize=(24, 12), facecolor="whitesmoke", tight_layout=True)

    # Draw the device nodes
    nx.draw_networkx_nodes(
        g,
        layout,
        nodelist=devices,
        node_size=contact_size,  # nodes with more contacts are larger
        node_color="lightblue",
    )

    # Draw on all nodes
    nx.draw_networkx_nodes(
        g, layout, nodelist=phoneNumbers, node_color="#79787a", node_size=50, alpha=0.5
    )

    # Draw nodes for numbers common beyween devices
    nx.draw_networkx_nodes(
        g, layout, nodelist=common_numbers, node_color="orange", node_size=100
    )

    # Draw links
    nx.draw_networkx_edges(g, layout, width=1, edge_color="#cccccc", alpha=0.7)

    # Create dict pairs for the labels
    device_labels = dict(zip(devices, devices))
    common_numbers_labels = dict(zip(common_numbers, common_numbers))

    # Draw lables on Device and common number nodes
    nx.draw_networkx_labels(g, layout, labels=device_labels, font_weight="bold")
    nx.draw_networkx_labels(g, layout, labels=common_numbers_labels, font_size=8)
    # Add title to plot.
    plt.title(
        "Linked Devices - Filters= {}".format(str(filters_on)),
        loc="left",
        fontweight="heavy",
        fontsize=24,
        alpha=0.8,
        fontvariant="small-caps",
    )
    print(nx.info(g))
    if save_image:
        plt.savefig("output_0.png", format="png", dpi=1200)

    plt.axis("off")
    print("Numbers shared between devices are, {}".format(common_numbers))

    plt.show()
# TODO Could this be a function ?
# --------------------------------------------------------------------------------------
if simple_chart:
    gg = nx.from_pandas_edgelist(df1, source="DeviceName", target="PhoneNumber")
    # make new device list from filtered frame to prevent errors when extra devices found.
    devices = df1["DeviceName"].tolist()

    # contact_size = [gg.degree(device) * 10 for device in devices]
    contact_size = 800
    layout = nx.spring_layout(gg, iterations=20)
    plt.figure(figsize=(24, 12), facecolor="white", tight_layout=True)

    # Draw the device nodes

    nx.draw_networkx_nodes(
        gg,
        layout,
        nodelist=devices,
        node_size=contact_size,  # nodes with more contacts are larger
        node_color="lightblue",
    )

    # Draw nodes for numbers common between devices
    nx.draw_networkx_nodes(
        gg, layout, nodelist=common_numbers, node_color="orange", node_size=100
    )

    # Draw links

    nx.draw_networkx_edges(gg, layout, width=1, edge_color="#cccccc", alpha=0.7)

    # Create dict pairs for the labels
    device_labels = dict(zip(devices, devices))
    common_numbers_labels = dict(zip(common_numbers, common_numbers))

    # Draw lables on Device and common number nodes
    nx.draw_networkx_labels(gg, layout, labels=device_labels, font_weight="bold")
    nx.draw_networkx_labels(gg, layout, labels=common_numbers_labels, font_size=8)

    plt.title(
        "Linked Devices - Clean - Filters= {}".format(str(filters_on)),
        loc="left",
        fontweight="heavy",
        fontsize=24,
        alpha=0.8,
        fontvariant="small-caps",
    )
    plt.show()
    print("Finalised and closing")
