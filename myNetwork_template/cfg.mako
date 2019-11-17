#!/bin/bash

# Create a virtual network using network namespaces and veth pairs
# to connect them.
# Assuming $CONFIGDIR == "cfg":
# * Files in cfg/<Node name> will be overlaid over /etc, i.e. if a file with
# the same name exists in both directory, the one in cfg/<Node name> will
# be the one used.
# * If cfg/<Node name>_$BOOT (defaults to cfg/<Node name>_boot) exists and
# is executable, it will be executed when the node is created
# * If cfg/<Node name>_$STARTUP (defaults to cfg/<Node name>_start) exists and
# is executable, it will be executed when the whole network has started
#

# IMPORTANT NOTE: Node names MUST NOT exceed 9 characters.
# This is due to the limitation to 14 characters of interface names

# You can override any of these settings on a per-topology basis
# Group number
GROUPNUMBER=${data['groupe_nbr']}
# Node configs
CONFIGDIR=myNetwork
# boot script name
BOOT="boot"
# startup script name
STARTUP="start"
PREFIXBASE="fde4:${data['groupe_nbr']}"
PREFIXLEN=${data['prefix_len']}
# You can reuse the above two to generate ip addresses/routes, ...

# This function describes the network topology that we want to emulate
function mk_topo {
    echo "@@ Adding links and nodes"
    #                       P1 ------ P3
    #                        \        /
    # Build a small network   \      /
    #                          \    /
    #                            P2
    # Nodes are creadted on the fly, and their interface are assigned as
    # <node name>-eth<count>, where count starts at 0 and is increased by 1
    # after each new interface
    # e.g. P1-eth0 links to P2-eth0
    %for link in data['links']:
    add_link ${link['router1']} ${link['router2']}
    %endfor

    echo "@@ Bridging nodes"
    %for bridge in data['bridges']:
    bridge_node ${bridge['router']} ${bridge['VM-interface']} ${bridge['router-interface']}
    %endfor
}

