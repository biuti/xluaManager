"""
xluaManager
X-Plane 12 python script for XPPython3 plugin

Copyright (c) 2025, Antonio Golfari
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree. 
"""

from datetime import datetime
from time import perf_counter

try:
    from XPPython3 import xp
    from XPPython3.utils.datarefs import DataRef, find_dataref
except ImportError:
    print('xp module not found')
    pass


# Version
__VERSION__ = 'v1.0.0'

# Plugin parameters required from XPPython3
plugin_name = 'xluaManager'
plugin_sig = 'xppython3.xluamanager'
plugin_desc = 'Simple Python script to manage xlua plugins in X-Plane 12'

# Aircrafts
AIRCRAFTS = [
    ('Zibo', 'B737-800X'),
    ('LevelUp', 'LevelUp')
]
# Other parameters
DEFAULT_SCHEDULE = 30  # positive numbers are seconds, 0 disabled, negative numbers are cycles


class Dref:

    def __init__(self) -> None:
        self._jit = find_dataref('xlua/jit_enabled')
        self._logging = find_dataref('xlua/logging_enabled')

    def _set(self, dref, value: float) -> None:
        try:
            dref.value = value
        except SystemError as e:
            xp.log(f"ERROR: {e}")

    def check_values(self) -> None:
        xp.log(f" - Current xlua/jit_enabled: {self._jit.value}, xlua/logging_enabled: {self._logging.value}")
        if self._jit.value == 0:
            self._jit.value = 1
        if self._logging.value == 1:
            self._logging.value = 0
        xp.log(f" - xlua/jit_enabled set to {self._jit.value}, xlua/logging_enabled set to {self._logging.value}")


class PythonInterface:

    def __init__(self) -> None:
        self.plugin_name = f"{plugin_name} - {__VERSION__}"
        self.plugin_sig = plugin_sig
        self.plugin_desc = plugin_desc

        # Dref init
        self.dref = False

    @property
    def aircraft_path(self) -> str:
        _, acf_path = xp.getNthAircraftModel(0)
        return acf_path

    @property
    def aircraft_detected(self) -> bool:
        loaded = bool(any(p[1] in self.aircraft_path for p in AIRCRAFTS))
        if not loaded and isinstance(self.dref, Dref):
            xp.log(f" *** Aircraft not loaded - Dref reset")
            self.dref = False
        return loaded

    @property
    def xlua_dref_exist(self) -> bool:
        if not isinstance(self.dref, Dref):
            try:
                self.dref = Dref()
            except ValueError as e:
                xp.log(f"xLua Drefs not found, probably standard xLua plugin is installed: {e}")
                self.dref = False
            except Exception as e:
                xp.log(f"xLua Dref ERROR: {e}")
                self.dref = False
        return isinstance(self.dref, Dref)

    def loopCallback(self, lastCall, elapsedTime, counter, refCon) -> int:
        """Loop Callback"""
        t = datetime.now()
        start = perf_counter()
        if self.aircraft_detected and self.xlua_dref_exist:
            # check if we need to change parameters
            xp.log(f"{t.strftime('%H:%M:%S')} - aircraft detected: {self.aircraft_path}")
            self.dref.check_values()

        xp.log(f" {t.strftime('%H:%M:%S')} - loopCallback() ended after {round(perf_counter() - start, 3)} sec | schedule = {DEFAULT_SCHEDULE} sec")
        return DEFAULT_SCHEDULE

    def XPluginStart(self) -> tuple[str, str, str]:
        return self.plugin_name, self.plugin_sig, self.plugin_desc

    def XPluginEnable(self) -> int:
        # loopCallback
        self.loop = self.loopCallback
        self.loop_id = xp.createFlightLoop(self.loop, phase=1)
        xp.log(f" - {datetime.now().strftime('%H:%M:%S')} Flightloop created, ID {self.loop_id}")
        xp.scheduleFlightLoop(self.loop_id, interval=DEFAULT_SCHEDULE)
        return 1

    def XPluginDisable(self) -> None:
        pass

    def XPluginStop(self) -> None:
        # Called once by X-Plane on quit (or when plugins are exiting as part of reload)
        xp.destroyFlightLoop(self.loop_id)
        xp.log("flightloop closed, exiting ...")
