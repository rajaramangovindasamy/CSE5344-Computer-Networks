#-------------------------------------------------------------------------------------
# STUDENT ID - 1001165700
#NAME - RAJARAMAN GOVINDASAMY
#-------------------------------------------------------------------------------------
#IMPORT STATEMENTS
#------------------
import socket
import sys
import thread
import time
#---------------
#CACHE FUNCTION
#---------------
def cache_fn(messageString, client_socket):
    #this method is responsible for caching
    HttpTypeMethod = messageString[0]
    URLpath = messageString[1]
    URLpath = URLpath[1:]
    print ("--------------------------------------------------\n")
    print "Request is ", HttpTypeMethod, " to URL : ", URLpath
    print ("--------------------------------------------------\n")
    start = time.clock()	
    current_file = "/" + URLpath
    try:
		#Search and open the current cache file for the URL entered
        file = open(current_file[1:], "r")
        contents = file.readlines()
        print "Match found in cache and reading the file\n"
        for i in range(0, len(contents)):
            print (contents[i])
            client_socket.send(contents[i])
        print "The above is the file read from Cache\n", "Time taken to read from Cache:",time.clock() - start , " Secs"

    except IOError:
		start = time.clock()
		print "Cache File not Found\n File is being fetched from Server to Create Cache\n"
		Proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host_url = URLpath
		try:
			Proxy_server.connect((host_url, 80))
			print 'Socket Connected on default Port 80 to fetch'
			ser_cache_file = Proxy_server.makefile('r', 0)
			ser_cache_file.write("GET " + "http://" + URLpath + " HTTP/1.0\n\n")           
			br = ser_cache_file.readlines()
			temp = open("./" + URLpath, "wb")
			for i in range(0, len(br)):
				print (br[i])
				temp.write(br[i])
				client_socket.send(br[i])
		except:
			print 'Not Valid URL'
		print "Time taken to read from Server:",time.clock() - start," Secs"
    client_socket.close()
#---------------
#MAIN FUNCTION
#---------------
def main():
	if len(sys.argv) <= 1: 
    		print ('Usage: python <filename> <port> >> log.txt')
    		sys.exit(2)
	#Server post number is port_serv
	print ("CSE5344 COMPUTER NETWORKS PROJECT - I\n")
	port_server = int(sys.argv[1]) 
	#-----------------------------------------------------------------------------------------------------------
	# SOCKET CREATION AND BINDING
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Prepare a server socket
	print ("Server is started\n")
	server_socket.bind(('', port_server))
	server_socket.listen(5)
	#-----------------------------------------------------------------------------------------------------------
	while True:
			print ("Bind Successful\n")
			print ("Connection Accepted\n")
			print ("-------------------------------------")
			#Accept connection from client using accept() function
			client_socket, addr = server_socket.accept() 
			print "Received Connection from <Host,Port> ", addr
			message = client_socket.recv(1024) 
			#Socket Contents
			messageString = message.split()
			if len(messageString) <= 1:
				continue	
			#Starting threads and ensuring multithreading	
			thread.start_new_thread(cache_fn ,(messageString, client_socket))


if __name__ == '__main__':
	main()
