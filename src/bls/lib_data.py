"""
    Copyright (C) 2018 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
import json
import os.path
from pprint import pprint
from .graph import strongly_connected_components_path
from .util import Commands, PushDir


class LibraryData(Commands):
    def __init__(self, args):
        self.args = args
        self.dependency_info = {}
        self.ranks_info = []

    def gen_dependency_info(self,
                            bin_root,
                            boost_root,
                            boostdep_exe='boostdep'):
        self.dependency_info = {}
        with PushDir(bin_root) as bin_root:
            boostdep = os.path.join(bin_root, boostdep_exe)
        with PushDir(boost_root):
            for lib in self.__check_output__([boostdep,
                                              '--list-modules']).split():
                self.dependency_info[lib] = {
                    'buildable': False,
                    'header_deps': None
                }
            for lib in self.__check_output__([boostdep,
                                              '--list-buildable']).split():
                self.dependency_info[lib]['buildable'] = True
            for lib, deps in self.__parse_deps_output__(
                    self.__check_output__([boostdep,
                                           '--list-dependencies'])).items():
                self.dependency_info[lib]['header_deps'] = sorted(list(deps))
            for lib, deps in self.__parse_deps_output__(
                    self.__check_output__(
                        [boostdep, '--track-sources',
                         '--list-dependencies'])).items():
                self.dependency_info[lib]['source_deps'] = sorted(
                    list(deps - set(self.dependency_info[lib]['header_deps'])))

    def __parse_deps_output__(self, output):
        result = {}
        for line in output.splitlines():
            parts = line.split()
            result[parts[0]] = set(parts[2:])
        return result

    def load_dependency_info(self, lib_deps_file):
        self.dependency_info = self.__load_data__(lib_deps_file)
        if self.args.trace:
            json_out = json.dumps(
                self.dependency_info,
                sort_keys=True,
                indent=2,
                separators=(',', ': '))
            print('LIBRARIES:')
            print(json_out)

    def save_dependency_info(self, lib_deps_file):
        return self.__save_data__(lib_deps_file, self.dependency_info)

    def gen_ranks(self, lib_deps_file, buildable=False):
        self.load_dependency_info(lib_deps_file)
        lib_deps = {}
        for lib, info in self.dependency_info.items():
            deps = set(info['header_deps'])
            if buildable:
                deps = deps + set(info['source_deps'])
            lib_deps[lib] = deps
        lib_levels = []
        while len(lib_deps) > 0:
            lib_level = {
                'index': len(lib_levels),
                'is_cycle': False,
                'libs': set()
            }
            for lib, deps in lib_deps.items():
                if len(deps) == 0:
                    lib_level['libs'].add(lib)
            if len(lib_level['libs']) == 0:
                # We have a cycle at this level. The cycle will be the items
                # with only one dependency.
                lib_level['is_cycle'] = True
                lib_cycle_deps = {}
                for lib, deps in lib_deps.items():
                    lib_cycle_deps[lib] = set(deps)
                for cycle in strongly_connected_components_path(
                        lib_cycle_deps.keys(), lib_cycle_deps):
                    if len(cycle) > 1:
                        if len(lib_level['libs']) == 0 or len(cycle) < len(
                                lib_level['libs']):
                            lib_level['libs'] = set(cycle)
                if len(lib_level['libs']) == 0:
                    if self.args.trace:
                        print("ERROR: NO CYCLE FOUND IN = ", lib_cycle_deps)
                    break
            for lib in list(lib_level['libs']):
                del lib_deps[lib]
                for deps in lib_deps.values():
                    deps.discard(lib)
            if self.args.trace:
                pprint(lib_level)
            lib_levels.append(lib_level)
        if self.args.debug:
            print('RANKS:')
            pprint(lib_levels)
        self.ranks_info = lib_levels

    def load_ranks_info(self, ranks_info_file):
        self.ranks_info = self.__load_data__(ranks_info_file)
        if self.args.trace:
            json_out = json.dumps(
                self.ranks_info,
                sort_keys=True,
                indent=2,
                separators=(',', ': '))
            print('RANKS:')
            print(json_out)
