'''
Created on Dec 9, 2016

@author: rk186048
'''
import logging
import os
from datetime import datetime
import threading as th
import multiprocessing as mp

class RangeText(object):
    '''
    To perform set of range text search operation
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        #self.__rangelst = ["[AaA, Bb)","(CA, CaC]","[Dd, Df]"]
        self.__rangelst = []
        self.__rcount = 1
        self.__opcoutn = 1
        self.__thlock = th.Lock()
        self.__prclock = mp.Lock()
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
        
     
    def addRange(self,r_list):
        '''
        This function will add range set without overlapping
        '''   
        with self.__prclock:
                with self.__thlock:
                    self.__opcoutn += 1
        self.info("Operation "+str(self.__opcoutn)+":")   
        self.info("\t\t Add \""+str(r_list)+"\"")   
        self.info("Ranges before operation : Ranges Count:"+str(self.__rcount)+", Ranges:("+str(self.__rangelst)+")") 
        if self.__rcount == 0:
            self.__rangelst.append(r_list)
            self.__rcount += 1
            self.info("Ranges after operation : Ranges Count:"+str(self.__rcount)+", Ranges:("+str(self.__rangelst)+")")
            return True
        
        new_word_list = r_list.split(",")
        search_list = []
        for nword in search_list:
            nword = nword.strip()
            temp = None
            if nword[0] == '[':
                search_list.append('[')
            elif nword[0] == '(':
                search_list.append('(') 
                        
            if nword[len(nword)-1] == ']':
                temp = ']'
            elif  nword[len(nword)-1] == ')':
                temp = ')'
            nword.strip("[]()")
            search_list.append(nword)
            if temp:
                search_list.append(temp)
                
        for i in range(len(self.__rangelst)):
            range_word = self.__rangelst[i]
            word_list = range_word.split(",")
            rangel = []
            for word in word_list:
                word = word.strip()
                temp = None
                if word[0] == '[':
                    rangel.append('[')
                elif word[0] == '(':
                    rangel.append('(') 
                        
                if word[len(word)-1] == ']':
                    temp = ']'
                elif  word[len(word)-1] == ')':
                    temp = ')'
                word.strip("[]()")
                rangel.append(word)
                if temp:
                    rangel.append(temp)
            print search_list,rangel    
            if search_list[1] >= rangel[1] and search_list[1] <= rangel[2]:
                if search_list[2] >= rangel[2]:
                    rangel[2] = search_list[2]
                    rangel[3] = search_list[3]
                    with self.__prclock:
                        with self.__thlock:
                            self.__rangelst[i]=''.join([rangel[0],rangel[1],",",rangel[2],rangel[3]])
                    
            if search_list[1] >= rangel[1] and search_list[1] > rangel[2]:
                with self.__prclock:
                    with self.__thlock:
                        self.__rangelst.append(r_list)
            
            if search_list[1] < rangel[1] and search_list[2] < rangel[2]:
                with self.__prclock:
                    with self.__thlock:
                        self.__rangelst.append(r_list)
                
            if search_list[1] <  rangel[1] and search_list[2] >= rangel[1]:
                    rangel[1] = search_list[1]
                    rangel[0] = search_list[0]
                    with self.__prclock:
                        with self.__thlock:
                            self.__rangelst[i]=''.join([rangel[0],rangel[1],",",rangel[2],rangel[3]])
            
               
                
                
        with self.__prclock:
                with self.__thlock:        
                    self.__rcount += 1
        self.info("Ranges after operation : Ranges Count:"+str(self.__rcount)+", Ranges:("+str(self.__rangelst)+")")
        
        
    def deleteRange(self,r_list):
        '''
        This function will delete the given range with adjustment
        '''
        self.info("Operation "+str(self.__opcoutn)+":")   
        self.info("\t\t Delete \""+r_list+"\"")   
        self.info("Ranges before operation : Ranges Count:"+str(self.__rcount)+", Ranges:("+str(self.__rangelst)+")") 
        self.__rcount -= 1
        self.__opcoutn += 1
        
        new_word_list = r_list.split(",")
        search_list = []
        for nword in search_list:
            nword = nword.strip()
            temp = None
            if nword[0] == '[':
                search_list.append('[')
            elif nword[0] == '(':
                search_list.append('(') 
                        
            if nword[len(nword)-1] == ']':
                temp = ']'
            elif  nword[len(nword)-1] == ')':
                temp = ')'
            nword.strip("[]()")
            search_list.append(nword)
            if temp:
                search_list.append(temp)
                
        for i in range(len(self.__rangelst)):
            range_word = self.__rangelst[i]
            word_list = range_word.split(",")
            rangel = []
            for word in word_list:
                word = word.strip()
                temp = None
                if word[0] == '[':
                    rangel.append('[')
                elif word[0] == '(':
                    rangel.append('(') 
                        
                if word[len(word)-1] == ']':
                    temp = ']'
                elif  word[len(word)-1] == ')':
                    temp = ')'
                word.strip("[]()")
                rangel.append(word)
                if temp:
                    rangel.append(temp)
            if rangel[1] < search_list[1] and rangel[2] > search_list[1] and search_list[2] < rangel[2]:
                temp = rangel[2]
                rangel[2] = search_list[1]
                rangel[3] = ")"
                self.__rangelst[i] = ''.join([rangel[0],rangel[1],",",rangel[2],rangel[3]])
                search_list[1] = search_list[2]
                search_list[0] = '('
                search_list[2] = rangel[2]
                search_list[3] = rangel[3]
                self.__rangelst.append(''.join([search_list[0],search_list[1],",",search_list[2],search_list[3]]))
            elif search_list[1] < rangel[1] and search_list[2] < rangel[2]:
                rangel[1] = search_list[2]
                rangel[0] = '('
                self.__rangelst[i] = ''.join([rangel[0],rangel[1],",",rangel[2],rangel[3]])
            elif search_list[2] > rangel[1] and search_list[2] > rangel[2]:
                rangel[2] = search_list[1]
                rangel[3] = ')'
                self.__rangelst[i] = ''.join([rangel[0],rangel[1],",",rangel[2],rangel[3]])
                
        
        self.info("Ranges after operation : Ranges Count:"+str(self.__rcount)+", Ranges:("+str(self.__rangelst)+")")
        
    def searchText(self,wrd):
        '''
        This function will search the given workd form the raange list, return True if successfull oterwise false
        '''
        self.info("Operation "+str(self.__opcoutn)+":")   
        self.info("\t\t Search \""+wrd+"\"")   
        status = "pass"
        self.info("Ranges before operation : Ranges Count:"+str(self.__rcount)+", Ranges:("+str(self.__rangelst)+")") 
        self.__opcoutn += 1
        if self._validateRange(wrd) is True:
            status = "Pass"
        else:
            status = "Fail"
        self.info("Search of \""+wrd+"\":"+status) 
    
    def _validateRange(self,rlist,is_list=False):
        '''
        If is_list False, check given rlist is fall or not in the range available
        if is_list True check given r list as list of range fall in available range or not
        '''
        is_incl = False
        is_excl = False
        is_inrange = False
        is_hi = False
        is_low = False
        if self.__rcount == 0:
            return False
        '''
        if is_list is False:
            for range_word in self.__rangelst:
                word_list = range_word.split(",")
                for word in word_list:
                    is_incl = False
                    is_excl = False
                    is_inrange = False
                    is_hi = False
                    is_low = False
                    
                    word = word.strip()
                    if word[0] == '[' or word[len(word)-1] == ']':
                        is_incl = True
                        if word[0] == '[':
                            is_low = True
                        elif word[len(word)-1] == ']':
                            is_hi = True
                        word = word.strip("[]")
                    elif word[0] == '(' or word[len(word)-1] == ')':
                        is_excl =True
                        if word[0] == '(':
                            is_low = True
                        elif word[len(word)-1] == ')':
                            is_hi = True
                        word = word.strip("()")
                    if is_low:
                        if is_incl:
                            if rlist >= word:
                                continue
        '''
        if is_list is False:
            for range_word in self.__rangelst:
                word_list = range_word.split(",")
                rangel = []
                for word in word_list:
                    word = word.strip()
                    temp = None
                    if word[0] == '[':
                        rangel.append('[')
                    elif word[0] == '(':
                        rangel.append('(') 
                        
                    if word[len(word)-1] == ']':
                        temp = ']'
                    elif  word[len(word)-1] == ')':
                        temp = ')'
                    word.strip("[]()")
                    rangel.append(word)
                    if temp:
                        rangel.append(temp)
                if rangel[0] == '[' and  rlist >= rangel[1] and rangel[3] == ']' and rangel[2] <= rlist:
                    return True
                elif rangel[0] == '(' and  rlist > rangel[1] and rangel[3] == ']' and rangel[2] <= rlist:
                    return True
                elif rangel[0] == '[' and  rlist >= rangel[1] and rangel[3] == ')' and rangel[2] < rlist:
                    return True
                elif rangel[0] == '(' and  rlist > rangel[1] and rangel[3] == ')' and rangel[2] < rlist:
                    return True
                else:
                    return False
        
                        
                    
                    
                    
                        
                    
        

    def info(self,msg):
        self.__logger.info(msg)
        

