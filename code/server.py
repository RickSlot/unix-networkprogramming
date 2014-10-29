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
    devices = pcapy.findalldevs() #Vind alle netwerk apparaten
    
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


    #open_live(apparaat, maximum-packet-lengte-in-bytes, promiscious_mode, timeout)
    #promiscious mode: Normaal gesproken ontvangt een netwerk interface alleen de packets die geadresseerd zijn aan die interface. In promiscious mode
    #onderschept hij alle pakketjes die hij langs ziet komen, of ze nou aan hem geadresseerd zijn of niet
    cap = pcapy.open_live(dev , 65536 , 1 , 0) #
 
    # start packets sniffing
    try:
        while 1:
            (header, packet) = cap.next() #Vind het volgende pakketje
            safe_packet(packet) #roept de safe packet methode aan met de gevonden Packet
    except KeyboardInterrupt:
        cur.close()
        db.close()
        sys.exit(1)
	
 
#  converteer een string naar een mac-adres
def eth_addr (a) :
    b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5])) #ord returned de integer waarde van een unicode
    return b
 
# 
def safe_packet(packet) :     
    #parse ethernet header
    eth_length = 14
    eth_header = packet[:eth_length] #: betekent slice, slice maakt een copy van 0 t/m eth_length(14) in dit geval
    eth = unpack('!6s6sH' , eth_header) #!6s6sH is de format, Hij maakt van bytes python objects

    #converteer 16-bit positieve integers van netwerk naar host byte volgorde. 
    #Op machines waar de host byte volgorde hetzelfde is als de netwerk byte volgorde wordt er niks gedaan,
    #anders wordt er een 2-byte swap operatie uitgevoerd
    eth_protocol = socket.ntohs(eth[2]) 
 
    #check of het protocol 8 is, IP
    if eth_protocol == 8 :
        # Slice het packet vanaf eth_length(14) tot 20+ethlength(14) = 34 dus  [14:34]
        ip_header = packet[eth_length:20+eth_length]
         
        #!BBHHHBBH4s4s is de format, Hij maakt van bytes python objects
        iph = unpack('!BBHHHBBH4s4s' , ip_header)
 


        version_ihl = iph[0] #krijg de ip_version en ip_header_length packet
        version = version_ihl >> 4 #bitshift 4 naar rechts om de versie van de ip_header_length in 4 bits te krijgen
        ihl = version_ihl & 0xF #get IP header length by using logical AND to 0xf #krijg de ip_header_length door logical AND met 0xf(15) te doen
        iph_length = ihl * 4 #vermenigvuldig de output met 4 om de ip_header_length te krijgen
 

        ttl = iph[5] #verkrijg de ttl(Time to live)
        protocol = iph[6] #verkrijg het protocol

        #inet_ntoa = Converteer een 32-bit ipv4 packet adress naar de standard four-dotted notatie( 192.168.1.1)
        s_addr = socket.inet_ntoa(iph[8]); #verkrijg source ip adress
        d_addr = socket.inet_ntoa(iph[9]); #verkrijg destination ip adress

        #TCP protocol
        if protocol == 6 :
            t = iph_length + eth_length #iph length + eth_length(14) als counter
            tcp_header = packet[t:t+20] #tcp header begint op t: en eindigt op t+20. dit wordt gesliced en in tcp_header gestopt
 

            #TODO: tcph mooier maken, renamen naar tcp_header
            tcph = unpack('!HHLLBBHHH' , tcp_header) #unpack de tcp header in het !HHLLBBHHH formaat
             
            #variables die in de database worden gestopt
            source_port = tcph[0]
            dest_port = tcph[1]
            sequence = tcph[2]
            acknowledgement = tcph[3]
            doff_reserved = tcph[4]
            tcph_length = doff_reserved >> 4 #logical bitshift 4 naar rechts
            

            if source_port != 22 and dest_port != 22: # filter ssh verkeer 
                #print 'Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol)
                #print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)
                #print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
                #print
                try:
                    # Execute the SQL command
                    cur.execute("INSERT INTO packets(dest_mac, src_mac, interface_protocol, version, ip_hdr_lngt, ttl, ip_protocol, src_adress, dest_adress, src_port, dest_port, seq_num, acknowledgement, tcp_header_lngt) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (eth_addr(packet[0:6]), eth_addr(packet[6:12]), str(eth_protocol), str(version), str(ihl), str(ttl), str(protocol), str(s_addr), str(d_addr), str(source_port), str(dest_port), str(sequence), str(acknowledgement), str(tcph_length)))
                    db.commit()
                except:
                    print 'exception'
                    db.rollback()
             
            #Hiermee kan je eventueel nog de data uit het pakketje halen
            # h_size = eth_length + iph_length + tcph_length * 4
            # data_size = len(packet) - h_size
            # #get data from the packet
            # data = packet[h_size:]

        # udp protocol
        elif protocol == 17 :
            u = iph_length + eth_length #iph_length + eth_length(14)
            udph_length = 8 # de header length van udp is 8
            udp_header = packet[u:u+udph_length]#udp header begint op u: en eindigt op u+udp_length(8). dit wordt gesliced en in udp_header gestopt

            
            udph = unpack('!HHHH' , udp_header) #unpack de udp header in het !HHHH formaat
            
            #variabelen om in de database te stoppen. 
            source_port = udph[0]
            dest_port = udph[1]
            length = udph[2]
            checksum = udph[3]
            
            #print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(length) + ' Checksum : ' + str(checksum)
            
            try:
                # Execute the SQL command
                cur.execute("INSERT INTO packetsudp(src_port, src_adress, dest_port, dest_adress, interface_protocol, version, length, checksum, ttl) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (str(source_port), str(s_addr), str(dest_port), str(d_addr), str(eth_protocol), str(version), str(length), str(checksum), str(ttl)))
                db.commit()
            except:
                print 'exception'
                db.rollback()


            #Als je de data eruit wil halen kan je dit gebruiken:
            # h_size = eth_length + iph_length + udph_length
            # data_size = len(packet) - h_size            
            # data = packet[h_size:]
            #print 'Data : ' + data


        else :
            print 'protocol is other'
                  
 
if __name__ == "__main__":
  main(sys.argv)
