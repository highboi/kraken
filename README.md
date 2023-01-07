# Kraken: IoT and Edge Computing Software

![Kraken Logo](https://github.com/highboi/kraken/blob/master/kraken_logo_blue.png)

# Synopsis:

Kraken is a piece of networking software that aims to bring edge computing and IoT (Internet-of-Things) to the big audience. By using wireless communication, data torrenting, and
wireless cluster computing, the collection of data through the use of hardware can become easier across all industries. By allowing anyone to establish, in essence, a wireless
supercomputer with modular, hot-swappable hardware, advances in scientific research, space exploration, defense, manufacturing, logistics, robotics, and more will increase at
an exponential rate.

# Concepts:

- Peer Relay:
Requests and responses can be relayed to parts of the network a given peer is not directly connected to, allowing for total network access without wasting bandwidth.

- Peer Limiting:
Peers connect to a limited amount of peers on the network. This way bandwidth is not wasted while at the same time peer relay allows for total network access.

- Peer Optimization:
Peer connections that are repeatedly used are created/prioritized while unused peer connections are severed/weakened. This allows for a more efficient network. If a connection
is not used then the connection is severed, but if an indirect (relayed) connection is repeatedly used, then a direct connection is made to that peer. Each peer connection
has a number that describes how useful it is on the network, meaning that the program can rank and cut/create connections in a meaningful way.

- Data Torrenting:
Data on the network is handled in a distributed manner similar to torrents. If a simple kind of data is needed to be stored (like a string), then the data is stored as a key-value
pair on the network. Each peer has a toy database for storing these key-value pairs. When data is needed, the local database is looked at first before fetching data from remote
peer databases. If the local and remote databases do not have the stored data or do not return the stored data after a certain period of time, the data is deemed to not exist.

- File Torrenting:
Using the previously described file torrenting, we can store the bits in a file as chunks on the network. Multiple key-value pairs are created to represent the different chunks of
a file, with one key-value pair representing a ledger for the file chunks stored on the network. When a file is needed to be downloaded, the program fetches the ledger for the file
and writes each chunk of the file stored on the network to a local file for download.

- WebAssembly Execution:
By using WebAssembly as the standard for executing programs on the network, programs written in a multitude of languages can be run on different architectures without compatibility
issues. Portable neural networks, web servers, CAD software, 3D rendering software, and other computationally intense programs can be made portable and computed on the edge instead
of the cloud, making data science and IoT uses more efficient.

- Wireless Cluster Computing:
As peers on the network are connected together and can share resources for data storage, the same can also be done for computing resources. Computer clusters work by orchestrating
and scheduling tasks across a LAN (local area network). Each peer on the network has tasks that it is meant to execute in order to contribute to the computing process of something
computationally intense like a neural network or data science program. Tasks are distributed on the network according to the software resources of each peer. More computing power
means more tasks are allocated to that peer. In this way, a wireless network of devices can combine their resources to act as one giant "network computer".
