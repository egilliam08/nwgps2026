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
    command = "QUIT" + "\r\n"
    dataOut = command.encode("utf-8")
    clientSocket.sendall(dataOut)
    dataIn = clientSocket.recv(1024)
    data = dataIn.decode("utf-8")
    print(data)
    if data.startswith("221"):
        print("Success")
    else:
        print("Failed")

def sendCommand(socket, command):
    dataOut = command.encode("utf-8")
    socket.sendall(dataOut)
    dataIn = socket.recv(1024)
    data = dataIn.decode("utf-8")
    return data



def receiveData(clientSocket):
    dataIn = clientSocket.recv(1024)
    data = dataIn.decode("utf-8")
    return data

# If you use passive mode you may want to use this method but you have to complete it
# You will not be penalized if you don't
def modePASV(clientSocket):
    command = "PASV" + "\r\n"
    dataSocket = socket(AF_INET, SOCK_STREAM)
    data = sendCommand(clientSocket, command)
    status = 0
    if data.startswith("227"):
        status = 227
        start = data.find("(")
        end = data.find(")")
        numbers = data[start+1:end].split(",")

        ip = ".".join(numbers[0:4])
        port = int(numbers[4]) * 256 + int(numbers[5])
        dataSocket.connect((ip, port))
        
    return status, dataSocket

    
    
def main():
    if len(sys.argv) != 2:
        print("Usage: python program1.py inet.cs.fiu.edu")
        sys.exit(1)

    username = input("Enter the username: ")
    password = input("Enter the password: ")

    HOST = sys.argv[1]
    PORT = 21

    clientSocket = socket(AF_INET, SOCK_STREAM) # TCP socket
    clientSocket.connect((HOST, PORT))

    dataIn = receiveData(clientSocket)
    print(dataIn)

    status = 0
    
    if dataIn.startswith("220"):
        status = 220
        print("Sending username")
        command = "USER " + username + "\r\n"
        dataIn = sendCommand(clientSocket, command)
        print(dataIn)

        print("Sending password")
        if dataIn.startswith("331"):
            status = 331
            command = "PASS " + password + "\r\n"
            dataIn = sendCommand(clientSocket, command)
            print(dataIn)
            if dataIn.startswith("230"):
                status = 230

       
    if status == 230:
        # It is your choice whether to use ACTIVE or PASV mode. In any event:
        print("Success\n")
        pasvStatus, dataSocket = modePASV(clientSocket)
        if pasvStatus == 227:
            print("Entering Passive Mode")
        
        while True:
            command = input("myftp> ").strip()
            
            if not command:
                continue
            
            parts = command.split()
            cmd = parts[0].lower()
            
            if cmd == "quit":
                quitFTP(clientSocket)
                break

            elif cmd == "ls":
                # List files
                status, dataSocket = modePASV(clientSocket)
                if status == 227:
                    sendCommand(clientSocket, "LIST\r\n")
                    fileList = ""
                    while True:
                        data = dataSocket.recv(4096)
                        if not data:
                            break
                        fileList += data.decode("utf-8")
                    dataSocket.close()
                    receiveData(clientSocket)
                    print(fileList.rstrip())
                    print("Success\n")
                else:
                    print("Failed\n")

            elif cmd == "cd":
                # Change directory 
                if len(parts) < 2:
                    print("Usage: cd remote-dir")
                else:
                    response = sendCommand(clientSocket, "CWD " + parts[1] + "\r\n")
                    print(response)
                    if response.startswith("250"):
                        print("Success\n")
                    else:
                        print("Failed\n")

            elif cmd == "get":
                # Get file
                if len(parts) < 2:
                    print("Usage: get remote-file")
                else:
                    status, dataSocket = modePASV(clientSocket)
                    if status == 227:
                        bytesTransferred = 0
                        sendCommand(clientSocket, "RETR " + parts[1] + "\r\n")
                        with open(parts[1], 'wb') as f:
                            while True:
                                data = dataSocket.recv(4096)
                                if not data:
                                    break
                                f.write(data)
                                bytesTransferred += len(data)
                        dataSocket.close()
                        receiveData(clientSocket)
                        print(f"Success: {bytesTransferred} bytes transferred\n")
                    else:
                        print("Failed\n")

            elif cmd == "put":
                # Put file
                if len(parts) < 2:
                    print("Usage: put local-file")
                else:
                    # Check if file exists first (before creating PASV connection)
                    try:
                        testFile = open(parts[1], 'rb')
                        testFile.close()
                    except FileNotFoundError:
                        print("Failed: Local file not found\n")
                    except:
                        print("Failed\n")
                    else:
                        # File exists, proceed with upload
                        status, dataSocket = modePASV(clientSocket)
                        if status == 227:
                            bytesTransferred = 0
                            sendCommand(clientSocket, "STOR " + parts[1] + "\r\n")
                            with open(parts[1], 'rb') as f:
                                while True:
                                    data = f.read(4096)
                                    if not data:
                                        break
                                    dataSocket.sendall(data)
                                    bytesTransferred += len(data)
                            dataSocket.close()
                            receiveData(clientSocket)
                            print(f"Success: {bytesTransferred} bytes transferred\n")
                        else:
                            print("Failed\n")

            elif cmd == "delete":
                # Delete file
                if len(parts) < 2:
                    print("Usage: delete remote-file")
                else:
                    response = sendCommand(clientSocket, "DELE " + parts[1] + "\r\n")
                    print(response.rstrip())
                    if response.startswith("250"):
                        print("Success\n")
                    else:
                        print("Failed\n")
            else:
                print("Unknown command. Available: ls, cd, get, put, delete, quit")

    print("Disconnecting...")
    

    clientSocket.close()
    dataSocket.close()
    
    sys.exit()#Terminate the program after sending the corresponding data

main()

