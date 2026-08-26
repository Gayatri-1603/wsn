import matplotlib.pyplot as plt
import networkx as nx
import time

# --------------------------------------
# Step 1: Build Network Topology
# --------------------------------------
G = nx.Graph()

# Devices (like PCs and Routers in Packet Tracer)
nodes = ["PC1", "PC2", "PC3", "PC4", "PC5",
         "R1", "R2", "R3", "R4", "R5"]
G.add_nodes_from(nodes)

# Links (like cables in Packet Tracer) with costs
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
    ("R1", "R5", 6),   # longer backup path
    ("R2", "R4", 4)    # alternate path
]
G.add_weighted_edges_from(edges)

# Positioning (layout)
pos = nx.spring_layout(G, seed=42)

# --------------------------------------
# Step 2: Drawing Function
# --------------------------------------
def draw_network(path=[]):
    plt.clf()
    edge_colors = []
    for u, v in G.edges():
        if (u, v) in path or (v, u) in path:
            edge_colors.append("red")  # active path
        else:
            edge_colors.append("gray")  # idle link

    nx.draw(G, pos, with_labels=True, node_size=1200,
            node_color="skyblue", font_size=10,
            font_weight="bold", edge_color=edge_colors, width=2)

    # Show link costs
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.pause(0.5)

# --------------------------------------
# Step 3: Routing (like RIP/OSPF in Packet Tracer)
# --------------------------------------
def find_route(src, dst):
    return nx.shortest_path(G, source=src, target=dst, weight="weight")

# --------------------------------------
# Step 4: Packet Simulation (like Ping in Packet Tracer)
# --------------------------------------
def send_packet(src, dst):
    path = find_route(src, dst)
    print(f"Routing from {src} to {dst}: {' -> '.join(path)}")
    for i in range(len(path)-1):
        hop = [(path[i], path[i+1])]
        draw_network(hop)
        print(f"Packet moved: {path[i]} → {path[i+1]}")
        time.sleep(1)
    print("✅ Packet delivered!\n")

# --------------------------------------
# Step 5: Run Simulation
# --------------------------------------
plt.ion()
draw_network()

# First packet transfer
send_packet("PC1", "PC3")

# Simulate cable failure (like disconnecting in Packet Tracer)
print("❌ Link R3–R4 failed!")
G.remove_edge("R3", "R4")
time.sleep(2)

# Recalculate and send packet again



draw_network()
send_packet("PC1", "PC5")

plt.ioff()
plt.show()