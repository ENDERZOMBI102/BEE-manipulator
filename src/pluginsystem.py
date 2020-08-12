import asyncio
import importlib.util
from enum import Enum
from pathlib import Path
from typing import Callable, Dict

handlers: dict = {}


class event(Enum):
    startup = 0
    close = 1
    downloading = 2
    dl_package = 3
    dl_bee = 4
    dl_finished = 5
    wdw_log_started = 6
    wdw_main = 7


class events:
    @staticmethod
    def on(event: event, callback: Callable):
        handlers[event].append(callback)


class regHandler:
    pass
class logWindowObj:
    pass


async def ph(th):
    pass


class system:

    plugins: Dict[str, object] = {}

    def __init__(self):
         self.instantiate()
         self.load()

    def instantiate(self):
        fdr = Path('./plugins')
        for plg in fdr.glob('*.py'):
            if not plg.name.startswith('PLUGIN_'):
                 continue
            name = plg.name.replace('PLUGIN_','').replace('.py','')
            spec = importlib.util.spec_from_file_location( name, plg )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.plugins[name] = module.Plugin()
            asyncio.run( getattr(self.plugins[name], 'register', ph)(regHandler) )
            asyncio.run( getattr(self.plugins[name], 'getLogWindow', ph)(logWindowObj) )

    def load( self, identifier: str = None ):
        if identifier is not None:
            if self.plugins[identifier].__state__ == 'loaded':
                raise Exception('trying to load an already loaded plugin!')
            asyncio.run( self.plugins[identifier].load() )
            self.plugins[identifier].__state__ = 'loaded'
            return
        for plg in self.plugins.values():
            asyncio.run( plg.load() )
            plg.__state__ = 'loaded'

    def unload( self, identifier: str = None):
        if identifier is not None:
            if self.plugins[identifier].__state__ == 'unloaded':
                raise Exception('trying to unload an already unloaded plugin!')
            asyncio.run( self.plugins[identifier].unload() )
            self.plugins[identifier].__state__ = 'unloaded'
            return
        for plg in self.plugins.values():
            asyncio.run( plg.unload() )
            plg.__state__ = 'unloaded'

    def reload(self, identifier: str):
        getattr(self.plugins[identifier], 'reload', str)()
        self.unload(identifier)
        self.load(identifier)

    def hardReload( self, identifier: str):
        asyncio.run( self.plugins[identifier].unload() )
        path = Path(f'./plugins/PLUGIN_{identifier}.py')
        spec = importlib.util.spec_from_file_location( identifier, path )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.plugins[identifier] = module.Plugin()
        asyncio.run( getattr(self.plugins[identifier], 'register', ph)(regHandler) )
        asyncio.run( getattr(self.plugins[identifier], 'getLogWindow', ph)(logWindowObj) )
        asyncio.run( self.plugins[identifier].load() )
        self.plugins[identifier].state = 'loaded'

        
