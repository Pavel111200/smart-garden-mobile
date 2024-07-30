import socket


class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self, address:str, port:int):
        self.client.connect((address, port))

    def send(self,msg):
        message = msg.encode("utf-8")
        msg_length = len(message)
        send_length = str(msg_length).encode("utf-8")
        send_length += b' ' * (64 - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
    
    def receive(self):
        msg_length = self.client.recv(64).decode("utf-8")
        if msg_length:
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length).decode("utf-8")
            return msg