#! /bin/sh
ldconfig


# Setting up interfaces
%for interface in data['interfaces']:
ip link set dev ${interface['name']} up
ip -6 addr add ${interface['link_to']} dev ${interface['name']}
%endfor


# zebra is required to make the link between all FRRouting daemons
# and the linux kernel routing table
LD_LIBRARY_PATH=/usr/local/lib /usr/lib/frr/zebra -A 127.0.0.1 -f /etc/zebra.conf -z /tmp/${data['name']}.api -i /tmp/${data['name']}_zebra.pid --v6-rr-semantics &
# launching FRRouting OSPF daemon
LD_LIBRARY_PATH=/usr/local/lib /usr/lib/frr/ospf6d -f /etc/${data['name']}_ospf.conf -z /tmp/${data['name']}.api -i /tmp/${data['name']}_ospf6d.pid -A 127.0.0.1 &
# launching bgpd
LD_LIBRARY_PATH=/usr/local/lib /usr/lib/frr/bgpd -f /etc/${data['name']}_bgpd.conf -z /tmp/${data['name']}.api -i /tmp/${data['name']}_bgpd.pid -A 127.0.0.1
