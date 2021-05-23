import socket


HOST = 'localhost'
PORT = 8080

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1024)
server_sock.bind((HOST, PORT))
server_sock.listen(10)

try:
    while True:
        client, address = server_sock.accept()

        request = client.recv(1024).decode('utf-8').split('\n')
        request_head = request[0].split()
        if not request_head:
            continue

        http_method = request_head[0]
        if http_method != 'GET':
            continue

        path = request_head[1]

        head = ''
        body = ''
        if path == r'/':
            head = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n'
            with open('index.html', 'r') as f:
                body = f.read()
        else:
            head = 'HTTP/1.1 404 NotFound\nContent-Type: text/html; charset=utf-8\n\n'
            body = 'Сори, но страница не найдена'

        responce = ''.join([head, body])
        client.send(responce.encode('utf-8'))

        client.shutdown(socket.SHUT_RDWR)
        client.close()
except Exception as e:
    print(f'Сервер отключен, причина: {e}')
    server_sock.close()
