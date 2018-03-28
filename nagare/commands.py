# --
# Copyright (c) 2008-2018 Net-ng.
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


class Command(plugin.Plugin):
    def __init__(self, name=None, dist=None, **config):
        super(Command, self).__init__(name if name is not None else os.path.basename(sys.argv[0]), dist, **config)

    def __call__(self, names, args):
        return self, names + (self.name,), args

    def set_arguments(self, parser):
        """Define the available options for this command
       """
        pass

    def parse(self, names, args):
        """Parse the command line
        """
        parser = argparse.ArgumentParser(prog=' '.join(names), description=self.DESC)
        self.set_arguments(parser)

        return vars(parser.parse_args(args))

    @staticmethod
    def run(**args):
        return 0

    def _run(self, **args):
        return self.run(**args)

    def execute(self, args=None):
        command, names, args = self((), args if args is not None else sys.argv[1:])

        return 2 if command is None else command._run(**command.parse(names, args))


class Commands(plugins.Plugins, Command):
    DESC = '<subcommands>'

    def __init__(self, name=None, dist=None, entry_points=None):
        self.entry_points = entry_points
        plugins.Plugins.__init__(self, {}, entry_points=entry_points)
        Command.__init__(self, name, dist)

    def _load_plugin(self, name, dist, plugin, initial_config, config):
        return super(Commands, self)._load_plugin(
            name, dist, plugin, initial_config, config,
            entry_points=self.entry_points + '.' + name
        )

    def usage(self, names, _):
        print 'Usage: ' + ' '.join(names) + (' <command>' if self else '')
        if self:
            print
            print 'with <command>:'

            name_max_len = max(map(len, self))
            for name, sub_command in sorted(self.items()):
                print ' - %s: %s' % (name.ljust(name_max_len), sub_command.DESC)

        return None, None, None

    def __call__(self, names, args):
        subcommand = args.pop(0) if args else None

        return self.get(subcommand, self.usage)(names + (self.name,), args)


def run(entry_points, commands=Commands):
    return commands(entry_points=entry_points).execute()
