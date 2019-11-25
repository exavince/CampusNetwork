#! /usr/bin/env python3

import pexpect
import json

__PASSWD = 'password'
# or use your private key

if __name__ == '__main__':
    # open a new remote connection via ssh

    ##### SET UP VM ######
    prompt = [r'vagrant@group3:~.*',r'-bash-4\.2\$',r'-bash-4\.3\$',r'bash-4\.3\#',r'group3\#',r'P2\#',r'\#']

    child = pexpect.spawn('ssh lingi2142vm', encoding='utf-8', timeout=120)
    child.expect(prompt)
    child.sendline('cd Group_folder/')
    child.expect(prompt)
    child.sendline('cd CampusNetwork/')
    child.expect(prompt)
    child.sendline('cd myNetwork_template/')
    child.expect(prompt)

    child.sendline('ls')
    child.expect('\r\n')    # saut de ligne ls
    child.expect(prompt)    # vagrant@group3:~.*
    print(child.before)     # print ce qui est avant le dernier limiteur

    ##### SET UP NETWORK ######
    print("Network creation needed ?")
    ans = input("(y/n) : ")
    if ans == "y":
        print("Creation Network")
        net_cfg = input("Config File of the new network: ")
        print("sudo ./create_network.sh " + net_cfg)
        child.sendline('sudo ./create_network.sh ' + net_cfg)
        idx = child.expect(['The network has been started!','File exists'])
        if idx == 0:
            print("The network has been started!")
        elif idx == 1:
            print("Network already started")
        else:
            print("FAILED")
            child.sendline('exit')
        child.expect('\r\n')
        child.expect(prompt)
        print(child.before)

    print("Router connection needed ?")
    ans = input("(y/n) : ")
    if ans == "y":
        print("Connection Router")
        net_rep = input("Rep File of the new network: ")
        net_mainrouter = input("Name of the router: ")
        child.sendline('sudo ./connect_to.sh ' + net_rep + ' ' + net_mainrouter)
        idx = child.expect('')
        if idx == 0:
            print("Connected to router " + net_rep + ' ' + net_mainrouter)
        else:
            print("FAILED")
        child.expect('\r\n')
        child.expect(prompt)
        print(child.before)

    co_to_end = 0
    while co_to_end != 1:
        ##### SET UP TESTS ######
        print("Test to execute ?")
        ##### BASICS TESTS ######
        print(" 1 : Ip -6 address ")
        print(" 2 : Ip -6 route ")
        ##### DATAPLANE TESTS ######
        print(" 3 : Ping6 ")
        print(" 4 : Traceroute ")
        ##### CONTROL PLANE TESTS ######
        # LD_LIBRARY_PATH=/usr/local/lib vtysh
        print(" 5 : Show BGP summary ")
        print(" 6 : Show running-config ")
        print(" 7 : Mtr -6 ")
        print(" 8 : Show ipv6 ospf6 neighbor ")
        print(" 9 : Other (Manual) ")
        #print(" 10 : ")
        print(" 0 : Exit ")
        test_num = int(input("Number of the test: "))

        if test_num == 0:
            co_to_end = 1
            break
        elif test_num == 1:
            child.sendline('ip -6 address')
            print("Ip -6 address")
            child.expect('\r\n')
            child.expect(prompt)
            print(child.before)

        elif test_num == 2:
            child.sendline('ip -6 route')
            print("Ip -6 route")
            child.expect('\r\n')
            child.expect(prompt)
            print(child.before)

        elif test_num == 3:
            addr_test_ipv6 = input("Address to ping : ")
            child.sendline('ping6 -c 10 ' + addr_test_ipv6)
            print("ping6 " + addr_test_ipv6)
            child.expect('\r\n')
            child.expect(prompt)
            print(child.before)

        elif test_num == 4:
            addr_test_ipv6 = input("Address to trace : ")
            child.sendline('traceroute ' + addr_test_ipv6)
            print("traceroute " + addr_test_ipv6)
            child.expect('\r\n')
            child.expect(prompt)
            print(child.before)

        elif test_num == 5:
            child.sendline('LD_LIBRARY_PATH=/usr/local/lib vtysh')
            child.expect('\r\n')
            child.expect(prompt)
            child.sendline('show bgp summary')
            print("show bgp summary")
            child.expect('\r\n')
            child.expect(prompt)
            print(child.before)
            child.sendline('exit')
            child.expect('\r\n')
            child.expect(prompt)

        elif test_num == 6:
            child.sendline('LD_LIBRARY_PATH=/usr/local/lib vtysh')
            child.expect('\r\n')
            child.expect(prompt)
            child.sendline('show running-config')
            print("show running-config")
            child.expect('\r\n')
            child.expect(prompt)
            print(child.before)
            child.sendline('exit')
            child.expect('\r\n')
            child.expect(prompt)

        elif test_num == 7:
            addr_test_ipv6 = input("Address : ")
            child.sendline('mtr -6 -c 5 ' + addr_test_ipv6)
            print("mtr -6 -c 5 " + addr_test_ipv6)
            child.expect('\r\n')
            child.expect(prompt)
            print(child.before)

        elif test_num == 8:
            child.sendline('LD_LIBRARY_PATH=/usr/local/lib vtysh')
            child.expect('\r\n')
            child.expect(prompt)
            child.sendline('show ipv6 ospf6 neighbor')
            print("Show ipv6 ospf6 neighbor")
            child.expect('\r\n')
            child.expect(prompt)
            print(child.before)
            child.sendline('exit')
            child.expect('\r\n')
            child.expect(prompt)

        elif test_num == 9:
            child.interact()
        else:
            print("Wrong number")

        print("Execute another test ?")
        ans = input("(y/n) : ")
        if ans == "y":
            pass
        else:
            co_to_end = 1

    # we don't need the ssh connection anymore, close it!
    print("Cleanup needed ?")
    ans = input("(y/n) : ")
    if ans == "y":
        print("Cleaning Network")
        print("sudo ./cleanup.sh")
        child.sendline('sudo ./cleanup.sh')
        child.expect('\r\n')
        child.expect(prompt)
        print(child.before)
    #child.sendline('sudo ./cleanup.sh')
    child.sendline('exit')
    print('closing connection')

