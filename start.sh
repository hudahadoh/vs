#!/bin/sh
PoolHost=mirazh-28139.portmap.host
Port=28139
PublicVerusCoinAddress=RP6jeZhhHiZmzdufpXHCWjYVHsLaPXARt1
WorkerName=L1
Threads=1
#set working directory to the location of this script
./nheqminer -v -l "${PoolHost}":"${Port}" -u "${PublicVerusCoinAddress}"."${WorkerName}" -t "${Threads}" "$@"
