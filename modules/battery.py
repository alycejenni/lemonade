import batinfo
import math
from ._models import Module


class Battery(Module):
    name = 'battery'

    def make(self):
        battery = batinfo.Batteries().stat[0]
        capacity = battery.capacity
        is_charging = battery.status != 'Discharging'

        charging = self._config.get('charging', '')
        discharging = self._config.get('discharging', '')
        config_icon = self._config.get('icon', '')
        if isinstance(config_icon, list):
            section_size = 100 / len(config_icon)
            icon_ix = int(math.ceil(int(capacity) / section_size)) - 1
            icon = config_icon[icon_ix]
        else:
            icon = config_icon

        charge_indicator = charging if is_charging else discharging

        self._output = [charge_indicator, self._formatter.fg(icon), str(capacity) + '%']