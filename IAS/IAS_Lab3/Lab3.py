import socket
from scapy.config import conf
from scapy.all import sniff
from scapy.all import *
from scapy.all import send
from scapy import all
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
f=open("output.txt","w")
def checkACL(packet):
	# print(packet.src)
	if IP in packet:
		ip_dst=packet[IP].dst
		ip_src=packet[IP].src
	if TCP in packet:
		dport=packet[TCP].dport
	print(ip_dst)
	if ip_src=="10.10.1.1" and dport==80:
		f.write("DENIED by Rule 1 from ACL file")
		print("DENIED by Rule 1 from ACL file")
		return 1
	if ip_dst=="100.100.100.100" and dport==80:
		f.write("DENIED by Rule 2 from ACL file")
		print("DENIED by Rule 2 from ACL file")
		return 1
	if ip_dst=="100.100.110.100" and dport==400:
		f.write("DENIED by Rule 3 from ACL file")
		print("DENIED by Rule 3 form ACL file")	
		return 1
	if ip_dst=="200.200.200.200":
		f.write("DENIED by Rule 4 from ACL file")
		print("DENIED by Rule 4 from ACL file")	
		return 1	
	if ip_dst=="100.102.100.102":
		f.write("DENIED by Rule 5 from ACL file")
		print("DENIED by Rule 5 from ACL file") 
		return 1
	else:
		f.write("DENIED by Rule 6 from ACL file")
		print("DENIED by Rule 6 from ACl file")
		return 1

			
def sendPacket(sourceIP,destIP,desport,srcport,option):
	# packet1 = IP(dst="10.100.54.1",src="10.100.55.1")/TCP()/"Packet1"
	# # print(packet.summary())
	# packet1.show()
	packet = IP(src=sourceIP,dst=destIP)/TCP(dport=desport,sport=srcport)/"This is the load part of the packet"
	if option==1:
		sr(packet,timeout=5)
	elif option==2:
		sr1(packet,timeout=5)
	elif option==3:
		srloop(packet,timeout=5)


global var
def callback(pack):
	print("Packet recieved")
	s=pack.show(dump=True)
	f.write(s)
	print(s)
	# NO NEED TO PRINT DENIED/ALLOWED:checkACL
	var=checkACL(pack)
	f.close()


	
	

def scapy_sniffing(src):
	var=0
	sniff(prn=callback,filter=src,store=0,count=10,timeout=3)
	# if var==0:
	# 	print("packets not recieved")



