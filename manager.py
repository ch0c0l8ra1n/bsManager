from socket import socket, AF_INET, SOCK_STREAM
import ast
import time

class BsManager:
    def __init__(self,addr):
        """
        Connect the telnet session to BombSquad instance.
        """
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.settimeout(5)
        self.s.connect(addr)
        self.s.settimeout(None)

        # Receive first prompt message ## " \nbombsquad>".
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


    def recv_long(self):
        """
        Sometimes s.recv returns incomplete message, so setup a
        way to receive the complete message in portions.
        """
        self.s.setblocking(0)
        total_data = []
        data = ''
        begin = time.time()
        while True:
            #if you got some data, then break after wait sec
            if total_data and time.time() - begin > 2:
                break
            #if you got no data at all, wait a little longer
            elif time.time() - begin > 2:
                break
            try:
                data = self.s.recv(8192)
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
        """
        Generates the command to be run in the connected
        telnet session.
        """
        cmd = '''
for p in bs.getSession().players:
    if p.getID() == {}:'''

        if node:
            cmd += '\n' + ' '*(cmd.count('\n')*4) + 'if p.actor.node.exists():'

        cmd += '\n' + ' '*(cmd.count('\n')*4) + call
        return cmd

    def getMessages(self):
        """
        Gets a list of current messages (upto 40).
        """
        self.s.send(self.MESSAGES.encode())

        ##strip last 12 character which is always " \nbombsquad>"
        self.messages = ast.literal_eval(self.recv_long()[:-12])
        return self.messages

    def getPlayers(self):
        """
        Returns a list of players currently playing the game round.
        """
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
        """
        Returns a list of players currently connected to the server.
        """
        self.s.send(self.ROSTER.encode())

        ##strip last 12 character which is always " \nbombsquad>"
        return ast.literal_eval(self.recv_long()[:-12])

    def getNewMessages(self):
        """
        Returns new messages
        (after last call to getNewMessages() or getMessages()).
        """
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
        """
        Send a message from a host.
        """
        self.s.send(self.SEND_MESSAGE.format(msg).encode())
        self.s.recv(1024)

    def kick(self, clientID):
        """
        Kick a player by clientID.
        """
        cmd = self._make_command(self.KICK)
        self.s.send(cmd.format(clientID).encode())
        self.s.recv(1024)

    def slomo(self, switch):
        """
        Enable or disable slow motion ingame.
        """
        cmd = self._make_command(self.SLOMO)
        self.s.send(cmd.format(switch).encode())
        self.s.recv(1024)

    def shields(self, playerID):
        """
        Gives shield to the respective player ID.
        """
        cmd = self._make_command(self.SHIELDS)
        self.s.send(cmd.format(playerID).encode())
        self.s.recv(1024)

    def gloves(self, playerID):
        """
        Gives boxing gloves to the respective player ID.
        """
        cmd = self._make_command(self.GLOVES)
        self.s.send(cmd.format(playerID).encode())
        self.s.recv(1024)

    def speedup(self, playerID, switch=True):
        """
        Increase moving speed of the respective player ID.
        """
        cmd = self._make_command(self.SPEEDUP, node=True)
        self.s.send(cmd.format(playerID, switch).encode())
        self.s.recv(1024)

    def fly(self, playerID, switch=True):
        """
        Enables fly mode for the respective player ID.
        """
        cmd = self._make_command(self.FLY, node=True)
        self.s.send(cmd.format(playerID, switch).encode())
        self.s.recv(1024)

    def invincible(self, playerID, switch=True):
        """
        Makes the player ID invincible to everything
        except curses and falling off cliffs.
        """
        cmd = self._make_command(self.INVINCIBLE, node=True)
        self.s.send(cmd.format(playerID, switch).encode())
        self.s.recv(1024)

    def freeze(self, playerID, switch=True):
        """
        Freezes the respective player ID (ice bomb like).
        """
        cmd = self._make_command(self.FREEZE, node=True)
        self.s.send(cmd.format(playerID, switch).encode())
        self.s.recv(1024)

    def curse(self, playerID):
        """
        Curses the respective player ID.
        """
        cmd = self._make_command(self.CURSE)
        self.s.send(cmd.format(playerID).encode())
        self.s.recv(1024)

    def kill(self, playerID):
        """
        Kills the respective player ID.
        """
        cmd = self._make_command(self.KILL)
        self.s.send(cmd.format(playerID).encode())
        self.s.recv(1024)

    def setPunchPowerScale(self, playerID, punchPowerScale):
        """
        Set the damage multiplier for punches for the respective
        player ID.
        """
        cmd = self._make_command(self.SET_PUNCHPOWERSCALE)
        self.s.send(cmd.format(playerID, punchPowerScale).encode())
        self.s.recv(1024)

    def setPunchCoolDown(self, playerID, punchCoolDown):
        """
        Set the delay between consecutive punches (in ms).
        """
        cmd = self._make_command(self.SET_PUNCHCOOLDOWN)
        self.s.send(cmd.format(playerID, punchCoolDown).encode())
        self.s.recv(1024)

    def setImpactScale(self, playerID, impactScale):
        """
        Set the damage multiplier for bombs (including land
        mines) for the respective player ID.
        """
        cmd = self._make_command(self.SET_IMPACTSCALE)
        self.s.send(cmd.format(playerID, impactScale).encode())
        self.s.recv(1024)

    def setBombType(self, playerID, bombType):
        """
        Set the current bomb type for the respective player ID.
        Possible values: "normal, "ice", "sticky", impact", "tnt".
        """
        cmd = self._make_command(self.SET_BOMBTYPE)
        self.s.send(cmd.format(playerID, bombType).encode())
        self.s.recv(1024)

    def setBombCount(self, playerID, bombCount):
        """
        Set the number of bombs a player ID can throw at a time.
        """
        cmd = self._make_command(self.SET_BOMBCOUNT)
        self.s.send(cmd.format(playerID, bombCount).encode())
        self.s.recv(1024)

    def setBlastRadius(self, playerID, blastRadius):
        """
        Set the bomb blast radius for the player ID.
        """
        cmd = self._make_command(self.SET_BLASTRADIUS)
        self.s.send(cmd.format(playerID, blastRadius).encode())
        self.s.recv(1024)

    def setHitPoints(self, playerID, hp):
        """
        Set current HitPoints for the player ID.
        """
        cmd = self._make_command(self.SET_HITPOINTS)
        self.s.send(cmd.format(playerID, hp).encode())
        self.s.recv(1024)

    def close(self):
        """
        Close this telnet session.
        """
        self.s.close()
