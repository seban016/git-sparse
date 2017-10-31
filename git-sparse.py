#! /usr/bin/env python
"""
Git helper command to make sparse checkouts easier.

Usage:
$ cd <git-repository>
$ git sparse                         # opens 'sparse-checkout' file for edit
$ git sparse add <path1> <path2> ... # add <path1>...<pathn> (alternative to 'git sparse')
$ git sparse update                  # update the working tree to show paths

Example workflow when cloning a new repo:
$ git clone -b <branch> -n --depth=1 <repo-url>  # shallow clone of one branch (no history)
$ cd <repo>
$ git sparse add <path1> <path2> ... <pathn>
$ git sparse update

Note: 
- To see the whole repository again, add "/*" to the sparse-checkout-file and run "git sparse update".
- To change the default editor, set the $EDITOR environmental variable, e.g.:
  $ export EDITOR=nano
"""
from __future__ import print_function

import sys
import os

from subprocess import (check_output, call,
                        CalledProcessError)


def issparse():
    """Check if git repsitory is configured for sparse checkouts."""
    gitconf = check_output(['git', 'config', '--list'])
    if 'sparsecheckout=true' in gitconf.lower():
        return True
    else:
        return False


def make_sparse(gitpath):
    """Configure git repository at <gitpath> to accept
    sparse checkouts."""
    if not issparse():
        print('Sparse checkout not active.')
        print('Setting core.sparseCheckout to true...')
        call(['git', 'config',
              'core.sparseCheckout', 'true'])


def touch_checkout_file(gitpath):
    """Check that path and sparse-checkout file exist, otherwise create it."""
    infopath = gitpath + '/.git/info'
    if not os.path.exists(infopath):
        try:
            os.makedirs(infopath)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    open(infopath + '/sparse-checkout', 'a').close()
    
    
def edit(filename):
    """Open <filename> in default text editor. 

    Opens either the editor defined by the
    $EDITOR environmental variable, or if not defined, 
    the OS-defined preferred editor."""
    try:
        call([os.environ['EDITOR'], filename])
    except KeyError:
        call(['xdg-open', filename])


def open_checkout_file(gitpath):
    """Open sparse-checkout-file for repo at <gitpath>
    using preferred text editor."""
    print("Opening text editor... ")
    print("Add paths to checkout, then save and close.")
    touch_checkout_file(gitpath) # in case no file
    edit(gitpath + '/.git/info/sparse-checkout')


def update_worktree():
    """Update worktree according to content in sparse-checkout file."""
    call(['git', 'read-tree', '-mu', 'HEAD'])


def add_sparse(gitpath, path):
    """Write <path> to sparse-checkout-file in repo at <gitpath>."""
    with open(gitpath + '/.git/info/sparse-checkout', 'a') as f:
        print(path, file=f)


def gitroot():
    """Return root path of current git repository."""
    try:
        root = check_output(['git', 'rev-parse',
                                '--show-toplevel']).strip()
    except CalledProcessError:
        # "git sparse" called outside git repository
        print(__doc__)
        sys.exit(0)
    return root


def main():
    msg_to_update = ('Run "git sparse update" to see changes.')
    gitpath = gitroot()
    arguments = sys.argv
    try:
        if arguments[1] == 'update':
            update_worktree()
        elif arguments[1] == 'add':
            make_sparse(gitpath)
            touch_checkout_file(gitpath)
            for path in arguments[2:]:
                add_sparse(gitpath, path)
            print('Done!')
            print(msg_to_update)
        elif arguments[1] == 'help' or len(arguments) > 1:
            # help or argument not recognized
            print(__doc__)
    except IndexError: # "git sparse" called with no arguments.
        make_sparse(gitpath)
        open_checkout_file(gitpath)
        print(msg_to_update)


if __name__ == '__main__':
    main()
