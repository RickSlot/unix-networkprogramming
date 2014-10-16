import socket
from struct import *
import datetime
import pcapy
import sys
import MySQLdb

db = MySQLdb.connect(host="localhost",
                     user="unix", 
                     passwd="123",
                     db="sniffer") 
cur = db.cursor()


def main(argv):
    devices = pcapy.findalldevs()
    
    print "Adapter to sniff"
    adapterList = []
    for d in devices :
    	if d == 'eth0' or d == 'eth1':
    		adapterList.append(d)
        	print d
    if len(adapterList) != 1:
    	dev = raw_input("Enter adapter name : ")
    else: 
   	dev = adapterList[0]
    # open selected device     
    cap = pcapy.open_live(dev , 65536 , 1 , 0)
 
    # start packets sniffing
    try:
        while(True) :
            (header, packet) = cap.next()
            safe_packet(packet)
    except KeyboardInterrupt:
        cur.close()
        db.close()
	sys.exit(1)
 
#  convert string to mac address
def eth_addr (a) :
    b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
    return b
 
# handel packet
def safe_packet(packet) :     
    #parse ethernet header
    eth_length = 14
     
    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH' , eth_header)
    eth_protocol = socket.ntohs(eth[2])
 
    #Parse IP packets, IP Protocol number = 8
    if eth_protocol == 8 :
        #Parse IP header
        #take first 20 characters for the ip header
        ip_header = packet[eth_length:20+eth_length]
         
        #now unpack them :)
        iph = unpack('!BBHHHBBH4s4s' , ip_header)
 
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
 
        iph_length = ihl * 4
 
        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);
  
        #TCP protocol
        if protocol == 6 :
            t = iph_length + eth_length
            tcp_header = packet[t:t+20]
 
            tcph = unpack('!HHLLBBHHH' , tcp_header)
             
            source_port = tcph[0]
            dest_port = tcph[1]
            sequence = tcph[2]
            acknowledgement = tcph[3]
            doff_reserved = tcph[4]
            tcph_length = doff_reserved >> 4
            

            if source_port != 22 and dest_port != 22: # filter ssh traffic 
                print 'Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol)
                print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)
                print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
                print
                try:
                    # Execute the SQL command
                    cur.execute("INSERT INTO packets(dest_mac, src_mac, interface_protocol, version, ip_hdr_lngt, ttl, ip_protocol, src_adress, dest_adress, src_port, dest_port, seq_num, acknowledgement, tcp_header_lngt) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (eth_addr(packet[0:6]), eth_addr(packet[6:12]), str(eth_protocol), str(version), str(ihl), str(ttl), str(protocol), str(s_addr), str(d_addr), str(source_port), str(dest_port), str(sequence), str(acknowledgement), str(tcph_length)))
                    db.commit()
                except:
                    print 'exception'
                    db.rollback()
             
            h_size = eth_length + iph_length + tcph_length * 4
            data_size = len(packet) - h_size
             
            #get data from the packet
            data = packet[h_size:]
        # udp protocol
        elif protocol == 17 :
            u = iph_length + eth_length
            udph_length = 8
            udp_header = packet[u:u+8]

            #now unpack them :)
            udph = unpack('!HHHH' , udp_header)
            
            source_port = udph[0]
            dest_port = udph[1]
            length = udph[2]
            checksum = udph[3]
            
            print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(length) + ' Checksum : ' + str(checksum)
            
            try:
                # Execute the SQL command
                cur.execute("INSERT INTO packetsudp(src_port, dest_port, length, checksum) VALUES ('%s', '%s', '%s', '%s')" % (str(source_port), str(dest_port), str(length), str(checksum)))
                db.commit()
            except:
                print 'exception'
                db.rollback()

            h_size = eth_length + iph_length + udph_length
            data_size = len(packet) - h_size
            
            #get data from the packet
            data = packet[h_size:]
            
            print 'Data : ' + data


        else :
            print 'protocol is other'
                  
 
if __name__ == "__main__":
  main(sys.argv)
