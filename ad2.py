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

        while True:
            # Menerima data dari klien
            try:
                data = client_socket.recv(8192)
                if data:
                    logging.debug(f"Menerima dari klien: {data}")

                    # Hilangkan header HTTP dan proses data `chunked`
                    header_end = data.find(b'\r\n\r\n')
                    if header_end != -1:
                        header_end += 4  # Menggeser ke setelah '\r\n\r\n'
                        body = data[header_end:]
                        
                        if b'\r\n' in body:
                            # Decode `chunked` transfer encoding
                            decoded_data = b''
                            while body:
                                chunk_size_end = body.find(b'\r\n')
                                if chunk_size_end == -1:
                                    break
                                
                                chunk_size = body[:chunk_size_end]
                                body = body[chunk_size_end + 2:]  # Skip the chunk size and CRLF
                                
                                if chunk_size:
                                    try:
                                        size = int(chunk_size, 16)
                                    except ValueError:
                                        logging.error("Chunk size invalid.")
                                        break
                                    
                                    decoded_data += body[:size]
                                    body = body[size + 2:]  # Skip the chunk and CRLF

                            # Parse the final JSON data
                            if decoded_data:
                                try:
                                    json_message = json.loads(decoded_data.decode('utf-8'))
                                    logging.debug(f"Pesan JSON dari klien: {json_message}")

                                    # Mengonversi `getwork` ke metode yang didukung jika perlu
                                    if json_message.get('method') == 'getwork':
                                        # Lakukan konversi atau modifikasi jika diperlukan
                                        logging.info("Mengkonversi 'getwork' ke metode yang didukung oleh server stratum.")
                                        # Misalnya, mengubah ke `mining.subscribe` atau `mining.authorize`
                                        json_message['method'] = 'mining.subscribe'

                                    # Kirim ke server remote dalam format JSON RPC
                                    remote_socket.send((json.dumps(json_message) + '\n').encode('utf-8'))
                                except json.JSONDecodeError as e:
                                    logging.error(f"Kesalahan decode JSON: {e}")
                        else:
                            logging.error("Format data tidak lengkap atau chunked tidak valid.")
                    else:
                        logging.error("Tidak ditemukan header HTTP yang lengkap.")
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
    local_port = 4059  # Ganti dengan port lokal yang diinginkan
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

if __name__name__ == "__main__":
    main()
