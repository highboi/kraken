#modules for networking and multithreading
import socket
import threading
from krakenstore import *

'''
CODE FOR NETWORK INTERACTION USING THE KRAKEN PROTOCOL
'''

#broadcast a message to all peers on the local network using the broadcast address
def broadcast_message(msg):
	pass

#handle peer messages from the network
def handle_peer(peer_sock):
	#print the remote ip address of the peer
	print(peer_sock.getpeername())

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
