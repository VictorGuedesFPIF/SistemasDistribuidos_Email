from datetime import datetime
import json
import bcrypt
import findServer
import os

def encrypta(passwd):
    passwdEncoded = passwd.encode()
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(passwdEncoded, salt)
    hash = hash.hex()
    return hash

class main:
    server = None
    serverFinded = None
    while True:
        print("\nCliente E-mail service BSI Online\n\n")
        print("\t1) Apontar Servidor\n\t2) Cadastrar Conta\n\t3) Acessar E-mail\n")
        op = int(input())
        if op == 1:
            os.system('clear')
            host = input("Indique o endereço IP do servidor: ")
            port = input("\nIndique a porta do servidor: ")
            endpoint = (host, int(port))
            server = findServer.findServer(endpoint)
            serverFinded = server.getConnection()

        elif op == 2 and serverFinded == True:
            os.system('clear')

            opServer = op.to_bytes(4, byteorder='big')
            server.clientSocket.sendall(opServer)

            name = input("Digite seu nome completo: ")
            while True:
                username = input("Digite seu email: ")
                server.clientSocket.sendall(json.dumps(username).encode())
                conf = server.clientSocket.recv(1024).decode()
                if json.loads(conf) == False:
                    
                    break
            password = input("Digite sua senha: ")
            
            account = {'Name':name, 'Username':username, 'Password':str(encrypta(password))}
            jsonSend = json.dumps(account)
            server.clientSocket.sendall(jsonSend.encode())

            confirmation = server.clientSocket.recv(1024).decode()

            if json.loads(confirmation) == True:
                print('Conta criada')

        elif op == 3 and serverFinded == True: 
            os.system('clear')

            opServer = op.to_bytes(4, byteorder='big')
            server.clientSocket.sendall(opServer)
            
            username = input('Digite seu email: ')
            password = input('Digite sua senha: ').encode()
            login = {'Username':username}
            jsonSend = json.dumps(login)
            server.clientSocket.sendall(jsonSend.encode())
            
            userReceived = json.loads(server.clientSocket.recv(1024).decode())
            if userReceived != False:
                hash = bytes.fromhex(userReceived.get("Passwd"))
                verifyPasswd = bcrypt.checkpw(password, hash)
                
                if verifyPasswd == True:

                    while True:

                        print(f'Seja bem vindo {userReceived.get("Name")}')
                        op = int(input('\n\t4) Enviar email\n\t5) Receber Email\n\t6) Logout\n'))

                        if op == 4:
                            os.system('clear')

                            opServer = op.to_bytes(4, byteorder='big')
                            server.clientSocket.sendall(opServer)

                            remetente = userReceived.get("Name")
                            data = datetime.now().strftime("%d-%m-%Y")
                            print(f'\nRemetente: {remetente}')
                            print(f'\nDia de envio: {data}')
                            destino = input("\nDestinatário do email: ")
                            assunto = input("\nAssunto do email: ")
                            corpo = input("\nEscreva o que deseja enviar.\n\n")
                            email = {"Remetente":remetente, "Data":data, "Destino":destino, "Assunto":assunto, "Corpo":corpo}

                            enviar = int(input("\nEnviar? 1 - sim, 0 - não\n"))
                            if enviar == 1:
                                jsonEmail = json.dumps(email).encode()
                                server.clientSocket.sendall(jsonEmail)
                                res = json.loads((server.clientSocket.recv(1024).decode()))
                                if res == True:
                                    print("\n\nEmail enviado com sucesso")
                                else:
                                    print("\nFalha no envio: remetente inexistente.")

                            else:
                                print("\nEmail abortado")
                            
                        elif op == 5:
                            while True:    
                                os.system('clear')
                                
                                opServer = op.to_bytes(4, byteorder='big')
                                server.clientSocket.sendall(opServer)
                                
                                server.clientSocket.sendall(userReceived.get("Username").encode())

                                print("\nRecebendo E-mails...")

                                emails = json.loads(server.clientSocket.recv(1024).decode())

                                print(f'\n{len(emails)} Emails recebidos:')

                                for i in emails:
                                    print(f'\n[{i}] {emails["Destino"]}: {emails["Assunto"]}')

                                seleciona = int(input("\nQual e-mail deseja ler? "))
                                
                                print(f'\n[{seleciona}] {emails[seleciona].get("Destino")}: {emails[seleciona].get("Assunto")}\n\nData de envio: {emails[seleciona].get("Data")}\n{emails[seleciona].get("Corpo")}')

                                op3 = int(input("\n\n aperte qualquer tecla para continuar lendo, 0 - para sair"))
                                if op3 == 0:
                                    break

                        elif op == 6:
                            server.closeConnection()
                            opServer = op.to_bytes(4, byteorder='big')
                            server.clientSocket.sendall(opServer)
                            SystemExit(0)

                else:
                    print(f'\nSenha incorreta')
            else:
                print("\nUsuário não encontrado")
        
        elif serverFinded == False:
            print("\nÉ necessário encontrar o server primeiro.\n")


