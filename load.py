import Tkinter as tk
import sys
import time

this = sys.modules[__name__]  # For holding module globals

try:
    from config import config
except ImportError:
    print(ImportError)
    config = dict()


CFG_CARGO = "Cargo_total"
CFG_INVENTORY = "Cargo_inventory"


class Cargo(object):
    speed_widget = None
    rate_widget = None
    dist_widget = None
    total_cargo = int(config.get(CFG_CARGO))
    inventory = {}

    def show_total(self):
        msg = "{0:.2f} Tons".format(self.total_cargo)
        self.total_widget.after(0, self.total_widget.config, {"text": msg})
    
    def set_cargo(self, inventory):
        self.inventory = inventory
        msg = ""
        for item in inventory:
            msg = msg + "{0}: {1} \n".format(item['Name'],item['Count'])
        self.current_widget.after(0, self.current_widget.config, {"text": msg})
    
    def load_cargo(self, cargo_name, count):
        self.total_cargo = self.total_cargo + count
        config.set(CFG_CARGO, str(self.total_cargo))
        self.show_total()
    
    def load(self):
        saved = config.get(CFG_CARGO)
        if not saved:
            self.saved_total = 0
        else:
            self.saved_total = float(saved)

        # inv = config.get(CFG_INVENTORY)
        # if inv:
        #     self.inventory = inv
        
    def save(self):
        config.set(CFG_INVENTORY, self.inventory)

    # def unload_cargo(self, cargo_name, count):
    #     haul = self.haul
       
    #     if cargo_name in haul:
    #         haul[cargo_name] = haul[cargo_name] - count

    #         if haul[cargo_name] <= 0:
    #             del haul[cargo_name]

    #     msg = ""
    #     for item in haul:
    #         msg = msg + "{0}: {1} \n".format(item,haul[item])
    #     self.current_widget.after(0, self.current_widget.config, {"text": msg})


def plugin_start(plugin_dir):
    cargo = Cargo()
    cargo.load()
    this.cargo = cargo

def plugin_stop():
    cargo = Cargo()


def plugin_app(parent):
    """
    Create a pair of TK widgets for the EDMC main window
    """
    cargo = this.cargo

    frame = tk.Frame(parent)

    cargo.total_widget = tk.Label(
        frame,
        text="...",
        justify=tk.RIGHT)
    total_label = tk.Label(frame, text="Total Hauled:", justify=tk.LEFT)
    total_label.grid(row=0, column=0, sticky=tk.W)
    cargo.total_widget.grid(row=0, column=2, sticky=tk.E)

    cargo.current_widget = tk.Label(
        frame,
        text="...",
        justify=tk.RIGHT)
    current_label = tk.Label(frame, text="Current Cargo:", justify=tk.LEFT)
    current_label.grid(row=1, column=0, sticky=tk.W)
    cargo.current_widget.grid(row=1, column=2, sticky=tk.E)

    cargo.show_total()
    cargo.set_cargo(cargo.inventory)
    cargo.save()
    return frame

def journal_entry(cmdr, system, station, entry, state):
    if "event" in entry:
        if "MarketBuy" in entry["event"]:
            this.cargo.load_cargo(entry['Type'],entry['Count'])
        # if "MarketSell" in entry["event"]:
        #     this.cargo.unload_cargo(entry['Type'],entry['Count'])
        if "Cargo" in entry["event"]:
