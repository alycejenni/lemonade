import subprocess as sp

from ._models import Module


class Bash(Module):
    name = 'bash'

    def make(self):
        script = self._config.get('script', None)
        if not script:
            return
        script_output = sp.check_output(['sh', script])
        self._output = [script_output]
