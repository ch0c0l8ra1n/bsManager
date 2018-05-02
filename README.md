# bsManager

This is an unofficial Python API for BombSquad making stuff easier to do.

## Usage

Here is a small example to get started:
```python
>>> from manager import BsManager

# Connect to BombSquad's telnet session.
# Note that the port is for your telnet server and not for the actual game instance.
>>> man = BsManager(("127.0.0.1", 43250))

# Return a list of player dictionaries currently playing the game round.
>>> man.getPlayers()
[{'name': 'Jack', 'id': 0, 'clientID': 113},
 {'name': 'Willy', 'id': 1, 'clientID': 114},
 {'name': 'Rico', 'id': 9, 'clientID': 119},
 {'name': 'Magua', 'id': 20, 'clientID': 133}]
 
# I don't like Willy.
>>> man.kick(114)
# `kick()` takes an integer as client ID and kicks out the player.
# Note that if multiple controllers are attached to the
# same game from same client, all of the clients will be kicked.

# Rico would do better with ice bombs.
>>> man.setBombType(9, "ice")
# All the powerups (player status effects) take in an integer which
# is the Player id.
# Note that player Id and client id are different.
```

## Disclaimer

Thanks [rjpj2016](https://github.com/rjpj2016) for working on this unofficial API
and to [Eric Froemling](https://www.froemling.net/about) for creating awesome
[BombSquad](https://www.froemling.net/apps/bombsquad) game.
