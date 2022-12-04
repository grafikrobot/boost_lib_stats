#!/usr/bin/env python3
"""
    Copyright (C) 2018 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
import os.path
from bls.util import Main, PushDir
import json
import urllib.request
import re
import time


class UserStats(Main):
	def __init_parser__(self, parser):
		parser.add_argument("++ghtoken")

	def __run__(self):
		members = []
		members_page = 1
		while members_page != None:
			page = self.gh_get(
				'orgs/boostorg/members?per_page=100&page={0}'.format(members_page))
			print('PAGE:', len(page))
			if len(page) == 0:
				members_page = None
			else:
				members_page += 1
				members.extend(page)
		for i in range(len(members)):
			try:
				# if members[i]['login'] != 'grafikrobot':
				# 	continue
				sponsor_info = self.gh_fetch_sponsor_info(members[i]['login'])
				members[i].update(sponsor_info)
				time.sleep(0.5)
			except Exception as e:
				print('ERROR MEMBER:\n',json.dumps(members[i], indent=2, sort_keys=True))
				raise e
		print('\nBoostORG Members ({0}) Sponsors: ("None" stands for not accepting sponsors.)\n'.format(len(members)))
		can_sponsor = 0
		total_sponsors = 0
		for i in range(len(members)):
			try:
				# if members[i]['login'] != 'grafikrobot':
				# 	continue
				if members[i]['login'] in ['Beman','beman2','boost-commitbot']:
					continue
				print('{name} ({login}): {sponsor_count}'.format_map(members[i]))
				if members[i]['sponsor_count'] != None:
					can_sponsor += 1
					total_sponsors += members[i]['sponsor_count']
			except Exception as e:
				print('ERROR MEMBER:\n',json.dumps(members[i], indent=2, sort_keys=True))
				raise e
		print('\nTotal members looking for sponsorship: {0} (out of {1})'.format(can_sponsor, len(members)))
		print('\nTotal individuals sponsoring members: {0}'.format(total_sponsors))

	def gh_get(self, path):
		req = urllib.request.Request("https://api.github.com/"+path)
		req.add_header('Accept', 'application/vnd.github+json')
		req.add_header('Authorization', 'Bearer {0}'.format(self.args.ghtoken))
		print('GET:', req.get_full_url())
		with urllib.request.urlopen(req) as u:
			return json.loads(u.read())

	def gh_fetch_sponsor_info(self, user):
		info = {'name': None, 'sponsor_count': None}
		req = urllib.request.Request("https://github.com/sponsors/{0}".format(user))
		print('GET:', req.get_full_url())
		with urllib.request.urlopen(req) as u:
			page = u.read().decode('utf-8')

			sponsor_count = re.search(r'<h4 [^>]+>\s+Current\s+sponsors\s+<span [^>]+>\s+([0-9]+)\s+</span>', page, flags=re.IGNORECASE)
			if sponsor_count:
				info['sponsor_count'] = sponsor_count.group(1)
			else:
				sponsor_title = re.search(r'<title>Sponsor @(\w+)', page, flags=re.IGNORECASE)
				if sponsor_title:
					info['sponsor_count'] = 0

			user_name = re.search(r'Become a sponsor to\s+<a [^>]*>\s*([^<]+)</a>', page, flags=re.IGNORECASE)
			if not user_name:
				user_name = re.search(r'itemprop="name"[^>]*>\s+([^<]+)</span>', page, flags=re.IGNORECASE)
			if user_name:
				info['name'] = user_name.group(1).strip()
			if not info['name']:
				info['name'] = user
		return info


if __name__ == "__main__":
    UserStats()
