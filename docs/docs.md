BEE Manipulator plugin documentation
-

this is how a basic plugin looks:

```python
class Plugin:
    def load( self ):
        self.logger.info( 'load!' )
    def unload( self ):
        self.logger.info( 'unload!' )
```

there's a list of coroutines that BM calls on a plugin and that you may implement;

|methods|
|-------|
|[load]|
|[unload]|
|[reload]|
|[getEventHandler]|


#### load
Called after the plugin has been instantiated, to finish up loading.
```
async def load():pass
```

#### unload
Called before the plugin is stopped and on unload.
```
async def unload():pass
```

#### reload
Called before the plugin is stopped on reload (and before unload).
```
async def reload():pass
```

#### getEventHandler
Called before load(), used to get the eventHandler.
```
async def geteventHandler():pass
```

pluginsystem object and classes
-

##### eventHandler.on(event, callback)
registers CALLBACK on the EVENT listener<br>
when EVENT is triggered CALLBACK will be executed
callbacks should implement the same parameter names that the event will give

##### eventhandler.send(event, **kwargs)
triggers EVENT with the given kw args, it may not have kw args


##### wx.GetTopLevelWindows()[0]
returns the main UI window object
