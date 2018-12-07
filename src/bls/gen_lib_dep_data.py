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
        parser.add_argument('++boostroot')
        parser.add_argument('++json')

    def __run__(self):
        lib_data = LibraryData(self.args)
        with PushDir('bin') as bin:
            bin_root = bin
        lib_data.gen_dependency_info(bin_root, self.args.boostroot)
        if self.args.json:
            json_out = lib_data.save_dependency_info(self.args.json)
        if self.args.trace:
            print('LIBRARIES:')
            print(json_out)
