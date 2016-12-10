'''
Created on Dec 9, 2016

@author: rk186048
'''
import socket
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process the User Input for client Program')
    parser.add_argument('-p',action='store',type=int,help="Test server",required=True)
    parser.add_argument('-H',action='store',help="host ip address",required=True)
    parser.add_argument('-c',action='store',default="",help='Command to be sent to server')
    args = parser.parse_args()
    port = int(args.p)
    addrs = str(args.H)
    addrs= addrs.strip()
    print addrs
    cmd = str(args.c)
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print "creating socket"
    # Connect the socket to the port where the server is listening
    server_address = (addrs, port)
   # print "Bonding to port"
    #print >>sys.stderr, 'connecting to %s port %s' % server_address
    try:
        sock.connect(server_address)
        print "connection created"
    except:
        print "Not able to create connection"
    try:
        print cmd
        if cmd:
            sock.sendall(cmd)
    finally:
        sock.close()
    pass