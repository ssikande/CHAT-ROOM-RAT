# CHAT-ROOM-RAT

This project takes stuff learnt from NeuralNine's video tutorial for an Advanced Chat Room in python and adds a lot more functionality to it. I added functionality with Malware in mind. I wanted to combine the idea of a Multiperson Chat Room and combine it with a Remote Acess Trojan. The RAT part is trivial as im using the subprocess library.

## THE CHAT ROOM
I have built a fully functional chat room (with some bugs, ill fixem later)

## To start the CHAT ROOM we start the server
```bash
python server.py 127.0.0.1 44444
```
## we also start the client 
```bash
python client.py 127.0.0.1 44444
```
## or if you want to use the packed/obfuscated file
```bash
python client_packed.py 127.0.0.1 44444
```
## Commands:
- *clear - Clears the screen
- *talk <nickname,...> - Starts a private chat with multiple or single person
- *end - Ends the private chat
- *help - Shows the help menu
- *online - Shows the online people
- *exit - Exits the chat

## ADMIN Commands:

username - admin, password - adminpass

- /kick <user> - Kicks a user
- /ban <user> - Bans a user
- /code <nickname> <message> - Executes a command on the server if no nickname given, else on given nickname
- /exit - Exits the server
 
I also added a way to obfuscate the client file when wanted to make it availible for download. I created a packer that compresses the original client file to the given client_packed file. This technique helps us evade some anti-viruses and also reverse engineers that might try to deconstruct the client code.

## to use the packer or create a packed version of the client or other files
```bash
python packer.py client.py client_packed.py
```

## there is also a make.bat file
This file is for testing purposes that spawns a environment for testing with a server and some clients.
to use it
```bash
just double click make.bat file
```
