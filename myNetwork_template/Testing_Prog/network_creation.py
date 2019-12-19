#! /usr/bin/env python3

import time
import pexpect
import json

if __name__ == '__main__':

    prompt = [r'vagrant@group3:~.*',r'-bash-4\.2\$',r'-bash-4\.3\$',r'bash-4\.3\#',r'group3\#',r'group\d+\#',r'P2\#',r'\#']

    child = pexpect.spawn('ssh lingi2142vm', encoding='utf-8', timeout=120)
    child.sendline('cd Group_folder/')
    child.sendline('cd CampusNetwork/')
    child.sendline('cd myNetwork_template/')

    ask_rebuild = input("Build Network Config ? (y/n) : ")
    if ask_rebuild == "y":
        child.sendline('./build_network.sh')
    else:
        pass

    #net_cfg = input("Config File of the network: ")
    net_cfg = "myNetwork_cfg"
    child.sendline('sudo ./create_network.sh ' + net_cfg)
    idx = child.expect(['The network has been started!','File exists','No such file or directory'])
    if idx == 0:
        print("Network started")
    elif idx == 1:
        print("The network is up")
    elif idx == 2:
        print("No such file or directory")
    else:
        print("FAILED")

    child.sendline('exit')

