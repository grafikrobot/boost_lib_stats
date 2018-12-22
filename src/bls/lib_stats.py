"""
    Copyright (C) 2018 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
from pprint import pprint
from .lib_data import LibraryData
from .util import Commands, PushDir


class LibraryStats(Commands):
    def __init__(self, args):
        self.args = args
        self.cycles_table = [['version', 'libs_in_cycles', 'cycles']]

    def gen_cycles_table(self, lib_data_list, lib_data_versions):
        for lib_data_i in range(0, len(lib_data_list)):
            lib_data = lib_data_list[lib_data_i]
            if self.args.trace:
                print('LIB #%s DATA:' % (lib_data_i))
                pprint(lib_data)
            lib_cycle_info = {
                'version': lib_data_versions[lib_data_i],
                'libs_in_cycles': 0,
                'cycles': 0
            }
            for ranks_info in lib_data:
                if ranks_info['is_cycle']:
                    lib_cycle_info['libs_in_cycles'] += len(ranks_info['libs'])
                    lib_cycle_info['cycles'] += 1
            self.cycles_table.insert(1, [
                lib_cycle_info['version'], lib_cycle_info['libs_in_cycles'],
                lib_cycle_info['cycles']
            ])
        if self.args.trace:
            print('CYCLES_TABLE:')
            pprint(self.cycles_table)
