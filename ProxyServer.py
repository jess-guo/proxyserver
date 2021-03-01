from socket import *
import sys
import datetime
import glob
import os


if len(sys.argv) <= 1:
	print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
	sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
print(sys.argv[1])
tcpSerSock.bind(('localhost', int(sys.argv[1])))
tcpSerSock.listen(5)

isGET = True
time = False

while 1:
	# Strat receiving data from the client
	print('Ready to serve...')
	tcpCliSock, addr = tcpSerSock.accept()
	print('Received a connection from:', addr)
	message = tcpCliSock.recv(1024)
	decoded_msg = message.decode()
	method = (decoded_msg.split('\r\n')[0]).split()[0]
	print("method:", method)

	if method == "POST":
		tcpSerSock.send(message)
		isGet = False
		
		continue

	if method == "GET":
		isGet = True
		headers = (decoded_msg.split('\r\n\r\n')[0]).split('\r\n')
		for h in headers:
			if "If-Modified-Since" in h:
				time = True
				timestr = (h.split(": ")[1]).rsplit(' ', 1)[0]
				time_found = datetime.datetime.strptime(timestr, '%a, %d %b %Y %H:%M:%S')
				

	if time == True:
		filename = ((message.decode()).split()[1].partition("/")[2]) + "_" + timestr
	else:
		filename = ((message.decode()).split()[1].partition("/")[2])

	filetouse = "/" + filename


	print("this is the client message:", decoded_msg)

	# Extract the filename from the given message
	try:
		modified = True
		# Check wether the file exist in the cache
		fileExist = "true"
		# ProxyServer finds a cache hit and generates a response message
		for f in glob.glob('filename*'):

			time_saved = f.rsplit("_")
			print("time:", time_saved)
			time_ref = datetime.datetime.strptime(t, '%a, %d %b %Y %H:%M:%S')
			if time_ref<=time_found:
				print("sent not modified")
				tcpCliSock.send("HTTP/1.0 304 Not Modified\r\n".encode())
				tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())

				outputdata = f.readlines()
				print("outputdata:",outputdata)
				for i in range(0, len(outputdata)):
            				tcpCliSock.send(outputdata[i].encode())
				
				print('Read from cache')
				modified = False
				continue

		if modified == True:
			modified = True
			fileExist = "false"
		# Check wether the file exist in the cache
			f = open("filetouse[1:]", "r")


	# Error handling for file not found in cache
	except IOError:
		print("in the except clause here")
		if fileExist == "false" or isGet == False:
			# Create a socket on the proxyserver
			c = socket(AF_INET, SOCK_STREAM)# Fill in start. # Fill in end.
			hostn = filename.split("_")[0].replace("www.","",1)
			print("this is hostn",hostn)
			try:
				# Connect to the socket to port 80
				# Fill in start.
				c.connect((hostn, 80))
				# Fill in end.
				# Create a temporary file on this socket and ask port 80 for the file requested by the client
				if isGET == False:
					request = "POST "+"http://" + filename.split("_")[0] + " HTTP/1.0\r\n\r\n"
				else:	
					request = "GET "+"http://" + filename.split("_")[0] + " HTTP/1.0\r\n\r\n"

				c.send(request.encode())
				print ("this is the request", request)

				buffer = b''
				while True:
					msg = c.recv(1024)
					if len(msg)<=0:
						break
					buffer += msg

				print("buffer", buffer.decode())

				if isGET == True:
					tmpFile = open("./" + filename,"wb")
					tmpFile.write(buffer)

				# Read the response into buffer
				# Create a new file in the cache for the requested file.
				# Also send the response in the buffer to client socket and the corresponding file in the cache

				# Fill in start.
				tcpCliSock.send(buffer)
				# Fill in end.
			except gaierror:
				print("Hostname doesn't have IP Address" + hostn)
			except ConnectionRefusedError:
				print("Invalid Hostname" + hostn)	
			except error:
				print("Illegal request")
		else:
			# HTTP response message for file not found
			# Fill in start.
			tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode())
			tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
			# Fill in end.
	# Close the client and the server sockets
	tcpCliSock.close()
# Fill in start.
tcpSerSock.close()
c.close()
# Fill in end.
