'''
Created on Jan 27, 2018

@author: Yishan McNabb
'''
import prompt
import goody
import file
import random
import math
import Player

num_rounds = 0

def check_if_played_before(player1, player2):
    for opponent in player1.get_opponents():
        if player2 == opponent:
            return True
    
    return False

def sort_seats(seats):
    def sum_points(seat):
        sum = 0
        try:
            sum = seat[0].get_points() + seat[1].get_points()
        except AttributeError:
            sum = seat[0].get_points() 
        return sum
    return sorted(seats, key = lambda x : -sum_points(x))

def players_to_seats(players):
    seats = []
    for i in range(0, len(players), 2):
        try:
            seats.append([players[i], players[i+1]])
        except IndexError:
            seats.append([players[i], "BYE"])

    return seats


def loss_fn(players):
    loss = 0
    #make them into the seats format
    seats = players_to_seats(players)
    
    for seat in seats:
        if check_if_played_before(seat[0], seat[1]):
            loss += 100000
        try:
            loss += abs(seat[0].get_points()-seat[1].get_points())
        except AttributeError:
            loss += seat[0].get_points() * 5
            pass

    return loss

            


def pair_round(players):
    min = 99999
    #try shuffle and sort first
    players_copy = list(players)
    for i in range(1000):
        random.shuffle(players)
        players = sorted(players, key = lambda x : -x.get_points())
        loss = loss_fn(players)
        if loss < 99999:
            return players_to_seats(players)
        
    #Complete Randomness
    for i in range(200000):
        random.shuffle(players)
        loss = loss_fn(players)
        if loss == 0:
            return players_to_seats(players)
        if loss < min:
            min = loss
            players_copy = list(players)

    if min == 99999:
        assert False

    print('The minimum was:', min)
    return sort_seats(players_to_seats(players_copy))
        
        


def print_pairings(seats):
    for i in range(0, len(seats)):
        try:
            print("Table", i+1, '    ', seats[i][0].name, "("+str(seats[i][0].get_points()) + ")", 'VS.', seats[i][1].name, "("+str(seats[i][1].get_points()) + ")")
        except AttributeError:
            print("Table", i+1, '    ', seats[i][0].name, "("+str(seats[i][0].get_points()) + ")",'VS.', seats[i][1], "This match does not need to be reported.")

    
def get_number_string(players):
    str = ''
    for player in players:
        str += str(player.get_number())

    return str


def check_for_same_pairs(seats):
    try:
        for x,y in seats:
            j = x.name
            k = y.name
            if x in y.get_opponents():
                return True
        return False
    except AttributeError:
        return False
        
def calculate_num_rounds(players):
    global num_rounds
    ppl = len(players)
    if ppl < 4:
        num_rounds = -1
    elif ppl in range(4,9):
        num_rounds = 3
    elif ppl in range(9,17):
        num_rounds = 4
    elif ppl in range(17,33):
        num_rounds = 5
    elif ppl in range(33,65):
        num_rounds = 6
    elif ppl in range(65,129):
        num_rounds = 7
    elif ppl in range(129,257):
        num_rounds = 8
    elif ppl in range(257, 513):
        num_rounds = 9
    elif ppl in range(513, 1025):
        num_rounds = 10
    elif ppl in range(1025, 2049):
        num_rounds = 11
    else:
        num_rounds = 12

#this function now does double duty at the end of the round
#it drops, adds or prints standings
def end_of_round_cleanup(players):
    while True:
        dropping = prompt.for_string("Enter the name of player who is dropping or (p)air next round or view (s)tandings or (a)dd a new player"
                                    , is_legal= lambda x : x in [y.name for y in players] or x == 'p' or x == 's' or x == 'a',
                                    error_message='Invalid player name or not p')
        if dropping == 'p':
            break;
        elif dropping == 's':
            calculate_standings(players)
            print_standings(players)
        elif dropping == 'a':
            players.append(Player.Player(input('Enter the name of the new player: ')))

        else:
            for i in range(len(players)):
                if dropping == players[i].name:
                    print(players[i].name, 'has been dropped.')
                    del players[i]
                    break

        print()
    
def get_results(pairs, players):
    still_playing = set(range(1, len(pairs) + 1))
    while len(still_playing)>0:
        print("Waiting for results from tables", still_playing)
        table = prompt.for_int("Enter a table number to report results", is_legal = lambda x : x in still_playing,
                                error_message="Enter a table that has not finished their match.")
        table -= 1
        winner = prompt.for_string("Enter a winner ("+ str(pairs[table][0].name) + ") or (" + str(pairs[table][1].name) + ") or (tie)",
                                    is_legal = (lambda x : x == pairs[table][0].name or x == pairs[table][1].name or x == "tie"),
                                    error_message="please enter the winner's full name or tie")
        if winner == 'tie':
            pairs[table][0].ties.append(pairs[table][1])
            pairs[table][1].ties.append(pairs[table][0])
        else:
            if winner == pairs[table][0].name:
                pairs[table][0].wins.append(pairs[table][1])
                pairs[table][1].losses.append(pairs[table][0])
            else:
                pairs[table][1].wins.append(pairs[table][0])
                pairs[table][0].losses.append(pairs[table][1])
        
        still_playing.remove(table + 1)
        print()

        
def calculate_standings(players):
    try:
        for player in players:
            player.tiebreaker += str(player.get_points())
        
        for player in players:
            if get_opponents_win_percentage(player) == 0:
                player.tiebreaker += "000"
            else:
                player.tiebreaker += str(int(round(get_opponents_win_percentage(player), 3)*1000))
            num_opponents = 0
            percentage = 0
            for opponent in (player.wins + player.losses + player.ties):
                if opponent != "BYE":
                    percentage += get_opponents_win_percentage(opponent)
                    num_opponents += 1
            
            if percentage/num_opponents == 0:
                player.tiebreaker += "000"
            else:
                player.tiebreaker+= str(int(round(percentage/num_opponents, 3)*1000))
    except ZeroDivisionError: #this means the player played no games
        player.tiebreaker = '0000000'
            

def get_opponents_win_percentage(player):
    num_opponents = 0
    percentage = 0
    for opponent in (player.wins + player.losses + player.ties):
        if opponent != "BYE":
            percentage += get_win_percentage(opponent)
            num_opponents+=1
    return percentage/num_opponents

def get_win_percentage(player):
    return player.num_wins()/(player.num_wins() + player.num_losses() + player.num_ties())

def print_standings(players):
    players = sorted(players, key = lambda x : -int(x.tiebreaker))
    for i in range(len(players)):
        print(i + 1, players[i].name, 'Tie-breaker number: ' + players[i].tiebreaker)


#runs tournament normally, if pairs is called with a value, it means it was run from 
#a save file. Round number can be passed in from run_tournament_from_file function
#which is why it needs to be an argument

def run_tournament(players, roundNumber, pairs=None):
    calculate_num_rounds(players)
    if roundNumber == 1:
        print("Today we are playing", num_rounds, "rounds.")
    for i in range(roundNumber ,num_rounds + 1):
        print()
        print("--------------Round", roundNumber, "Pairings--------------")
        if pairs == None:#If we need to generate pairs(i.e. not given from a savefile) then call the pair_round function
            pairs = pair_round(players)
        print_pairings(pairs)
        write_to_file(players, roundNumber)
        append_pairings_to_file(f"{roundNumber}", pairs)
        print()
        if len(players)%2 != 0: #if there is a BYE
            pairs[len(pairs)-1][0].wins.append('BYE')#give the player that has a BYE a win
            del pairs[len(pairs)-1] #delete that pairing before get results is called
        get_results(pairs, players)
        end_of_round_cleanup(players)
        roundNumber +=1
        print("*Results up to round " + str(roundNumber - 1) + " have been saved.\n")
        pairs = None #need to reset pairs to none so that we generate a new set of pairs

    calculate_standings(players)
    print_standings(players)

#very important function that allows results to be saved into files
#in between rounds. Can also do many things to force pairings as well
#change mistakes/go back in time/add players if users understand file structure
def run_from_file(filename):
    playerdict = {"BYE" : "BYE"}# must establish the dictionary that will have the names of players along with their associated player object
    savefile = open(filename, 'r')
    round_num = savefile.readline().rstrip()#First line in savefile is current round number
    round_num = int(round_num)
    playerNames = savefile.readline().rstrip().split(',')[0:-1]#second line has all player names, there is an extra comma at the end
                                                               #which causes a player with the empty string name, we delete that player here
    currentPlayer = ""
    entryCategory = None
    pairs = [] #this value will store pairs
    for num, name in enumerate(playerNames):
        playerdict[name] = Player.Player(name)#Create all player objects and put them in the playerdict
    for line in savefile:
        line = line.rstrip()
        if line == "":#there shouldn't be any empty lines (except for the last line)
            pass
        elif line[0] == '%':#the if part of the loop figures out which player and which entry category (that players wins losses or ties) it is inputting
            currentPlayer = line[1:]
        elif line[0] == "$":
            entryCategory = line[1:]
        elif line[0] == "*":#this is a special case, at the end of the file there will be pairings that we need to keep track of
            people = line.split(":")[1]
            peopleList = people.split(",")[0:-1] #again there is an extra comma, which we need to delete 
            for i in range(0, len(peopleList)-1, 2):
                pairs.append([playerdict[peopleList[i]], playerdict[peopleList[i+1]]])
        else:
        #The else part of the loop actually puts the wins losses or ties inside that players attributes
            if entryCategory == 'wins':
                    playerdict[currentPlayer].wins.append(playerdict[line])
            elif entryCategory == 'losses':
                playerdict[currentPlayer].losses.append(playerdict[line])
            elif entryCategory == 'ties':
                playerdict[currentPlayer].ties.append(playerdict[line])
                
    del playerdict["BYE"]
    players = list(playerdict.values())
    savefile.close()
    run_tournament(players, round_num, pairs)


def write_to_file(players, round):
    savefile = open("{}".format(round), "w")
    savefile.write(str(round)+"\n")
    for player in players:
        savefile.write(player.name + ",")
    savefile.write("\n")
    for player in players:
        savefile.write("%"+player.name+"\n")
        savefile.write("$wins\n")
        for opponent in player.wins:
            if opponent == "BYE":
                savefile.write("BYE" + "\n")
            else:
                savefile.write(opponent.name+ "\n")
        savefile.write("$losses\n")
        for opponent in player.losses:
            savefile.write(opponent.name+ "\n")
        savefile.write("$ties\n")
        for opponent in player.ties:
            savefile.write(opponent.name+"\n")
        
    
    savefile.close()

def append_pairings_to_file(filename, pairs):
    
    savefile = open(filename, "a")
    savefile.write('*pairs:')
    for pair in pairs:
        if pair[1] == "BYE":
            savefile.write(pair[0].name + ",BYE,")
        else:
            savefile.write(pair[0].name + "," + pair[1].name + ",")
        
    
    savefile.close()


def print_welcome_screen():
        print("Welcome to Yishan's Tournament Software!\n")
        print("---------------How To Use---------------\n")
        print("1. Press s or n to either load a saved tournament or start a new one.")
        print("2. Find the players.txt file and enter participans on separate lines.")
        print("3. Follow on screen prompts to run tournament, all command available are enclosed in ().\n")
        
def main():
        print_welcome_screen()
        shouldLoadFromSavefile = prompt.for_string("Load a (s)aved tournament or start a (n)ew one?" 
                                                    ,is_legal = (lambda x: x == 's' or x == 'n'), error_message = 'Please enter s or n.')
        if shouldLoadFromSavefile == "s":
                fileStr = prompt.for_string("Enter the name of the savefile")
                run_from_file(fileStr)
        else:
                fob = goody.safe_open("Press enter if your partipants are in players.txt, otherwise type out the name of your file.",
                                    'r', 'There was an error finding/opening the file.', default='players.txt')
                players = file.get_names(fob)
                while len(players) < 4:
                        print()
                        print("You need at least 4 players to start a tournaments, please edit your file and press enter")
                        input()
                        fob.close()
                        fob = goody.safe_open("Name of file with players", 'r', 'There was an error finding/opening the file.', default='players.txt')
                        players = file.get_names(fob)
                        
                for player in players:
                        print(player.name)
                while True:
                        print("***There are currently", len(players), "players enrolled.***")
                        start = prompt.for_string("Start tournament? Enter (y)es or (n)o", 
                                                is_legal = (lambda x: x == 'y' or x == 'n'), error_message = 'Please enter y or n.')
                        if start =='y':
                                run_tournament(players, 1)
                                break
                        else:
                                print("Edit file then hit enter.")
                                input()
                                fob = goody.safe_open("Name of file with players", 'r', 'There was an error finding/opening the file.', default='players.txt')
                                players = file.get_names(fob)
                                for player in players:
                                        print(player.name)

                fob.close()

if __name__ == "__main__":
        main()
