# Filename: sample1.py
# Python equivalent of NS-2 sample1.tcl

import time
import matplotlib.pyplot as plt


# -----------------------------
# Simulation Parameters
# -----------------------------

SIM_TIME = 10.0

AREA_X = 500
AREA_Y = 400

NUM_NODES = 2

TRACE_FILE = "sample1.tr"


# -----------------------------
# Node Class
# -----------------------------

class Node:
    def __init__(self, node_id, x, y):
        self.id = node_id
        self.x = x
        self.y = y
        self.color = "black"
        self.label = ""

    def set_color(self, color):
        self.color = color

    def set_label(self, label):
        self.label = label


# -----------------------------
# Create Nodes
# -----------------------------

node1 = Node(1, 200, 100)
node2 = Node(2, 200, 300)


node1.set_color("blue")
node1.set_label("Node1")

node2.set_color("black")
node2.set_label("Node2")


nodes = [node1, node2]


# -----------------------------
# Trace File Creation
# -----------------------------

trace = open(TRACE_FILE, "w")

trace.write("# Python Wireless Simulation Trace\n")
trace.write("# Time Node X Y Event\n")


# -----------------------------
# Simulation
# -----------------------------

print("Starting simulation...")
print("--------------------------------")

current_time = 0

while current_time <= SIM_TIME:

    for node in nodes:
        trace.write(
            f"{current_time:.2f} "
            f"Node{node.id} "
            f"{node.x} "
            f"{node.y} "
            f"ACTIVE\n"
        )

    print(
        f"Time {current_time:.2f}s : "
        f"Node1({node1.x},{node1.y}) "
        f"Node2({node2.x},{node2.y})"
    )

    current_time += 1

    time.sleep(0.1)


trace.close()


# -----------------------------
# Draw Network (NAM equivalent)
# -----------------------------

plt.figure(figsize=(6,5))

for node in nodes:

    plt.scatter(
        node.x,
        node.y,
        s=400,
        color=node.color
    )

    plt.text(
        node.x + 10,
        node.y,
        node.label,
        fontsize=12
    )


# Wireless link representation

plt.plot(
    [node1.x, node2.x],
    [node1.y, node2.y],
    linestyle="--",
    color="gray"
)


plt.xlim(0, AREA_X)
plt.ylim(0, AREA_Y)

plt.xlabel("X coordinate")
plt.ylabel("Y coordinate")

plt.title(
    "Wireless Network Simulation\n"
    "AODV - 2 Nodes"
)

plt.grid(True)

plt.savefig("sample1.png")

plt.show()


print("--------------------------------")
print("end simulation")
print("Trace file created : sample1.tr")
print("Visualization saved : sample1.png")
