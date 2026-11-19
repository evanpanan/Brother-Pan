#!/usr/bin/env python3
"""Commit verified library/rule changes; push only when explicitly requested/authorized."""
import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = ['SKILL.md', 'README.md', 'AGENTS.md', '.gitignore', '.github', 'agents', 'config', 'references', 'scripts', 'tests', 'library', 'assets', 'examples', 'docs', 'ASSETS.md', 'CHANGELOG.md', 'requirements-voice.txt']


def git(*args, capture=True):
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
    return subprocess.run(['git', '-C', str(ROOT), *args], check=True, text=True, capture_output=capture, env=env).stdout.strip() if capture else subprocess.run(['git', '-C', str(ROOT), *args], check=True, env=env)


def main(message, push):
    if not (ROOT / '.git').exists():
        raise ValueError('Use an authorized maintenance checkout, not an installed snapshot')
    origin = git('remote', 'get-url', 'origin')
    if origin not in {'git@github.com:evanpanan/Brother-Pan.git', 'https://github.com/evanpanan/Brother-Pan.git', 'https://github.com/evanpanan/Brother-Pan'}:
        raise ValueError('Unexpected origin; maintain your fork explicitly with normal git commands')
    subprocess.run([sys.executable, str(ROOT / 'scripts/check_repository.py')], check=True)
    subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', str(ROOT / 'tests'), '-v'], cwd=ROOT, check=True)
    branch = git('symbolic-ref', '--short', 'HEAD')
    if push:
        git('fetch', 'origin')
        remote = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', '--verify', f'refs/remotes/origin/{branch}'], capture_output=True, text=True)
        if remote.returncode == 0:
            ancestor = subprocess.run(['git', '-C', str(ROOT), 'merge-base', '--is-ancestor', f'origin/{branch}', 'HEAD'], capture_output=True)
            if ancestor.returncode != 0:
                raise ValueError('Remote history changed; inspect and reconcile without force-push')
    staged = git('diff', '--cached', '--name-only').splitlines()
    if any(name.split('/')[0] not in ALLOWED for name in staged):
        raise ValueError('Unrelated staged changes; refusing to include them')
    git('add', '--', *(x for x in ALLOWED if (ROOT / x).exists()))
    if git('diff', '--cached', '--name-only'):
        git('commit', '-m', message, capture=False)
    commit = git('rev-parse', 'HEAD')
    if push:
        git('push', '-u', 'origin', branch, capture=False)
        remote = git('ls-remote', 'origin', f'refs/heads/{branch}').split()[0]
        if remote != commit:
            raise ValueError('Remote verification failed; do not report a successful sync')
    print(('REMOTE_SYNCED ' if push else 'LOCAL_ONLY ') + commit)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--message', required=True)
    parser.add_argument('--push', action='store_true', help='Requires maintainer authorization; never force-pushes')
    args = parser.parse_args()
    main(args.message, args.push)
