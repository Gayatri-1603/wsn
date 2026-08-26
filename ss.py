import tkinter as tk
import time
import threading

def run_simulation(log_box, canvas, packet):
    # Logs for mock simulation
    logs = [
        "Logging enabled for UdpEchoClientApplication",
        "Logging enabled for UdpEchoServerApplication",
        "Created 2 nodes",
        "Point-to-Point link: DataRate=5Mbps, Delay=2ms",
        "Node0 IP: 10.1.1.1",
        "Node1 IP: 10.1.1.2",
        "Starting UDP Echo Server on Node1 at port 9 at time 1.0s",
        "Stopping server at 10.0s",
        "Starting UDP Echo Client on Node0 targeting 10.1.1.2:9",
        "MaxPackets=1, Interval=1s, PacketSize=1024 bytes",
        "Stopping client at 10.0s",
        "Animation positions set: Node0(50,105), Node1(275,105)",
        "Running simulation..."
    ]
    
    for log in logs:
        log_box.insert(tk.END, log + "\n")
        log_box.see(tk.END)
        time.sleep(0.5)
    
    # Animate packet from Node0 to Node1
    log_box.insert(tk.END, "Sending packet from Node0 → Node1\n")
    log_box.see(tk.END)
    
    for x in range(100, 250, 5):  # move packet step by step
        canvas.coords(packet, x-5, 100, x+5, 110)
        time.sleep(0.05)
    
    log_box.insert(tk.END, "Packet received at Node1 ✅\n")
    log_box.see(tk.END)
    
    # Animate echo reply back to Node0
    log_box.insert(tk.END, "Sending echo reply from Node1 → Node0\n")
    log_box.see(tk.END)
    
    for x in range(250, 100, -5):
        canvas.coords(packet, x-5, 100, x+5, 110)
        time.sleep(0.05)
    
    log_box.insert(tk.END, "Echo reply received at Node0 ✅\n")
    log_box.see(tk.END)
    
    log_box.insert(tk.END, "Simulation finished. Cleaning up...\n")
    log_box.see(tk.END)

def main():
    # GUI setup
    root = tk.Tk()
    root.title("Point-to-Point Simulation (Mock)")
    
    # Canvas for drawing nodes
    canvas = tk.Canvas(root, width=400, height=200, bg="white")
    canvas.pack(pady=10)
    
    # Draw nodes
    canvas.create_oval(50, 80, 100, 130, fill="lightblue")   # Node0
    canvas.create_oval(250, 80, 300, 130, fill="lightgreen") # Node1
    
    # Labels
    canvas.create_text(75, 70, text="Node0\n10.1.1.1")
    canvas.create_text(275, 70, text="Node1\n10.1.1.2")
    
    # Link (line between nodes)
    canvas.create_line(100, 105, 250, 105, width=2)
    
    # Packet (hidden initially)
    packet = canvas.create_oval(-10, -10, -5, -5, fill="red")
    
    # Log box
    log_box = tk.Text(root, height=12, width=55)
    log_box.pack(pady=10)
    
    # Run simulation in separate thread
    threading.Thread(target=run_simulation, args=(log_box, canvas, packet), daemon=True).start()
    
    root.mainloop()

if __name__ == "__main__":
    main()

