from pypresence import Presence, Activity
from config import reconfig
from asyncio import sleep

class richPresence():
      r"""
            the main class for the discord rich presence integration.
            create an object to initialize the class
      """
      def __init__(self):
            self.RPC = Presence(reconfig.discordToken())  # Initialize the Presence client
            self.RPC.connect() # connect the client
            self.RPC.update(state="Starting BEE Manipulator!")
            """
                  this will let discord know that the app is still running
            """
            self.run()

      def update(self, data = "init"):
            r"""
                  can be: init, brows, idle, settings, BEE
            """
            if data == "init":
                  self.RPC.update(state="Starting BEE Manipulator!")
            elif data == "brows":
                  self.RPC.update(state="Browsing BEEmod packages.")
            elif data == "idle":
                  self.RPC.update(state="Idle")
            elif data == "settings":
                  self.RPC.update(state="In the settings tab")
            elif data.upper() == "BEE":
                  self.RPC.update(state="Using BEE2.4")

      async def run(self):
            r"""
                  i hate async
            """
            while True:
                  await sleep(15)


if __name__ == "__main__":
      obj = richPresence()
