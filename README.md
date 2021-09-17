# Personal Git Hooks
This directory contains some scripts designed for use as [git hooks](https://git-scm.com/docs/githooks). They should have a pretty simple command line interface (see docstrings for details) so usage should be self-explanatory.

## Installation
You can install the entire hook package with `pip install metovhooks`.

## Usage
You can run the scripts manually in your shell. For example, `protect_branch master` will exit with code 1 if the current git branch is `master` and exit with 0 if not (if your shell does not display exit codes, you can check the code with `echo $?`).

Of course, it isn't very useful to run these manually. You can just type `git status` and see what the current branch is. But these scripts are intended to be used as git hooks. This is why the commands themselves are verbose - you'd be reading them much more often than typing them. However, you still have the option of just typing them manually -- a useful thing when troubleshooting.

If you're looking for a tool to help you manage git hooks, check out [yaghm](https://github.com/metov/yaghm). This repository also contains a yaghm config defining the hooks I use when developing it. This is optional; it won't actually do anything until you install yaghm and enable them.
