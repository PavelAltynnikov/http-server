# -*- coding: utf-8 -*-
import os
import socket


HOST = 'localhost'
PORT = 8080

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1024)
server_sock.bind((HOST, PORT))
server_sock.listen(10)


def print_request(http_method, path, protocol, headers):
    print(http_method)
    print(path)
    print(protocol, end='\n\n')
    for key, value in headers.items():
        print(f'{key}: {value}')
    print()


def is_path_exists(path: str) -> bool:
    if path == r'/':
        return True
    return os.path.exists(f'.{path}')


def find_source_path(path: str) -> str:
    if path == r'/':
        return './static/html/index.html'
    return f'.{path}'


def choise_content_type(extension: str) -> str:
    if extension in ('html', 'css', ''):
        return 'text'
    return 'image'


def generate_responce(path: str) -> bytes:
    starting_line = b'HTTP/1.1 '
    headers = ''.encode('utf-8')
    body = ''.encode('utf-8')

    if is_path_exists(path):
        starting_line += b'200 OK\n'

        extension = os.path.splitext(path)[1].strip('.')
        if extension or path == r'/':
            if not extension:
                extension = 'html'
            source_path = find_source_path(path)
            content_type = choise_content_type(extension)
            headers += f'Content-Type: {content_type}/{extension}'.encode('utf-8')
            if content_type == 'text':
                headers += b'; charset=utf-8\n'
            else:
                headers += b'\n'

            if content_type == 'text':
                with open(source_path, 'r') as f:
                    body = f.read().encode('utf-8')
            else:
                with open(source_path, 'rb') as f:
                    img = f.read()

                headers += 'Accept-Ranges: bytes\n' \
                           f'Content-length: {len(img)}\n' \
                           f'Location: https://localhost:8000{path}\n'.encode('utf-8')
                body = img
    else:
        starting_line += b'404 NotFound\n'
        body = 'Сори, но страница не найдена'.encode('utf-8')

    headers += b'\n'
    print(b''.join((starting_line, headers)), end='\n\n')
    responce = b''.join((starting_line, headers, body))
    return responce


try:
    while True:
        client, address = server_sock.accept()

        request = client.recv(1024).decode('utf-8').strip().split('\r\n')

        starting_line = request[0].split()
        http_method, path, protocol = starting_line
        headers = {line.split(': ')[0]: line.split(': ')[1] for line in request[1:]}

        # print_request(http_method, path, protocol, headers)
        print(path)

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
