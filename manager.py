from socket import socket
import ast
from pprint import pprint
import time

class manager:
    def __init__(self,addr):
        self.s = socket()
        self.s.settimeout( 5 )
        self.s.connect( addr )

        #recv first prompt message ## " \nbombsquad>"
        self.s.recv( 1024 )

        #encode some text
        self.MESSAGES = 'bsInternal._getChatMessages()'.encode()
        self.ROSTER = 'bsInternal._getGameRoster()'.encode()
        self.PLAYERS = 'bs.getSession().players'.encode()

        self.messages = []


    #Sometimes s.recv returns incomplete message, so setup a 
    def recv_long( self ):
        self.s.setblocking(0)
        total_data=[];data='';begin=time.time()
        while 1:
            #if you got some data, then break after wait sec
            if total_data and time.time()-begin>2:
                break
            #if you got no data at all, wait a little longer
            elif time.time()-begin>2:
                break
            try:
                data=self.s.recv( 8192 )
                if data:
                    total_data.append(data.decode( "utf" ))
                    begin=time.time()
                else:
                    time.sleep( 0.1 )
            except:
                pass
        return ''.join(total_data)

    def getMessages( self ):
        self.s.send( self.MESSAGES )

        ##strip last 12 character which is always " \nbombsquad>"
        self.messages = ast.literal_eval( self.recv_long()[:-12] )

        return self.messages

    def getPlayers( self ):
        self.s.send( self.PLAYERS )

        ##strip last 12 character which is always " \nbombsquad>"
        return ast.literal_eval( self.recv_long()[:-12] )

    def getRoster( self ):
        self.s.send( self.ROSTER )

        ##strip last 12 character which is always " \nbombsquad>"
        return ast.literal_eval( self.recv_long()[:-12] )

    def getNewMessages( self ):
        temp = self.messages
        self.getMessages()
        if len(self.messages) > len(temp):
            return self.messages[len(temp):]
        for i in range(len(temp)):
            if all(temp[j] == self.messages[j-i] for j in range(i,len(temp))):
                    if i == 0:
                            return []
                    return self.messages[(-1)*i:]
        return self.messages

    def sendMessage( self , msg ):
        pass

    def kick( self , clientId ):
        pass

    def slomo( self ):
        pass

    def shields ( self , playerIndex ):
        pass










