from abc import abstractmethod
class PluginBase:
    __state__: str = 'unloaded'
    def __init__(self):
        print('base plugin is being instantiated')
    @abstractmethod
    async def load(self):
        pass
    @abstractmethod
    async def unload(self):
        pass