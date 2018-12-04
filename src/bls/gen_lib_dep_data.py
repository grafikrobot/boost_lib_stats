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


class GenerateLibDepencyData(Main):
    def __init_parser__(self, parser):
        parser.add_argument('++boostroot')
        parser.add_argument('++json')

    def __run__(self):
        lib_info = {}
        with PushDir('bin') as bin:
            boostdep = os.path.join(bin, 'boostdep')
        with PushDir(self.args.boostroot):
            for lib in self.__check_output__([boostdep,
                                              '--list-modules']).split():
                lib_info[lib] = {'buildable': False, 'header_deps': None}
            for lib in self.__check_output__([boostdep,
                                              '--list-buildable']).split():
                lib_info[lib]['buildable'] = True
            for lib, deps in self.__parse_deps_output__(
                    self.__check_output__([boostdep,
                                           '--list-dependencies'])).items():
                lib_info[lib]['header_deps'] = list(deps)
            for lib, deps in self.__parse_deps_output__(
                    self.__check_output__(
                        [boostdep, '--track-sources',
                         '--list-dependencies'])).items():
                lib_info[lib]['source_deps'] = list(
                    deps - set(lib_info[lib]['header_deps']))
        json_out = json.dumps(
            lib_info, sort_keys=True, indent=2, separators=(',', ': '))
        if self.args.trace:
            print('LIBRARIES:')
            print(json_out)
        if self.args.json:
            with open(self.args.json, "w") as f:
                f.write(json_out)

    def __parse_deps_output__(self, output):
        result = {}
        for line in output.splitlines():
            parts = line.split()
            result[parts[0]] = set(parts[2:])
        return result
