"""Reads the GameInfo file to determine where Source game data is stored."""
from pathlib import Path
import os
import sys
from typing import Union, List

import itertools

from srctools import Property
from srctools.filesys import FileSystemChain, VPKFileSystem, RawFileSystem


GINFO = 'gameinfo.txt'


class Game:
    """Represents the data in GameInfo."""
    def __init__(self, path: Union[str, Path]):
        """Parse a game from a folder."""
        if isinstance(path, Path):
            self.path = path
        else:
            self.path = Path(path)
        with open(self.path / GINFO) as f:
            gameinfo = Property.parse(f).find_key('GameInfo')
        fsystems = gameinfo.find_key('Filesystem', [])

        self.game_name = gameinfo['Game']
        self.app_id = fsystems['SteamAppId']
        self.tools_id = fsystems['ToolsAppId', None]
        self.additional_content = fsystems['AdditionalContentId', None]
        self.fgd_loc = gameinfo['GameData', 'None']
        self.search_paths = []  # type: List[Path]

        for path in fsystems.find_children('SearchPaths'):
            self.search_paths.append(self.parse_search_path(path))

        # Add DLC folders based on the first/bin folder.
        try:
            first_search = self.search_paths[0]
        except IndexError:
            pass
        else:
            folder = first_search.parent
            stem = first_search.name + '_dlc'
            for ind in itertools.count(1):
                path = folder / (stem + str(ind))
                if path.exists():
                    self.search_paths.insert(0, path)
                else:
                    break

            # Force including 'platform', for Hammer assets.
            self.search_paths.append(self.path.parent / 'platform')

    @property
    def root(self) -> Path:
        """Return the game's root folder."""
        return self.path.parent

    def parse_search_path(self, prop: Property) -> Path:
        """Evaluate options like |gameinfo_path|."""
        if prop.value.startswith('|gameinfo_path|'):
            return (self.path / prop.value[15:]).absolute()

        # We should have to figure out which of the possible paths this is.
        # But, the game (public/filesystem_init.cpp) doesn't actually, it
        # assumes Steam has included the needed VPKs.
        if prop.value.startswith('|all_source_engine_paths|'):
            return (self.root / prop.value[25:]).absolute()

        return (self.root / prop.value).absolute()

    def get_filesystem(self) -> FileSystemChain:
        """Build a chained filesystem from the search paths."""
        vpks = []
        raw_folders = []

        for path in self.search_paths:
            if path.is_dir():
                raw_folders.append(path)
                if (path / 'pak01_dir.vpk').is_file():
                    vpks.append(path / 'pak01_dir.vpk')
                continue

            if not path.suffix:
                path = path.with_suffix('.vpk')
            if not path.name.endswith('_dir.vpk'):
                path = path.with_name(path.name[:-4] + '_dir.vpk')

            if path.is_file() and path.suffix == '.vpk':
                vpks.append(path)

        fsys = FileSystemChain()
        for path in vpks:
            fsys.add_sys(VPKFileSystem(path))
        for path in raw_folders:
            fsys.add_sys(RawFileSystem(path))

        return fsys

    def bin_folder(self) -> Path:
        """Retrieve the location of the bin/ folder."""
        folder = self.path.parent / 'bin'
        # Variant in some versions.
        if (folder / 'win32').is_dir():
            return folder / 'win32'
        return folder


def find_gameinfo(argv=sys.argv) -> Game:
    """Locate the game we're in, if launched as a a compiler.
    
    This checks the following:
    * -vproject
    * -game
    * the VPROJECT environment variable
    * the current folder and all parents.
    """
    for i, value in enumerate(argv):
        if value.casefold() in ('-vproject', '-game'):
            try:
                path = argv[i+1]
            except IndexError:
                raise ValueError(
                    '"{}" argument has no value!'.format(value)
                ) from None
            if Path(path, GINFO).exists():
                return Game(path)
    else:
        # Check VPROJECT
        if 'VPROJECT' in os.environ:
            path = os.environ['VPROJECT']
            if Path(path, GINFO).exists():
                return Game(path)
        else:
            if Path(os.getcwd(), GINFO).exists():
                return Game(os.getcwd())

            for folder in Path(os.getcwd()).parents:
                path = folder / GINFO
                if path.exists():
                    return Game(path)
    raise ValueError("Couldn't find gameinfo.txt!")
