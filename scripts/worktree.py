#!/usr/bin/env python3
"""Dharma3 worktree helper — isolation for parallel operating agents.

Each task in a wave gets its own git worktree + branch so parallel agents never collide.
Thin, deterministic wrapper over `git worktree`. Zero deps.

Usage:
    python3 scripts/worktree.py create <branch> [path]   # default path: .d3-worktrees/<branch>
    python3 scripts/worktree.py merge  <branch>          # merge branch into current, --no-ff
    python3 scripts/worktree.py remove <branch> [path]   # remove worktree + delete branch
    python3 scripts/worktree.py list
"""
import subprocess
import sys
from pathlib import Path


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(r.returncode)
    return r


def default_path(branch):
    safe = branch.replace("/", "-")
    return f".d3-worktrees/{safe}"


def cmd_create(branch, path=None):
    path = path or default_path(branch)
    Path(".d3-worktrees").mkdir(exist_ok=True)
    git("worktree", "add", path, "-b", branch)
    print(f"✓ worktree {path}  (branch {branch})")


def cmd_merge(branch):
    git("merge", "--no-ff", "--no-edit", branch)
    print(f"✓ merged {branch}")


def cmd_remove(branch, path=None):
    path = path or default_path(branch)
    git("worktree", "remove", path, "--force", check=False)
    git("branch", "-D", branch, check=False)
    print(f"✓ removed worktree {path} + branch {branch}")


def cmd_list():
    print(git("worktree", "list").stdout, end="")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    sub = sys.argv[1]
    rest = sys.argv[2:]
    if sub == "create" and rest:
        cmd_create(*rest[:2])
    elif sub == "merge" and rest:
        cmd_merge(rest[0])
    elif sub == "remove" and rest:
        cmd_remove(*rest[:2])
    elif sub == "list":
        cmd_list()
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
