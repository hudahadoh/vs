CPU ONLY CCminer Verushash2.2 v3.8.3 (pbaas) Latest
There are 3 active branch names in ccminer github repo:

ARM(for 64bit ARM chips with AES intrinsic)

Verus2.2(standard x86-64 pc's)

Verus2.2gpu(NVIDIA GPUs) Please see: ccminer for NVIDIA GPUS

Note: Replace ARM in the git clone line below with the branchname above you want to use. e.g.
for standard x86-64 CPUS use

--single-branch -b Verus2.2

Installation instructions:

sudo apt-get install libcurl4-openssl-dev libssl-dev libjansson-dev automake autotools-dev build-essential

 git clone --single-branch -b ARM https://github.com/monkins1010/ccminer.git

cd ccminer

 chmod +x build.sh

 chmod +x configure.sh

 chmod +x autogen.sh

 ./build.sh

Then To Run the miner do the following

branch	Program	Algo	Pool	User	Password	threads	devices
ARM	ccminer	-a verus	-o stratum+tcp://POOLURL:PORT	-u WALLETADDRESS.name	-p password	-t 4	N/A
Verus2.2GPU	ccminer.exe	-a verus	-o stratum+tcp://POOLURL:PORT	-u WALLETADDRESS.name	-p password	N/A	-d 0,1,2
Verus2.2	ccminer.exe	-a verus	-o stratum+tcp://POOLURL:PORT	-u WALLETADDRESS.name	-p password	-t 4	N/A
For example to run 8 threads on a CPU miner do:

ccminer.exe -a verus -o stratum+tcp://pool.veruscoin.io:9999 -u REoPcdGXthL5yeTCrJtrQv5xhYTknbFbec.name -p x -t 8

Mining on Atomic PI (Atom based)

IMAGE ALT TEXT HERE

Mining on Windows

IMAGE ALT TEXT HERE

Assets Below

These are pre compiled files for windows x86-64 CPU only miner. For the ARM version following the instructions above will compile the files for you.

Password : 12345678
