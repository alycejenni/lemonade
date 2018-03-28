import platform
import re
import subprocess as sp

from ._models import Module


class PackageManager(Module):
    name = 'package_manager'

    def make(self):
        os = self._config.get('os', platform.uname().release)
        os_cmds = {
            '(?i).*arch.*': 'checkupdates'
            }
        n_updates = None
        for k, v in os_cmds.items():
            if re.match(k, os):
                try:
                    n_updates = len(sp.check_output(v.split(' '), timeout=1).decode('utf-8').strip().split('\n'))
                    break
                except Exception as e:
                    continue
        self._output = [self._formatter.fg(''), n_updates]
