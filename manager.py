from socket import socket, AF_INET, SOCK_STREAM
import ast
from pprint import pprint
import time

class BsManager:
    def __init__(self,addr):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.settimeout( 5 )
        self.s.connect( addr )
        self.s.settimeout( None )

        #recv first prompt message ## " \nbombsquad>"
        self.s.recv( 1024 )

        #some texts
        self.MESSAGES = 'bsInternal._getChatMessages()'
        self.ROSTER = 'bsInternal._getGameRoster()'
        self.PLAYERS = '[p.getName() for p in bs.getSession().players]'
        self.SEND_MESSAGE = 'bsInternal._chatMessage("{}")'
        self.KICK = 'bsInternal._disconnectClient({})'
        self.SLOMO = 'setattr( bs.getNodes()[0] , u"slowMotion" , {} )'
        
        self.SHIELDS = '''
for p in bs.getSession().players:
    if p.getID() == {}:
        p.actor.equipShields()
        '''

        self.GLOVES = '''
for p in bs.getSession().players:
    if p.getID() == {}:
        p.actor.equipBoxingGloves()
        '''

        self.SPEEDUP = '''
for p in bs.getSession().players:
    if p.getID() == {}:
        if p.actor.node.exists():
            setattr(p.actor.node,u'hockey',True)
        '''

        self.FLY = '''
for p in bs.getSession().players:
    if p.getID() == {}:
        if p.actor.node.exists():
            setattr(p.actor.node,u'fly',True)
        '''

        self.INVINCIBLE = '''
for p in bs.getSession().players:
    if p.getID() == {}:
        if p.actor.node.exists():
            setattr(p.actor.node,u'invincible',True)
        '''

        self.FREEZE = '''
for p in bs.getSession().players:
    if p.getID() == {}:
        if p.actor.node.exists():
            setattr(p.actor.node,u'frozen',True)
        '''

        self.CURSE = '''
for p in bs.getSession().players:
    if p.getID() == {}:
        p.actor.curse()
        '''

        self.KILL = '''
for p in bs.getSession().players:
    if p.getID() == {}:
        p.actor.shatter()
        '''

        self.SET_BOMBTYPE = '''
for p in bs.getSession().players:
    if p.getID() == {}:
        p.actor.bombType = {}
        '''

        self.SET_HITPOINTS = '''
for p in bs.getSession().players:
    if p.getID() == {}:
        p.actor.hitPoints = {}
        '''

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
        self.s.setblocking(1)
        return ''.join(total_data)

    def getMessages( self ):
        self.s.send( self.MESSAGES.encode() )

        ##strip last 12 character which is always " \nbombsquad>"
        self.messages = ast.literal_eval( self.recv_long()[:-12] )
        return self.messages

    def getPlayers( self ):
        temp = self.getRoster()
        players = []
        for item in temp:
            for player in item['players']:
                player['clientID'] = item['clientID']
                players.append(player)
        return players


    def getRoster( self ):
        self.s.send( self.ROSTER.encode() )

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
        self.s.send( self.SEND_MESSAGE.format( msg ).encode() )
        self.s.recv( 1024 )

    def kick( self , clientID ):
        self.s.send( self.KICK.format( clientID ).encode() )
        self.s.recv(1024)

    def slomo( self , onOff ):
        self.s.send( self.SLOMO.format(onOff).encode() )
        self.s.recv(1024)

    def shields ( self , playerID ):
        self.s.send( self.SHIELDS.format( playerID ).encode() )
        self.s.recv(1024)

    def gloves ( self , playerID ):
        self.s.send( self.GLOVES.format( playerID ).encode() )
        self.s.recv(1024)

    def speedup ( self , playerID ):
        self.s.send( self.SPEEDUP.format( playerID ).encode() )
        self.s.recv(1024)

    def fly ( self , playerID ):
        self.s.send( self.FLY.format( playerID ).encode() )
        self.s.recv(1024)

    def invincible ( self , playerID ):
        self.s.send( self.INVINCIBLE.format( playerID ).encode() )
        self.s.recv(1024)

    def freeze ( self , playerID ):
        self.s.send( self.FREEZE.format( playerID ).encode() )
        self.s.recv(1024)

    def curse ( self , playerID ):
        self.s.send( self.CURSE.format( playerID ).encode() )
        self.s.recv(1024)

    def kill ( self , playerID ):
        self.s.send( self.KILL.format( playerID ).encode() )
        self.s.recv(1024)

    def setBombType ( self , playerID , bombType ):
        self.s.send( self.SET_HITPOINTS.format( playerID , bombType ).encode() )
        self.s.recv(1024)

    def setHitPoints( self , playerID , hp ):
        self.s.send( self.SET_HITPOINTS.format( playerID , hp ).encode() )
        self.s.recv(1024)










