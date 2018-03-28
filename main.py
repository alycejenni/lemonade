import os
import time
import click
import yaml
from loader import get_module
from format import Formatter
import itertools

home_config = '{0}/.config/lemonade/config'.format(os.path.expanduser('~'))


@click.command()
@click.option('--config', default=home_config)
@click.argument('monitor')
def lemonade(monitor, config):
    if not os.path.exists(config):
        click.echo('Config does not exist. Exiting.')
        return
    with open(config, 'r') as f:
        conf = yaml.safe_load(f)

    formatter = Formatter(conf)
    config_modules = conf['modules']
    modules = []
    for m in config_modules:
        name, options = list(m.items())[0]
        if options is None:
            options = {}
        module = get_module(name)(options, formatter, monitor)
        modules.append(module)
    module_alignments = {k: list(v) for k, v in itertools.groupby(sorted(modules, key=lambda x: x.align), lambda x: x.align)}
    while True:
        output = '%{S' + monitor + '}'
        for alignment in ['l', 'c', 'r']:
            module_group = module_alignments.get(alignment, None)
            if module_group is None:
                continue
            output += formatter.align(alignment)
            group_output = ' | '.join([m.get for m in module_group])
            output += group_output
        click.echo(f' {output} ')
        time.sleep(float(conf.get('interval', 1)))


lemonade()
