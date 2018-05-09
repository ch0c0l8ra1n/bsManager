from socket import socket, AF_INET, SOCK_STREAM
from . import const
import ast
import time

class BsManager:
    def __init__(self, addr):
        """
        Connect the telnet session to BombSquad instance.
        """
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.settimeout(5)
        self.s.connect(addr)
        self.s.settimeout(None)

        # Receive first prompt message ## " \nbombsquad>".
        self.s.recv(1024)

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
            # If you got some data, then break after wait sec
            if total_data and time.time() - begin > 2:
                break
            # If you got no data at all, wait a little longer
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

    def execute(self, cmd):
        """
        Execute a custom command.
        """
        self.s.send(cmd.encode())
        return ast.literal_eval(self.recv_long()[:-12])

    def getMessages(self):
        """
        Gets a list of current messages (upto 40).
        """
        self.s.send(const.MESSAGES.encode())

        # Strip last 12 character which is always " \nbombsquad>"
        self.messages = ast.literal_eval(self.recv_long()[:-12])
        return self.messages

    def getPlayers(self):
        """
        Returns a list of players currently playing the game round.
        """
        x = '''[ { "name"     : x.getName(),
                   "team"     : x.getTeam().getID(),
                   "playerID" : x.getID(),
                   "clientID" : x.getInputDevice().getClientID(),
                   "profiles" : x.getInputDevice()._getPlayerProfiles(),
                   "account"  : x.getInputDevice()._getAccountName(0) }
               for x in bs.getSession().players ]'''

        self.s.send(x.encode())

        while True:
            try:
                players = ast.literal_eval(self.recv_long()[:-12])
            except SyntaxError:
                # Sometimes the telnet session may deliver us
                # data in abnormal format, so keep looping until it
                # returns data in expected format.
                pass
            else:
                break

        self.players = players
        return players

    def getRoster(self):
        """
        Returns a list of players currently connected to the server.
        """
        self.s.send(const.ROSTER.encode())

        # Strip last 12 character which is always " \nbombsquad>"
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
            if all(temp[j] == self.messages[j-i] for j in range(i, len(temp))):
                    if i == 0:
                            return []
                    return self.messages[(-1)*i:]
        return self.messages

    def dropRandomPowerups(self):
        """
        Drops random powers around the map just like the
        game does it automatically once in a while.
        """
        self.s.send(const.POWERUPS.encode())
        return self.s.recv(1024)[:-12]

    def endGame(self):
        """
        End the current game round. The current score decides
        the winning team.
        """
        self.s.send(const.ENDGAME.encode())
        return self.s.recv(1024)[:-12]

    def sendMessage(self, msg):
        """
        Send a message from a host.
        """
        self.s.send(const.SEND_MESSAGE.format(msg).encode())
        return self.s.recv(1024)[:-12]

    def kickByClientID(self, clientID):
        """
        Kick a player by clientID.
        """
        self.s.send(const.KICK.format(clientID).encode())
        return bool(self.s.recv(1024)[:-12])

    def kickByPlayerID(self, playerID):
        """
        Kick a player by playerID.
        """
        for player in self.players:
            if player['playerID'] == playerID:
                return self.kickByClientID(player['clientID'])

    def slomo(self, switch):
        """
        Enable or disable slow motion ingame.
        """
        self.s.send(const.SLOMO.format(switch).encode())
        return self.s.recv(1024)[:-12]

    def shields(self, playerID):
        """
        Gives shield to the respective player ID.
        """
        cmd = self._make_command(const.SHIELDS)
        self.s.send(cmd.format(playerID).encode())
        return self.s.recv(1024)[:-12]

    def gloves(self, playerID):
        """
        Gives boxing gloves to the respective player ID.
        """
        cmd = self._make_command(const.GLOVES)
        self.s.send(cmd.format(playerID).encode())
        return self.s.recv(1024)[:-12]

    def speedup(self, playerID, switch=True):
        """
        Increase moving speed of the respective player ID.
        """
        cmd = self._make_command(const.SPEEDUP, node=True)
        self.s.send(cmd.format(playerID, switch).encode())
        return self.s.recv(1024)[:-12]

    def fly(self, playerID, switch=True):
        """
        Enables fly mode for the respective player ID.
        """
        cmd = self._make_command(const.FLY, node=True)
        self.s.send(cmd.format(playerID, switch).encode())
        return self.s.recv(1024)[:-12]

    def invincible(self, playerID, switch=True):
        """
        Makes the player ID invincible to everything
        except curses and falling off cliffs.
        """
        cmd = self._make_command(const.INVINCIBLE, node=True)
        self.s.send(cmd.format(playerID, switch).encode())
        return self.s.recv(1024)[:-12]

    def freeze(self, playerID, switch=True):
        """
        Freezes the respective player ID (ice bomb like).
        """
        cmd = self._make_command(const.FREEZE, node=True)
        self.s.send(cmd.format(playerID, switch).encode())
        return self.s.recv(1024)[:-12]

    def curse(self, playerID):
        """
        Curses the respective player ID.
        """
        cmd = self._make_command(const.CURSE)
        self.s.send(cmd.format(playerID).encode())
        return self.s.recv(1024)[:-12]

    def kill(self, playerID):
        """
        Kills the respective player ID.
        """
        cmd = self._make_command(const.KILL)
        self.s.send(cmd.format(playerID).encode())
        return self.s.recv(1024)[:-12]

    def setColor(self, playerID, color):
        """
        Set player character's main color by
        passing a tuple containing RGB values.
        """
        cmd = self._make_command(const.SET_COLOR)
        self.s.send(cmd.format(playerID, color).encode())
        return self.s.recv(1024)[:-12]

    def setColorHightlight(self, playerID, color):
        """
        Set player character's highlight color by
        passing a tuple containing RGB values.
        """
        cmd = self._make_command(const.SET_COLORHIGHLIGHT)
        self.s.send(cmd.format(playerID, color).encode())
        return self.s.recv(1024)[:-12]

    def setColorName(self, playerID, color):
        """
        Set player character's name color by passing
        a tuple containing RGB values.
        """
        cmd = self._make_command(const.SET_COLORNAME)
        self.s.send(cmd.format(playerID, color).encode())
        return self.s.recv(1024)[:-12]

    def setName(self, playerID, name):
        """
        Change player's current name.
        """
        cmd = self._make_command(const.SET_NAME)
        self.s.send(cmd.format(playerID, name).encode())
        return self.s.recv(1024)[:-12]

    def setPunchPowerScale(self, playerID, punchPowerScale):
        """
        Set the damage multiplier for punches for the respective
        player ID.
        """
        cmd = self._make_command(const.SET_PUNCHPOWERSCALE)
        self.s.send(cmd.format(playerID, punchPowerScale).encode())
        return self.s.recv(1024)[:-12]

    def setPunchCoolDown(self, playerID, punchCoolDown):
        """
        Set the delay between consecutive punches (in ms).
        """
        cmd = self._make_command(const.SET_PUNCHCOOLDOWN)
        self.s.send(cmd.format(playerID, punchCoolDown).encode())
        return self.s.recv(1024)[:-12]

    def setImpactScale(self, playerID, impactScale):
        """
        Set the damage multiplier for bombs (including land
        mines) for the respective player ID.
        """
        cmd = self._make_command(const.SET_IMPACTSCALE)
        self.s.send(cmd.format(playerID, impactScale).encode())
        return self.s.recv(1024)[:-12]

    def setBombType(self, playerID, bombType):
        """
        Set the current bomb type for the respective player ID.
        Possible values: "normal, "ice", "sticky", impact", "tnt".
        """
        cmd = self._make_command(const.SET_BOMBTYPE)
        self.s.send(cmd.format(playerID, bombType).encode())
        return self.s.recv(1024)[:-12]

    def setBombCount(self, playerID, bombCount):
        """
        Set the number of bombs a player ID can throw at a time.
        """
        cmd = self._make_command(const.SET_BOMBCOUNT)
        self.s.send(cmd.format(playerID, bombCount).encode())
        return self.s.recv(1024)[:-12]

    def setBlastRadius(self, playerID, blastRadius):
        """
        Set the bomb blast radius for the player ID.
        """
        cmd = self._make_command(const.SET_BLASTRADIUS)
        self.s.send(cmd.format(playerID, blastRadius).encode())
        return self.s.recv(1024)[:-12]

    def setHitPoints(self, playerID, hp):
        """
        Set current HitPoints for the player ID.
        """
        cmd = self._make_command(const.SET_HITPOINTS)
        self.s.send(cmd.format(playerID, hp).encode())
        return self.s.recv(1024)[:-12]

    def setTimeLimit(self, limit):
        """
        Change time limit for the current game round (value
        passed must be in seconds).
        """
        self.s.send(const.SET_TIMELIMIT.format(limit).encode())
        return self.s.recv(1024)[:-12]

    def close(self):
        """
        Close this telnet session.
        """
        self.s.close()
