import socket
import math
import random
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 8084
sock.connect((host, port))


p=467
q=479

s=223694

n=p*q
print("Private key = ",s)
print()
if s>n:
	print("The Private key is greater than n-1")
	exit()	

r=[15,16,41]
flag=0
for loo in range(3):

	if r[loo]>n-1:
		print("Invalid Random Value")
		flag=1
		continue

	print("For R=",r[loo])
	x=str(int(math.pow(r[loo],2)%n))

	sock.send(x.encode())
	c = int(sock.recv(2048).decode())

	y = int((r[loo]*math.pow(s,c))%n)

	sock.send(str(int(y)).encode())
	public_key=int(math.pow(s,2)%n)
	sock.send(str(public_key).encode())
	qwer=input("press enter\n")
	flag=0
if flag==1:
	sock.send(str("-1").encode)