import sys
from importlib import _bootstrap
from types import ModuleType
from typing import Dict

from wx.py import dispatcher

_RELOADING = {}


def reload(module: ModuleType, additionalSearchDict: Dict[str, ModuleType] = None) -> ModuleType:
	"""
	Reload the module and return it.

	The module must have been successfully imported before.

	:param module: The module to reload
	:param additionalSearchDict: An additional search path to use alongside sys.modules
	:return: The module
	"""
	if not module or not isinstance(module, ModuleType):
		raise TypeError("module argument must be a ModuleType instance")
	try:
		name = module.__spec__.name
	except AttributeError:
		name = module.__name__

	if additionalSearchDict is None:
		additionalSearchDict = {}

	useCustom = module in additionalSearchDict.values()

	if useCustom:
		if additionalSearchDict.get(name) is not module:
			msg = "module {} not found in sys.modules or in additional search dict"
			raise ImportError(msg.format(name), name=name)
	else:
		if sys.modules.get(name) is not module:
			msg = "module {} not found in sys.modules or in additional search dict"
			raise ImportError(msg.format(name), name=name)
	if name in _RELOADING:
		return _RELOADING[name]
	_RELOADING[name] = module
	try:
		parent_name = name.rpartition('.')[0]
		if parent_name:
			try:
				parent = additionalSearchDict[parent_name]
			except KeyError:
				try:
					parent = sys.modules[parent_name]
				except KeyError:
					msg = "parent {!r} not in sys.modules nor in additional search dict"
					raise ImportError( msg.format(parent_name), name=parent_name ) from None
				else:
					pkgpath = parent.__path__
			else:
				pkgpath = parent.__path__
		else:
			pkgpath = None
		target = module
		spec = module.__spec__ = _bootstrap._find_spec(name, pkgpath, target)
		if spec is None:
			raise ModuleNotFoundError( f"spec not found for the module {name!r}", name=name )
		_bootstrap._exec(spec, module)

		# ModuleReloadEvent
		dispatcher.send(
			signal='ModuleReloadEvent',
			module=additionalSearchDict[name] if useCustom else sys.modules[name]
		)

		# The module may have replaced itself in sys.modules!
		return additionalSearchDict[name] if useCustom else sys.modules[name]
	finally:
		try:
			del _RELOADING[name]
		except KeyError:
			pass
