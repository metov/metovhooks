"""
Compares the current version to the one in a baseline branch. The exit code
will be:
* 0 if current version is higher
* 1 if current version is not higher
* 2 if the version could not be parsed from given files

This is intended for a workflow where you have some long living "baseline"
branch (eg. dev) and develop features in feature branches, with the convention
that feature branches must have a higher version than the baseline.

Currently, only the following methods of specifying a version are supported:
* setup.py
* pyproject.toml file managed by https://github.com/python-poetry/poetry

Usage:
    require_version_bump REFERENCE_BRANCH VERSION_FILE
"""
import re
from pathlib import Path

import toml
from docopt import docopt
from pre_commit_hooks.util import cmd_output

from metovhooks import log


def main():
    args = docopt(__doc__)
    version_file = Path(args["VERSION_FILE"])
    ref_branch = args["REFERENCE_BRANCH"]
    check_version(version_file, ref_branch)


def check_version(version_file, base_branch):
    cur_file, ref_file = read_version_files(version_file, base_branch)

    cur_raw = parse_version_file(cur_file, version_file.name)
    ref_raw = parse_version_file(ref_file, version_file.name)

    # TODO: Actually parse the version here
    cur_ver = cur_raw
    ref_ver = ref_raw

    if cur_ver > ref_ver:
        log.info(f"The current version {cur_ver} > {base_branch} version {ref_ver}.")
        exit(0)
    else:
        log.error(
            f"The current version is {cur_ver} while the one on the "
            f"{base_branch} is {ref_ver} -- did you forget to bump it?"
        )
        exit(1)


def read_version_files(version_file: Path, reference_branch: str):
    cur_file = version_file.read_text()
    ref_file = cmd_output("git", "show", f"{reference_branch}:{version_file}")
    return cur_file, ref_file


def parse_version_file(contents: str, version_file_name: str) -> str:
    try:
        if version_file_name == "setup.py":
            return parse_setup_py(contents)
        elif version_file_name == "pyproject.toml":
            return parse_pyproject_toml(contents)
        else:
            RuntimeError(f"Don't know how to parse: {version_file_name}")
    except VersionParsingError:
        log.critical("No version found in file.")
        exit(2)


class VersionParsingError(Exception):
    pass


def parse_setup_py(contents):
    r = r"version\s*=\s*['\"]([^'\"]+)['\"]"
    m = re.search(r, contents)
    return m[1]


def parse_pyproject_toml(contents):
    t = toml.loads(contents)
    return t["tool"]["poetry"]["version"]


if __name__ == "__main__":
    main()
