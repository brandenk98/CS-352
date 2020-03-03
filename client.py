# Michael Rizzo
# Branden Kushnir
# Client for Project 1 

import socket as mysoc
import sys 

def newSocket(socket_type):
	try: 
		ret_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print "[C]: Client socket to " + socket_type + " created"
	except mysoc.error as err: 
		print "[C]: Could not create socket to " + socket_type + "\n error: ", str(err)
	return ret_socket

def argCheck(size, expected):
	if size is not expected:
		raise TypeError("Expected %d arguments, got %d" % (expected, size))
		exit()

def getQueries():
	input_file = open("PROJI-HNS.txt", "r")
	queries = input_file.read().splitlines()
	input_file.close()	
	return queries

def ts_process(ts_hostname_ip, query):	
	ts_socket = newSocket("ts")
	ts_socket.connect((ts_hostname_ip, int(sys.argv[3])))
	ts_socket.send(query.encode('utf-8'))
	ts_response = ts_socket.recv(4096).decode('utf-8')
	ts_response_parsed = ts_response.split()
	ts_flag = ts_response_parsed[2]

	if ts_flag == "A":
		print "[C]: Entry found in the Top-Level Server table: ", str(ts_response)
	elif ts_flag == "Error:HOST":
		print "[C]: IP address not found: ", str(ts_response)
	else:
		raise ValueError("Unrecognized Flag")

	ts_socket.close()
	return ts_response

def rs_process():
	argCheck(len(sys.argv), 4)
	output_file = open("RESOLVED.txt", "w+")
	queries = getQueries()
	rs_socket = newSocket("rs")
	rs_socket.connect((mysoc.gethostbyname(sys.argv[1]) , int(sys.argv[2])))	
	for query in queries:
		print "[C]: current query hostname: " + query
		rs_socket.send(query.encode("utf-8"))
		rs_response = rs_socket.recv(4096).decode("utf-8")
		rs_response_parsed = rs_response.split()
		argCheck(len(rs_response_parsed), 3)
		rs_flag = rs_response_parsed[2]

		if rs_flag == "A":
			print "[C]: Entry found in Root Server table ", str(rs_response)
			output_file.write(rs_response + str("\n"))
		elif rs_flag == "NS":
			ts_response = ts_process(mysoc.gethostbyname(rs_response_parsed[0]), query)
			output_file.write(ts_response + str("\n"))

	rs_socket.send("close".encode('utf-8'))
	rs_socket.close()	
	output_file.close()
	exit()
	return

rs_process()