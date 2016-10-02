#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: manage script for application instance start and other function

import os

# create application instance
from application import create_application
application = create_application(os.getenv('CONFIG') or 'default')

# init application by Manager
from flask_script import Manager
manager = Manager(application)

# init application by Migrate
from application import database
from flask_migrate import Migrate
migrate = Migrate(application, database)

# add shell command support
from application.models import Role, User
from flask_script import Shell
def make_shell_context():
    return dict(application=application, database=database, Role=Role, User=User)

# add command to shell
from flask_migrate import MigrateCommand
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('database', MigrateCommand)

# add unit test command to shell
@manager.command
def test():
    import unittest
    test = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(test)

# start application instance
if __name__ == '__main__':
    manager.run()

