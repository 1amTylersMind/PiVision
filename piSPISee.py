import sys, hashlib, os, socket
hasGPIO = False
try:
    import RPi.GPIO as GPIO
    hasGPIO = True
except ImportError:
    pass


class Sender:

    @staticmethod
    def one_way_msg(message, where, to):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((where, to))
        sock.send(message)
        print 'Sending Message to: '+where
        response = sock.recv(1024)
        sock.close()
        return response


class Reciever:

    @staticmethod
    def one_way_reader(where, what):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((where, what))
        message = sock.recv(4096)
        sock.close()
        return message

    @staticmethod
    def tcp_server():
        if hasGPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(22,GPIO.OUT)
            GPIO.output(22,GPIO.HIGH)
        print ":: Opening Listener on Port 9999 ::"
        running = True

        
def whoAmI():
    # os.system("sudo su")
    os.system("touch self.txt")
    os.system("ifconfig >> self.txt")
    f = open("self.txt", "r")
    ip = ""
    mac = ""
    interfaces = []
    donuthin = 0
    for ln in f.readlines():
        #print(ln)
        try:
            ip = ln.split("inet ")[1].split("netmask")[0]
            mac = ln.split("ether ")[1].split("tx")[1]
            interfaces.append(ln.split(": flags")[0])
        except:
            donuthin += 1
    os.system("rm self.txt")
    return ip, mac, interfaces


def main():

    peers = {}

    if len(sys.argv) > 2:
        if sys.argv[2] != '-pi':
            # Get the name of peer to connect to
            peerIP = sys.argv[1]
            # Get own address
            ip, mac, interfaces = whoAmI()
            # Generate a Peer Id
            myID = hashlib.sha256(ip + mac).hexdigest()
            # Send UserID to PI
            Sender.one_way_msg(myID, peerIP, 9999)
            # Get the reply of the user's own Peer ID
            peerID = Reciever.one_way_reader(peerIP, 9999)
            peers[peerIP] = peerID
            print 'Completed Handshake With Peer ' + peerIP + '[' + peerID + ']'
    if len(sys.argv) > 1:
        if sys.argv[1] == '-pi':
            ip,mac, interfaces  = whoAmI()
            # Generate PeerID
            myID = hashlib.sha256(ip+mac).hexdigest()



if __name__ == '__main__':
    main()