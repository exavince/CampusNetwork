#!/bin/bash

sudo rm -r myNetwork
mkdir -p myNetwork

python make_router.py -i "bgpd.json" -t "bgpd.mako" -o " " -m
python make_router.py -i "ospf6d.json" -t "ospf6d.mako" -o " " -m
python make_router.py -i "zebra.json" -t "zebra.mako" -o " " -m
python make_router.py -i "start.json" -t "start.mako" -o " " -m
python make_router.py -i "cfg.json" -t "cfg.mako" -o "./myNetwork_cfg"

router_count=$(python3 router_counter.py)

for i in $(seq 1 $router_count); do
    mkdir -p "myNetwork/P$i"
    mv p"$i"_zebra.conf "myNetwork/P$i"
    mv p"$i"_ospf.conf "myNetwork/P$i"
    mv p"$i"_bgpd.conf "myNetwork/P$i"
    mv p"$i".conf myNetwork/P"$i"_start
    cp boot myNetwork/P"$i"_boot
    sudo chmod +x myNetwork/P"$i"_boot
    sudo chmod +x myNetwork/P"$i"_start
done

