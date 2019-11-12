! -*- zebra -*-
!
! zebra sample configuration file
!
hostname ${data['hostname']}
password zebra
enable password zebra
!
! Interface's description.
!
interface lo
 description loopback.
%for interface in data['interfaces']:
!
interface ${interface['name']} 
 description Link to ${interface['link_to']}
!
%endfor
