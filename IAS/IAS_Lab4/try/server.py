import socket
import sys
from random import *
from math import floor
host = 'localhost'
port = 1367
address = (host, port)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(5)

f=open("Server","w")
print ("Listening for client . . .")
conn, address = server_socket.accept()
print ("Connected to client at ", address)


N=int(conn.recv(2048).decode())
print("Recieved N:",N)
v=int(conn.recv(2048).decode())
print("Recieved Claimants Public Key v=",v)

f.write("Recieved N:"+str(N)+"\n")
f.write("Recieved Claimants Public Key v="+str(v)+"\n")

count =1
while count!=4:
    print("Round ",count,"***************************")
    f.write("Round "+str(count)+"\n")
    x = conn.recv(1024).decode()
    if(x=="ERR"):
        print("Not Authorized, Error.")
        f.write("Not Authorized. Error ")
        count+=1
        exit(0)
        continue
    x=int(x)
    print("Recieved x=",x)
    f.write("Recieved x="+str(x)+"\n")
    c=int(input("Enter Challenge c:"))
    f.write("Entered Challenge c:"+str(c)+"\n")
    print("c=",c)

    conn.send(str(c).encode())
    y=int(conn.recv(2048).decode())
    print("y=",y)
    f.write("Response from Claimant:"+str(y)+"\n")
    result = x*pow(v,int(c))%N
    print("result=",result)
    f.write("result="+str(result)+"\n")
    if (y**2)%N==result :
        print("Authorized")
        f.write("Authorized\n")
    else:
        print("You are not Authorized")
        f.write("Your are not Authorized")

    count+=1

