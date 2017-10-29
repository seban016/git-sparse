# git sparse
`git sparse` is a helper command to make sparse checkouts easier.

Let's say you have a big repository, but you are only interested in `<repo>/directory-one/` and `<repo>/directory-two/`.
Then all you have to do is:
```
$ cd <path-to-repo>
$ git sparse add "/directory-one" "/directory-two"
$ git sparse update
```
And all you will see in the working tree are those two directories and their corresponding content.

Usage:
```
$ cd <path-to-repo>
$ git sparse                         # opens 'sparse-checkout' file for edit
$ git sparse add <path1> <path2> ... # add <path1>...<pathn> (alternative to 'git sparse')
$ git sparse update                  # updates the working tree
```
Example workflow when cloning a new repo:
```
$ git clone -b <branch> -n --depth=1 <repo-url>  # shallow clone of one branch (no history)
$ cd <repo>
$ git sparse add <path1> <path2> ... <pathn>
$ git sparse update
$ # use git push, git pull, etc., as usual.
```
Note: To see the whole repository again, add `/*` to the
sparse-checkout-file:
```
$ git sparse add "/*" && git sparse update
```

# Requirements
A Linux environment with Python installed.

# Installation
1. Make sure to have a `bin/` directory in your home directory and that it is included in the path, e.g.:
```
$ mkdir ~/.local/bin
$ PATH=~/.local/bin:$PATH
```
2. Copy `git-sparse.py` to the above `bin/` directory and remove the `.py` ending. Also make sure it's executable:
```
$ cp git-sparse.py ~/.local/bin/git-sparse 
$ chmod a+x ~/.local/bin/git-sparse
```
Now you can call `git sparse` from wherever you want. If `~/.local/bin/` wasn't on the path before, you might want to add
`PATH=~/.local/bin:$PATH` to your `~/.bashrc`.
