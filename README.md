# xLua Manager
python script for XPPython3 in X-Plane 12, to manage xlua features using datarefs if available 

## Features
@wahltho created an [advanced xLua version](https://github.com/wahltho/XLua) for Zibo, that creates some dref permitting to set logging and jit features.\
This script checks if the xLua is installed, and changes automatically:
- logging to 0 
- jit to 1

These are the settings that should optimize performances

## How to use
It works only with **Zibo B737-800 modified** and **LevelUp B737NG series**.\
The plugin uses the aircraft path to recognize the aircraft, so _B737-800X_ or _LevelUp_ need to be present in the path.For example:
```
- x-plane 12
    - Aircraft
        - Zibo
            - B737-800X
        - LevelUp
            - 737NG Series V2
```

## Requirements
- MacOS 10.14, Windows 7 and Linux kernel 4.0 and above
(tested using macOS 12.7.6)
- X-Plane **12.4 and above** (not tested with previous versions, may work) 
- pbuckner's [XPPython3 plugin **4.6.0 or above**](https://xppython3.readthedocs.io/en/latest/index.html) (tested using version 4.6.1)
- [Zibo B737-800 Modified](https://forums.x-plane.org/index.php?/forums/forum/384-zibo-b738-800-modified/) for X-Plane 12 **ver. 4.04** and above (**may be compatible with some previous versions**) or [LevelUp B737NG Series](https://forum.thresholdx.net/files/file/3865-levelup-737ng-series/) for X-Plane 12 **ver. U1 and U2**

> [!NOTE]
> **(*) Latest XPPython3 [plugin version (4.3.0 and above)](https://xppython3.readthedocs.io/en/latest/index.html) will contain all python needed libraries, so it won't be necessary to install Python on the machine anymore. Read carefully XPPython3 plugin documentation**

> [!IMPORTANT]
> **xLuaManager requires XPPython3 version 4.6.0 or above!**

## Installation
Just copy or move the file _PI_xluaManager.py_ to the folder:

    X-Plane/Resources/plugins/PythonPlugins/

> [!NOTE]
> XPPython3 will create the _PythonPlugins_ folder the first time XP12 runs with the plugin installed.
