from ._models import Module


class Undefined(Module):
    name = 'undefined'

    def make(self):
        self._output = ['UNDEFINED']
