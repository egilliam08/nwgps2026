# Help: https://www.eventhelix.com/networking/ftp/
# Help: https://www.eventhelix.com/networking/ftp/FTP_Port_21.pdf
# Help: https://realpython.com/python-sockets/
# Help: PASV mode may be easier in the long run. Active mode works 
# Reading: https://unix.stackexchange.com/questions/93566/ls-command-in-ftp-not-working
# Reading: https://stackoverflow.com/questions/14498331/what-should-be-the-ftp-response-to-pasv-command

#import socket module
from socket import *
import sys # In order to terminate the program

def quitFTP(clientSocket):
    # COMPLETE
    dataOut = command.encode("utf-8")
    clientSocket.sendall(dataOut)
    dataIn = clientSocket.recv(1024)
    data = dataIn.decode("utf-8")
    print(data)

def sendCommand(socket, command):
    dataOut = command.encode("utf-8")
    # Complete
    return data



def receiveData(clientSocket):
    dataIn = clientSocket.recv(1024)
    data = dataIn.decode("utf-8")
    return data

# If you use passive mode you may want to use this method but you have to complete it
# You will not be penalized if you don't
def modePASV(clientSocket):
    command = "PASV" + "\r\n"
    # Complete
    status = 0
    if data.startswith(""):
        status = 227
        # Complete
        dataSocket.connect((ip, port))
        
    return status, dataSocket

    
    
def main():
    # COMPLETE

    username = input("Enter the username: ")
    password = input("Enter the password: ")

    clientSocket = socket(AF_INET, SOCK_STREAM) # TCP socket
    # COMPLETE

    HOST = # COMPLETE
    # COMPLETE

    dataIn = receiveData(clientSocket)
    print(dataIn)

    status = 0
    
    if dataIn.startswith(""):
        status = 220
        print("Sending username")
        # COMPLETE
        
        print(dataIn)

        print("Sending password")
        if dataIn.startswith(""):
            status = 331
            # COMPLETE
            
            print(dataIn)
            if dataIn.startswith(""):
                status = 230

       
    if status == 230:
        # It is your choice whether to use ACTIVE or PASV mode. In any event:
        # COMPLETE
        pasvStatus, dataSocket = modePASV(clientSocket)
        if pasvStatus == 227:
            # COMPLETE
    
    print("Disconnecting...")
    

    clientSocket.close()
    dataSocket.close()
    
    sys.exit()#Terminate the program after sending the corresponding data

main()

