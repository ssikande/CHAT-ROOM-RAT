import threading
import socket
import sys
import subprocess
import os

if len(sys.argv) != 3:
    print("Usage: python3 server.py <host> <port>")
    sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
nicknames = []

def online_clients():
    online = []
    for client in clients:
        online.append(nicknames[clients.index(client)])
    return online

def broadcast(message, custom_clients):
    for client in custom_clients:
        client.send(message)

def private_message(message, client, recipients):
    ans = ', '.join(recipients)
    for recipient in recipients:
        if recipient in nicknames:
            recipient_index = nicknames.index(recipient)
            recipient_client = clients[recipient_index]
            broadcast(f'{nicknames[clients.index(client)]} -> {ans}: {message.decode("ascii").split()[1]}'.encode('ascii'), [recipient_client])
        else:
            client.send(f'User {recipient} not found'.encode('ascii'))

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by an admin!'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by an admin!'.encode('ascii'), clients)
    else:
        print("User does not exist!")
        
def handle(client):
    while True:
        try:
            msg = message = client.recv(4096)
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':  
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open("bans.txt", 'a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned!')
            elif msg.decode('ascii').startswith('CODE'):
                print("from client: ",msg.decode('ascii').split())
                if len(msg.decode('ascii').split()) == 2 and nicknames[clients.index(client)] == 'admin':
                    command = msg.decode('ascii').split()[1]
                    try:
                        result = subprocess.check_output(command, shell=True)
                        client.send(result)
                    except:
                        client.send('An error occurred!'.encode('ascii'))
                elif len(msg.decode('ascii').split()) == 3 and nicknames[clients.index(client)] == 'admin':
                    _, other_client, command = msg.decode('ascii').split()
                    other_client_index = nicknames.index(other_client)
                    other_client = clients[other_client_index]
                    other_client.send(f'CODE {nicknames[clients.index(client)]} {command}'.encode('ascii'))
            elif msg.decode('ascii').startswith('TO'):
                recipient = msg.decode('ascii').split()[1]
                result = msg.decode('ascii')[5+len(recipient)+1:]
                if recipient in nicknames:
                    recipient_index = nicknames.index(recipient)
                    recipient_client = clients[recipient_index]
                    recipient_client.send(f'{nicknames[clients.index(client)]} -> {recipient}: {result}'.encode('ascii'))
                    #recipient_client.send(f'{result}'.encode('ascii'))
                else:
                    client.send('User not found'.encode('ascii'))
            elif msg.decode('ascii').startswith('TALK'):
                recipient = msg.decode('ascii').split()[1]
                if ',' in recipient:
                    recipients = recipient.split(',')
                else:
                    recipients = [recipient]
                while True:
                    message = client.recv(1024)
                    if message.decode('ascii').split()[1] == '*end':
                        break
                    private_message(message, client, recipients)
            elif msg.decode('ascii').startswith('ONLINE'):
                client.send(f'Online: {online_clients()}'.encode('ascii'))
            elif msg.decode('ascii') == 'EXIT':
                print("Exiting")
                if nicknames[clients.index(client)] == 'admin':
                    for client in clients:
                        client.send('Server is shutting down!'.encode('ascii'))
                        client.close()
                    try:
                        server.close()
                    except Exception as e:
                        print(e)
                    os._exit(1)       
            elif not msg.decode('ascii').split()[1] == '*talk':
                broadcast(message, clients)
        except:
            if client in clients and nicknames[clients.index(client)] != 'admin':
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat!'.encode('ascii'), clients)
                nicknames.remove(nickname)
                break

def receive():
    while True:
        print("Server is running and listening ...")
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send('nickname?'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        if nickname+'\n' in bans:
            client.send('banned'.encode('ascii'))
            client.close()
            continue

        if nickname == 'admin':
            client.send('password?'.encode('ascii'))
            password = client.recv(1024).decode('ascii')

            if password != 'adminpass':
                client.send('The password is incorrect!'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client is {nickname}!")
        broadcast(f"{nickname} joined the chat!".encode('ascii'), clients)
        client.send('Connected to the server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()