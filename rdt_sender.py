import socket
from math import ceil


class Sender:
    def __init__(self, address):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.settimeout(1)
        self.dest = address
        #self.udp.bind(address)
        self.n_seq = 0

    def checksum(self, msg):
        s = 0
        for i in range(0, len(msg), 2):
            if (i+1) < len(msg):
                a = ord(msg[i])
                b = ord(msg[i+1])
                s = s + (a+(b << 8))
            elif (i+1) == len(msg):
                s += ord(msg[i])
            else:
                raise "Something Wrong here"
        s = s + (s >> 16)
        s = ~s & 0xffff
        return s

    def corrupt(self, pkt):
        checksum = int(pkt[:5])
        msg = pkt[6:]
        return self.checksum(msg) != checksum

    def extract(self, data):
        return data[6:]

    def r_seq(self, pkt):
        return int(pkt[5])

    def is_ack(self, pkt, n_seq):
        if not self.corrupt(pkt):
            return self.extract(pkt) == "_ACK" and self.r_seq(pkt) == n_seq

    def make_pkt(self, data, n_seq):
        checksum = str(self.checksum(data))
        data = checksum.zfill(5) + str(n_seq) + data
        return data

    def _send(self, msg):
        self.udp.sendto(msg.encode('ANSI'), self.dest)

    def _recv(self):
        data, cliente = self.udp.recvfrom(self.dest[1]+10)
        return data.decode('ANSi')

    def close(self):
        self.udp.close()

    def send(self, data):
        test = True
        state = 0
        def seq(x): return x % 2
        while state != -1:
            if state == 0:
                pkt = self.make_pkt(data, self.n_seq)
                self._send(pkt)
                state = 1
                #print("Enviando pacote: ", data, "seq: ", self.n_seq, ".")
                self.n_seq = seq(self.n_seq + 1)
            elif state == 1:
                try:
                    ARQ = self._recv()
                except socket.timeout:
                    print("Timeout. Reenviando pacote.")
                    state = 0
                    self.n_seq = seq(self.n_seq - 1)
                except ConnectionResetError:
                    print("Server off")
                else:
                    if(data == "erro" and test):  # Simular pacote corrompido
                        test = False
                        ARQ = "14578655g8"
                    if self.is_ack(ARQ, seq(self.n_seq - 1)) and not self.corrupt(ARQ):
                        state = -1
                        #print("ACK Recebido.")
                    else:
                        state = 0
                        self.n_seq = seq(self.n_seq - 1)
                        #print("ACK duplicado Recebido. Reenviando pacote.")

    def rdt_send(self, data):
        SEGMENT_SIZE = 4000
        offset = 0
        x = ceil(len(data)/SEGMENT_SIZE)
        self.send(str(x))
        while offset < len(data):
            if offset + SEGMENT_SIZE > len(data):
                segment = data[offset:]
            else:
                segment = data[offset:offset + SEGMENT_SIZE]
            offset += SEGMENT_SIZE
            self.send(segment)
        print(len(data))
        print("Pacote enviado", self.dest)


#dest_address = ('127.0.0.1', 40000)
#c1 = Sender(dest_address)

#msg = ""
#while msg != "x":
#    msg = input()
#    c1.rdt_send(msg)
#c1.close()
