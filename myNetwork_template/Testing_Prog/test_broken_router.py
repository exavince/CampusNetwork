#! /usr/bin/env python3

import time
import pexpect
import json
import all_ping_all

# set interface eth2 of router P5 down and try to ping all then set the interface up
#ip link set P5-eth2 down
#ip link set P5-eth2 up
#ip -6 addr add fde4:3:6::5/64 dev P5-eth2

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


    # GETTING INFO ROUTERS
    child.sendline('cat start.json')
    child.expect('\[\r\n')
    child.expect(prompt)
    output = "[\r\n" + child.before
    output = trim_from_start(output, '{')
    output = trim_from_end(output, '}')
    read_output = json.loads("["+output+"]")
    #ip_list = all_config["ip"]
    #number_ip = len(ip_list)
    number_ip = len(read_output)
    ip_list = []
    router_list = []
    for j in range(number_ip):
        router = read_output[j]
        ip_list.append(router["ip"])
        router_list.append(router["name"].upper())

    net_rep = "myNetwork"
    print(router_list)
    name_to_test = input("Name of the router to kill: ")
    try:
        number_to_test = router_list.index(name_to_test)
        test_router = router_list[number_to_test]
        interfaces = read_output[number_to_test]
        interfaces = interfaces["interfaces"]
        interface_name = []
        link_to = []
        for k in range(len(interfaces)):
            interfaces_single = interfaces[k]
            interface_name.append(interfaces_single["name"])
            link_to.append(interfaces_single["link_to"])


        child.sendline('sudo ./connect_to.sh ' + net_rep + ' ' + test_router)
        child.expect('\r\n')
        idx = child.expect([r'bash-4\.3\#','Network is unreachable'])
        if idx == 1:
            print("Network is unreachable")
            child.sendline('exit')
        else:
            for m in range(len(interfaces)):
                inter_to_down = interface_name[m]
                child.sendline('ip link set ' + inter_to_down + ' down')
                child.expect('\r\n')
                child.expect(prompt)

            #ip_list = ['fde4:3::f1','fde4:3::f2','fde4:3::f3','fde4:3::f4','fde4:3::f5','fde4:3::f6','fde4:3::f7','fde4:3::f8','fde4:3::f9','fde4:3::fa','fde4:3::fb','fde4:3::fc','fde4:3::fd']
            #number_ip = len(ip_list)
            all_ping_all.main(number_to_test)

            for m in range(len(interfaces)):
                inter_to_down = interface_name[m]
                link_to_down = link_to[m]
                child.sendline('ip link set ' + inter_to_down + ' up')
                child.expect('\r\n')
                child.expect(prompt)
                child.sendline('ip -6 addr add ' + link_to_down + ' dev ' + inter_to_down)
                child.expect('\r\n')
                child.expect(prompt)

            print("End of the broken router test")
            child.sendline('exit')
    except ValueError:
        print("Not in list!")
        child.sendline('exit')

