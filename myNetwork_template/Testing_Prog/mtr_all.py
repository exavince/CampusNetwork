#! /usr/bin/env python3

import time
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

    #net_cfg = input("Config File of the network: ")
    #child.sendline('sudo ./create_network.sh ' + net_cfg)
    #child.expect('\r\n')
    #idx = child.expect(['The network has been started!','File exists','No such file or directory'])
    #child.expect(prompt)
    #if idx == 0:
    #    pass
    #elif idx == 1:
    #    pass
    #elif idx == 2:
    #    print("No such file or directory")
    #    child.sendline('exit')
    #else:
    #    print("FAILED")
    #    child.sendline('exit')

    net_rep = input("Rep File of the network: ")
    test_router = input("Name of the router to test: ")
    child.sendline('sudo ./connect_to.sh ' + net_rep + ' ' + test_router)
    child.expect('\r\n')
    idx = child.expect('')
    child.expect(prompt)
    if idx == 0:
        print("Connected to router " + net_rep + ' ' + test_router)
    else:
        print("FAILED")
        child.sendline('exit')

    time.sleep(1)
    ip_list = ['fde4:3::f1','fde4:3::f2','fde4:3::f3','fde4:3::f4','fde4:3::f5','fde4:3::f6','fde4:3::f7','fde4:3::f8','fde4:3::f9','fde4:3::fa','fde4:3::fb','fde4:3::fc','fde4:3::fd']
    number_ip = len(ip_list)
    count = 0
    for i in range(number_ip):

        child.sendline('mtr -6 -c 2 --json ' + ip_list[i])
        #child.expect('\r\n')
        idx = child.expect(['\r\n mtr: udp socket connect failed: Network is unreachable','\r\n'])
        child.expect(prompt)
        if idx == 0:
            print("udp socket connect failed")
            pass
        else:
            output = child.before
            time.sleep(2)
            output = trim_from_start(output, '{')
            output = trim_from_end(output, '}')
            try:
                results = json.loads(output)['report']
                nb_hops = len(results['hubs'])
                if nb_hops > 0:
                    count = count + 1
                print("Total hops to reach %s: %d" % (results['hubs'][nb_hops-1]['host'], nb_hops))
            except json.decoder.JSONDecodeError:
                # FIX TODO
                print("JSONDecodeError")

    print("End of the test")
    if count == number_ip:
        print("Able to ping all the routers of the network")
    else:
        print("Unable to ping all the routers of the network")
    child.sendline('exit')

