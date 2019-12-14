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
        self.pop_index_table = []

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

    def gen_ranks_graph(self, lib_data_list, lib_data_versions):
        ranks_graph = {'data': [], 'links': []}
        for lib_data_i in range(0, len(lib_data_list)):
            lib_data = lib_data_list[lib_data_i]
            if self.args.trace:
                print('LIB #%s DATA:' % (lib_data_i))
                pprint(lib_data)
            for rank_info in lib_data.rank_info:
                rank_node = {
                    'name': '#%s (%s)' % (rank_info['index'] + 1),
                    'value': len(rank_info['libs'])
                }
                ranks_graph['data'].append(rank_node)
                for lib in rank_info['libs']:
                    lib_node = {
                        'name':
                        '%s (%s)' % (lib, lib_data_versions[lib_data_i]),
                        'value': 1
                    }
                    ranks_graph['data'].append(lib_node)
        return ranks_graph

    def gen_pop_index_table(self, lib_data):
        def pop_index(gh_info):
            return gh_info['forks'] * 1.5 + gh_info[
                'stars'] + gh_info['watchers'] * 2

        tool_names = set([
            'auto_index', 'bcp', 'boostbook', 'boostdep', 'bpm', 'build',
            'docca', 'inspect', 'litre', 'quickbook'])
        tools = []
        tools_value = [0,0,0,0]
        libs = []
        libs_value = [0,0,0,0]

        for lib in sorted(lib_data.github_info.keys()):
            sum_value = None
            if lib in tool_names:
                sum_value = tools_value
            else:
                sum_value = libs_value
            gh_info = lib_data.github_info[lib]
            pop_value = pop_index(gh_info)
            sum_value[0] += pop_value
            sum_value[1] += gh_info['forks']
            sum_value[2] += gh_info['stars']
            sum_value[3] += gh_info['watchers']
            entry = {
                'name': lib,
                'value': [
                    pop_value,
                    gh_info['forks'],
                    gh_info['stars'],
                    gh_info['watchers']]}
            if lib in tool_names:
                tools.append(entry)
            else:
                libs.append(entry)
        self.pop_index_table.append({
            'name': 'Libraries',
            'value': libs_value,
            'children': libs})
        self.pop_index_table.append({
            'name': 'Tools',
            'value': tools_value,
            'children': tools})
