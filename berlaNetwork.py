"""
facelessg00n 2020
Made in Australia

Relational analysis tool for files output by Berla iVe
Determines if phone numbers are common between devices allowing relationships between devices to be quickly analysed.

"""

import os
import tqdm
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


# ----Demo Mode----
# Loads a sample dataset for testing.
demo_mode = True
demo_file = "Contact1.csv"


# -----Load data-----
if demo_mode:
    df = pd.read_csv(demo_file)

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
        df = contactConvert
    except:
        pass


# --- Create lists of unique entities.
devices = list(df.DeviceIdentifier.unique())
phoneNumbers = list(df.PhoneNumber.unique())

# ---- Draw relationship chart----
g = nx.from_pandas_edgelist(df, source="DeviceIdentifier", target="PhoneNumber")
contact_size = [g.degree(device) * 10 for device in devices]
layout = nx.spring_layout(g, iterations=200)

nx.draw_networkx_nodes(
    g,
    layout,
    nodelist=devices,
    node_size=contact_size,  # nodes with more contacts are larger
    node_color="lightblue",
)

nx.draw_networkx_nodes(
    g, layout, nodelist=phoneNumbers, node_color="#79787a", node_size=50, alpha=0.5
)

common_numbers = [pNumber for pNumber in phoneNumbers if g.degree(pNumber) > 1]
nx.draw_networkx_nodes(
    g, layout, nodelist=common_numbers, node_color="orange", node_size=100
)

print("Numbers shared between devices are, {}".format(common_numbers))
print(common_numbers)
nx.draw_networkx_edges(g, layout, width=1, edge_color="#cccccc", alpha=0.5)

# Create dict pairs for the labels
node_labels = dict(zip(devices, devices))
node_lables2 = dict(zip(common_numbers, common_numbers))

# draw lables on Device and common number nodes
nx.draw_networkx_labels(g, layout, labels=node_labels, font_weight="bold")
nx.draw_networkx_labels(g, layout, labels=node_lables2, font_size=8)

plt.title("Linked Devices")
print(nx.info(g))
# plt.savefig("output_0.png", format="png", dpi=1200)
plt.show()
