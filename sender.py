from socket import *
import sys
from packet import *
import signal

n_emulator_address = sys.argv[1]
n_emulator_port = int(sys.argv[2]) 
server_port = int(sys.argv[3]) 
timeout = int(sys.argv[4]) 
max_window_size = int(sys.argv[5]) 
file_name = sys.argv[6]

window_size = 5
window = []                         # window that will save and send all the packets
file = open(file_name,"r")
last_seq_num = 0

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', server_port))

def handler(signum, frame):                 # For timeout
    global window
    global window_size

    if(window == []):
        if(window_size + 1 <= max_window_size):
            window_size += 1
    else:
        for i in range(len(window)):       #Retransmit all packets
            serverSocket.sendto(window[i].encode(), (n_emulator_address, n_emulator_port))
        window_size = 5

    raise Exception("Receive Done")

signal.signal(signal.SIGALRM, handler)

while True:
    try:
        for i in range(window_size):
            if( i >= len(window) ):             #If in-transit packets are less than 5, create new packets
                data = file.read(500)

                if(data == ''):
                    if(window == []):                       #If all packets been sent, send EOT
                        packet = Packet(2, 0, 0, '')
                        serverSocket.sendto(packet.encode(), (n_emulator_address, n_emulator_port))
                        message, client_address = serverSocket.recvfrom(2048)
                        packet = Packet(message)
                        if (packet.typ == 2):
                            serverSocket.close()
                            raise Exception("Done")
                        else:
                            raise Exception("EOT wasn't send after I sent EOT")
                    else:                                   #Receive Acks first for all packets
                        break

                packet = Packet(1, last_seq_num, len(data), data)   # Create new packets
                last_seq_num += 1
                window.append(packet)
                serverSocket.sendto(window[i].encode(), (n_emulator_address, n_emulator_port))
        try:                                    #timer on receiving the ACKs
            signal.setitimer(signal.ITIMER_REAL, timeout / 1000)
            while True:
                message, client_address = serverSocket.recvfrom(2048)
                packet = Packet(message)
                
                if (packet.typ == 0):              
                    for i in range(len(window)):
                        if(window[i].seqnum == packet.seqnum):
                            window.pop(i)
                            break
        except Exception as e:
            signal.setitimer(signal.ITIMER_REAL, 0) # Disable the alarm
    except Exception as e:
        break
