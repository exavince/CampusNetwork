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
 ${interface['command']}
%endfor
!
address-family ipv6 unicast
%for rule in data['addres-family']:
 ${rule['command']}
%endfor
exit address-family
