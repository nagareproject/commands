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


class Commands(plugins.Plugins, plugin.Plugin):
    DESC = '<subcommands>'

    def __init__(self, name, dist, entry_points):
        self.name = name
        self.entry_points = entry_points
        super(Commands, self).__init__({}, entry_points=entry_points)

    def _load_plugin(self, name, dist, plugin, config):
        return super(Commands, self)._load_plugin(
            name, dist, plugin, config,
            entry_points=self.entry_points + '.' + name
        )

    '''
    def validate(self, args, services_service):
        sub_commands = {
            name: subcommand
            for name, subcommand in self.items()
            if services_service(subcommand.validate, args)
        }

        self.clear()
        self.update(sub_commands)

        return bool(self)
    '''

    def get_command_names(self, names):
        return names + (self.name,)

    def find_subcommand(self, names, args):
        command_names = self.get_command_names(names)

        args = args or [None]
        command = self.get(args[0])

        return (command_names, self, None) if command is None else command.find_subcommand(command_names, args[1:])

    def parse(self, command_name, args):
        print 'Usage: ' + command_name + (' <command>' if self else '')
        if self:
            print
            print 'with <command>:'

            name_max_len = max(map(len, self))
            for name, sub_command in sorted(self.items()):
                print ' - %s: %s' % (name.ljust(name_max_len), sub_command.DESC)

        return None


class ConsoleScript(Commands):
    def __init__(self, entry_points, script_name=None):
        if script_name is None:
            script_name = os.path.basename(sys.argv[0])

        super(ConsoleScript, self).__init__(script_name, None, entry_points)

    def find_subcommand(self, args):
        names, sub_command, args = super(ConsoleScript, self).find_subcommand((self.name,), args)
        return ' '.join(names), sub_command, args

    def get_command_names(self, names):
        return names

    def __call__(self, args=None):
        if args is None:
            args = sys.argv[1:]

        command_name, command, args2 = self.find_subcommand(args)
        arguments = command.parse(command_name, args2)

        return (command, arguments) if arguments is not None else (None, None)


class Command(plugin.Plugin):
    """The base class of all the commands"""
    DESC = ''

    def __init__(self, name, dist, **config):
        super(Command, self).__init__(name, dist, **config)
        self.name = name

    def find_subcommand(self, names, args):
        return names + (self.name,), self, args

    '''
    def validate(self, args):
        return True
    '''

    def set_arguments(self, parser):
        """Define the available options for this command
       """
        pass

    def parse(self, command_name, args):
        """Parse the command line
        """
        parser = argparse.ArgumentParser(prog=command_name, description=self.DESC)
        self.set_arguments(parser)

        return vars(parser.parse_args(args))
