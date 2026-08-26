import matplotlib.pyplot as plt
import networkx as nx
import time
import random

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
def draw_network(highlight_path=[], failed_links=[]):
    plt.clf()
    edge_colors = []
    edge_styles = []

    for u, v in G.edges():
        if (u, v) in highlight_path or (v, u) in highlight_path:
            edge_colors.append("red")
            edge_styles.append("solid")
        elif (u, v) in failed_links or (v, u) in failed_links:
            edge_colors.append("black")
            edge_styles.append("dashed")
        else:
            edge_colors.append("gray")
            edge_styles.append("solid")

    nx.draw(
        G, pos,
        with_labels=True,
        node_size=1500,
        node_color="skyblue",
        font_size=10,
        font_weight="bold",
        edge_color=edge_colors,
        width=2,
        style=edge_styles
    )

    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.pause(0.5)

# --- RIP-like routing: shortest path by edge weights ---
def rip_route(src, dst):
    try:
        return nx.shortest_path(G, source=src, target=dst, weight="weight")
    except nx.NetworkXNoPath:
        print("❌ No available path from SRC to DST")
        return []

# --- Simulate ping packets with packet loss ---
def simulate_ping(loss_prob=0.2):
    path = rip_route("SRC", "DST")
    if not path:
        return

    print(f"Ping route chosen: {' -> '.join(path)}")
    for i in range(len(path) - 1):
        hop = [(path[i], path[i + 1])]
        draw_network(hop)

        if random.random() < loss_prob:
            print(f"💥 Packet lost at {path[i]} → {path[i+1]}")
            return

        print(f"Packet moved {path[i]} → {path[i+1]}")
        time.sleep(1)

    print("✅ Echo Reply received back at SRC")

# --- Link failure simulation ---
failed_links = []

def fail_link(u, v):
    if G.has_edge(u, v):
        G.remove_edge(u, v)
        failed_links.append((u, v))
        print(f"❌ Link {u}–{v} failed!")

def recover_link(u, v, cost=1):
    if (u, v) in failed_links or (v, u) in failed_links:
        G.add_edge(u, v, weight=cost)
        failed_links.remove((u, v))
        print(f"🔄 Link {u}–{v} recovered with cost {cost}")

# --- Dynamic link cost fluctuation ---
def fluctuate_link_cost(u, v):
    if G.has_edge(u, v):
        new_cost = random.randint(1, 15)
        G[u][v]['weight'] = new_cost
        print(f"⚡ Link {u}-{v} cost updated to {new_cost}")

# --- Run simulation ---
plt.ion()

# Initial network
draw_network()

# First ping
simulate_ping()

time.sleep(3)

# Fail B-D link
fail_link("B", "D")
draw_network(failed_links=failed_links)

time.sleep(3)

# Ping again after link failure
simulate_ping()

time.sleep(3)

# Fluctuate link costs
fluctuate_link_cost("A", "C")
fluctuate_link_cost("C", "D")
draw_network(failed_links=failed_links)

time.sleep(3)

# Recover B-D link
recover_link("B", "D", cost=2)
draw_network()

time.sleep(3)

# Ping again after recovery
simulate_ping()

plt.ioff()
plt.show()