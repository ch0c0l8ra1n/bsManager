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
[{'account': 'Android12345678',
  'name': 'Watermelons',
  'playerID': 92,
  'profiles': {'__account__': {'color': [1, 1, 0],
    'highlight': [1, 0.1499999999999999, 0.1499999999999999],
    'global': False,
    'character': 'Zoe',
    'icon': '\ue01e'},
   'Watermelons': {'color': [1, 0.1499999999999999, 0.1499999999999999],
    'highlight': [1, 1, 1],
    'global': False,
    'character': 'Zoe',
    'icon': '\ue01e'}},
  'clientID': 192,
  'team': 1},
 {'account': 'PC123456',
  'name': 'Jack',
  'playerID': 120,
  'profiles': {'Chikoo': {'color': [0.1, 0.1, 1],
    'highlight': [0.4, 0.2, 0.1],
    'global': False,
    'character': 'Kronk',
    'icon': '\ue01e'},
   '__account__': {'color': [1, 1, 1],
    'highlight': [0.13, 0.13, 0.13],
    'global': False,
    'character': 'Spaz',
    'icon': '\ue01e'},
   'Jack': {'color': [1, 0.15, 0.15],
    'highlight': [1, 1, 0],
    'global': False,
    'character': 'Jack Morgan',
    'icon': '\ue01e'}},
  'clientID': 217,
  'team': 1},
 {'account': 'VagrantPie123123',
  'name': 'Donald',
  'playerID': 121,
  'profiles': {'Donald': {'color': [0.13, 0.13, 0.13],
    'highlight': [1, 0.1499999999999999, 0.1499999999999999],
    'global': False,
    'character': 'Spaz',
    'icon': '\ue01e'},
   '__account__': {'color': [0.5, 0.25, 1.0],
    'highlight': [0.5, 0.25, 1.0],
    'character': 'Spaz'}},
  'clientID': 219,
  'team': 0}]

# I don't like Willy.
>>> man.kick(114)
# `kick()` takes an integer as ClientID and kicks out the player.
# Note that if multiple controllers are attached to the
# same game from same client, all of the clients will be kicked.

# Rico would do better with ice bombs.
>>> man.setBombType(9, "ice")
# All the powerups (player status effects) take in an integer which
# is the PlayerID.
# Note that PlayerID and ClientID are different.

# Increase blast radius to 6.5 for Jack's bombs.
>>> man.setBlastRadius(0, 6.5)

# Make Magua move around faster.
>>> man.speedup(20, True)

# Let's turn on slow motion for the current game round.
>>> man.slomo(True)
```

## Documentation

Currently there is no proper documentation online. You can however, take a look
in [manager.py](manager.py) to understand what all various methods are available
and what purpose they serve.

## Disclaimer

Thanks to [rjpj2016](https://github.com/rjpj2016) for
[working on this unofficial API](https://github.com/rjpj2016/bsManager)
and [Eric Froemling](https://www.froemling.net/about) for creating the
awesome [BombSquad](https://www.froemling.net/apps/bombsquad) game.
