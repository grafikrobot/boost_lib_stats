#!/usr/bin/env python3
"""
    Copyright (C) 2018 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
import os
import os.path
from bls.lib_stats import LibraryStats
from bls.lib_data import LibraryData
from bls.util import Main, PushDir
import json


class GneLibStats(Main):
    def __init_parser__(self, parser):
        parser.add_argument('++data-dir')
        parser.add_argument('++versions')
        parser.add_argument('++cycles-table-json')

    def __run__(self):
        lib_data_headers = []
        lib_data_build = []
        lib_data_versions = []
        with PushDir(self.args.data_dir):
            for v in self.args.versions.split(','):
                v = v.split('-')
                if len(v) > 1:
                    for r in range(int(v[0]), int(v[1]) + 1):
                        data_headers = LibraryData(self.args)
                        data_headers.load_ranks_info(
                            'boost-1.%s.0-ranks-headers.json' % (r))
                        data_build = LibraryData(self.args)
                        data_build.load_ranks_info(
                            'boost-1.%s.0-ranks-build.json' % (r))
                        lib_data_versions.append('1.%s.0' % (r))
                        lib_data_headers.append(data_headers.ranks_info)
                        lib_data_build.append(data_build.ranks_info)
                else:
                    data_headers = LibraryData(self.args)
                    data_headers.load_ranks_info(
                        '%s-ranks-headers.json' % (v[0]))
                    data_build = LibraryData(self.args)
                    data_build.load_ranks_info('%s-ranks-build.json' % (v[0]))
                    lib_data_versions.append(v[0])
                    lib_data_headers.append(data_headers.ranks_info)
                    lib_data_build.append(data_build.ranks_info)
        lib_stats_headers = LibraryStats(self.args)

        if self.args.cycles_table_json:
            lib_stats_headers.gen_cycles_table(lib_data_headers,
                                               lib_data_versions)
            with open(self.args.cycles_table_json, "w") as f:
                f.write(
                    json.dumps(
                        lib_stats_headers.cycles_table,
                        sort_keys=True,
                        indent=4))


if __name__ == "__main__":
    GneLibStats()
