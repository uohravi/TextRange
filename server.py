"""
Created on Dec 9, 2016

@author: rk186048
"""
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
        self.__info = {"oper": 0, "add": 0, "del": 0, "search": 0, "s_search": 0, "f_search": 0,
                       "start": 0, "range_obj":RangeText()}
        self.listen(5)
        
    def handle_accept(self):
        '''
        Function waiting for client request
        '''
        newSocket, address = self.accept()
        #self.__logger.info("Client Connected at:"+str(address))
        self.__info["start"] = datetime.now()
        SecondaryServerSocket(newSocket,self.__info)

class SecondaryServerSocket(asyncore.dispatcher_with_send):

    def __init__(self,sock,info):
        '''
        :param sock:  Socket on which listen for input
        :param info: infor contains output for statics
        '''
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.logger = logging.getLogger("server_ops")
        self.__stats = info

    def handle_read(self):

        receivedData = self.recv(8192)
        rangeobj = self.__stats["range_obj"]
        print rangeobj
        print receivedData
        receivedData = str(receivedData.strip())
        if receivedData == "Quit" or receivedData == "":
            #print "going to write statics"
            time_taken = datetime.now() - self.__stats["start"]
            time_taken = time_taken.total_seconds()
            self.logger.info("======================= Overall Statics Main =============================")
            self.logger.info("Total operations done:"+str(self.__stats["oper"]))
            self.logger.info(" Add operations done:"+str(self.__stats["add"]))
            self.logger.info(" Delete operations done:"+str(self.__stats["del"]))
            self.logger.info(" Search operations done:"+str(self.__stats["search"]))
            self.logger.info(" Successful Search operations done:"+str(self.__stats["s_search"]))
            self.logger.info(" Failed Search operations done:"+str(self.__stats["f_search"]))
            self.logger.info("Total Elapsed Time(sec):"+str(time_taken))
            self.logger.info("======================================================================")
            self.close()
        else:
            #print "spliting values",receivedData
            data_list = receivedData.split(",")
            if len(data_list) == 2:
                opr,rangetext = data_list[0].split(" ")
                rangetext = "".join([rangetext, ",", data_list[1]])

            elif len(data_list) == 1:
                opr,rangetext = data_list[0].split(" ")

            #print "rangetext", rangetext
            #print "operation",opr
            #rangetext = receivedData.split(" ")
            #opr = rangetext[0]
            if opr == "add":
                self.__stats["oper"] += 1
                self.__stats["add"] += 1
                self.logger.info("Operation " + str(self.__stats["oper"]) + ":")
                self.logger.info("\t\t Add \"" + rangetext + "\"")
                #print "going to perform add", rangetext
                rangeobj.addRange(rangetext)
            elif opr == "delete":
                self.__stats["oper"] += 1
                self.__stats["del"] += 1
                self.logger.info("Operation " + str(self.__stats["oper"]) + ":")
                self.logger.info("\t\t Delete \"" + rangetext + "\"")
                #print "going to perform delete", rangetext
                rangeobj.deleteRange(rangetext)
            elif opr == "search":
                self.__stats["oper"] += 1
                self.__stats["search"] += 1
                self.logger.info("Operation " + str(self.__stats["oper"]) + ":")
                self.logger.info("\t\t Search \""+rangetext+"\"")
                #print "going to perform search", rangetext
                if rangeobj.searchText(rangetext) is True:
                    self.__stats["s_search"] += 1
                else:
                    self.__stats["f_search"] += 1
            elif opr == "bulk":
                #rangetext = rangetext[1]
                #print "Bulk Operation Statics"
                self.logger.info("Operation " + str(self.__stats["oper"]) + ":")
                self.logger.info("\t\t Bulk \"" + rangetext + "\"")
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
                        if line[0] == "#":
                            continue
                        data_list = line.strip().split(",")
                        if len(data_list) == 2:
                            opr, rangetext = data_list[0].split(" ")
                            rangetext = "".join([rangetext, ",", data_list[1]])
                            print "rangetext", rangetext
                        elif len(data_list) == 1:
                            opr, rangetext = data_list[0].split(" ")
                        if opr == "add":
                            boper += 1
                            badcnt += 1
                            self.__stats["oper"] += 1
                            self.__stats["add"] += 1
                            self.logger.info("Operation " + str(self.__stats["oper"]) + ":")
                            self.logger.info("\t\t Add \"" + rangetext + "\"")
                            rangeobj.addRange(rangetext)
                        elif opr == "delete":
                            boper += 1
                            bdelcnt += 1
                            self.__stats["oper"] += 1
                            self.__stats["del"] += 1
                            self.logger.info("Operation " + str(self.__stats["oper"]) + ":")
                            self.logger.info("\t\t Delete \"" + rangetext + "\"")
                            rangeobj.deleteRange(rangetext)
                        elif opr == "search":
                            boper += 1
                            bserchcnt += 1
                            self.__stats["oper"] += 1
                            self.__stats["search"] += 1
                            self.logger.info("Operation " + str(self.__stats["oper"]) + ":")
                            self.logger.info("\t\t Search \"" + rangetext + "\"")
                            if rangeobj.searchText(rangetext) is True:
                                bserchs += 1
                                self.__stats["s_search"] += 1
                            else:
                                bserchf += 1
                                self.__stats["f_search"] += 1

                bttaken = datetime.now() - start_time
                bttaken = bttaken.total_seconds()
                self.logger.info("======================= Overall Statics  Bulk =============================")
                self.logger.info("Total operations done:"+str(boper))
                self.logger.info(" Add operations done:"+str(badcnt))
                self.logger.info(" Delete operations done:"+str(bdelcnt))
                self.logger.info(" Search operations done:"+str(bserchcnt))
                self.logger.info(" Successful Search operations done:"+str(bserchs))
                self.logger.info(" Failed Search operations done:"+str(bserchf))
                self.logger.info("Total Elapsed Time(sec):"+str(bttaken))
                self.logger.info("======================================================================")


            '''
            time_taken =  datetime.now() - self.__stats["start"]
            time_taken = time_taken.total_seconds()
            self.logger.info("======================= Overall Statics Main =============================")
            self.logger.info("Total operations done:" + str(self.__stats["oper"]))
            self.logger.info(" Add operations done:" + str(self.__stats["add"]))
            self.logger.info(" Delete operations done:" + str(self.__stats["del"]))
            self.logger.info(" Search operations done:" + str(self.__stats["search"]))
            self.logger.info(" Successful Search operations done:" + str(self.__stats["s_search"]))
            self.logger.info(" Failed Search operations done:" + str(self.__stats["f_search"]))
            self.logger.info("Total Elapsed Time(sec):" + str(time_taken))
            self.logger.info("======================================================================")

            rangetext = receivedData.split(" ")
            opr = rangetext[0]
            if opr == "search":
               rangetext = rangetext[1]
            else:
                rangetext = ''.join([rangetext[1],rangetext[2]])
            print "rangetext",rangetext
            print "done"
            '''

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