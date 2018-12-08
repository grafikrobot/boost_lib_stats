"""
    Copyright (C) 2018 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
from pprint import pprint
from .lib_data import LibraryData
from .util import Main, PushDir


class GenerateLibDepencyData(Main):
    def __init_parser__(self, parser):
        parser.add_argument('++boost-root')
        parser.add_argument('++json')

    def __run__(self):
        lib_data = LibraryData(self.args)
        with PushDir('bin') as bin:
            bin_root = bin
        lib_data.gen_dependency_info(bin_root, self.args.boost_root)
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
