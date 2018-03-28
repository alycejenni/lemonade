from datetime import datetime as dt

from ._models import Module


class Clock(Module):
    name = 'clock'

    def make(self):
        _format = self._config.get('format', '%Y-%m-%d %H:%M')
        time_now = dt.now().strftime(_format)
        self._output = [time_now]
