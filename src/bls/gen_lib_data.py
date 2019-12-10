"""
    Copyright (C) 2018-2019 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
from pprint import pprint
from .lib_data import LibraryData
from .util import Main, PushDir
import os


class GenerateLibDepencyData(Main):
    def __init_parser__(self, parser):
        parser.add_argument('++boost-root')
        parser.add_argument('++json')
        parser.add_argument('++boostdep')

    def __run__(self):
        lib_data = LibraryData(self.args)
        lib_data.gen_dependency_info(
            self.args.boost_root, boostdep_exe=self.args.boostdep)
        if self.args.json:
            json_out = lib_data.save_dependency_info(self.args.json)
            if self.args.trace:
                print('DEPENDENCY INFO:')
                print(json_out)


class GenerateLibRanksData(Main):
    def __init_parser__(self, parser):
        parser.add_argument('++lib-info')
        parser.add_argument('++buildable', action='store_true')
        parser.add_argument('++json')

    def __run__(self):
        lib_data = LibraryData(self.args)
        lib_data.gen_ranks(self.args.lib_info, buildable=self.args.buildable)
        if self.args.json:
            json_out = lib_data.save_rank_info(self.args.json)
            if self.args.trace:
                print('RANKS INFO:')
                print(json_out)

class GenerateGitHubData(Main):
    def __init_parser__(self, parser):
        parser.add_argument('++json')

    def __run__(self):
        lib_data = LibraryData(self.args)
        lib_data.gen_github_info(os.environ['GH_TOKEN'])
        if self.args.json:
            json_out = lib_data.save_github_info(self.args.json)
            if self.args.trace:
                print('GITHUB INFO:')
                print(json_out)
