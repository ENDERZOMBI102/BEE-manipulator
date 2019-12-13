from pypresence import Presence, Activity
from bases import costants
import time

class richPresence:
      r"""
            the main class for the discord rich presence integration.
            create an object to initialize the class
      """
      def __init__(self):
            client_id = discordToken()
            RPC = Presence(client_id)  # Initialize the Presence client
            RPC.connect() # connect the client
            RPC.update(state="Rich Presence using pypresence!")
            """
                  this will let discord know that the app is still running
            """
            while True:
                  time.sleep(15)
      def update(self, data = "init"):
            if data == 
obj = richPresence()
