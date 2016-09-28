import sys
from flask import url_for
from flask.ext.script import Manager, Command, Option, Server

from multivac import create_app

app = create_app()
manager = Manager(app)


@manager.command
def worker():
    from flask.ext.rq import get_worker
    get_worker().work()


@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(
            rule.endpoint, methods, url))
        output.append(line)


class Test(Command):
    option_list = (
        Option('--path', '-n', dest='test_path', default=".", required=False),
    )

    def run(self, test_path="."):
        import unittest
        tests = unittest.TestLoader().discover(test_path)
        ret = unittest.TextTestRunner(verbosity=2).run(tests).wasSuccessful()
        sys.exit(not ret)


if __name__ == "__main__":

    manager.add_command('test', Test())
    manager.add_command('runserver', Server('0.0.0.0', port=5000))
    manager.run()