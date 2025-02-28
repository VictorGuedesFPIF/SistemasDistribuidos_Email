import socket

class findServer:

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    def getConnection(self):
        try:
            self.clientSocket.connect(self.endpoint)
            print('Servidor encontrado')
            return True
        except socket.error:
            print("Servidor não encontrado, corrija os dados")
            return False

    def closeConnection(self):
        self.clientSocket.close()     
