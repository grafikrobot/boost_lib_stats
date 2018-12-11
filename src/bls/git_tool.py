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
        self.__git__('submodule', 'foreach', 'git', *cmd)

    def status(self):
        self.__git_sub__('status', '-bsu', '--ignored')

    def clean(self):
        self.__git_sub__('clean', '-dxff')

    def switch(self, branch):
        self.clean()
        self.__git__('checkout', '--force', branch)
        self.__git__('reset', '--hard')
        self.__git__('submodule', 'update', '--init', '--no-fetch',
                     '--checkout', '--force', '--recursive')
        self.__git_sub__('reset', '--hard')
        self.__git_sub__('clean', '-dxff')

    def clone_all(self, url, dir):
        self.__git__('clone', '--recurse-submodules', '--', url, dir)

    def fetch_all(self, dir):
        with PushDir(dir):
            self.__git__('fetch', '--all', '--prune', '--tags',
                         '--recurse-submodules')
