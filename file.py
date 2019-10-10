import Player
'''
Created on Jan 27, 2018

@author: Yishan McNabb
'''
def get_names(fob)->[str]:
    players = []
    for num, line in enumerate(fob):
        line = line.rstrip()
        players.append(Player.Player(line, num))
    return players


def run_from_file(filename):
	playerdict = {}
	savefile = open(filename, 'r')
	round_num = savefile.readline().rstrip()
	round_num = int(round_num)
	playerNames = savefile.readline().rstrip().split(' ')
	currentPlayer = ""
	entryCategory = None
	for name in playerNames:
		playerdict[name] = Player.Player(name)
	for line in savefile:
		line = line.rstrip()
		if line == "":
			pass
		elif line[0] == '%':
			currentPlayer = line[1:]
		elif line[0] == "$":
			entryCategory = line[1:]
		else:
			if entryCategory == 'wins':
				if line == "BYE":
					playerdict[currentPlayer].wins.append(line)
				else:
					playerdict[currentPlayer].wins.append(playerdict[line])
			elif entryCategory == 'losses':
				playerdict[currentPlayer].losses.append(playerdict[line])
			elif entryCategory == 'ties':
				playerdict[currentPlayer].ties.append(playerdict[line])
	
	players = playerdict.values()
	
			
		

	
if __name__ == "__main__":
    run_from_file("savefile.txt")
