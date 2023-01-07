from scapy.all import *
import socket
import json


#an array to store ip/port tuples for communication
peers = []

#a cache for data not stored locally
cache = {}

'''
FUNCTIONS FOR HANDLING STORAGE OF DATA LOCALLY
'''

#function for initializing a simple database
def initData():
	#create a database txt file if it does not exist
	if (not os.path.exists("./database.txt")):
		#create the new file
		file = open("database.txt", "x")
		file.close()

		#write data to the new file
		file = open("database.txt", "w")
		file.write("{}")
		file.close()

#function for reading data from the simple db
def readData(key):
	#open the file and read the contents
	file = open("./database.txt", "r")
	data = file.read()
	data = json.loads(data)
	file.close()

	#check if the data exists or not
	if (key in data):
		return data[key]
	else:
		return None

#function for writing data to the simple db
def writeData(key, value):
	#read current data in the file and alter it
	file = open("./database.txt", "r")
	data = file.read()
	data = json.loads(data)
	data[key] = value
	file.close()

	#write the new data to the file
	file = open("database.txt", "w")
	file.write(json.dumps(data))
	file.close()

#initialize the simple database
initData()

'''
CODE FOR CONNECTING TO SOCKET PEERS
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

		print("ACTIVE:", active)

		#append the peer if it is actively connected to the network on the designated port
		if active:
			peers.append((peerip, peerport))

	#return the final list of ip/port pairs of active peers on the network
	return peers

#scan peers on the network
peers = scanPeers()

