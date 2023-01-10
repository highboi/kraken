'''
CODE FOR IMPORTING IMPORTANT LIBRARIES FOR NETWORKING AND COMMUNICATION
'''

#import libraries for networking and multithreading
from scapy.all import *
import socket
import threading
import json
import os

#local libraries to import for avoiding hairball code
from krakenstore import *
from krakenscan import *
from krakencomm import *

'''
CODE FOR SETTING UP VARIABLES USED LATER IN THE CODE
'''

#a cache for data not stored locally
cache = {}

#initialize a simple local database
initData()

#scan peers on the network
peeraddrs = scan_peers()

#connect to active peers and get the socket connections
peersockets = connect_peers(peeraddrs)

'''
CODE FOR STARTING/MAINTAINING NETWORK INTERACTION
'''
run_node()
