===============
Nagare Commands
===============

.. image:: https://img.shields.io/pypi/v/nagare-commands.svg
   :target: https://pypi.python.org/pypi/nagare-commands/
   :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/nagare-commands.svg
   :target: https://pypi.python.org/pypi/nagare-commands/
   :alt: License

Overview
========

Nagare Commands is an extensible command-line interface framework for Python applications. It provides a flexible and modular approach to creating command-line tools with subcommands, similar to Git, Docker, or other modern CLI applications.

This package is part of the Nagare Python web framework but can be used independently in other Python projects that need a robust command-line interface system.

Key Features
===========

* **Plugin-based architecture**: Easily extend with new commands and subcommands
* **Hierarchical command structure**: Support for nested subcommands
* **Automatic help generation**: Comprehensive help text for all commands
* **Argument parsing**: Built on top of Python's argparse with enhanced error handling
* **Command discovery**: Automatic loading of commands through entry points

Architecture
===========

The Nagare Commands system consists of:

* **Core command framework**: Base classes and utilities for defining commands
* **Command plugins**: Independent command implementations that extend functionality

Available Command Packages
========================

The Nagare Commands system includes several command packages:

* **commands-base**: The core 'nagare-admin' executable
* **commands-create**: Project scaffolding functionality
* **commands-db-cli**: Database command-line interface
* **commands-db-ide**: Database IDE integration
* **commands-exec**: Shell execution commands
* **commands-proxy**: Web server proxy configuration
* **commands-redis-cli**: Redis CLI integration

Usage
=====

Basic usage:

.. code-block:: python

    from nagare.commands import Commands, Command

    class HelloCommand(Command):
        DESC = 'Say hello'

        def set_arguments(self, parser):
            parser.add_argument('--name', default='World', help='Name to greet')

        def run(self, command_names, name, **kw):
            print(f'Hello, {name}!')
            return 0

    # Create a command registry
    commands = Commands(entry_points='my.commands')
    commands.register('hello', HelloCommand())

    # Execute commands from command line
    commands.execute()

Defining a Custom Command
========================

To create a custom command:

1. Subclass the ``Command`` class
2. Define a ``DESC`` class attribute as a short description
3. Implement ``set_arguments()`` to define command-line arguments
4. Implement ``run()`` to execute the command logic
5. Register your command with a ``Commands`` instance

.. code-block:: python

    class MyCommand(Command):
        DESC = 'My custom command'

        def set_arguments(self, parser):
            parser.add_argument('--option', help='An option')

        def run(self, command_names, option, **kw):
            # Command implementation
            return 0

Creating Command Hierarchies
===========================

You can create nested command structures:

.. code-block:: python

    # Parent command
    parent_commands = Commands(name='parent', entry_points='parent.commands')

    # Subcommand
    class SubCommand(Command):
        DESC = 'A subcommand'

        def run(self, command_names, **kw):
            print('Subcommand executed')
            return 0

    # Register subcommand
    parent_commands.register('sub', SubCommand())

    # Usage: parent sub

Error Handling
=============

The framework provides custom error classes:

* ``CommandError``: Base error for command execution failures
* ``ArgumentError``: Errors related to command-line arguments

Installation
============

.. code-block:: bash

    pip install nagare-commands

To install with all command plugins:

.. code-block:: bash

    pip install nagare-commands[all]

License
=======

BSD License

Copyright (c) 2008-2025 Net-ng.
All rights reserved.

This software is licensed under the BSD License, as described in
the file LICENSE.txt, which you should have received as part of
this distribution.
