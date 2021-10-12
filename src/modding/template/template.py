from pathlib import Path
from typing import List

import wx


class FileTemplate:
	_path: str
	_content: str

	def __init__(self, path: str, content: str):
		self._content = content
		self._path = path

	def getPath( self, kwargs: dict ) -> str:
		return self._path.format(kwargs)

	def getContent( self, kwargs: dict ) -> str:
		return self._content.format(kwargs)


class TemplateProgressListener(wx.Dialog):

	def __init__(self, parent: wx.Window, template: 'Template'):
		super(TemplateProgressListener, self).__init__(
			parent=parent,
			title=f'Generating {template.getName()}'
		)
		self.prog: wx.Gauge = wx.Gauge(
			parent=self,
			range=template.getTotalFiles()
		)
		self.curFile: wx.StaticText = wx.StaticText(
			parent=self,
			label='Loading...'
		)

	def update( self, current: str ) -> None:
		self.prog.SetValue( self.prog.GetValue() + 1 )
		self.curFile.SetLabel( f'Writing {current}' )


class Template:
	files: List[FileTemplate]
	name: str = '<invalid>'

	def __init__( self ):
		self.files = []

	def generate( self, progressListener: TemplateProgressListener, folder: Path, kwargs ) -> None:
		for fileTemplate in self.files:
			file = folder / fileTemplate.getPath( kwargs )
			file.touch()
			file.write_text( fileTemplate.getContent( kwargs ) )

	def getName( self ):
		return self.name

	def getTotalFiles( self ) -> int:
		return len(self.files)
