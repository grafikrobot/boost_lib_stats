"""
    Copyright (C) 2018 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
from .util import Main, PushDir
import os.path
from pprint import pprint
import json
from .graph import strongly_connected_components_path
from .lib_data import LibraryData


class GenerateLibRanksData(Main):
    def __init_parser__(self, parser):
        parser.add_argument('++lib-info')
        parser.add_argument('++buildable', action='store_true')

    def __run__(self):
        lib_data = LibraryData(self.args)
        lib_data.gen_ranks(self.args.lib_info, buildable=self.args.buildable)
