'''
Created on Dec 9, 2016

@author: rk186048
'''
from datetime import datetime
import asyncore
import socket
from RangeText import RangeText
import logging
import os
import argparse

class MainServerSocket(asyncore.dispatcher):
    '''
    This class will start a server at pet given by command line 
    and then wait for client request
    '''
    def __init__(self, port):
        '''
        Initialize server program and listen for client
        '''
        asyncore.dispatcher.__init__(self)
        log_file = "server_ops"
        self.__logger = logging.getLogger(log_file)
        self.__logger.setLevel(logging.DEBUG)
        self.logName = log_file
        self.__handler = logging.FileHandler(os.path.join(os.getcwd(),log_file+".log"))
        self.__handler.setLevel(logging.DEBUG)
        self.__formater = logging.Formatter('%(message)s ')
        self.__handler.setFormatter(self.__formater)
        if not self.__logger.handlers:
            self.__logger.addHandler(self.__handler)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('localhost',port))
        self.listen(5)
        
    def handle_accept(self):
        '''
        Function waiting for client request
        '''
        newSocket, address = self.accept()
        self.__logger.info("Client Connected at:"+str(address))
        SecondaryServerSocket(newSocket)

class SecondaryServerSocket(asyncore.dispatcher_with_send):
    
    def handle_read(self):
        oper = 0
        adcnt = 0
        delcnt = 0
        serchcnt = 0
        serchs = 0
        serchf = 0
        ttaken = 0 
        start_time = datetime.now()
        receivedData = self.recv(8192)
        rangeobj = RangeText()
        print receivedData
        receivedData = str(receivedData.strip())
        if receivedData == "Quit" or receivedData == "": 
            end_time = start_time = datetime.now()
            ttaken = end_time - start_time
            ttaken = ttaken.total_seconds()
            print "going to write infor"
            rangeobj.info("======================= Overall Statics =============================")   
            rangeobj.info("Total operations done:"+str(oper))
            rangeobj.info(" Add operations done:"+str(adcnt))
            rangeobj.info(" Delete operations done:"+str(delcnt))
            rangeobj.info(" Search operations done:"+str(serchcnt))
            rangeobj.info(" Successful Search operations done:"+str(serchs))
            rangeobj.info(" Failed Search operations done:"+str(serchf))
            rangeobj.info("Total Elapsed Time(msec):"+str(ttaken))
            rangeobj.info("======================================================================") 
            self.close()
        else:
            print "spliting values",receivedData
            rangetext = receivedData.split(" ")
            opr = rangetext[0]
            if opr == "bulk":
                rangetext = rangetext[1]
                print "Bulk Operation Statics"
                boper = 0
                badcnt = 0
                bdelcnt = 0
                bserchcnt = 0
                bserchs = 0
                bserchf = 0
                bttaken = 0 
                start_time = datetime.now()
                
                with open(rangetext) as infp:
                    for line in infp:
                        opr,rangetext = line.strip().split(" ")
                        if line[0] == "#":
                            continue
                        if opr == "add":
                            oper += 1
                            adcnt += 1
                            rangeobj.addRange(rangetext)
                        elif opr == "delete":
                            oper += 1
                            delcnt += 1
                            rangeobj.deleteRange(rangetext)
                        elif opr == "search":
                            oper += 1
                            serchcnt += 1
                            if rangeobj.searchText(rangetext) is True:
                                serchs += 1
                            else:
                                serchf += 1
                                
                end_time = start_time = datetime.now()
                bttaken = end_time - start_time
                bttaken = bttaken.total_seconds()
                rangeobj.info("======================= Overall Statics =============================")   
                rangeobj.info("Total operations done:"+str(boper))
                rangeobj.info(" Add operations done:"+str(badcnt))
                rangeobj.info(" Delete operations done:"+str(bdelcnt))
                rangeobj.info(" Search operations done:"+str(bserchcnt))
                rangeobj.info(" Successful Search operations done:"+str(bserchs))
                rangeobj.info(" Failed Search operations done:"+str(bserchf))
                rangeobj.info("Total Elapsed Time(msec):"+str(bttaken))
                rangeobj.info("======================================================================")
                
            rangetext = receivedData.split(" ")
            opr = rangetext[0]
            if opr == "search":
               rangetext = rangetext[1]
            else:
                rangetext = ''.join([rangetext[1],rangetext[2]])
            print "rangetext",rangetext
            print "done"
            if opr == "add":
                oper += 1
                adcnt += 1
                print "going to perform add",rangetext
                rangeobj.addRange(rangetext)
                
            elif opr == "delete":
                oper += 1
                delcnt += 1
                print "going to perform delete",rangetext
                rangeobj.deleteRange(rangetext)
                
            elif opr == "search":
                oper += 1
                serchcnt += 1
                print "going to perform search",rangetext
                if rangeobj.searchText(rangetext) is True:
                    serchs += 1
                else:
                    serchf += 1
            
                         
    def handle_close(self):
        print "Disconnected from", self.getpeername(  )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process the User Input for Server program')
    parser.add_argument('-p',action='store',type=int,help="Port number on which listen for client",required=True)
    args = parser.parse_args()
    port = int(args.p)
    MainServerSocket(port)
    asyncore.loop()      
    pass