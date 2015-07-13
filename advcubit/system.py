"""Module that handles the include path and the startup of cubit

The module provides helper functions to locate the cubit inlcude paths on
different operating systems and imports the cubit files
"""

import sys as _sys
import os as _os
import warnings as _warnings

cubitModule = None  # reference to the cubit module, used in all submodules
cubitExec = None    # reference to the used cubit command


class AdvCubitException(RuntimeError):
    """ default exception for advcubit
    """
    def __init__(self, msg):
        """ Constructor
        :param msg: message string
        """
        super(AdvCubitException, self).__init__(msg)


def init(cubitPath=None, silentMode=True):
    """ Sets up the advcubit module

    :param cubitPath: Path to cubit installation director, if None $CUBIT_PATH will be used
    :param silentMode: Flag to suppress cubit commands
    :return: None
    """
    import platform

    global cubitModule

    if cubitPath is None:
        try:
            cubitPath = _os.environ['CUBIT_PATH']
        except KeyError:
            raise EnvironmentError('$CUBIT_PATH not set')

    osType = platform.system()
    if osType == 'Linux':
        _initLinux(cubitPath)
    elif osType == 'Darwin':
        _initDarwin(cubitPath)
    else:
        raise RuntimeError('Unsupported operating system: ' + osType)

    import cubit

    cubitModule = cubit
    enableSilentMode(silentMode)


def enableSilentMode(silentMode=True):
    """ Activates the silent mode

    :param silentMode: Flag for activation or deactivation
    :return: None
    """
    global cubitExec
    if silentMode:
        cubitExec = cubitModule.silent_cmd
    else:
        cubitExec = cubitModule.cmd


def _initLinux(cubitPath):
    """ Adds the necessary folders to the python path on Linux OS

    :param cubitPath: path to Cubit installation directory
    :return: None
    """
    cubitDirs = [cubitPath + '/bin', cubitPath + '/structure', cubitPath + '/GUI']
    _sys.path.extend(cubitDirs)


def _initDarwin(cubitPath):
    """ Adds the necessary folders to the python path on Mac OS

    :param cubitPath: path to Cubit installation directory
    :return: None
    """
    if _sys.version_info[0] != 2 and _sys.version_info[1] >= 7:
        EnvironmentError('Mac OS cubit can only handle Python 2.6 or maybe less')

    cubitDirs = [cubitPath, cubitPath + '/bin', cubitPath + '/structure', cubitPath + '/GUI']
    _sys.path.extend(cubitDirs)


def checkVersion():
    if _sys.version[0] > 2:
        EnvironmentError('Cubit can only handle Python version 2')


def cubitCmd(cmdStr):
    """ Executes a cubit command and checks for errors
    :param cmdStr: cubit journal command string
    :raises AdvCubitException: Raises an exception, if command fails
    :return: None
    """
    errorCount = cubitModule.get_error_count()
    cubitExec(cmdStr)
    newCount = cubitModule.get_error_count()
    # check if a new error occurred
    if newCount > errorCount:
        raise AdvCubitException('Error executing command: {0}'.format(cmdStr))


def warning(msg):
    """ Central warning wrapper
    :param msg: Warning message
    :return: None
    """
    _warnings.warn(msg, RuntimeWarning)
