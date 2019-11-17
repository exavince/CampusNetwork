! -*- bgp -*-
!
! BGP configuration file
!
hostname bgpd
password zebra
service advanced-vty
!
debug

router bgp ${data['ASN']}

bgp router-id ${data['router-id']}
no bgp default ipv4-unicast

%for interface in data['interfaces']:
${interface['command']} ${interface['addr']} ${interface['arg1']} ${interface['arg2']}
%endfor

address-family ipv6 unicast
%for rule in data['addres-family']:
${rule['command']} ${rule['addr']} ${rule['arg1']} ${rule['arg2']}
%endfor
exit address-family
