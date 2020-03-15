# Michael Rizzo
# Branden Kushnir
# Top-Level Server for Project 1

import socket as mysoc
import sys
import threading

def newSocket():
	try: 
		ret_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print "[TS]: Top Level Server socket created"
	except mysoc.error as err: 
		print "[TS]: Could not create socket \n Error: " , str(err)
	return ret_socket

def argCheck(size, expected):
	if size is not expected:
		raise TypeError("Expected %d arguments, got %d" % (expected, size))
		exit()

def makeTable():
	input_file = open("PROJI-DNSTS.txt", "r")
	lines = input_file.read().splitlines()
	input_file.close()
	ts_dns_table = {}
	for line in lines:
		line_parsed = line.split()
		hostname = line_parsed[0].strip().lower()
		flag = line_parsed[2]
		if flag == "A":
			ts_dns_table[hostname] = line.strip()
		else:
			raise ValueError("[TS]: Error - PROJI-DNSTS.txt file contains unrecognized flags")
	return ts_dns_table

def printHostName():
	host = mysoc.gethostname()
	print "[TS]: Top-level server host name is: ", host
	host_ip = mysoc.gethostbyname(host)
	print "[TS]: Top-level server host IP address is: ", host_ip 
	return

def top_level_server():
	argCheck(len(sys.argv), 2)
	printHostName()	
	socket = newSocket()
	server_binding = ("", int(sys.argv[1]))
	socket.bind(server_binding)
	socket.listen(10)
	launch_handler(socket, makeTable())
	socket.close()
	return 

def launch_handler(socket, ts_dns_table):
	while True:
		connection, addr = socket.accept()
		print "[TS]: Received a connection request from:", addr
		thread = threading.Thread(name='connection_handler', target=connection_handler, args=(connection, ts_dns_table))
		thread.start()
	socket.close()
	exit()
	return

def connection_handler(connection, ts_dns_table):
	client_query = connection.recv(4096).decode('utf-8').strip().lower()
	print "[TS]: Received request to find IP address for the hostname: ", client_query
	if client_query in ts_dns_table:
		addr_response = ts_dns_table[client_query]
		print "[TS]: Found query in Top-Level server DNS table" 
		print "[TS]: Sending following string back to client: ", addr_response
		connection.send(addr_response.encode('utf-8'))
	else:
		error_response = client_query + " - Error:HOST NOT FOUND"
		print "[TS]: Could not locate query in Top-Level server DNS table"
		connection.send(error_response.encode('utf-8'))
	connection.close()
	exit()
	return 

top_level_server()