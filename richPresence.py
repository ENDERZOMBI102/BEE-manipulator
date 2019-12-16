from pypresence import Presence, Activity
from bases import costants
import time

class richPresence:
      r"""
            the main class for the discord rich presence integration.
            create an object to initialize the class
      """
      def __init__(self):
            self.RPC = Presence(costants.discordToken())  # Initialize the Presence client
            self.RPC.connect() # connect the client
            self.RPC.update(state="Starting BEE Manipulator!")
            """
                  this will let discord know that the app is still running
            """
            while True:
                  time.sleep(15)
      def update(self, data = "init"):
            if data == "init":
                  self.RPC.update(state="Starting BEE Manipulator!")
            elif data == "browsing":
                  self.RPC.update(state="Browsing BEEmod packages.")
            elif data == "idle":
                  self.RPC.update(state="Idle")
            elif data == "settings":
                  self.RPC.update(state="In the settings tab")
            elif data == "BEE":
                  self.RPC.update(state="Using BEE2.4")
      
      

if __name__ == "__main__":
      obj = richPresence()
