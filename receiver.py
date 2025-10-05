from socket import *
import sys
from packet import *
from heapq import *

n_emulator_address = sys.argv[1]
n_emulator_port = int(sys.argv[2]) 
client_port = int(sys.argv[3]) 
buffer_size = int(sys.argv[4]) 
file_name = sys.argv[5]

file = open(file_name,"w")
arrival = open("arrival.log", "w")
buffer = []                             # Heap of tuples (packet.seqnum, packet)
next_seq_num = 0

# n_emulator_address = '127.0.0.1'
# n_emulator_port = int(sys.argv[1]) 
# client_port = int(sys.argv[2])
# buffer_size = 5
# file_name = "test_server"

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(('', client_port))
# client_port = (clientSocket.getsockname()[1])

while True:
    message, server_name = clientSocket.recvfrom(2048)
    packet = Packet(message)
    
    if (packet.typ == 1):
        if(len(buffer) >= buffer_size or packet.seqnum >= next_seq_num + buffer_size): #Drop
            arrival.write(f"{packet.seqnum}D\n")
            continue
        sendAck = Packet(0, packet.seqnum, 0, '')
        clientSocket.sendto(sendAck.encode(), (n_emulator_address, n_emulator_port))

        found = False #Is packet already in buffer or was in buffer
        if(packet.seqnum < next_seq_num):               #Drop but Acknowledged
            arrival.write(f"{packet.seqnum}D\n")
            continue
        for i in range(len(buffer)):
            if(packet.seqnum == buffer[i][1].seqnum):
                found = True
                break
        if(found):                                     #Drop but Acknowledged
            arrival.write(f"{packet.seqnum}D\n")
            continue
        
        # Push latest and write if applicable
        heappush(buffer, (packet.seqnum, packet))
        arrival.write(f"{packet.seqnum}B\n")
        while True:
            if(buffer != [] and buffer[0][1].seqnum == next_seq_num):
                file.write(heappop(buffer)[1].data)
                next_seq_num += 1
            else: 
                break
         
    elif (packet.typ == 2):
        arrival.write("EOT")
        packet = Packet(2, 0, 0, '')
        clientSocket.sendto(packet.encode(), (n_emulator_address, n_emulator_port))
        clientSocket.close()
        break

    clientSocket.sendto(packet.encode(), (n_emulator_address, n_emulator_port))