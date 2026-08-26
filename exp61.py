import matplotlib.pyplot as plt
import networkx as nx
import time

# --------------------------------------
# Step 1: Build Network Topology
# --------------------------------------

G = nx.Graph()

nodes = [
    "PC1", "PC2", "PC3", "PC4", "PC5",
    "R1", "R2", "R3", "R4", "R5"
]

G.add_nodes_from(nodes)

edges = [
    ("PC1", "R1", 1),
    ("PC2", "R2", 1),
    ("PC3", "R3", 1),
    ("PC4", "R4", 1),
    ("PC5", "R5", 1),

    ("R1", "R2", 2),
    ("R2", "R3", 2),
    ("R3", "R4", 2),
    ("R4", "R5", 2),

    ("R1", "R5", 6),
    ("R2", "R4", 4)
]

G.add_weighted_edges_from(edges)

# Fixed position so network does NOT move/scramble
pos = {
    "PC1": (-3, 1),
    "R1": (-2, 1),
    "R2": (-1, 1),
    "R3": (0, 1),
    "R4": (1, 1),
    "R5": (2, 1),
    "PC5": (3, 1),

    "PC2": (-1, 0),
    "PC3": (0, 0),
    "PC4": (1, 0)
}

# Failed routers
failed_nodes = set()


# --------------------------------------
# Step 2: Draw Network
# --------------------------------------

def draw_network(path=[]):

    plt.clf()

    # Draw all edges
    edge_colors = []

    for u, v in G.edges():

        if u in failed_nodes or v in failed_nodes:
            edge_colors.append("black")

        elif (u, v) in path or (v, u) in path:
            edge_colors.append("red")

        else:
            edge_colors.append("gray")

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=1500,
        node_color="skyblue",
        font_size=10,
        font_weight="bold",
        edge_color=edge_colors,
        width=2
    )

    # Draw failed routers in RED
    if failed_nodes:

        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=list(failed_nodes),
            node_color="red",
            node_size=1500
        )

    # Show link costs
    edge_labels = nx.get_edge_attributes(G, "weight")

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels
    )

    plt.pause(0.5)


# --------------------------------------
# Step 3: Find Route
# --------------------------------------

def find_route(src, dst):

    # Create temporary graph
    H = G.copy()

    # Remove failed routers ONLY for routing calculation
    H.remove_nodes_from(failed_nodes)

    return nx.shortest_path(
        H,
        source=src,
        target=dst,
        weight="weight"
    )


# --------------------------------------
# Step 4: Send Packet
# --------------------------------------

def send_packet(src, dst):

    try:

        path = find_route(src, dst)

        print(
            f"\nRouting from {src} to {dst}: "
            f"{' -> '.join(path)}"
        )

        for i in range(len(path) - 1):

            hop = [(path[i], path[i + 1])]

            draw_network(hop)

            print(
                f"Packet moved: "
                f"{path[i]} → {path[i + 1]}"
            )

            time.sleep(1)

        print("✅ Packet delivered!\n")

    except nx.NetworkXNoPath:

        print(
            f"❌ No route available from {src} to {dst}"
        )


# --------------------------------------
# Step 5: Start Simulation
# --------------------------------------

plt.ion()

draw_network()

# ======================================
# FIRST PACKET
# PC1 → PC3
# ======================================

print("\n==============================")
print(" FIRST PACKET: PC1 → PC3")
print("==============================")

send_packet("PC1", "PC3")


# ======================================
# FAIL R2 AND R4
# ======================================

print("\n❌ R2 FAILED!")
failed_nodes.add("R2")

print("❌ R4 FAILED!")
failed_nodes.add("R4")

time.sleep(2)

draw_network()


# ======================================
# SECOND PACKET
# PC1 → PC5
# ======================================

print("\n==============================")
print(" SECOND PACKET: PC1 → PC5")
print("==============================")

send_packet("PC1", "PC5")


# --------------------------------------
# End
# --------------------------------------

plt.ioff()
plt.show()