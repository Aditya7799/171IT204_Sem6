import socket
import time
from random import *
from math import floor

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 1367))

f=open("Client.txt","w")
P=int(input("Enter P:"))
Q=int(input("Enter Q:"))
N=P*Q
f.write("Generated N:"+str(N)+"\n")
client_socket.send(str(N).encode())

S=int(input("Enter S:"))
v=(S**2)%N
f.write("Generated Public Key "+str(v)+"\n")
client_socket.send(str(v).encode())




count=1
while count!=4:

	print("Round ",count,"\n")
	f.write("Round "+str(count)+"\n")
	if(S>N-1):
		print("S>N-1 Invalid Input")
		f.write("S>N-1 Invalid Input")
		client_socket.send("ERR".encode())
		count+=1
		exit(0)
		continue
	r=int(input("Enter Random Number:"))
	print("r=",r)
	if(r>N-1):
		print("r > N-1 Invalid Input")
		f.write("r>N-1 Invalid Input")
		count+=1
		client_socket.send("ERR".encode())
		exit(0)
		continue
	x=str(pow(r,2,N))
	client_socket.send(x.encode())
	print("x=",x)
	f.write("Random number r ="+str(r)+"\n"+ "Witness x="+str(x)+"\n")	

	c = int(client_socket.recv(2048).decode())
	print("Challenge c=",c)
	f.write("Challege c="+str(c)+"\n")
	y=str(r*pow(S,c)%N)
	print("y=",y)
	f.write("Response y="+str(y)+"\n")
	client_socket.send(y.encode())
	f.write("***********************************\n")

	count+=1