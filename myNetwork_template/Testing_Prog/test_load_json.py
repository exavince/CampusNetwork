#! /usr/bin/env pytho,3

import json

if __name__ == "__main__":
        with open('../start.json') as conf_ospf:
                info_load = json.load(conf_ospf)[1]
                router_count = len(info_load)
                print(info_load['ip'])
