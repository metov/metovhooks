"""
Fails if the current git branch matches the one passed in the argument.

This is intended for a workflow where you have a "protected" branch such as
master, which you never directly commit to (presumably you merge pull request
to it instead).

Usage:
    protect_branch BRANCH
"""

from docopt import docopt
from git import Repo

from metovhooks import log


def main() -> int:
    args = docopt(__doc__)
    protbranch = args["BRANCH"]

    repo = Repo(".")
    curbranch = repo.active_branch.name
    if curbranch == protbranch:
        log.error(f'Commits to "{curbranch}" branch are not allowed.')
        return 1
    else:
        log.info(f'Current branch is "{curbranch}", not "{protbranch}" -- good!')
        return 0


if __name__ == "__main__":
    exit(main())
