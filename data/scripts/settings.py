joinNotification = True  # Whether or not to show the notification when a player joins

leaveNotification = True  # Whether or not to show the notification when a player leaves

nameOnPowerUps = True  # Whether or not to show the powerup's name on top of powerups

shieldOnPowerUps = True  # Whether or not to add shield on powerups

discoLightsOnPowerUps = True  # Whether or not to show disco lights on powerup's location

FlyMaps = True  # Whether or not to enable the 3D flying maps in games playlist

generateStats = True  # Whether or not to generate the html stats of the server

botFile = True  # Whether or not to generate the file to be read by my discord bot,
# botFile won't work if `generateStats` is False

partyName = "Someone's party"  # Type your party's name here.

filteredWords = ["some****", "words****"]  # Some words to filter from the chat messages in the party.

showFilteredMessage = True  # Whether to show the message containing restricted word after removing the word or not.

replaceText = "**RESTRICTED WORD FILTERED BY SERVER**"  # The string to replace the filtered words with.

kickAbusers = False  # Whether to kick or not the players who use filtered words.

abuserBanTiming = 300  # The time upto which the kicked abusers may not join the server after being kicked.

showScoresInTopRightCorner = True

showTextsInBottom = True

gameTexts = ["WELCOME MY BOMBSQUAD SERVER", "HAPPY BOMBSQUADING",
             "PLAY FAIR AND HAVE FUN", "SUBSCRIBE TO NAZMI X BOMBSQUAD IN YT", "THIS SERVER ADD SUPERMAN MOD\nENJOY"]


def return_yielded_game_texts():
    for text in gameTexts:
        yield text


def return_players_yielded(bs):
    for player in bs.getSession().players:
        yield player
