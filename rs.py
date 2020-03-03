# Michael Rizzo
# Branden Kushnir
# Root Server for Project 1

import socket as mysoc
import sys
import threading

def newSocket():
	try: 
		ret_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print "[RS]: Root Server socket created"
	except mysoc.error as err: 
		print "[RS]: Could not create socket \n Error: " , str(err)
	return ret_socket

def argCheck(size, expected):
	if size is not expected:
		raise TypeError("Expected %d arguments, got %d" % (expected, size))
		exit()

def makeTable():
	input_file = open("PROJI-DNSRS.txt", "r")
	lines = input_file.read().splitlines()
	input_file.close()
	rs_dns_table = {}
	ts_information = ""
	for line in lines:
		line_parsed = line.split()
		hostname = line_parsed[0].strip().lower()
		flag = line_parsed[2]
		if flag == "A":
			rs_dns_table[hostname] = line.strip()
		elif flag == "NS":
			ts_information = line.strip()
		else:
			raise ValueError("[RS]: Error - PROJI-DNSRS.txt file contains unrecognized flags")
	return (rs_dns_table, ts_information)

def printHostName():
	host = mysoc.gethostname()
	print "[RS]: Root server hostname is:", host
	host_ip = mysoc.gethostbyname(host)
	print "[RS]: Root server IP address is:", host_ip 
	return

def root_server():
	argCheck(len(sys.argv), 2)
	table = makeTable()
	printHostName()
	socket = newSocket()
	server_binding = ("", int(sys.argv[1]))
	socket.bind(server_binding)
	socket.listen(10)
	launch_handler(socket, table[0], table[1])
	socket.close()
	return 

def launch_handler(socket, rs_dns_table, ts_information):
	while True:
		connection, addr = socket.accept()
		print "[RS]: Received a connection request from:", addr
		thread = threading.Thread(name='connection_handler', target=connection_handler, args=(connection, rs_dns_table, ts_information))
		thread.start()
	socket.close()
	return

def connection_handler(connection, rs_dns_table, ts_information):
	while True:
		client_query = connection.recv(4096).decode('utf-8').strip().lower()
		print "[RS]: Received request to find IP address for the hostname: ", client_query
		if client_query in rs_dns_table:
			addr_response = rs_dns_table[client_query]
			print "[RS]: Found query in root server DNS table" 
			print "[RS]: Sending following string back to client: ", addr_response
			connection.send(addr_response.encode('utf-8'))
		elif client_query == "close":
			break
		else:
			print "[RS]: Could not locate ", client_query, " in root server DNS table"
			print "[RS]: Sending following Top-Level server hostname back to client: ", ts_information
			connection.send(ts_information.encode('utf-8'))
	connection.close()
	return 

root_server()