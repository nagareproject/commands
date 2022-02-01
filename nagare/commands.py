# --
# Copyright (c) 2008-2022 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import os
import sys
import argparse

from nagare.services import plugin, plugins


class CommandError(ValueError):
    def __init__(self, message='', status=1):
        super(CommandError, self).__init__((message, status))

    @property
    def message(self):
        return self.args[0][0]

    @property
    def status(self):
        return self.args[0][1]


class ArgumentError(CommandError):
    def __init__(self, message='', status=2):
        super(ArgumentError, self).__init__(message, status)


class ArgumentParser(argparse.ArgumentParser):
    def exit(self, status=0, message=': : '):
        raise ArgumentError(message.split(': ', 2)[2].strip(), status)


class Command(plugin.Plugin):
    def __init__(self, name=None, dist=None, **config):
        super(Command, self).__init__(name if name is not None else os.path.basename(sys.argv[0]), dist, **config)

    def usage_name(self, ljust=0):
        return self.name.ljust(ljust)

    def _create_parser(self, name):
        return ArgumentParser(name, description=self.DESC)

    def set_arguments(self, parser):
        """Define the available options for this command
       """
        pass

    def parse(self, parser, args):
        """Parse the command line
        """
        self.set_arguments(parser)
        return vars(parser.parse_args(args))

    @staticmethod
    def run(command_names, **arguments):
        return 0

    def _run(self, command_names, next_method=None, **arguments):
        return (next_method or self.run)(command_names, **arguments)

    def execute(self, command_names=(), args=None):
        command_names += (self.name,)
        if args is None:
            args = sys.argv[1:]

        try:
            parser = self._create_parser(' '.join(command_names))
            arguments = self.parse(parser, args)

            status = self._run(command_names, **arguments) or 0
        except CommandError as e:
            status = e.status

            if e.message:
                parser._print_message('error: {}\n'.format(e.message))

        return status


class Commands(plugins.Plugins, Command):
    DESC = '<subcommands>'

    def __init__(self, name=None, dist=None, entry_points=None):
        self.entry_points = entry_points
        plugins.Plugins.__init__(self)
        Command.__init__(self, name, dist)

        self.load_plugins(name, entry_points=entry_points)

    def _load_plugin(self, name_, dist, plugin, **config):
        command = super(Commands, self)._load_plugin(
            name_, dist, plugin,
            activated=True,
            entry_points=self.entry_points + '.' + name_,
            **config
        )

        command.PLUGIN_CATEGORY = self.entry_points
        return command

    def set_arguments(self, parser):
        super(Commands, self).set_arguments(parser)
        parser.add_argument('subcommands', nargs='...')

    def run(self, command_names, subcommands):
        self.load_plugins(self.name)
        if subcommands:
            subcommand = self.get(subcommands.pop(0))
            if subcommand is not None:
                return subcommand.execute(command_names, subcommands)

        return self.usage(command_names)

    def usage(self, names, display=None):
        display = display or (lambda m: sys.stderr.write(m + '\n'))
        display('Usage: ' + ' '.join(names) + (' <command>' if self else ''))
        if self:
            display('')
            display('with <command>:')

            name_max_len = max(map(len, self))
            for _, sub_command in sorted(self.items()):
                display('  - {}{}{}'.format(
                    sub_command.usage_name(name_max_len),
                    ': ' if sub_command.DESC else '',
                    sub_command.DESC
                ))

        raise ArgumentError(status=0)


def run(entry_points):
    return Commands(entry_points=entry_points).execute()
