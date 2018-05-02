from socket import socket, AF_INET, SOCK_STREAM
import ast
from pprint import pprint
import time

class BsManager:
    def __init__(self,addr):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.settimeout(5)
        self.s.connect(addr)
        self.s.settimeout(None)

        #recv first prompt message ## " \nbombsquad>"
        self.s.recv(1024)

        #some texts
        self.MESSAGES = 'bsInternal._getChatMessages()'
        self.ROSTER = 'bsInternal._getGameRoster()'
        self.PLAYERS = '[ p.getName() for p in bs.getSession().players ]'
        self.SEND_MESSAGE = 'bsInternal._chatMessage("{}")'
        self.KICK = 'bsInternal._disconnectClient({})'
        self.SLOMO = 'bs.getNodes()[0].slowMotion = {}'

        self.SHIELDS = 'p.actor.equipShields()'
        self.GLOVES = 'p.actor.equipBoxingGloves()'
        self.SPEEDUP = 'p.actor.node.hockey = {}'
        self.FLY = 'p.actor.node.fly = {}'
        self.INVINCIBLE = 'p.actor.node.invincible = {}'
        self.FREEZE = 'p.actor.node.frozen = {}'

        self.CURSE = 'p.actor.curse()'
        self.KILL = 'p.actor.shatter()'

        self.SET_PUNCHPOWERSCALE = 'p.actor._punchPowerScale = {}'
        self.SET_PUNCHCOOLDOWN = 'p.actor._punchCooldown = {}'
        self.SET_IMPACTSCALE = 'p.actor._impactScale = {}'
        self.SET_BOMBTYPE = 'p.actor.bombType = "{}"'
        self.SET_BOMBCOUNT = 'p.actor.bombCount = {}'
        self.SET_HITPOINTS = 'p.actor.hitPoints = {}'
        self.SET_BLASTRADIUS = 'p.actor.blastRadius = {}'

        self.messages = self.getMessages()
        self.players = self.getPlayers()


    #Sometimes s.recv returns incomplete message, so setup a
    def recv_long(self):
        self.s.setblocking(0)
        total_data = []
        data = ''
        begin = time.time()
        while 1:
            #if you got some data, then break after wait sec
            if total_data and time.time() - begin > 2:
                break
            #if you got no data at all, wait a little longer
            elif time.time() - begin > 2:
                break
            try:
                data=self.s.recv(8192)
                if data:
                    total_data.append(data.decode("utf"))
                    begin = time.time()
                else:
                    time.sleep(0.1)
            except:
                pass
        self.s.setblocking(1)
        return ''.join(total_data)

    def _make_command(self, call, node=False):
        cmd = '''
for p in bs.getSession().players:
    if p.getID() == {}:'''

        if node:
            cmd += '\n' + ' '*(cmd.count('\n')*4) + 'if p.actor.node.exists():'

        cmd += '\n' + ' '*(cmd.count('\n')*4) + call
        return cmd

    def getMessages(self):
        self.s.send(self.MESSAGES.encode())

        ##strip last 12 character which is always " \nbombsquad>"
        self.messages = ast.literal_eval( self.recv_long()[:-12] )
        return self.messages

    def getPlayers(self):
        temp = self.getRoster()
        players = []
        for item in temp:
            for player in item['players']:
                player['clientID'] = item['clientID']
                player.pop('nameFull')
                players.append(player)

        self.players = players
        return players


    def getRoster(self):
        self.s.send( self.ROSTER.encode() )

        ##strip last 12 character which is always " \nbombsquad>"
        return ast.literal_eval( self.recv_long()[:-12] )

    def getNewMessages(self):
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

    def sendMessage(self, msg):
        self.s.send(self.SEND_MESSAGE.format(msg).encode())
        self.s.recv(1024)

    def kick(self, clientID):
        cmd = self._make_command(self.KICK)
        self.s.send(cmd.format(clientID).encode())
        self.s.recv(1024)

    def slomo(self, switch):
        cmd = self._make_command(self.SLOMO)
        self.s.send(cmd.format(switch).encode())
        self.s.recv(1024)

    def shields(self, playerID):
        cmd = self._make_command(self.SHIELDS)
        self.s.send(cmd.format(playerID).encode())
        self.s.recv(1024)

    def gloves(self, playerID):
        cmd = self._make_command(self.GLOVES)
        self.s.send(cmd.format(playerID).encode())
        self.s.recv(1024)

    def speedup(self, playerID, switch=True):
        cmd = self._make_command(self.SPEEDUP, node=True)
        self.s.send(cmd.format(playerID, switch).encode())
        self.s.recv(1024)

    def fly(self, playerID, switch=True):
        cmd = self._make_command(self.FLY, node=True)
        self.s.send(cmd.format(playerID, switch).encode())
        self.s.recv(1024)

    def invincible(self, playerID, switch=True):
        cmd = self._make_command(self.INVINCIBLE, node=True)
        self.s.send(cmd.format(playerID, switch).encode())
        self.s.recv(1024)

    def freeze(self, playerID, switch=True):
        cmd = self._make_command(self.FREEZE, node=True)
        self.s.send(cmd.format(playerID, switch).encode())
        self.s.recv(1024)

    def curse(self, playerID):
        cmd = self._make_command(self.CURSE)
        self.s.send(cmd.format(playerID).encode())
        self.s.recv(1024)

    def kill(self, playerID):
        cmd = self._make_command(self.KILL)
        self.s.send(cmd.format(playerID).encode())
        self.s.recv(1024)

    def setPunchPowerScale(self, playerID, punchPowerScale):
        cmd = self._make_command(self.SET_PUNCHPOWERSCALE)
        self.s.send(cmd.format(playerID, punchPowerScale).encode())
        self.s.recv(1024)

    def setPunchCoolDown(self, playerID, punchCoolDown):
        cmd = self._make_command(self.SET_PUNCHCOOLDOWN)
        self.s.send(cmd.format(playerID, punchCoolDown).encode())
        self.s.recv(1024)

    def setImpactScale(self, playerID, impactScale):
        cmd = self._make_command(self.SET_IMPACTSCALE)
        self.s.send(cmd.format(playerID, impactScale).encode())
        self.s.recv(1024)

    def setBombType(self, playerID, bombType):
        cmd = self._make_command(self.SET_BOMBTYPE)
        self.s.send(cmd.format(playerID, bombType).encode())
        self.s.recv(1024)

    def setBombCount(self, playerID, bombCount):
        cmd = self._make_command(self.SET_BOMBCOUNT)
        self.s.send(cmd.format(playerID, bombCount).encode())
        self.s.recv(1024)

    def setBlastRadius(self, playerID, blastRadius):
        cmd = self._make_command(self.SET_BLASTRADIUS)
        self.s.send(cmd.format(playerID, blastRadius).encode())
        self.s.recv(1024)

    def setHitPoints(self, playerID, hp):
        cmd = self._make_command(self.SET_HITPOINTS)
        self.s.send(cmd.format(playerID, hp).encode())
        self.s.recv(1024)

    def close(self):
        self.s.close()
