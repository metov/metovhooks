"""
Compares the current version to the one in a baseline branch. If the current
version is higher, exist with 0, otherwise exits with 1. Errors will raise Python
exceptions.

This is intended for a workflow where you have some long living "baseline"
branch (eg. dev) and develop features in feature branches, with the convention that
feature branches must have a higher version than the baseline.

Currently, only the following methods of specifying a version are supported:
* setup.py
* pyproject.toml file managed by https://github.com/python-poetry/poetry

Usage:
    require_version_bump REFERENCE_BRANCH VERSION_FILE
"""
import logging
from pathlib import Path
from typing import Callable

import toml
from docopt import docopt
from packaging.version import Version
from pre_commit_hooks.util import cmd_output
from metovhooks import log


def main() -> int:
    args = docopt(__doc__)
    basebranch = args["REFERENCE_BRANCH"]
    pv = Path(args["VERSION_FILE"])

    parse = get_parser(pv)
    curver = parse(pv.read_text())
    basever = parse(get_reference_file(pv, basebranch))

    if curver > basever:
        log.info(f"The current version {curver} > {basebranch} version {basever}.")
        return 0
    else:
        log.error(
            f"The current version is {curver} while the one on the "
            f"{basebranch} is {basever} -- did you forget to bump it?"
        )
        return 1


def get_parser(path) -> Callable[[str], Version]:
    """Determine the appropriate parse method for given file."""
    if path.name == "setup.py":
        # noinspection PyTypeChecker
        return lambda _: Parsers.setup_py(str(path))
    elif path.name == "pyproject.toml":
        return Parsers.pyproject_toml

    raise RuntimeError(f"Don't know how to parse: {path}")


class Parsers:
    @staticmethod
    def setup_py(path: str):
        # https://stackoverflow.com/a/39579627/15629542
        return cmd_output("python", path, "--version")

    @staticmethod
    def pyproject_toml(contents):
        t = toml.loads(contents)
        return t["tool"]["poetry"]["version"]


def get_reference_file(path: Path, branch: str):
    return cmd_output("git", "show", f"{branch}:{path}")


if __name__ == "__main__":
    exit(main())
