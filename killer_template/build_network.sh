#!/bin/bash

rm -r myNetwork
mkdir -p myNetwork

python make_router.py -i "bgpd.json" -t "bgpd.mako" -o " " -m
python make_router.py -i "ospf6d.json" -t "ospf6d.mako" -o " " -m
python make_router.py -i "zebra.json" -t "zebra.mako" -o " " -m
python make_router.py -i "start.json" -t "start.mako" -o " " -m
python make_router.py -i "cfg.json" -t "cfg.mako" -o "./myNetwork_cfg"

for i in $(seq 1 13); do
    mkdir -p "myNetwork/P$i"
    mv p"$i"_zebra.conf "myNetwork/P$i"
    mv p"$i"_ospf.conf "myNetwork/P$i"
    mv p"$i"_bgpd.conf "myNetwork/P$i"
    mv P"$i"_start.conf myNetwork/P"$i"_start
    cp boot myNetwork/P"$i"_boot
done

