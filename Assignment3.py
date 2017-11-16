def gameOfNuts(nuts, comp1=None):
    '''
    :param nuts: 		The amount of nuts on the table
    :param comp1: 		The optional computer that will play as player 2
    :return:			Doesn't return anything

            Primary component that runs the game. The game can either be ran against an AI or another player.
            Games against the AI will be saved to be learnt
            By default, The AI is set to None, indicating that the game will be played against a player.
            adding an instance of the computer from the computer class, will be played against the computer.
            the instance of the computer will be trained from the following game
    '''
    player_turn = 2																										# intially set to 2, so that the first time the game loops, Player 1 will start
    while nuts > 0:																										# only runs if there is more than 1 nut on the board
        # switchs the player from the previous round
        player_turn = switch_turns(player_turn)
        nut_status(nuts)																								# print out the status of nuts
        # checks if the computer exist and it is the computers turn
        if player_turn == 2 and comp1 is not None:
            # the computer makes it move
            sub = comp1.makeMove(nuts)
            print('Player ' + str(player_turn) +
                  ': How many nuts do you take (1-3)?', sub)
        else:
            # the player, that isn't a computer, will be asked to input a move
            sub = input_nuts(player_turn)
        nuts -= sub																										# the players move subs from the total nuts
    # once broken out of the loop, the player who just went will lose
    print('\n', 'player ' + str(player_turn) + ', you lose', '\n')

    if comp1 is not None:																								# updates the computer to learn
        if player_turn == 1:
            comp1.update("win")
        else:
            comp1.update("lose")


def train(nuts, comp1, comp2):
    '''
    A system that trains the AI in simulated games against another AI
    the AI will train in the game and learn from it

    :param nuts: 				The amount of nuts on the table
    :param comp1:				The computer being trained
    :return:					Returns nothing
    '''

    player_turn = 2
    while nuts > 0:																										# the game runs essentially the same as the base game, just without any prompts or prints
        player_turn = switch_turns(player_turn)

        if player_turn == 2:																							# just like in the game with the player, the AI will always go second
            sub = comp1.makeMove(nuts)
        elif player_turn == 1:
            sub = comp2.makeMove(nuts)
        nuts -= sub

    if player_turn == 1:																								# updates the Computers
        comp1.update('win')
        comp2.update('lose')
    else:
        comp1.update("lose")
        comp2.update("win")


def switch_turns(player):
    '''
    :param player:				The player that just went
    :return: 					The player that will go next
    '''
    if player == 1:
        return 2
    return 1


def nut_status(nuts):
    '''
    :param nuts: 				the current amount of nuts on the board
    :return:					Nothing
    '''
    print()
    print("There are " + str(nuts) + " nuts on the board")


def init_table():
    '''
    :return:					the amount of nuts that will be on the table
    '''
    nuts = int(input("How many nuts are there on the table initially (10-100)?"))
    if nuts < 10 or nuts > 100:
        print("Please enter a number between 10 and 100")
        nuts = init_table()
    return nuts


def input_nuts(player):
    '''
    Will prompt the player to input a number from [1-3] for the amount that they want to take off the board
    :param player: 				The player that will be prompted
    :return: 					The amount that the player inputted
    '''
    sub = int(input('Player ' + str(player) +
                    ': How many nuts do you take (1-3)?'))
    if sub < 1 or sub > 3:
        print("Please enter a number between 1 and 3")
        sub = input_nuts(player)
    return sub


import random


class Computer():
    '''
    A computer that will be used to play against the player
    The computer initially starts off not knowing how to play the game, but will gradually get better over games played
    '''

    def __init__(self):
        # holds the amount of games that the AI has played
        self.games_played = 0
        self.table = self.generate_table()
        # a dictionary that will hold the moves made by the AI. Key = nuts at the given moment. Value = move made
        self.moves_made = {}

    def generate_table(self):
        '''
        The table[hats] that will hold the values[nuts] that the AI will later use to play
        :return: a 2d table. 101 rows, 4 columns each -> [0,1,1,1]
        '''
        table = []
        for index in range(101):
            table.append([0, 1, 1, 1])
        return table

    def print_moves_made(self):
        '''
        prints out dictionary of moves made. key: nuts at the given moment. value: move made
        :return:
        '''
        print(self.moves_made)

    def makeMove(self, nuts):
        '''

        :param nuts: 		The amount of nuts on the table
        :return: 			The move that the AI has decided to make
        '''
        row = self.table[nuts]
        # the AI will randomly select a nut from the table, based on the statistical win/loss
        rand = random.randint(1, row[1] + row[2] + row[3])
        if (rand <= row[1]):
            move = 1
        elif (rand <= row[1] + row[2]):
            move = 2
        else:
            move = 3
        # adds the move made to the dictionary
        self.moves_made[nuts] = move
        return move

    @staticmethod
    def printTable(comp1):
        '''
        THIS IS FOR DEBUGGING PURPOSES AND GENERALLY MESSING AROUND WITH FORMATTING
        prints a nicely formatted table that consist of the stats that the AI randomly chooses from
        This will also create a log of the table to a file
        :param comp1: 		The AI
        :return:
        '''
        table1 = comp1.table
        user = input('Do you want to print the table to a file (y/n)')

        file = open("Game_" + str(comp1.games_played) + ".txt", "w")

        for row in range(len(table1) - 1, 0, -1):
            if row == len(table1) - 1:
                print("{:^50}".format("Computer 1"))
                file.write("{:^50}".format("Computer 1") + "\n")
            print("{:^10d} {:^10d} {:^10d} {:^10d}".format(
                row, table1[row][1], table1[row][2], table1[row][3]))

            file.write("{:^10d} {:^10d} {:^10d} {:^10d}".format(
                row, table1[row][1], table1[row][2], table1[row][3]))
        file.close()

    def update(self, result):
        '''
        updates the table of the computer based on a win/lose
        uses the moves_made dictionary to trace back and update the table
        :param result:			Did the Computer win or did it lose
        :return: 				None
        '''
        if (result == "win"):																							# if the computer has won
            for keys, value in self.moves_made.items():
                # it will loop through the dictionary and increase the odds of that moving being played again
                self.table[keys][value] += 1
        if (result == "lose"):																							# if the computer has loss
            for keys, value in self.moves_made.items():
                if self.table[keys][value] > 1:
                    # if will loop through the dictionary and decrease the odds of that moving being played again. Value does not drop past 1
                    self.table[keys][value] -= 1
        self.moves_made = {}																							# moves made gets cleared
        # AI increases the amount of games played
        self.games_played += 1


def playAgain():
    '''
    asks whether the player wants to play again
    :return: whether the player wants to play again
    '''
    user = int(input('Play again (1 = yes, 0 = no)? '))
    if user == 1:
        return True
    elif user == 0:
        return False
    else:
        print('Invalid response')
        return playAgain()


def printOptions():
    '''
    asks the play whether they want to PVP, PVAi or PV(Train Ai)
    :return: the option the player has chosen
    '''
    print('Options: ')
    print('    Play against a friend           (1) ')
    print('    Play against the computer       (2) ')
    print('    Play against the train computer (3) ')
    print('    Quit                            (4) ')
    user = int(input('which option do you take            (1-4)? '))
    if user < 1 or user > 5:
        print()
        print('enter a number from [1-4]')
        return printOptions()
    return user


if __name__ == "__main__":
    # the computer that the game will be used to train
    comp1 = Computer()
    print('Welcome to the game of Nuts!')
    # the amount of nuts that the game will be played with
    nuts = init_table()
    while (True):

        user = printOptions()																							# ask the user for input

        if (user == 1):
            gameOfNuts(nuts)																							# plays against player
            # loops the game asking whether they want to play again
            while(playAgain()):
                gameOfNuts(nuts)

        elif (user == 2):
            # plays against an unskilled computer
            gameOfNuts(nuts, comp1)
            while (playAgain()):
                # loops the game whether they want to play again
                gameOfNuts(nuts, comp1)
        elif (user == 3):
            i = 100000
            comp2 = Computer()
            for x in range(i):
                print("[{}/{}]".format(x, i), "{:.3f}%".format((x / i) * 100))
                # trains the AI 100000 times against another computer
                train(nuts, comp1, comp2)

            # the user gets to play against the AI
            gameOfNuts(nuts, comp1)
            while (playAgain()):																						# loops the game whether they want to play again
                gameOfNuts(nuts, comp1)

        elif (user == 5):																								# prints table FOR DEBUGGING PERPOSES
            Computer.printTable(comp1)
        elif (user == 4):
            break																										# breaks out of the game
