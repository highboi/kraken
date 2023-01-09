#import libraries for networking and multithreading
from scapy.all import *
import socket
import threading
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

#scan peers on the network
peers = scanPeers()


'''
CODE FOR CONNECTING TO OTHER PEERS ON THE NETWORK ON THEIR SOCKET SERVERS
'''

#make a global list of peer socket connections
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

'''
CODE FOR RUNNING A SERVER FOR OTHER PEERS TO CONNECT TO
'''

#handle peer messages from the network
def handle_peer(peer_sock):
	#constantly recieve data from the peer
	while True:
		#get data from the peer
		data = client_sock.recv(4096)

		#if the data doesn't exist, the peer broke the connection
		if not data:
			break

		#parse the data and the event associated with this
		data = json.loads(data)
		event = data["event"]

		#create a response or perform actions based on the event
		if (event == "relay-get"):
			value = readData(data["key"])

			if (value != None or len(data["batonholders"]) == data["echo"]):
				valueObj = {"event": "relay-get-response", "key": data["key"], "value": value, "batonholders": data["batonholders"]}
				valueObj = json.dumps(valueObj)

				#SEND DATA BACK TO ORIGINAL REQUESTER
			else:
				data["batonholders"].append("a")

				dataObj = {"key": data["key"], "event": "relay-get", "echo": data["echo"], "batonholders": data["batonholders"]}

				#SEND DATA REQUEST TO ALL PEERS
		elif (event == "relay-put"):
			writeData(data["key"], data["value"])

			data["batonholders"].append("a")

			if (len(data["batonholders"]) < data["echo"]):
				#RELAY THIS REQUEST TO OTHER PEERS
				pass
		elif (event == "relay-get-response"):
			cache[data["key"]] = data["value"]

			#SIGNAL THAT THE DATA HAS BEEN FETCHED FROM THE NETWORK

		#send data back to the peer based on the data recieved
		peer_sock.sendall(data.upper())

#run the socket server to recieve messages from peers on the network
def run_node():
	#make a socket and bind it to this address and a specified port
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(("", 8000))

	#listen for incoming connections
	sock.listen()

	print("BOOTING NODE...")

	#loop to accept multiple connections
	while True:
		#accept a new connection from a peer on the network
		peer_sock, peer_addr = sock.accept()

		#start the thread for handling requests/responses with the peer
		peer_thread = threading.Thread(target=handle_peer, args=(peer_sock,))
		peer_thread.start()

	#close the socket if done
	sock.close()

#boot the node on the network
#run_node()

