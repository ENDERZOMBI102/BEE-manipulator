import json
from winreg import QueryValueEx, ConnectRegistry, HKEY_CURRENT_USER, OpenKey

from srctools import Property
from utilities import *

logger = get_logger()
overwriteDict: dict = {}
# the plugins dict HAS to be the last
default_config = {
    'config_type': 'BEE2.4 Manipulator Config File',
    'appVersion': '0.0.1',
    'lastVersion': True,
    'beeUpdateUrl': None,
    'steamDir': None,
    'portal2Dir': None,
    'beePath': None,
    'logWindowVisibility': False,
    'logLevel': 'info',
    'databasePath': './assets/database.json',
    'noVerifyDialog': False,
    'plugins': {}

}


def createConfig():

    """
        a simple function that make the config file
    """
    global default_config
    with open('config.cfg', 'w', encoding='utf-8') as file:
        json.dump(default_config, file, indent=3)


def load(section) -> Union[str, int, None, dict, list]:  # load a config

    """
    loads a section of the config (json-formatted) and return the data.
    raise an exception if the config or the requested section doesn't exist
    example::

        >>> import config
        >>> print(config.load('version'))
        2.6
    :param section: section of the config to read
    :returns: the readed data
    """
    if section in overwriteDict.keys():
        logger.debug('using overwrited data!')
        return overwriteDict[section]
    try:
        with open('config.cfg', 'r', encoding='utf-8') as file:
            config = json.load(file)  # load the config
            readeData = config[section]  # take the requested field
        return readeData  # return the readed data
    except:
        if section in default_config:
            logger.warning(f"can't load {section} from config file, using default")
            return default_config[section]
        else:
            logger.error(f"can't load {section} from config file")


def save(data, section):  # save a config

    """
    save the data on the config (json-formatted), re-create the config if no one is found.
    example::
        >>> import config
        >>> print(config.load('version'))
        '2.6'
        >>> config.save('2.5','version')
        >>> print(config.load('version'))
        '2.5'
    :param data: the data to save
    :param section: the section of the config to save the data to
    """

    try:
        with open('config.cfg', 'r', encoding='utf-8') as file:
            cfg = json.load(file)  # load the config file
            cfg[section] = data
        with open('config.cfg', 'w', encoding='utf-8') as file:
            json.dump(cfg, file, indent=3)
        logger.debug(f'saved {section}')
    except:
        logger.error(f'failed to save {data} to {section}!')
        raise configError('error while saving the config')


def loadAll(overwrite: bool = False) -> dict:

    """
    A function that returns all the configs
    :param overwrite: if true, act like load() and enable config overwrite
    :return: the config dict
    """
    try:
        logger.debug('loading config file')
        with open('config.cfg', 'r', encoding='utf-8') as file:
            cfg = json.load(file)  # load the config file
            if overwrite:  # only if overwrite is true
                logger.debug(f'overwriting configs..')
                for key in overwriteDict:  # cycle in the keys
                    if key in cfg:  # overwrite, not create a key
                        cfg[key] = overwriteDict[key]  # finally, overwrite the value
        logger.debug('finished config file operations, returning configs as dict')
        return cfg
    except:
        logger.error('no config file found! creating & loading new one')
        createConfig()  # create new config file and call the function again
        return loadAll()


def saveAll(cfg: dict = None):

    """
    A function that saves (and overwrites) the config file
    :param cfg: the config dict
    """
    if ( cfg is None ) or ( 'config_type' is not 'BEE2.4 Manipulator Config File' ):
        raise ValueError("parameter cfg can't be an invalid config!")
    try:
        with open('config.cfg', 'w', encoding='utf-8') as file:
            json.dump(cfg, file, indent=3)
    except:
        logger.error('An error happened while saving config file, probably is now corrupted')


def check(cfg: dict = None) -> bool:

    """
    check if the config file exist and if is a BM config file
    :param cfg: optional string to use instead of reopening from the file system
    :return: True if is a valid config
    """
    if cfg is None:
        try:
            with open('config.cfg', 'r') as file:
                cfg = json.load(file)  # load the file
        except FileNotFoundError:
            return False
    # check if EVERY config exists
    for i in default_config.keys():
        if i in cfg.keys():
            continue
        return False
    # final check
    if cfg['config_type'] == 'BEE2.4 Manipulator Config File':
        # the check is made successfully
        return True
    else:
        # the config file is not a BM config file
        return False


def overwrite(section: str, data: any) -> None:

    """
    overwrite in run time a config
    :param section: the section that has to be overwritten
    :param data: the value the section is overwritten with
    :return: None
    """
    overwriteDict[section] = data
    logger.debug(f'Overwritten config {section}!')


# dynamic/static configs

def steamDir() -> str:

    """
    a function that retrives the steam installation folder by reading the win registry
    :return: path to steam folder
    """
    if 'steamDir' not in loadAll().keys():
        save(None, 'steamDir')  # create the config without value in case it doesn't exist

    if not load('steamDir') is None:
        return load('steamDir')  # return the folder
    elif platform == 'win32':
        # get the steam directory from the windows registry
        # HKEY_CURRENT_USER\Software\Valve\Steam
        try:
            logger.debug('Opening windows registry...')
            with ConnectRegistry(None, HKEY_CURRENT_USER) as reg:
                aKey = OpenKey(reg, r'Software\Valve\Steam')  # open the steam folder in the windows registry
        except Exception as e:
            logger.critical("Can't open windows registry! this is *VERY* bad!", exc_info=1)
            raise Exception(e)
        try:
            keyValue = QueryValueEx(aKey, 'SteamPath')  # find the steam path
            save(keyValue[0], 'steamDir')  # save the path, so we don't have to redo all this
            return keyValue[0]
        except:
            raise KeyError("Can't open/find the steam registry keys")


def portalDir() -> str:

    """
    a function that retrives the portal 2 folder by searching in all possible libraries
    :return: path to p2 folder
    """
    if not load('portal2Dir') is None:
        return load('portal2Dir')  # check if we already saved the path, in case, return it
    else:
        # check every library if has p2 installed in it
        library = libraryFolders()
        for path in library:
            try:
                logger.info(f'searching in {path}..')
                with open(path + 'appmanifest_620.acf', 'r') as file:
                    pass
                # if yes save it
                path += 'common/Portal 2/'
                logger.info(f'portal 2 found! path: {path}')
                save(path, 'portal2Dir')
                return path
            except FileNotFoundError:
                # if no, just continue
                continue


discordToken: str = '655075172767760384'


def libraryFolders() -> list:

    """
    retrives the steam library folders by parsing the libraryfolders.vdf file
    :return: a list with all library paths
    """
    paths = [steamDir() + '/steamapps/']  # create a list for library paths
    try:
        # open the file that contains the library paths
        with open(steamDir() + '/steamapps/libraryfolders.vdf', 'r') as file:
            library = Property.parse(file, 'libraryfolders.vdf').as_dict()
            # remove useless stuff
            library['libraryfolders'].pop('timenextstatsreport')
            library['libraryfolders'].pop('contentstatsid')
    except Exception as e:
        raise Exception(f'Error while reading steam library file: {e}')

    # check for other library paths, if the dict is empty, there's no one
    if not len(library['libraryfolders']) is 0:
        for i in len(library['libraryfolders']):
            paths.append(library['libraryfolders'][str(i)] + '/steamapps/')  # append the path

    # return the "compiled" list of libraries
    return paths


def steamUsername():

    """
    retrives the steam username
    :return: steam username
    """
    try:
        with ConnectRegistry(None, HKEY_CURRENT_USER) as reg:
            aKey = OpenKey(reg, r'Software\Valve\Steam')
    except Exception as e:
        raise Exception(e)
    try:
        keyValue = QueryValueEx(aKey, 'LastGameNameUsed')
        return keyValue[0]
    except:
        return None


def checkUpdates() -> bool:
    if not isonline():  # if we're not online return false
        return False
    if not load('lastVersion'):  # if we're not on latest version return true
        return True
    available, url, ver = checkUpdate( 'https://github.com/ENDERZOMBI102/BEE-manipulator', load("appVersion") )
    if available:
        save(url, 'lastVersionUrl')
        save(False, 'lastRelease')
        save(ver, 'onlineAppVersion')
    return available


def version():
    return load('appVersion')


def onlineVersion():
    return load('onlineAppVersion')


def devMode() -> bool:
    return boolcmp( load('devMode') )


class configError(BaseException):
    r"""
    base error for config operations
    """


if __name__ == '__main__':
    print(portalDir())
