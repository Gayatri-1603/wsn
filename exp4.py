import tkinter as tk
import time, threading


class Sensor:
    def __init__(self, sid, stype, value, unit, loc, protocol):
        self.sid = sid
        self.stype = stype
        self.value = value
        self.unit = unit
        self.loc = loc
        self.protocol = protocol

    def info(self):
        return f"{self.sid} | {self.stype} | {self.value}{self.unit} | {self.loc} | {self.protocol}\n"


class App:
    def __init__(self, root):
        self.nodes, self.root = [], root
        root.title("Sensor → Server Packet Simulation")

        # Input fields
        self.entries = {}

        for i, lbl in enumerate(["ID", "Type", "Value", "Unit", "Location", "PROTOCOL"]):
            tk.Label(root, text=lbl).grid(row=i, column=0, sticky="w")

            e = tk.Entry(root)
            e.grid(row=i, column=1)

            self.entries[lbl] = e

        # Press Enter after protocol input
        self.entries["PROTOCOL"].bind("<Return>", self.add_node)

        # Log window
        self.log = tk.Text(root, width=55, height=10)
        self.log.grid(row=7, column=0, columnspan=2, pady=5)

        # Drawing area
        self.canvas = tk.Canvas(root, width=700, height=250, bg="white")
        self.canvas.grid(row=8, column=0, columnspan=2)


    def add_node(self, event=None):
        try:
            s = Sensor(
                self.entries["ID"].get(),
                self.entries["Type"].get(),
                float(self.entries["Value"].get()),
                self.entries["Unit"].get(),
                self.entries["Location"].get(),
                self.entries["PROTOCOL"].get()
            )

            self.nodes.append(s)

            self.log.insert(tk.END, "Added: " + s.info())

            # Clear input fields
            for e in self.entries.values():
                e.delete(0, tk.END)

            threading.Thread(target=self.simulate, daemon=True).start()

        except:
            self.log.insert(tk.END, "❌ Invalid input!\n")


    def simulate(self):

        self.canvas.delete("all")

        n = len(self.nodes)

        if n < 1:
            return

        gap = 120


        # Draw sensor nodes
        for i, s in enumerate(self.nodes):

            x = 40 + i * gap

            # Sensor circle
            self.canvas.create_oval(
                x, 100,
                x + 50, 150,
                fill="lightblue"
            )

            # Sensor name
            self.canvas.create_text(
                x + 25,
                85,
                text=s.sid
            )

            # Connection between sensors
            if i < n - 1:
                self.canvas.create_line(
                    x + 50,
                    125,
                    x + gap,
                    125,
                    width=2
                )


        # Server position
        sx = 40 + n * gap


        # Line from last sensor to server
        last_x = 40 + (n - 1) * gap

        self.canvas.create_line(
            last_x + 50,
            125,
            sx,
            125,
            width=2
        )


        # Draw triangular server
        self.canvas.create_polygon(
            sx + 35, 70,
            sx, 150,
            sx + 70, 150,
            fill="orange",
            outline="black"
        )

        self.canvas.create_text(
            sx + 35,
            165,
            text="SERVER"
        )


        # Create packet
        pkt = self.canvas.create_oval(
            40,
            120,
            50,
            130,
            fill="red"
        )


        self.log.insert(
            tk.END,
            "▶ Packet transfer started...\n"
        )


        # Move packet through sensors and server
        for x in range(40, sx + 35, 5):

            self.canvas.coords(
                pkt,
                x,
                120,
                x + 10,
                130
            )

            time.sleep(0.03)


        for i in range(n):

            self.log.insert(
                tk.END,
                f"✔ Reached {self.nodes[i].sid}\n"
            )


        self.log.insert(
            tk.END,
            "✔ Packet delivered to SERVER\n"
        )



def main():

    root = tk.Tk()

    App(root)

    root.mainloop()



if __name__ == "__main__":
    main()