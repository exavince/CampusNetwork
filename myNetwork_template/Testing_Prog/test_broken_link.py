#! /usr/bin/env python3

import time
import pexpect
import json

# set interface eth2 of router P5 down and try to ping all then set the interface up
#ip link set P5-eth2 down
#ip link set P5-eth2 up
#ip -6 addr add fde4:3:6::5/64 dev P5-eth2


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

    net_rep = "myNetwork"
    test_router = "P5"

    child.sendline('sudo ./connect_to.sh ' + net_rep + ' ' + test_router)
    child.expect('\r\n')
    idx = child.expect('')
    child.expect(prompt)
    if idx == 0:
        print("Connected to router " + net_rep + ' ' + test_router)
    else:
        print("FAILED")
        child.sendline('exit')

    child.sendline('ip link set P5-eth2 down')
    child.expect('\r\n')
    child.expect(prompt)

    ip_list = ['fde4:3::f1','fde4:3::f2','fde4:3::f3','fde4:3::f4','fde4:3::f5','fde4:3::f6','fde4:3::f7','fde4:3::f8','fde4:3::f9','fde4:3::fa','fde4:3::fb','fde4:3::fc','fde4:3::fd']
    number_ip = len(ip_list)
    count = 0
    for i in range(number_ip):
        child.sendline('ping6 -c 5 -i 1 ' + ip_list[i])
        child.expect('\r\n')
        child.expect('received, ')
        idx = child.expect('% packet loss')
        packet_loss = child.before
        reach = 1

        try:
            packet_loss_int = int(packet_loss)
        except ValueError:
            res = [int(i) for i in packet_loss.split() if i.isdigit()]
            packet_loss_int = res[0]
            reach = 0

        child.expect(prompt)
        if packet_loss_int == 100:
            if reach == 0:
                print("Unable to ping router " + ip_list[i] + " Address unreachable")
            else:
                print("Unable to ping router " + ip_list[i])
        else:
                count = count + 1

                print("Able to ping router " + ip_list[i] + " with " + packet_loss + " % packet loss")

    child.sendline('ip link set P5-eth2 up')
    child.expect('\r\n')
    child.expect(prompt)
    child.sendline('ip -6 addr add fde4:3:6::5/64 dev P5-eth2')
    child.expect('\r\n')
    child.expect(prompt)

    print("End of the test")
    if count == number_ip:
        print("Able to ping all the routers of the network")
    else:
        print("Unable to ping all the routers of the network")
    child.sendline('exit')

