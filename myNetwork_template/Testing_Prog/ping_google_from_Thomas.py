#! /usr/bin/env python3

import pexpect
import json

def trim_from_start(text, char):
    for i in range(0, len(text)):
        if text[i] == char:
            return text[i:]
    return text


def trim_from_end(text, char):
    str_len = len(text)
    j = 0
    for i in range(str_len - 1, -1, -1):
        if text[i] == char:
            return text[:-j]
        j += 1

    return text

if __name__ == '__main__':

    prompt = [r'vagrant@group3:~.*',r'-bash-4\.2\$',r'-bash-4\.3\$',r'bash-4\.3\#',r'group3\#',r'P2\#',r'\#']

    child = pexpect.spawn('ssh lingi2142vm', encoding='utf-8', timeout=120)
    child.expect('\r\n')
    child.expect(prompt)
    child.sendline('cd Group_folder/')
    child.expect('\r\n')
    child.expect(prompt)
    child.sendline('cd CampusNetwork/')
    child.expect('\r\n')
    child.expect(prompt)
    child.sendline('cd myNetwork_template/')
    child.expect('\r\n')
    child.expect(prompt)

    net_cfg = input("Config File of the network: ")
    child.sendline('sudo ./create_network.sh ' + net_cfg)
    child.expect('\r\n')
    idx = child.expect(['The network has been started!','File exists','No such file or directory'])
    child.expect(prompt)
    if idx == 0:
        pass
    elif idx == 1:
        pass
    elif idx == 2:
        print("No such file or directory")
        child.sendline('exit')
    else:
        print("FAILED")
        child.sendline('exit')

    net_rep = input("Rep File of the network: ")
    test_router = input("Name of the router to test: ")
    child.sendline('sudo ./connect_to.sh ' + net_rep + ' ' + test_router)
    child.expect('\r\n')
    idx = child.expect([r'bash-4\.3\#','Network is unreachable'])
    if idx == 1:
        print("Network is unreachable")
        child.sendline('exit')
    else:

        child.sendline('ping6 -c 5 -i 1 2001:4860:4860::8888')
        child.expect('\r\n')
        idx = child.expect(['100% packet loss'])
        child.expect(prompt)

        if idx == 0:
            print("Unable to ping Google")
        else:
            print("Able to ping Google")
        child.sendline('exit')

