import csv
f=open("output.txt","w")
def hexdec(a):
    l=[int(i,base=16) for i in a]
    s=""
    for x in l:
    	s=s+":"+str(x)
    return s[1:]


def verifyACL(sip):
	sip=sip.split(':')
	print(sip)
	if(int(sip[0])==10 and int(sip[1])==100 and int(sip[2])==53):
		return True
	else:
		return False

def read_hexdump():
	"""Note input file is to be changed here"""
	f = open("hex-dump.txt","r").read()
	frames = f.split('\n')

	while '' in frames:
		frames.remove('')
	# print(frames)
	return frames


def decode_packet(packet):
	
	dest_mac=(packet[:6])
	dmac=""
	for x in dest_mac:
		dmac=dmac+":"+str(x)
	dmac=dmac[1:]

	source_mac=(packet[6:12])
	smac=""
	for x in source_mac:
		smac=smac+":"+str(x)
	smac=smac[1:]

	ether_ver=hexdec(packet[12:14])
	
	ip_ver=int(packet[14][0])
	no_bytes_header=packet[14][1]
	differentiated_services=packet[15]
	length_of_IP_header=hexdec(packet[16:18])
	fragment_id=hexdec(packet[18:20])
	fragment_field=hexdec(packet[20:22])
	ttl=packet[22]


	protocol=int(packet[23],16)
	if(protocol==6):
		protocol="TCP"
	elif(protocol==17):
		protocol="UDP"

	checksum=hexdec(packet[24:26])
	source_IP=hexdec(packet[26:30])
	dest_IP=hexdec(packet[30:34])
	source_port=int(''.join(packet[34:36]),16)
	dest_port=int(''.join(packet[36:38]),16)
	
	print("Source IP-"+source_IP)
	print("Destination IP-"+dest_IP)
	print("Source Port-"+str(source_port))
	print("Destination Port-"+str(dest_port))
	print("Destination Mac Address-"+dmac)
	print("Source Mac Address-"+smac)
	print("Ethernet Address-"+ether_ver[1:])
	print("IP Version-"+"IPv"+str(ip_ver))
	print("No. of bytes in Header-"+str(no_bytes_header)+"bytes")
	print("Length of Header-"+str(length_of_IP_header[3:]))
	print("Protocol-"+protocol)
	

	f.write("Source IP :-"+source_IP+"\n")
	f.write("Destination IP :-"+dest_IP+"\n")
	f.write("Source Port :-"+str(source_port)+"\n")
	f.write("Destination Port :-"+str(dest_port)+"\n")
	f.write("Destination Mac Address :-"+dmac+"\n")
	f.write("Source Mac Address :-"+smac+"\n")
	f.write("Ethernet Address :-"+ether_ver[1:]+"\n")
	f.write("IP Version :-"+"IPv"+str(ip_ver)+"\n")
	f.write("No. of bytes in Header :-"+str(no_bytes_header)+"bytes\n")
	f.write("Length of Header :-"+str(length_of_IP_header[3:])+"\n")
	f.write("Protocol :-"+protocol+"\n")

	if(verifyACL(source_IP)):
			print("PACKET ALLOWED")
			f.write("PACKET ALLOWED\n")
	else:
		print("PACKET DENIED")
		f.write("PACKET DENIED\n")
	print("******************************************************************")
	

	f.write("*****************************************************************\n")
	
	return [source_IP,source_port,dest_IP,dest_port,ip_ver]


def main():
	frames=read_hexdump()
	for frame in frames:
		frame = frame.split(' ')
		packet_details = decode_packet(frame)
		# print(x)
		

if __name__ == '__main__':
	main()
