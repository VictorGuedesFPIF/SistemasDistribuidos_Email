import socket
import json
import concurrent.futures

class createAccount:
    
    def __init__(self, name, username, passwd):    
        self.name = name
        self.username = username
        self.passwd = passwd
        self.emails = []

Accounts = []

def verifyUser(username):
    for i in range(len(Accounts)):
        try:
            if Accounts[i].username == username:
                return True
        except AttributeError:
            continue
    return False

def getUser(username):
    for i in range(len(Accounts)):
        try:
            if Accounts[i].username == username:
                return Accounts[i]
        except AttributeError:
            continue
    return False

def adicionaEmail(username, email):
    for i in range(len(Accounts)):
        try:
            if Accounts[i].username == username:
                Accounts[i].emails.append(email)
        except AttributeError:
            continue
        finally:
            continue

def handle_client(connection):
    while True:
        op = connection.recv(4)
        opInt = int.from_bytes(op, byteorder='big')
        if opInt == 2:
            while True:
                userExists = json.loads(connection.recv(1024).decode())
                exists = verifyUser(userExists)
                connection.sendall(json.dumps(exists).encode())
                if exists == False:
                    break
            account = json.loads(connection.recv(1024).decode())
            Accounts.append(createAccount(account.get('Name'), account.get('Username'), account.get('Password')))
            connection.sendall(json.dumps(True).encode())
            print(f'Usuario {account.get("username\n")} criado!')

        elif opInt == 3:
            user = json.loads(connection.recv(1024).decode())
            exists = verifyUser(user.get('Username')) 
            
            if exists == True:
                user = getUser(user.get("Username"))
                sendUser = {"Name":user.name, "Username":user.username, "Passwd":user.passwd}
                
                connection.sendall(json.dumps(sendUser).encode())
                print(f'Conexão com {user} bem sucedida\n')            
            else:    
                connection.sendall(json.dumps(False).encode())
                print(f'Usuário inexistente\n')

        elif opInt == 4:
            email = json.loads(connection.recv(1024).decode())
            user = email.get("Destino")
            exists = verifyUser(user)
            if exists == True:
                adicionaEmail(user, email)
                connection.sendall(json.dumps(True).encode())
                print(f'Novo email enviado para o usuário {user}')
            else:
                connection.sendall(json.dumps(False).encode())
                print("Usuário inexistente\n")

        elif opInt == 5:
            user = json.loads(connection.recv(1024).decode())
            if verifyUser(user) == True:
                findUser = getUser(user)
                
                connection.sendall(json.dumps(findUser.emails).encode())
                print(f"Emails pedentes enviado ao usuário {findUser.name}\n")

        elif opInt == 6:
            break
            
            


def main():
    endpoint = ('0.0.0.0', 8080)

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(endpoint)
    serverSocket.listen()

    print("Server em execução")
    with concurrent.futures.ThreadPoolExecutor(10) as workers:
        while True:
            connection, address = serverSocket.accept()
            print(f'Novo cliente aceito, {address}')
            workers.submit(handle_client, connection)

main()