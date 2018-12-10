"""
    Copyright (C) 2018 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
from .git_tool import Git
from .util import Main, PushDir
import os.path


class BuildB2(Main):
    def __init_parser__(self, parser):
        parser.add_argument('++rebuild', action='store_true')
        parser.add_argument('++boost-root')
        parser.add_argument('++bin-dir')

    def __run__(self):
        git = Git(self.args)
        with PushDir(self.args.bin_dir) as bin:
            if not os.path.exists(
                    os.path.join(bin, 'b2_root', 'bin',
                                 'b2')) or self.args.rebuild:
                with PushDir(self.args.boost_root):
                    git.clean()
                with PushDir(self.args.boost_root, 'tools', 'build'):
                    self.__check_call__(['./bootstrap.sh'])
                    self.__check_call__([
                        './b2', 'install',
                        '--prefix=%s' % (os.path.join(bin, 'b2_root'))
                    ])


class BuildBoostDep(Main):
    def __init_parser__(self, parser):
        parser.add_argument('++rebuild', action='store_true')
        parser.add_argument('++boost-root')
        parser.add_argument('++bin-dir')

    def __run__(self):
        git = Git(self.args)
        with PushDir(self.args.bin_dir) as bin:
            if not os.path.exists(os.path.join(
                    bin, 'boostdep')) or self.args.rebuild:
                with PushDir(self.args.boost_root) as root:
                    git.clean()
                    self.__check_call__(['./bootstrap.sh'])
                    with PushDir('tools', 'boostdep', 'build'):
                        self.__check_call__([os.path.join(root, 'b2'), '-j2'])
                    self.__check_call__([
                        'cp',
                        os.path.join(root, 'dist', 'bin', 'boostdep'),
                        os.path.join(bin)
                    ])
                    self.__check_call__([
                        'cp',
                        os.path.join(root, 'dist', 'bin', 'boostdep'),
                        os.path.join(bin, 'boostdep')
                    ])
