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
import pytest
from flask.cli import FlaskGroup
from src import app

os.environ["FLASK_APP"] = "src.__main__:main()"

cli = FlaskGroup(app)


def main():
    return app


@cli.command()
def test():
    """Run tests"""
    pytest.main(["--doctest-modules", "--junitxml=junit/test-results.xml"])


if __name__ == "__main__":
    cli()
