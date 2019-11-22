import socket
import time


class Receiver:
    def __init__(self, address):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.orig = address
        self.udp.bind(self.orig)
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

    def make_pkt(self, data, n_seq):
        checksum = str(self.checksum(data))
        data = checksum.zfill(5) + str(n_seq) + data
        return data

    def _send(self, msg):
        self.udp.sendto(msg.encode('ANSI'), self.dest)

    def _recv(self):
        data, cliente = self.udp.recvfrom(self.orig[1]+10)
        self.dest = cliente
        return data.decode('ANSI')

    def close(self):
        self.udp.close()

    def recv(self):
        def seq(x): return x % 2
        while True:
            pkt = self._recv()
            data = self.extract(pkt)
            r_seq = self.r_seq(pkt)
            if data == "n_internet":
                time.sleep(10)
            if not self.corrupt(pkt) and r_seq == self.n_seq:
                pkt = self.make_pkt("_ACK", self.n_seq)
                if data != "espere":  # Simular o ack sendo perdido
                    self._send(pkt)
                self.n_seq = seq(self.n_seq + 1)
                #print("Recebendo pacote: ", data, "seq: ", r_seq, ".")
                #print("ok")
                return data
            elif self.corrupt(pkt) or r_seq != self.n_seq:
                pkt = self.make_pkt("_ACK", seq(self.n_seq-1))
                self._send(pkt)
                #print("Pacote corrompido ou duplicado. Enviando N° seq: ",
                #      seq(self.n_seq-1))

    def rdt_recv(self):
        x = int(self.recv())
        data = ""
        for i in range(x):
            data += self.recv()
        print(x)
        print('Pacote Recebido', self.orig)
        return data


#dest_address = ('127.0.0.1', 40000)
#c1 = Receiver(dest_address)
#
#msg = "a"
#while msg != "x":
#    msg = c1.rdt_recv()
#    print(msg)
#c1.close()
