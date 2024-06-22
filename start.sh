#!/bin/sh
PoolHost=158.69.251.105
Port=4052
PublicVerusCoinAddress=RP6jeZhhHiZmzdufpXHCWjYVHsLaPXARt1
WorkerName=L1
Threads=1
#set working directory to the location of this script
./nheqminer -v -l "${PoolHost}":"${Port}" -u "${PublicVerusCoinAddress}"."${WorkerName}" -t "${Threads}" "$@"
