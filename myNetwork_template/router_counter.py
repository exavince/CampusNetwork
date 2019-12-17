#! /usr/bin/env pytho,3

import json

if __name__ == "__main__":
	with open('ospf6d.json') as conf_ospf:
		info_load = json.load(conf_ospf)
		router_count = len(info_load)
		print(router_count)
