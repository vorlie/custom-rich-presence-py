import pystray
import subprocess
from PIL import Image
import time
from pypresence import Presence
import threading

class DiscordPresence:
    def __init__(self, client_id):
        self.client_id = client_id
        self.RPC = Presence(client_id)
        self.RPC.connect()
    
    def connect(self):
        self.RPC.connect()

    def update_presence(self, large_image, details, buttons):
        start = time.time()
        while True:
            self.RPC.update(
                large_image=large_image,
                details=details,
                start=start,
                buttons=buttons
            )
            time.sleep(60) 

class TrayIcon:
    def __init__(self, presence):
        self.presence = presence
        image = Image.open("icon.png") # the path to the icon to use for the tray (also will show in the task manager)
        self.icon = pystray.Icon("uwu", image, "uwu", menu=pystray.Menu(
            pystray.MenuItem("Reconnect", self.reconnect), # Reconnects to discord after a discord reload (ctrl + r) for example
            pystray.MenuItem("Close tray", self.close_app), # Closes the tray icon and closes the rich presence
            pystray.MenuItem("Close RPC", self.close_rpc) # Closes the connection between discord and the script
        ))

    def close_app(self, icon, item):
        icon.stop()
        self.presence.RPC.close()

    def reconnect(self, icon, item):
        self.presence.RPC.close()
        time.sleep(1)
        self.presence.connect()
    
    def close_rpc(self, icon, item):
        self.presence.RPC.close()

# Create an instance of DiscordPresence; Insert your application id = it will use its name as the "game"
presence = DiscordPresence('')

# Create an instance of TrayIcon and pass the presence instance
tray_icon = TrayIcon(presence)

# Start the presence thread; customize your rich presence
presence_thread = threading.Thread(target=presence.update_presence, args=(
    "", # Large image, use links 
    "", # Details
    [{"label": "example", "url": "https://example.com"},{"label": "example2", "url": "https://example.com"}] # Buttons
))
presence_thread.start()

# Start the tray icon
tray_thread = threading.Thread(target=tray_icon.icon.run)
tray_thread.start()
