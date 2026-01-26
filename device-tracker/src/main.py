import tkinter as tk
from tkinter import ttk
from device_tracker import DeviceTracker
import asyncio
from threading import Thread

'''
A simplified desktop application to display a list of connected devices and their information.
'''
class DeviceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Device Tracker")
        self.device_tracker = DeviceTracker()

        self.device_list_frame = ttk.Frame(root, padding=10)
        self.device_list_frame.pack(fill='both', expand=True)

        self.title_label = ttk.Label(self.device_list_frame, text="Connected Devices", font=("Arial", 16))
        self.title_label.pack(pady=10)

        self.device_tree = ttk.Treeview(self.device_list_frame, columns=("Name", "Battery", "Plugged"), show="headings")
        self.device_tree.heading("Name", text="Device Name")
        self.device_tree.heading("Battery", text="Battery (%)")
        self.device_tree.heading("Plugged", text="Plugged In")
        self.device_tree.pack(fill='both', expand=True)

        self.loop = asyncio.new_event_loop()
        Thread(target=self.start_async_loop, daemon=True).start()
        self.loop.create_task(self.update_device_list())

    def start_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def update_device_list(self):
        while True:
          print("Updating device list...")
          for item in self.device_tree.get_children():
              self.device_tree.delete(item)

          devices = await self.device_tracker.get_connected_devices()
          for device in devices:
              self.device_tree.insert("", "end", 
                values=(
                  device['name'],
                  device['battery'],
                  "Yes" if device.get('plugged', False) else "No"
                )
              )

          await asyncio.sleep(60)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeviceTrackerApp(root)
    root.mainloop()