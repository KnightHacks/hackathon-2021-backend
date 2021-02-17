# -*- coding: utf-8 -*-
"""
    src.__main__
    ~~~~~~~~~~~~
    Handles arguments from the cli and runs the app.

    Functions:

        main()
        test()

    Misc Variables:

        cli

"""
import os
import unittest
from flask.cli import FlaskGroup
from src import app

os.environ["FLASK_APP"] = "src.__main__:main()"


cli = FlaskGroup(app)


def main():
    return app


@cli.command()
def test():
    """Run tests"""
    tests = unittest.TestLoader().discover("tests", pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    cli()
