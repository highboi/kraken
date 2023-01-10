#import modules for network interaction
from scapy.all import *
import socket

'''
CODE FOR COLLECTING PEERS ON THE NETWORK
'''

#a function to see if a host is active on a port or not
def scanHost(host, port):
	#make a socket and set the timeout to 2 seconds
	s = socket.socket()
	s.settimeout(2)

	#try connecting to the ip/port pair and return true or false based on the connection working
	try:
		s.connect((host, port))
		return True
	except socket.error as e:
		return False
	finally:
		s.close()

#a function for getting all of the active peers on a specific subnet
def scanPeers(subnet="192.168.88.0/24"):
	print("SCANNING FOR PEERS...")

	#send arp requests to the local network
	answered, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=subnet), timeout=2)

	#a list to store ip/port pairs of peers
	peers = []

	#the port to scan for
	peerport = 8000

	#loop through the peers that responded to the arp requests
	for send, recv in answered:
		#get the peer ip address on the local network
		peerip = recv[ARP].psrc

		#scan the host to see if it is active on the designated port
		active = scanHost(peerip, peerport)

		#append the peer if it is actively connected to the network on the designated port
		if active:
			peers.append((peerip, peerport))

	#return the final list of ip/port pairs of active peers on the network
	return peers

#a function for connecting to a list of ip/port pairs and returning a list of socket connections
def connectPeers(peers):
	#a list to store the socket connections
	peersockets = []

	#check to see if there are any active peers on the network
	if (len(peers)):
		#loop through the ip/port pairs of each peer
		for peer in peers:
			#connect to this peer on the local network
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect(peer)

			#add the peer to the list
			peersockets.append(sock)

	#return the list of peers to communicate with
	return peersockets
