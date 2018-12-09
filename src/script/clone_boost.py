#!/usr/bin/env python3
"""
    Copyright (C) 2018 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
import os
import os.path
from bls.git_tool import Git
from bls.util import Main


class CloneBoost(Main):
    def __init_parser__(self, parser):
        parser.add_argument('++root')
        parser.add_argument('++branch')

    def __run__(self):
        git = Git(self.args)
        if not os.path.exists(self.args.root):
            if not os.path.exists(os.path.dirname(self.args.root)):
                os.makedirs(os.path.dirname(self.args.root))
            git.clone_all('https://github.com/boostorg/boost.git',
                          self.args.root)
        else:
            git.fetch_all(self.args.root)


if __name__ == "__main__":
    CloneBoost()
