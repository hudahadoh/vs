import socket
import json
from multiprocessing import Process

def handle_client(client_socket, remote_host, remote_port):
    try:
        # Buat koneksi ke server remote
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
        
        client_buffer = ""
        remote_buffer = ""
        
        while True:
            # Set socket timeout to prevent hanging
            client_socket.settimeout(5.0)
            remote_socket.settimeout(5.0)

            # Menerima data dari klien
            try:
                data = client_socket.recv(8192)
                if data:
                    client_buffer += data.decode('utf-8')
                    # Proses data jika lengkap (dipisahkan dengan newline '\n')
                    while '\n' in client_buffer:
                        line, client_buffer = client_buffer.split('\n', 1)
                        try:
                            json_message = json.loads(line)
                            # Contoh modifikasi (jika diperlukan)
                            # json_message['params']['example_param'] = 'modified_value'
                            remote_socket.send((json.dumps(json_message) + '\n').encode('utf-8'))
                        except json.JSONDecodeError:
                            remote_socket.send((line + '\n').encode('utf-8'))
                else:
                    break  # Jika tidak ada data, akhiri loop
            except socket.timeout:
                pass  # Lanjutkan untuk membaca dari remote_socket

            # Menerima data dari server remote
            try:
                data = remote_socket.recv(8192)
                if data:
                    remote_buffer += data.decode('utf-8')
                    # Proses data jika lengkap (dipisahkan dengan newline '\n')
                    while '\n' in remote_buffer:
                        line, remote_buffer = remote_buffer.split('\n', 1)
                        try:
                            json_message = json.loads(line)
                            # Contoh modifikasi (jika diperlukan)
                            # json_message['result']['example_param'] = 'modified_value'
                            client_socket.send((json.dumps(json_message) + '\n').encode('utf-8'))
                        except json.JSONDecodeError:
                            client_socket.send((line + '\n').encode('utf-8'))
                else:
                    break  # Jika tidak ada data, akhiri loop
            except socket.timeout:
                pass  # Lanjutkan untuk membaca dari client_socket
            
    except Exception as e:
        print(f"[*] Kesalahan: {e}")
    finally:
        client_socket.close()
        remote_socket.close()

def main():
    local_host = "0.0.0.0"  # Mengikat ke semua antarmuka yang tersedia
    local_port = 4055  # Ganti dengan port lokal yang diinginkan
    remote_host = "na.luckpool.net"  # Ganti dengan alamat server target
    remote_port = 3956  # Ganti dengan port server target
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_host, local_port))
    server.listen(100)
    
    print(f"[*] Mendengarkan di {local_host}:{local_port}")
    
    while True:
        try:
            client_socket, addr = server.accept()
            print(f"[*] Menerima koneksi dari {addr[0]}:{addr[1]}")
            client_process = Process(target=handle_client, args=(client_socket, remote_host, remote_port))
            client_process.start()
            client_socket.close()  # Menutup soket klien di proses induk
        except KeyboardInterrupt:
            print("[*] Menutup server.")
            server.close()
            break

if __name__ == "__main__":
    main()
