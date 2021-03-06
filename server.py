#  coding: utf-8 
import SocketServer, os, time

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Copyright 2016 Tiancheng Shen
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        seq = self.data.splitlines()
        sequence = seq[0]
        request = sequence.split(" ")
        action = request[0]
        path = request[1]
        
        # check if the request is GET
        if action == 'GET':
            response = self.handlePath(path)
        else:
            response = self.notFound()
        #print response
        self.request.sendall(response)

    def handlePath(self, path):
        # when the request is GET, this function will make a correct response
        rsp = os.getcwd() + '/www'
        page = None
        
        # check if the path is valid
        pathlist = ['/','/index.html','/base.css','/deep.css','/deep','/deep/','/deep/index.html','/deep/deep.css']
        checkpath = os.path.abspath(path)
        if checkpath in pathlist:
            # check file type
            if path.endswith('.html'):
                fileType = 'Content-Type: text/html\r\n\r\n'
                page = rsp + path
            elif path.endswith('base.css'):
                fileType = 'Content-Type: text/css\r\n\r\n'
		page = rsp + path
	    elif path.endswith('deep.css'):
		fileType = 'Content-Type: text/css\r\n\r\n'
		if path.endswith ('deep/deep.css'):
		    page = rsp + path
		else:
		    page = rsp + '/deep' + path
            elif path.endswith('/'):
                fileType = 'Content-Type: text/html\r\n\r\n'
                if path == '/':
                    page = rsp + '/index.html'
                else:
                    page = rsp + path + 'index.html'
	    elif path.endswith('deep'):
		fileType = 'Content-Type: text/html\r\n\r\n'
		page = rsp + path + '/index.html'
            
            try:
                # open and read file
                File = open(page, 'r')
                contents = File.read()
                File.close()
                
                # create HTTP
                response = 'HTTP/1.1 200 OK\r\n' + 'Date: ' + time.strftime("%c") + ' GMT\r\n' + 'Content-Length:' + str(len(contents)) + '\r\n' + fileType + contents

                return response
            except IOError:
                return self.notFound()
        
        else:
            return self.notFound()
        
    def notFound(self):
        # handle 404 not found problem
        fileType = 'Content-Type: text/html\r\n\r\n'
        response = 'HTTP/1.1 404 NOT FOUND\r\n' + 'Date: ' + time.strftime("%c") + ' GMT\r\n' + fileType + '404 NOT FOUND'
        return response
                
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print 'Start connecting...'
    server.serve_forever()
