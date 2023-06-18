from pathlib import Path

import pydantic
import tomlkit


class Config( pydantic.BaseModel ):
	language: str = 'en_us'

	class Config:
		anystr_strip_whitespace = True
		use_enum_values = True
		validate_assignment = True


def get() -> Config:
	global __config
	if __config is None:
		if __path.exists():
			__config = Config( **tomlkit.loads( __path.read_text() ).unwrap() )
		else:
			__config = Config()
	return __config


def save() -> None:
	""" Save the config to disk """
	global __config
	if __config is not None:
		with open( __path, 'w' ) as file:
			tomlkit.dump( __config.dict(), file )


__path: Path = Path.cwd() / 'config.toml'
__config: Config | None = None
