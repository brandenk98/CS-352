# Michael Rizzo
# Branden Kushnir
# Client for Project 2 

import sys
import socket as mysoc

def newSocket():
	try: 
		ret_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print ("[C]: Client socket created")
	except mysoc.error as err: 
		print ("[C]: Could not create socket \n Error: " + str(err))
	return ret_socket

def argCheck(size, expected):
	if size is not expected:
		raise TypeError("Expected %d arguments, got %d" % (expected, size))
		exit()

def getQueries():
	input_file = open("PROJ2-HNS.txt", "r")
	queries = input_file.read().splitlines()
	input_file.close()	
	return queries

def client():
	argCheck(len(sys.argv), 3)
	clientSocket = newSocket()
	bind = (str(sys.argv[1]), int(sys.argv[2]))
	clientSocket.connect(bind)
	
	queries = getQueries()
	file = open("RESOLVED.txt", "w+")
 	
	for query in queries:
		print ("[C]: Sent: " + query) 
		clientSocket.send(query.encode("utf-8"))
		lsResponse = clientSocket.recv(4096).decode("utf-8")
		print ("[C]: The received response is: "+ lsResponse) 
		file.write(lsResponse + "\n")

	file.close()
	clientSocket.close()

client()