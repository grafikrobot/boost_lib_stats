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
        parser.add_argument('++build-data', action='store_true')
        parser.add_argument('++website-update', action='store_true')

    def __run__(self):
        bin_dir = None
        boost_root_dir = None
        script_dir = None
        data_dir = None

        with PushDir(self.args.bin_dir) as dir:
            bin_dir = dir
            boost_root_dir = os.path.join(bin_dir, 'boost_root')
        with PushDir('src', 'script') as dir:
            script_dir = dir
        with PushDir(bin_dir, 'data') as dir:
            data_dir = dir

        with PushDir('.'):
            build_b2_py = os.path.join(script_dir, 'build_b2.py')
            build_bdep_py = os.path.join(script_dir, 'build_boostdep.py')
            clone_boost_py = os.path.join(script_dir, 'clone_boost.py')
            gen_lib_deps_py = os.path.join(script_dir, 'gen_lib_deps.py')
            gen_lib_ranks_py = os.path.join(script_dir, 'gen_lib_ranks.py')
            git_switch_py = os.path.join(script_dir, 'git_switch.py')

            b2_exe = os.path.join(bin_dir, 'b2_root', 'bin', 'b2')

            if not self.args.local:
                self.__check_call__([
                    clone_boost_py,
                    '++root=%s' % (boost_root_dir), '++trace'
                ])
            self.__check_call__([
                git_switch_py,
                '++root=%s' % (boost_root_dir), '++branch=develop', '++trace'
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

            def gen_lib_data(branch=None, tag=None, rebuild=False):
                label = branch if branch else tag
                print('[GEN LIB DATA %s]' % (label))
                deps_file = os.path.join(data_dir, '%s-deps.json' % (label))
                ranks_headers_file = os.path.join(
                    data_dir, '%s-ranks-headers.json' % (label))
                ranks_build_file = os.path.join(
                    data_dir, '%s-ranks-build.json' % (label))
                if rebuild or not os.path.exists(deps_file):
                    self.__check_call__([
                        git_switch_py,
                        '++root=%s' % (boost_root_dir),
                        '++branch=%s' % (branch)
                        if branch else '++tag=%s' % (tag)
                    ])
                    self.__check_call__([
                        gen_lib_deps_py,
                        '++boost-root=%s' % (boost_root_dir),
                        '++json=%s' % (deps_file),
                        '++boostdep=%s' % (os.path.join(bin_dir, 'boostdep'))
                    ])
                    self.__check_call__([
                        gen_lib_ranks_py,
                        '++lib-info=%s' % (deps_file),
                        '++json=%s' % (ranks_headers_file)
                    ])
                    self.__check_call__([
                        gen_lib_ranks_py,
                        '++lib-info=%s' % (deps_file),
                        '++json=%s' % (ranks_build_file), '++buildable'
                    ])

            if self.args.build_data:
                gen_lib_data(branch='develop', rebuild=True)
                gen_lib_data(branch='master', rebuild=True)
                for v in range(57, 69 + 1):
                    gen_lib_data(tag='boost-1.%s.0' % (v))

            if self.args.website_update:
                self.__check_call__([
                    b2_exe, '-d+2',
                    '--data-dir=%s' % (data_dir), '--versions=57-69,master,develop'
                ])


if __name__ == "__main__":
    CIBuild()
