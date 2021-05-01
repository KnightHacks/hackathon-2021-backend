# -*- coding: utf-8 -*-
# noqa: E402
"""
    src.__main__
    ~~~~~~~~~~~~
    Handles arguments from the cli and runs the app.

    Functions:

        main()
        test()

    Misc Variables:

        cli
        test_present

"""
from src import app
from flask.cli import FlaskGroup
import os
try:
    import pytest
    test_present = True
except ImportError:  # pragma: no cover
    test_present = False

os.environ["FLASK_APP"] = "src.__main__:main()"

cli = FlaskGroup(app)


def main():
    return app


@cli.command()
def test():
    """Run tests"""
    if test_present:
        pytest.main(["--doctest-modules", "--junitxml=junit/test-results.xml"])
    else:  # pragma: no cover
        app.logger.error("Module PyTest is not installed! Install dev dependencies before testing!")  # noqa: E501


if __name__ == "__main__":
    cli()
