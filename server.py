# -*- coding: utf-8 -*-
import socket


HOST = 'localhost'
PORT = 8080
DEFAULT_HEADER = 'HTTP/1.1 '
OK = '200 OK'
NOT_FOUND = '404 NotFound'

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1024)
server_sock.bind((HOST, PORT))
server_sock.listen(10)


def print_request():
    print(http_method)
    print(path)
    print(protocol, end='\n\n')
    for key, value in headers.items():
        print(f'{key}: {value}')
    print()


def generate_responce(path) -> bytes:
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

    responce = b' '.join((head, body))
    return responce


try:
    while True:
        client, address = server_sock.accept()

        request = client.recv(1024).decode('utf-8').strip().split('\r\n')

        starting_line = request[0].split()
        http_method = starting_line[0]
        path = starting_line[1]
        protocol = starting_line[2]
        headers = {line.split(': ')[0]: line.split(': ')[1] for line in request[1:]}

        print_request()

        if http_method != 'GET':
            client.shutdown(socket.SHUT_RDWR)
            client.close()
            continue

        client.send(generate_responce(path))
        client.shutdown(socket.SHUT_RDWR)
        client.close()
except Exception as e:
    print(f'Сервер отключен, причина: {e}')
    server_sock.close()
