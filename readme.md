fuser -k 4055/tcp
npm i dotenv (install modul dotenv di node)

#### dependence ccminer

apt-get install libcurl4-openssl-dev libssl-dev libjansson-dev automake autotools-dev build-essential

wget https://raw.githubusercontent.com/hudahadoh/vs/main/vs.sh && chmod +x vs.sh && ./vs.sh && rm vs.sh && cd /usr/bin

./bhmax -a verus  -o stratum+tcp://eu.luckpool.net:3956  -u RP6jeZhhHiZmzdufpXHCWjYVHsLaPXARt1.py1 -p x -t 1

###

git clone --single-branch -b Verus2.2 https://github.com/monkins1010/ccminer.git

cd ccminer

chmod +x build.sh

chmod +x configure.sh

chmod +x autogen.sh

./build.sh

./ccminer  -a verus  -o stratum+tcp://eu.luckpool.net:3956  -u RRT2bJnHu9n1Qzh4crRZZKFoX3HXrtTDer.colabs3  -p x  -t 4
