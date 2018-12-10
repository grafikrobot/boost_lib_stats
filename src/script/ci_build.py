#!/usr/bin/env python3
"""
    Copyright (C) 2018 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
import os.path
from bls.git_tool import Git
from bls.util import Main, PushDir


class CIBuild(Main):
    def __init_parser__(self, parser):
        parser.add_argument('++bin-dir')
        parser.add_argument('++local', action='store_true')

    def __run__(self):
        bin_dir = None
        boost_root_dir = None
        script_dir = None

        with PushDir(self.args.bin_dir) as dir:
            bin_dir = dir
        with PushDir(os.path.join(bin_dir, 'boost_root')) as dir:
            boost_root_dir = dir
        with PushDir('src', 'script') as dir:
            script_dir = dir

        with PushDir('.') as root:
            build_b2_py = os.path.join(script_dir, 'build_b2.py')
            build_bdep_py = os.path.join(script_dir, 'build_boostdep.py')
            clone_boost_py = os.path.join(script_dir, 'clone_boost.py')
            git_switch_py = os.path.join(script_dir, 'git_switch.py')

            if not self.args.local:
                self.__check_call__(
                    [clone_boost_py,
                     '++root=%s' % (boost_root_dir)])
            self.__check_call__([
                git_switch_py,
                '++root=%s' % (boost_root_dir), '++branch=develop'
            ])
            self.__check_call__([
                build_b2_py,
                '++boost-root=%s' % (boost_root_dir),
                '++bin=%s' % (bin_dir)
            ])
            self.__check_call__([
                build_bdep_py,
                '++boost-root=%s' % (boost_root_dir),
                '++bin=%s' % (bin_dir)
            ])


if __name__ == "__main__":
    CIBuild()
