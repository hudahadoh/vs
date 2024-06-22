import socket
import json
from multiprocessing import Process
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_client(client_socket, remote_host, remote_port):
    try:
        logging.info(f"Mencoba untuk menghubungkan ke server remote {remote_host}:{remote_port}")
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
        logging.info(f"Terhubung ke server remote {remote_host}:{remote_port}")

        client_buffer = ""

        while True:
            # Menerima data dari klien
            try:
                data = client_socket.recv(8192)
                if data:
                    logging.debug(f"Menerima dari klien: {data}")

                    # Parsing hanya pesan JSON tanpa header HTTP
                    # Ambil bagian dari pesan setelah '\r\n\r\n' (mengabaikan header HTTP)
                    try:
                        request_parts = data.decode('utf-8').split('\r\n\r\n', 1)
                        if len(request_parts) > 1:
                            json_data = request_parts[1].strip()
                            if json_data:
                                try:
                                    json_message = json.loads(json_data)
                                    logging.debug(f"Pesan JSON dari klien: {json_message}")
                                    # Kirim ke server remote dalam format JSON RPC
                                    remote_socket.send((json.dumps(json_message) + '\n').encode('utf-8'))
                                except json.JSONDecodeError as e:
                                    logging.error(f"Kesalahan decode JSON: {e}")
                        else:
                            logging.error("Format data tidak lengkap, tidak ada pesan JSON yang ditemukan.")
                    except UnicodeDecodeError as e:
                        logging.error(f"Kesalahan decode: {e}")
                else:
                    logging.debug("Klien menutup koneksi.")
                    break  # Jika tidak ada data, akhiri loop

            except socket.timeout:
                pass  # Lanjutkan untuk membaca dari remote_socket

            # Menerima data dari server remote
            try:
                data = remote_socket.recv(8192)
                if data:
                    logging.debug(f"Menerima dari server remote: {data}")
                    # Kirim kembali ke klien tanpa modifikasi
                    client_socket.send(data)
                else:
                    logging.debug("Server remote menutup koneksi.")
                    break  # Jika tidak ada data, akhiri loop
            except socket.timeout:
                pass  # Lanjutkan untuk membaca dari client_socket

    except Exception as e:
        logging.error(f"[*] Kesalahan: {e}")
    finally:
        client_socket.close()
        remote_socket.close()

def main():
    local_host = "0.0.0.0"  # Mengikat ke semua antarmuka yang tersedia
    local_port = 4058  # Ganti dengan port lokal yang diinginkan
    remote_host = "eu.luckpool.net"  # Ganti dengan alamat server target
    remote_port = 3956  # Ganti dengan port server target
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_host, local_port))
    server.listen(100)
    
    print(f"[*] Mendengarkan di {local_host}:{local_port}")
    logging.info(f"[*] Server dimulai di {local_host}:{local_port}")
    
    while True:
        try:
            client_socket, addr = server.accept()
            logging.info(f"[*] Menerima koneksi dari {addr[0]}:{addr[1]}")
            client_process = Process(target=handle_client, args=(client_socket, remote_host, remote_port))
            client_process.start()
            client_socket.close()  # Menutup soket klien di proses induk
        except KeyboardInterrupt:
            print("[*] Menutup server.")
            logging.info("[*] Server dihentikan oleh pengguna.")
            server.close()
            break

if __name__ == "__main__":
    main()
