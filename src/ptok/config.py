from enum import Enum
from pathlib import Path

import pydantic
import tomlkit


class Config( pydantic.BaseModel ):
	language: str = 'en_us'

	class Config:
		anystr_strip_whitespace = True
		use_enum_values = True
		validate_assignment = True


__path: Path = Path.cwd() / 'config.toml'
__config: Config | None = None


def get() -> Config:
	if __config is None:
		if not __path.exists():
			__config = Config()
		Config( tomlkit.load() )

	return __config


def save() -> None:

