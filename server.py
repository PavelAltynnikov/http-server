# -*- coding: utf-8 -*-
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
        # print(path)
        # print(path, os.path.exists('.' + path))

        head = ''.encode('utf-8')
        body = ''.encode('utf-8')
        if path == r'/':
            head = b'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n'
            with open('./static/html/index.html', 'r') as f:
                body = f.read().encode('utf-8')
        elif path == r'/static/css/style.css':
            head = b'HTTP/1.1 200 OK\nContent-Type: text/css; charset=utf-8\n\n'
            with open('./static/css/style.css', 'r') as f:
                body = f.read().encode('utf-8')
        elif path == r'/static/img/logo/logo_black.png':
            with open('./static/img/logo/logo_black.png', 'rb') as f:
                img = f.read()

            head = 'HTTP/1.1 200 OK\n' \
                   'Content-Type: image/png\n' \
                   'Accept-Ranges: bytes\n' \
                   f'Content-length: {len(img)}\n' \
                   f'Location: https://localhost:8000/static/img/logo/logo_black.png\n\n'
            head = head.encode('utf-8')
            body = img
        else:
            head = 'HTTP/1.1 404 NotFound\nContent-Type: text/html; charset=utf-8\n\n' \
                .encode('utf-8')
            body = 'Сори, но страница не найдена'.encode('utf-8')

        # responce = ''.join([head, body])
        # client.send(responce.encode('utf-8'))
        client.send(head)
        client.send(body)

        client.shutdown(socket.SHUT_RDWR)
        client.close()
except Exception as e:
    print(f'Сервер отключен, причина: {e}')
    server_sock.close()
