import subprocess as sp

from ._models import Module


class Cmd(Module):
    name = 'cmd'

    def make(self):
        cmd = self._config.get('cmd', None)
        if not cmd:
            return
        pipe = sp.Popen(cmd.split(' '), stdout=sp.PIPE)
        try:
            op, er = pipe.communicate(timeout=1)
            op = op.decode('utf-8').replace('\n', ' ')
        except Exception as e:
            op = ''
        self._output = [op]
