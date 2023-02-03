"""
    Copyright (C) 2018-2023 René Ferdinand Rivera Morell.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
import json
import os.path
from pprint import pprint
from .graph import strongly_connected_components_path
from .util import Commands, PushDir
import urllib.parse
import urllib.request

class LibraryData(Commands):
    def __init__(self, args):
        self.args = args
        self.dependency_info = {}
        self.ranks_info = []
        self.github_info = {}

    def gen_dependency_info(self, boost_root, boostdep_exe='boostdep'):
        self.dependency_info = {}
        with PushDir(boost_root):
            for lib in self.__check_output__([boostdep_exe,
                                              '--list-modules']).split():
                self.dependency_info[lib] = {
                    'buildable': False,
                    'header_deps': None
                }
            for lib in self.__check_output__(
                [boostdep_exe, '--list-buildable']).split():
                self.dependency_info[lib]['buildable'] = True
            for lib, deps in self.__parse_deps_output__(
                    self.__check_output__(
                        [boostdep_exe, '--list-dependencies'])).items():
                self.dependency_info[lib]['header_deps'] = sorted(list(deps))
            for lib, deps in self.__parse_deps_output__(
                    self.__check_output__([
                        boostdep_exe, '--track-sources', '--list-dependencies'
                    ])).items():
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
                deps.update(info['source_deps'])
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
            lib_level['libs'] = sorted(list(lib_level['libs']))
            lib_levels.append(lib_level)
        if self.args.debug:
            print('RANKS INFO:')
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
            print('RANKS INFO:')
            print(json_out)

    def save_rank_info(self, ranks_info_file):
        return self.__save_data__(ranks_info_file, self.ranks_info)

    def gen_github_info(self, gh_token):
        self.github_info = {}
        query_fmt = '''\
{
  organization(login: "boostorg") {
    repositories(first: 100, orderBy: {field: NAME, direction: ASC} %s) {
      edges {
        cursor
        repository: node {
          name
          forkCount
          stargazers(first: 1) {
            totalCount
          }
          watchers(first: 1) {
            totalCount
          }
        }
      }
    }
  }
}
'''
        exclude = set([
            'admin', 'boost', 'boost-ci', 'boost_install', 'documentation-fixes',
            'headers', 'mincmake', 'release-tools', 'regression', 'website',
            'wiki'])
        cursor = None
        while cursor != "-":
            data = {}
            if cursor == None:
                data['query'] = query_fmt % ("")
            else:
                data['query'] = query_fmt % (', after: "%s"' % (cursor))
            # data = urllib.parse.urlencode(data)
            data = json.dumps(data)
            if self.args.trace:
                print('DATA:')
                print(data)
            data = data.encode('utf-8')
            req = urllib.request.Request(
                'https://api.github.com/graphql',
                data,
                headers={'Authorization': 'token %s' % (gh_token)})
            resp = urllib.request.urlopen(req)
            resp_data = resp.read()
            data = json.loads(resp_data.decode())
            cursor = "-"
            for lib_data in data['data']['organization']['repositories']['edges']:
                cursor = lib_data['cursor']
                if not lib_data['repository']['name'] in exclude:
                    self.github_info[lib_data['repository']['name']] = {
                        'forks': lib_data['repository']['forkCount'],
                        'stars': lib_data['repository']['stargazers']['totalCount'],
                        'watchers': lib_data['repository']['watchers']['totalCount']
                        }
        if self.args.debug:
            print('GITHUB INFO:')
            pprint(self.github_info)

    def load_github_info(self, github_info_file):
        self.github_info = self.__load_data__(github_info_file)
        if self.args.trace:
            json_out = json.dumps(
                self.github_info,
                sort_keys=True,
                indent=2,
                separators=(',', ': '))
            print('GITHUB INFO:')
            print(json_out)

    def save_github_info(self, github_info_file):
        return self.__save_data__(github_info_file, self.github_info)
