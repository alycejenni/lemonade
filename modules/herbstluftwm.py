import subprocess as sp

from ._models import Module


class Herbstluftwm(Module):
    name = 'herbstluftwm'

    def make(self):
        tag_status = sp.check_output(
            ['herbstclient', 'tag_status', self.monitor]).decode('utf-8').strip()
        tag_list = tag_status.split('\t')

        # config options
        this_monitor_only = self._config.get('this_monitor_only', False)
        show_empty = self._config.get('show_empty', True)
        tag_formats = self._config.get('tag_formats', None)

        # filter
        if this_monitor_only:
            tag_list = [t for t in tag_list if not t.startswith('-') and not t.startswith('%')]
        if not show_empty:
            tag_list = [t for t in tag_list if not t.startswith('.')]

        # format
        format_key = {'.': 'empty',
                      ':': 'not_empty',
                      '+': 'unfocused_this',
                      '#': 'focused_this',
                      '-': 'unfocused_other',
                      '%': 'focused_other',
                      '!': 'urgent'}
        formatted_tags = []
        if tag_formats is None:
            formatted_tags = [t[1:] for t in tag_list]
        else:
            for t in tag_list:
                status = t[0]
                t = t[1:]
                t = self._formatter.click(t, f'herbstclient use {t}')
                f = format_key[status]
                config_format = tag_formats.get(f, tag_formats.get('default', None))
                if config_format is not None:
                    if 'bg' in config_format:
                        t = self._formatter.bg(t, config_format['bg'])
                    if 'fg' in config_format:
                        t = self._formatter.fg(t, config_format['fg'])
                    if 'ul' in config_format:
                        t = self._formatter.decorate(t, config_format['ul'])
                formatted_tags.append(t)

        self._output = formatted_tags
