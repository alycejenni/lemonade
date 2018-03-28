from abc import ABC, abstractmethod


class Module(ABC):
    name = 'module'

    def __init__(self, config, formatter, monitor):
        self._config = config
        self.align = self._config.get('align', 'c')
        self._formatter = formatter
        self.monitor = monitor
        self._output = ['']

    @abstractmethod
    def make(self):
        """
        Do stuff to the _output. It should be kept as a list so individual parts can be
        formatted separately if desired.
        """
        pass

    @property
    def get(self):
        """
        Returns the _output as a string.
        :return:
        """
        delimiter = self._config.get('delimiter', ' ')
        self.make()
        return delimiter.join([str(o) for o in self._output])
