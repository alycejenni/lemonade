import json

import yaml


class Formatter(object):
    def __init__(self, config):
        self.config = config['formatter']

    @staticmethod
    def _flatten(d, filter=None):
        def flat(item_list):
            items = []
            for k, v in item_list:
                if isinstance(v, dict):
                    items += flat(v.items())
                else:
                    items.append((k, v))
            return items

        flattened = [(k, v) for k, v in flat(d.items()) if filter is None or filter(v)]
        return dict(flattened)

    @property
    def colours(self):
        config_var = self.config.get('colours', self.config.get('colors', {}))
        if isinstance(config_var, str):
            with open(config_var, 'r') as f:
                if config_var.endswith('.json'):
                    _colours = json.load(f)
                elif config_var.endswith('.yml') or config_var.endswith('.yaml'):
                    _colours = yaml.safe_load(f)
        else:
            _colours = config_var
        return self._flatten(_colours, lambda x: x.startswith('#'))

    @staticmethod
    def align(pos='c'):
        while pos not in ['l', 'r', 'c']:
            if len(pos) > 1:
                pos = pos[0]
            else:
                pos = 'c'
        return '%{' + pos + '}'

    def fg(self, string, colour=None):
        if not colour:
            colour = self.colours.get('foreground', '-')
        if not colour.startswith('#'):
            colour = self.colours.get(colour, '#' + colour)
        return '%{F' + colour + '}' + string + '%{F-}'

    def bg(self, string, colour=None):
        if not colour:
            colour = self.colours.get('background', '-')
        if not colour.startswith('#'):
            colour = self.colours.get(colour, '#' + colour)
        return '%{B' + colour + '} ' + string + ' %{B-}'

    def decorate(self, string, colour=None):
        if not colour:
            colour = self.colours.get('foreground', '-')
        if not colour.startswith('#'):
            colour = self.colours.get(colour, '#' + colour)
        return '%{U' + colour + '}' + string + '%{U-}'

    def click(self, string, cmd, button='left'):
        buttons = {
            'left': '1',
            'middle': '2',
            'right': '3',
            'scrollup': '4',
            'scrolldown': '5'
        }
        return ''.join(['%{A',
                        buttons.get(button, '1'),
                        ':',
                        cmd,
                        ':}',
                        string,
                        '%{A}'])
