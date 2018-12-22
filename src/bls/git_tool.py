"""
    Copyright (C) 2018 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
import os.path
from pprint import pprint
from .util import Commands, PushDir


class Git(Commands):
    def __init__(self, args):
        self.args = args

    def __git__(self, *cmd):
        self.__check_call__(['git'] + list(cmd))

    def __git_sub__(self, *cmd):
        self.__git__(*cmd)
        self.__git__('submodule', '--quiet', 'foreach', 'git', *cmd)

    def status(self):
        print("[GIT STATUS]")
        self.__git__('status', '-bsu', '--ignored')
        self.__git__('submodule', 'status')

    def clean(self):
        self.__git_sub__('clean', '-qdxff')

    def switch(self, branch=None, tag=None):
        print('[GIT SWITCH %s]' % (branch if branch else tag))
        self.__git__('reset', '-q', '--hard')
        self.__git__('submodule', '--quiet', 'deinit', '--force', '--all')
        self.clean()
        self.__git__('checkout', '-q', '--force', '--no-recurse-submodules',
                     'develop')
        self.__call__(['git', 'branch', '-D', 'temp'])
        if branch:
            self.__git__('branch', '--no-track', '-f', 'temp', 'origin/' + branch)
        else:
            self.__git__('branch', '--no-track', '-f', 'temp', tag)
        self.__git__('checkout', '-q', '--force', '--no-recurse-submodules',
                     'temp')
        self.__git__('submodule', 'update', '--init', '--no-fetch',
                     '--recursive')

    def clone_all(self, url, dir):
        self.__git__('clone', '--recurse-submodules', '--', url, dir)

    def fetch_all(self, dir):
        with PushDir(dir):
            self.__git__('fetch', '--all', '--prune', '--tags',
                         '--recurse-submodules')
