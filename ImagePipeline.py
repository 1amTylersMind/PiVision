import os, sys, numpy as np, socket, threading
from PIL import Image
import hashlib
from Crypto.Cipher import AES
from Crypto import Random


def hand_shake(client, addr):
    passwd = client.recv(1024)
    # Send back ACK
    client.send('ACK '+passwd)
    return passwd


def phone_home(img_dims):
    msg = 'INCOMING IMAGE\n'+str(img_dims)+'\nEOM'
    # whip up a quick socket
    s = socket.socket()
    s.bind(('0.0.0.0',9999))
    s.listen(5)
    remotes = []
    keys = []
    try:
        client, addr = s.accept()
        client_handler = threading.Thread(target=hand_shake,args=(client,addr))
        key = client_handler.start()
        remotes.append(addr)
        keys.append(key)
    except IOError:
        s.close()
        exit(0)

    print addr
    print key


def aes_encrypt(password,message):
    key = hashlib.sha256(password).hexdigest()[0:16]
    iv = Random.new().read(AES.block_size)
    ciph = AES.new(key, AES.MODE_CFB, iv)
    return iv + ciph.encrypt(bytes(message)), iv


def aes_decrypt(ciphertext,password,iv):
    key = hashlib.sha256(password).hexdigest()[0:16]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(bytes(ciphertext))


def usage():
    print "Incorrect Usage!"
    exit(0)


def main():
    debug = False
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        # Capture image (debug supplies existing image)
        print "Snapping Image"
        os.system('raspistill -o ' + fname)
        # Convert Image to matrix
        image_data = np.array(Image.open(fname))
        # Let the user know the picture was taken successfully
        print 'Image Captured!'
        print '[Dimension ' + str(image_data.shape) + ']'
        phone_home(image_data.shape)
    else:
        usage()


if __name__ == '__main__':
    main()
