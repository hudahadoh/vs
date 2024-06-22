import socket
import json
from multiprocessing import Process

def handle_client(client_socket, remote_host, remote_port):
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
        
        while True:
            # Membaca data dari klien
            data = client_socket.recv(8192)
            if not data:
                break
            try:
                # Mencoba untuk mem-parsing data JSON
                messages = data.decode('utf-8').split('\n')
                for message in messages:
                    if message:
                        json_message = json.loads(message)
                        
                        # Contoh modifikasi (jika diperlukan)
                        # json_message['params']['example_param'] = 'modified_value'
                        
                        # Encode dan kirim ke server remote
                        remote_socket.send((json.dumps(json_message) + '\n').encode('utf-8'))
            except json.JSONDecodeError:
                # Jika data bukan JSON, hanya diteruskan
                remote_socket.send(data)
            
            # Membaca data dari server remote
            data = remote_socket.recv(8192)
            if not data:
                break
            try:
                # Mencoba untuk mem-parsing data JSON
                messages = data.decode('utf-8').split('\n')
                for message in messages:
                    if message:
                        json_message = json.loads(message)
                        
                        # Contoh modifikasi (jika diperlukan)
                        # json_message['result']['example_param'] = 'modified_value'
                        
                        # Encode dan kirim ke klien
                        client_socket.send((json.dumps(json_message) + '\n').encode('utf-8'))
            except json.JSONDecodeError:
                # Jika data bukan JSON, hanya diteruskan
                client_socket.send(data)
    except Exception as e:
        print(f"[*] Kesalahan: {e}")
    finally:
        client_socket.close()
        remote_socket.close()

def main():
    local_host = "0.0.0.0"  # Mengikat ke semua antarmuka yang tersedia
    local_port = 4052  # Ganti dengan port lokal yang diinginkan
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
