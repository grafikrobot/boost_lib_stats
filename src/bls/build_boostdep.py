"""
    Copyright (C) 2018 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
from .util import Main, PushDir
import os.path


class BuildBoostDep(Main):
    def __init_parser__(self, parser):
        pass

    def __run__(self):
        with PushDir('bin') as bin:
            self.__call__(['rm', '-rf', os.path.join(bin, 'git-boost-tools')])
            self.__check_call__([
                'git', 'clone', '-b', 'develop', '--depth', '1',
                'https://github.com/boostorg/boost.git', 'git-boost-tools'
            ])
            with PushDir('git-boost-tools') as root:
                for lib in ['config', 'filesystem']:
                    self.__check_call__([
                        'git', 'submodule', 'update', '--init',
                        'libs/%s' % (lib)
                    ])
                self.__check_call__(
                    ['git', 'submodule', 'update', '--init', 'libs/config'])
                self.__check_call__(
                    ['git', 'submodule', 'update', '--init', 'tools/build'])
                self.__check_call__(
                    ['git', 'submodule', 'update', '--init', 'tools/boostdep'])
                self.__check_call__([
                    'python', 'tools/boostdep/depinst/depinst.py', '--verbose',
                    'filesystem'
                ])
                self.__check_call__(['./bootstrap.sh'])
                with PushDir('tools', 'boostdep', 'build'):
                    self.__check_call__([os.path.join(root, 'b2'), '-j2'])
                self.__check_call__(['cp', os.path.join(root, 'dist', 'bin', 'boostdep'), os.path.join(bin)])
            self.__check_call__(['cp', os.path.join(root, 'dist', 'bin', 'boostdep'), os.path.join(bin, 'boostdep')])
            self.__call__(['rm', '-rf', os.path.join(bin, 'git-boost-tools')])
