# bsManager

This is an unofficial Python api for BombSquad.

Initialize a BsManager instance with a tuple containing your ip-address and port.

Eg:

man = BsManager( ("127.0.0.1",43250) ) # Note that the port is for your telnet server and not for the actual game instance.

Usage:

getPlayers() returns a list of dict containing the name, clientId, and playerId for each player in the game.

kick() takes an integer as client id and kicks out the player.

kickById() #todo

Note that if multiple controllers are attached to the same game from same client, all of the clients will be kicked

getMessages() returns a list of current messages. Upto 40.

getNewMessages() returns messages that were sent after last call of getMessages() or getNewMessages itself.

sendMessage() takes in a string and sends that message as the server.

slomo() takes in a bool and changes the game mode accordingly.

All the powerups (player status effects) take in an int which is the Player id. Note that player Id and client id are different.

setBombType() takes in player id and a string to change the bomb type. The string can be either of these

"normal"

"ice"

"sticky"

"impact"

"tnt"

setHitPoints() takes in player id and another int. The hit point of the player is then set to the aforementioned int.

TODO's:

setBombCount()

kickById()

spawnPlayer()

spawnBomb()


