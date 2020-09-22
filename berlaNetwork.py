import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


# -----Load data-----
df = pd.read_csv("Contact1.csv")

# --- Create lists of unique entities.
devices = list(df.DeviceIdentifier.unique())
phoneNumber = list(df.PhoneNumber.unique())

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
    g, layout, nodelist=phoneNumber, node_color="#cccccc", node_size=50, alpha=0.5
)

common_numbers = [pNumber for pNumber in phoneNumber if g.degree(pNumber) > 1]
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
nx.draw_networkx_labels(g, layout, labels=node_labels)
nx.draw_networkx_labels(g, layout, labels=node_lables2, font_size=8)

plt.title("Linked Devices")
print(nx.info(g))
plt.savefig("output_0.png", format="png", dpi=1200)
plt.show()
