import socket
import math
host = '127.0.0.1'
port = 8084
address = (host, port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(address)
s.listen()
conn,addr=s.accept()

p=int(input("Enter P"))
q=int("Enter Q")

c=[0,0,1]

n=p*q
print("Values of")
print("P = ",p)
print("Q = ",q)
print("N = ",n)

print("*********************************************************	")
loo=0
while True:
	if loo>=len(c):
		exit()
	try:
		# qwer=input("Enter")
		x = int(conn.recv(2048).decode())
		if x==-1:
			exit()
	except:
		print("Connection terminated. Invalid parameters")
		exit()
	
    
	print("ROUND ",loo+1,", for c=",c[loo])
	conn.send(str(c[loo]).encode())
	y=int(conn.recv(2048).decode())
	v=int(conn.recv(2048).decode())
	res=(x*math.pow(v,c[loo]))%n
	if (y**2)%n==res:
		 print("Probable")
	else:
		print("Improbable")
	print("**********************************************************")
	loo+=1
