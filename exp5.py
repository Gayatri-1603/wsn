import matplotlib.pyplot as plt
import networkx as nx
import time

# --- Build the topology ---

G = nx.Graph()

# Add routers and hosts
nodes = ["SRC", "A", "B", "C", "D", "DST"]
G.add_nodes_from(nodes)

# Add links with cost (weight)
edges = [
    ("SRC", "A", 1),
    ("A", "B", 1),
    ("A", "C", 1),
    ("B", "C", 1),
    ("C", "D", 10),   # high cost link
    ("B", "D", 1),
    ("D", "DST", 1)
]

G.add_weighted_edges_from(edges)

# Positioning for visualization
pos = nx.spring_layout(G, seed=42)


# --- Draw network ---

def draw_network(highlight_path=[]):
    plt.clf()

    edge_colors = []

    for u, v in G.edges():
        if (u, v) in highlight_path or (v, u) in highlight_path:
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

    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels
    )

    plt.pause(0.5)


# --- RIP-like routing: shortest path by edge weights ---

def rip_route(src, dst):
    return nx.shortest_path(
        G,
        source=src,
        target=dst,
        weight="weight"
    )


# --- Simulate ping packets ---

def simulate_ping():
    path = rip_route("SRC", "DST")

    print(f"Ping route chosen: {' -> '.join(path)}")

    for i in range(len(path) - 1):
        hop = [(path[i], path[i + 1])]

        draw_network(hop)

        print(
            f"Packet moved {path[i]} → {path[i + 1]}"
        )

        time.sleep(1)

    print("✅ Echo Reply received back at SRC")


# --- Link failure simulation ---

def fail_link(u, v):
    if G.has_edge(u, v):
        G.remove_edge(u, v)
        print(f"❌ Link {u}–{v} failed!")


# --- Run simulation ---

plt.ion()

# Initial network
draw_network()

# First ping
simulate_ping()

time.sleep(3)

# Fail B-D link
fail_link("B", "D")

# Display network after failure
draw_network()

time.sleep(3)

# Ping again after link failure
simulate_ping()

plt.ioff()
plt.show()