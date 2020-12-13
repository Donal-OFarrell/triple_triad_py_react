from random import choice
# cards have 4 poles with values from 1 to 9 
class Card():   
    def __init__(self,card_id,north,east,south,west):
        self.card_id = card_id 
        self.north = north
        self.east= east
        self.south = south 
        self.west = west 
        self.blue_or_red = 'neutral' # initially cards are neither red nor blue
        self.compass_values={'north':north,'east':east,'south':south,'west':west}

    def get_colour(self):
        return self.blue_or_red 
    
    def set_colour(self,colour): 
        self.blue_or_red = colour

    def get_north(self):
        return self.north 

    # setters for poles for debugging only - to be removed once game functions 
    def set_north(self,north):
        self.north = north
        self.compass_values['north'] = north 

    def get_east(self):
        return self.east 

    def set_east(self,east):
        self.east = east
        self.compass_values['east'] = east 

    def get_south(self):
        return self.south

    def set_south(self,south):
        self.south = south
        self.compass_values['south'] = south

    def get_west(self):
        return self.west

    def set_west(self,west):
        self.west = west
        self.compass_values['west'] = west 

    def show_compass_values(self):
        print(self.compass_values)

    def return_compass_values(self):
        return self.compass_values 

    def card_power(self):
        ''' defines the power of a card by summing the poles '''
        return self.north + self.south + self.east + self.west 

class Player():
    '''Player class AKA Squall - (i.e. the player playing vs cpu)'''
    colour = 'blue'
    def __init__(self):
        self.inventory = [] 

    def get_player_colour(self):
        return self.colour

    def add_to_inventory(self,card):
        self.inventory.append(card)

    def get_inventory(self):
        return self.inventory


# deck class will generate the deck 
class Deck():
    num_cards = 10 # class variables 
    card_values=[1,2,3,4,5,6,7,8,9]
    cards=[]

    def __init__(self):
        for i in range(0,self.num_cards):
            self.cards.append(Card(i,choice(self.card_values),choice(self.card_values),choice(self.card_values),choice(self.card_values)))
        for i in range (len(self.cards)):
            if i % 2 == 0: # 5 cards of each colour? 
                self.cards[i].set_colour('blue')
            else:
                self.cards[i].set_colour('red')

    def deal_to_player(self,player): # pass player/AI object to the class
        for card in self.cards:
            if player.get_player_colour() == card.get_colour():
                player.add_to_inventory(card)




# card opposite filter 
# if a card is red, the opposite is blue etc 
#opposite_colour = {'blue':'red',
#                    'red':'blue'}


# each card can occupy a position on the board R1: 0,1,2  R2: 3,4,5  R3: 7,8,9
# board has become sort of a game class too - but the board's magic I guess :P 
class Board():
    board_spaces = 9 
    spaces_filled = 0 # when this equals above game is over 
    def __init__(self):
        self.positions = {'pos_0':['empty',self.pos_0_combat],'pos_1':['empty',self.pos_1_combat],'pos_2':['empty',self.pos_2_combat],
        'pos_3':['empty',self.pos_3_combat],'pos_4':['empty',self.pos_4_combat],'pos_5':['empty',self.pos_5_combat],
        'pos_6':['empty',self.pos_6_combat],'pos_7':['empty',self.pos_7_combat],'pos_8':['empty',self.pos_8_combat]}

    def accept_card(self,position,card):
        ''' card places into position - not very 'oopy' consider revision'''
        if self.positions[position][0] == 'empty':
            self.positions[position][0] = card # place card 
            
            self.positions[position][1]() # then invoke the combat method for that space 

            self.spaces_filled += 1 # increment board occupancy 
        else:
            print("This space is full, you can't place a card over another card")

    def get_positions(self):
        return self.positions

    def get_spaces_filled(self):
        return self.spaces_filled

    def state_of_board(self):
        ''' displays the baord in it's current state'''
        #print(self.positions)
        positions=self.positions

        keys = positions.keys()

        for key in keys:
            
            card = positions[key][0]
            if card == 'empty':
                print(key,card, end=" ")
            else:
                print(key, end=" ")
                card.show_compass_values()
            if key in ['pos_2','pos_5']:
                print()
    
    def ret_board_in_play(self):
        ''' returns dictionary structure with positions and their occupancies '''
        positions=self.positions

        board_dict = {}

        keys = positions.keys()

        for key in keys:
            card = positions[key][0]
            if card == 'empty':
                board_dict[key] = ['empty','no_values']
            else:
                board_dict[key] = [card,card.return_compass_values()]

        return board_dict 

        
        




        
    def pos_0_combat(self):
        ''' 0 fights 1 and 3 '''
        # fight 1 
        if self.positions['pos_1'][0] != 'empty': 
            if self.positions['pos_1'][0].get_colour() != self.positions['pos_0'][0].get_colour(): # then try to attack the card 
                if self.positions['pos_0'][0].get_west() > self.positions['pos_1'][0].get_east(): # if the number is bigger -> then flip the card 
        #  TO DO: create a pointer to array containing two colours - apply the opposite of attacking card
                    print("0 fighting 1")
                    self.positions['pos_1'][0].set_colour(self.positions['pos_0'][0].get_colour()) # flip the card to attacking cards colour 
                    print("0 flipped 1") # debug checks 
        # TO DO: adjust score for red/blue player 

        # fight 3 
        if self.positions['pos_3'][0] != 'empty':
            if self.positions['pos_3'][0].get_colour() != self.positions['pos_0'][0].get_colour(): 
                if self.positions['pos_0'][0].get_south() > self.positions['pos_3'][0].get_north():
                    print("0 fighting 3")
                    self.positions['pos_3'][0].set_colour(self.positions['pos_0'][0].get_colour()) # again opposite of placed card 
                    print("0 flipped 3") # to colour

    def pos_1_combat(self):
        ''' 1 fights 0, 4 and 2'''
        # fight 0
        if self.positions['pos_0'][0] != 'empty':
            if self.positions['pos_0'][0].get_colour() != self.positions['pos_1'][0].get_colour():
                if self.positions['pos_1'][0].get_west() > self.positions['pos_0'][0].get_east():
                    print("1 fighting 0")
                    self.positions['pos_0'][0].set_colour(self.positions['pos_1'][0].get_colour()) # flip the card to attacking cards colour 
                    print("1 flipped 0")
        # fight 2
        if self.positions['pos_2'][0] != 'empty':
            if self.positions['pos_2'][0].get_colour() != self.positions['pos_1'][0].get_colour():
                if self.positions['pos_1'][0].get_east() > self.positions['pos_2'][0].get_west():
                    print("1 fighting 2")
                    self.positions['pos_2'][0].set_colour(self.positions['pos_1'][0].get_colour()) # flip the card to attacking cards colour 
                    print("1 flipped 2")

        # fight 4 
        if self.positions['pos_4'][0] != 'empty':
            if self.positions['pos_4'][0].get_colour() != self.positions['pos_1'][0].get_colour():
                if self.positions['pos_1'][0].get_south() > self.positions['pos_4'][0].get_north():
                    print("1 fighting 4")
                    self.positions['pos_4'][0].set_colour(self.positions['pos_1'][0].get_colour()) # flip the card to attacking cards colour 
                    print("1 flipped 4")

    def pos_2_combat(self):
        ''' 2 fights 5 and 1'''
        # fight 1
        if self.positions['pos_1'][0] != 'empty':
            if self.positions['pos_1'][0].get_colour() != self.positions['pos_2'][0].get_colour():
                if self.positions['pos_2'][0].get_west() > self.positions['pos_1'][0].get_east(): 
                    print("2 fighting 1")
                    self.positions['pos_1'][0].set_colour(self.positions['pos_2'][0].get_colour()) # flip the card to attacking cards colour
                    print("2 flipped 1")
        # fight 5 
        if self.positions['pos_5'][0] != 'empty': 
            if self.positions['pos_5'][0].get_colour() != self.positions['pos_2'][0].get_colour():
                if self.positions['pos_2'][0].get_south() > self.positions['pos_5'][0].get_north():
                    print("2 fighting 5")
                    self.positions['pos_5'][0].set_colour(self.positions['pos_2'][0].get_colour()) # flip the card to attacking cards colour
                    print("2 flipped 5")

    def pos_3_combat(self):
        ''' 3 fights 0,4 and 6'''
        # fight 0 
        if self.positions['pos_0'][0] != 'empty':
            if self.positions['pos_0'][0].get_colour() != self.positions['pos_3'][0].get_colour():
                if self.positions['pos_3'][0].get_north() > self.positions['pos_0'][0].get_south():
                    print("3 fighting 0")
                    self.positions['pos_0'][0].set_colour(self.positions['pos_3'][0].get_colour()) # flip the card to attacking cards colour
                    print("3 flipped 0")

        #fight 4 
        if self.positions['pos_4'][0] != 'empty':
            if self.positions['pos_4'][0].get_colour() != self.positions['pos_3'][0].get_colour():
                if self.positions['pos_3'][0].get_east() > self.positions['pos_4'][0].get_west():
                    print("3 fighting 4")
                    self.positions['pos_4'][0].set_colour(self.positions['pos_3'][0].get_colour()) # flip the card to attacking cards colour
                    print("3 flipped 4")
        
        # fight 6 
        if self.positions['pos_6'][0] != 'empty':
            if self.positions['pos_6'][0].get_colour() != self.positions['pos_3'][0].get_colour():
                if self.positions['pos_3'][0].get_south() > self.positions['pos_6'][0].get_north():
                    print("3 fighting 6")
                    self.positions['pos_6'][0].set_colour(self.positions['pos_3'][0].get_colour()) # flip the card to attacking cards colour
                    print("3 flipped 6")

    def pos_4_combat(self):
        ''' 4 fights 1,3,5 and 7 '''
        # fight 1 
        if self.positions['pos_1'][0] != 'empty':
            if self.positions['pos_1'][0].get_colour() != self.positions['pos_4'][0].get_colour():
                if self.positions['pos_4'][0].get_north() > self.positions['pos_1'][0].get_south():
                    print("4 fighting 1")
                    self.positions['pos_1'][0].set_colour(self.positions['pos_4'][0].get_colour()) # flip the card to attacking cards colour
                    print("4 flipped 1")
        # fight 3 
        if self.positions['pos_3'][0] != 'empty':
            if self.positions['pos_3'][0].get_colour() != self.positions['pos_4'][0].get_colour():
                if self.positions['pos_4'][0].get_west() > self.positions['pos_3'][0].get_east():
                    print("4 fighting 3")
                    self.positions['pos_3'][0].set_colour(self.positions['pos_4'][0].get_colour()) # flip the card to attacking cards colour
                    print("4 flipped 3")

        # fight 5 
        if self.positions['pos_5'][0] != 'empty':
            if self.positions['pos_5'][0].get_colour() != self.positions['pos_4'][0].get_colour():
                if self.positions['pos_4'][0].get_east() > self.positions['pos_5'][0].get_west():
                    print("4 fighting 5")
                    self.positions['pos_5'][0].set_colour(self.positions['pos_4'][0].get_colour()) # flip the card to attacking cards colour
                    print("4 flipped 5")

        # fight 7 
        if self.positions['pos_7'][0] != 'empty':
            if self.positions['pos_7'][0].get_colour() != self.positions['pos_4'][0].get_colour():
                if self.positions['pos_4'][0].get_south() > self.positions['pos_7'][0].get_north():
                    print("4 fighting 7")
                    self.positions['pos_7'][0].set_colour(self.positions['pos_4'][0].get_colour()) # flip the card to attacking cards colour
                    print("4 flipped 7") 


    def pos_5_combat(self):
        ''' 5 fights 2,4 and 8 '''
        # fight 2 
        if self.positions['pos_2'][0] != 'empty':
            if self.positions['pos_2'][0].get_colour() != self.positions['pos_5'][0].get_colour():
                if self.positions['pos_5'][0].get_north() > self.positions['pos_2'][0].get_south():
                    print("5 fighting 2")
                    self.positions['pos_2'][0].set_colour(self.positions['pos_5'][0].get_colour()) # flip the card to attacking cards colour
                    print("5 flipped 2")
        
        # fight 4 
        if self.positions['pos_4'][0] != 'empty':
            if self.positions['pos_4'][0].get_colour() != self.positions['pos_5'][0].get_colour():
                if self.positions['pos_5'][0].get_west() > self.positions['pos_4'][0].get_east():
                    print("5 fighting 4")
                    self.positions['pos_4'][0].set_colour(self.positions['pos_5'][0].get_colour()) # flip the card to attacking cards colour
                    print("5 flipped 4")

        # fight 8 
        if self.positions['pos_8'][0] != 'empty':
            if self.positions['pos_8'][0].get_colour() != self.positions['pos_5'][0].get_colour():
                if self.positions['pos_5'][0].get_south() > self.positions['pos_4'][0].get_north():
                    print("5 fighting 8")
                    self.positions['pos_8'][0].set_colour(self.positions['pos_5'][0].get_colour()) # flip the card to attacking cards colour
                    print("5 flipped 8")

    def pos_6_combat(self):
        ''' 6 fights 3 and 7 '''
        # fight 3 
        if self.positions['pos_3'][0] != 'empty':
            if self.positions['pos_3'][0].get_colour() != self.positions['pos_6'][0].get_colour():
                if self.positions['pos_6'][0].get_north() > self.positions['pos_3'][0].get_south():
                    print("6 fighting 3")
                    self.positions['pos_3'][0].set_colour(self.positions['pos_6'][0].get_colour()) # flip the card to attacking cards colour
                    print("6 flipped 3")

        # fight 7 
        if self.positions['pos_7'][0] != 'empty':
            if self.positions['pos_7'][0].get_colour() != self.positions['pos_6'][0].get_colour():
                if self.positions['pos_6'][0].get_east() > self.positions['pos_7'][0].get_west():
                    print("6 fighting 7")
                    self.positions['pos_7'][0].set_colour(self.positions['pos_6'][0].get_colour()) # flip the card to attacking cards colour
                    print("6 flipped 7")

    def pos_7_combat(self):
        '''7 fights 6, 4 and 8 '''
        # fight 6 
        if self.positions['pos_6'][0] != 'empty':
            if self.positions['pos_6'][0].get_colour() != self.positions['pos_7'][0].get_colour():
                if self.positions['pos_7'][0].get_west() > self.positions['pos_6'][0].get_east():
                    print("7 fighting 6")
                    self.positions['pos_6'][0].set_colour(self.positions['pos_7'][0].get_colour()) # flip the card to attacking cards colour
                    print("7 flipped 6")
        # fight 4
        if self.positions['pos_4'][0] != 'empty':
            if self.positions['pos_4'][0].get_colour() != self.positions['pos_7'][0].get_colour():
                if self.positions['pos_7'][0].get_north() > self.positions['pos_4'][0].get_south():
                    print("7 fighting 4")
                    self.positions['pos_4'][0].set_colour(self.positions['pos_7'][0].get_colour()) # flip the card to attacking cards colour
                    print("7 flipped 4")

        # fight 8 
        if self.positions['pos_8'][0] != 'empty':
            if self.positions['pos_8'][0].get_colour() != self.positions['pos_7'][0].get_colour():
                if self.positions['pos_7'][0].get_east() > self.positions['pos_8'][0].get_west():
                    print("7 fighting 8")
                    self.positions['pos_8'][0].set_colour(self.positions['pos_7'][0].get_colour()) # flip the card to attacking cards colour
                    print("7 flipped 8")

    def pos_8_combat(self):
        '''8 fights 7 and 5 '''
        # fight 7 
        if self.positions['pos_7'][0] != 'empty':
            if self.positions['pos_7'][0].get_colour() != self.positions['pos_8'][0].get_colour():
                if self.positions['pos_8'][0].get_west() > self.positions['pos_7'][0].get_east():
                    print("8 fighting 7")
                    self.positions['pos_7'][0].set_colour(self.positions['pos_8'][0].get_colour()) # flip the card to attacking cards colour
                    print("8 flipped 7")
        
        # fight 5 
        if self.positions['pos_5'][0] != 'empty':
            if self.positions['pos_5'][0].get_colour() != self.positions['pos_8'][0].get_colour():
                if self.positions['pos_8'][0].get_north() > self.positions['pos_5'][0].get_south():
                    print("8 fighting 5")
                    self.positions['pos_5'][0].set_colour(self.positions['pos_8'][0].get_colour()) # flip the card to attacking cards colour
                    print("8 flipped 5")


class CPU():
    '''CPU class which play versus a player 
    we'll need a play_defense() method also
    for this need to have a score for the exposed edges'''
    colour = 'red'

    def __init__(self):
        self.inventory=[]
        self.attack_map= {'pos_0':self.pos_0_attack, 
                      'pos_1':self.pos_1_attack,
                      'pos_2':self.pos_2_attack,
                      'pos_3':self.pos_3_attack,
                      'pos_4':self.pos_4_attack,
                      'pos_5':self.pos_5_attack,
                      'pos_6':self.pos_6_attack,
                      'pos_7':self.pos_7_attack,
                      'pos_8':self.pos_8_attack}
        self.board_status = {}
        self.spaces_in_play={}
        self.occupied_spaces={}
        self.possible_moves = {} #{'pos_0':{inv_0:[card power as int,score as int]}}
        

    def add_to_inventory(self,card):
        self.inventory.append(card)

    def get_inventory(self):
        return self.inventory 

    def show_inventory(self):
        print (self.inventory)

    def get_player_colour(self):
        return self.colour

    def assess_board(self,board):
        self.board_status = board.ret_board_in_play()
        print()
        #print ("Printing board in play from CPU class")
        #print(self.board_status)



        # if the board is empty - play a defensive opener
        empty = board.get_spaces_filled()

        if empty == 0: # need to address this 
            print("Playing defensive card")
            # limit this to the 4 corners 

        for key,value in self.board_status.items():
            if value[1] == 'no_values':
                self.spaces_in_play[key] = value
            else:
                self.occupied_spaces[key] = value

        #print()
        print("Available spaces from CPU class")
        print(self.spaces_in_play)
        #print("Unavailable spaces from CPU class")
        #print(self.occupied_spaces)


    def make_move(self,board):
        ''' this is the CPU brain '''
        # needs to read state of board 
        self.assess_board(board)


        attack_options = self.spaces_in_play.keys()

        print("looping through attack options")
        for option in attack_options: 
            print()
            print(option)
            self.attack_map[option]()
            print("printing board status")
            print(self.board_status)


        # then here assess the possible moves and pick the best - ie produces flip with weakest card 
        print("printing possible moves")
        print(self.possible_moves)

        # if nothing play defensive 

    def pos_0_attack(self):
        ''' access board as attributes'''
        # need to loop through inventory
        # need a data strcuture to store possible moves 
        pos_0_checks={} # this will be added to self.possible_moves at the end of the method if not empty 
        
        for inv_card in self.inventory:
            three_check = False # if 3 has been checked in the initial execution body (bool=True) - don't check it again
            inv_card_power = inv_card.card_power() # assses cards power/score 
            inv_card_index = self.inventory.index(inv_card)# assign an index to card being assessed 
            # pos 1 check with double case 
            print("first check")
            if self.board_status['pos_1'][0] != 'empty':
                if self.board_status['pos_1'][0].get_colour() != inv_card.get_colour():
                    print("colour check passed")
                    if inv_card.get_east() > self.board_status['pos_1'][0].get_west():
                        print("0 versus 1 is a flip with ",inv_card_index)
                        # here we assign the value to possible_moves 
                        pos_0_checks[inv_card_index] = [inv_card_power,1] # how to increment score? 
                        # another if statement here for the double case? 
                        if self.board_status['pos_3'][0] != 'empty':
                            print("nested boolean")
                            three_check = True
                            if self.board_status['pos_3'][0].get_colour() != inv_card.get_colour(): 
                                if inv_card.get_south() > self.board_status['pos_3'][0].get_north():
                                    print("Double case for pos 0 with ", inv_card_index)
                                    pos_0_checks[inv_card_index] = [inv_card_power,2]
                                    
            # then a solitary check here for pos 3 check
            if self.board_status['pos_3'][0] != 'empty' and three_check == False: # if the double check has taken place don't run this
                if self.board_status['pos_3'][0].get_colour() != inv_card.get_colour(): 
                    if inv_card.get_south() > self.board_status['pos_3'][0].get_north():
                        print("0 versus 3 is a flip with ", inv_card_index)
                        pos_0_checks[inv_card_index] = [inv_card_power,1] 

        self.possible_moves['pos_0'] = pos_0_checks
        print("checking possible moves")
        print(self.possible_moves)

    def pos_1_attack(self):
        '''AI actions for pos_1 
        fights 0,2 and 4'''
        pos_1_checks={}
        for inv_card in self.inventory:
            inv_card_power = inv_card.card_power() # assses cards power/score
            inv_card_index = self.inventory.index(inv_card)# assign an index to card being assessed 
            four_check = False # control boolean to prevent repeat checks on position 4 
            two_check = False # control boolean to prevent repeat checks on position 2

            # pos 0 check 
            if self.board_status['pos_0'][0] != 'empty': # card present 
                if self.board_status['pos_0'][0].get_colour() != inv_card.get_colour(): # colour is opposite - fight! 
                    if inv_card.get_west() > self.board_status['pos_0'][0].get_east():
                        print("1 versus 0 is a flip with ",inv_card_index)
                        # here we assign the value to possible_moves 
                        pos_1_checks[inv_card_index] = [inv_card_power,1]
                        # another if statement here for the double case for pos 4 

                        # pos 4 - double check
                        print("first 4 check on double")
                        print()
                        if self.board_status['pos_4'][0] != 'empty': # card present
                            four_check = True
                            print("initial 4 check not empty passed")
                            print(self.board_status['pos_4'][0].get_colour())
                            print(inv_card.get_colour())
                            if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour(): 
                                print("colour checks passed")
                                if inv_card.get_south() > self.board_status['pos_4'][0].get_north():
                                    # here we assign the value to possible_moves 
                                    print("1 versus 4 is a double flip with ",inv_card_index)
                                    pos_1_checks[inv_card_index] = [inv_card_power,2]
                                    
                                    # another if statement here for the triple case?
                                    print("triple case")
                                    if self.board_status['pos_2'][0] != 'empty' and two_check == False: # card present
                                        two_check = True
                                        if self.board_status['pos_2'][0].get_colour() != inv_card.get_colour():
                                            if inv_card.get_east() > self.board_status['pos_2'][0].get_east():
                                                # here we assign the value to possible_moves 
                                                print("1 versus 2 is a triple flip with ",inv_card_index)
                                                pos_1_checks[inv_card_index] = [inv_card_power,3]

                        # pos 2 alternate double check
                        if self.board_status['pos_2'][0] != 'empty' and two_check==False: # card present
                            two_check = True 
                            if self.board_status['pos_2'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_east() > self.board_status['pos_2'][0].get_east():
                                    # here we assign the value to possible_moves 
                                    print("solo 1 versus 2 is a double flip with ",inv_card_index)
                                    pos_1_checks[inv_card_index] = [inv_card_power,2]

            # pos 4 check
            if self.board_status['pos_4'][0] != 'empty' and four_check==False: # card present
                four_check=True
                if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour(): 
                    if inv_card.get_south() > self.board_status['pos_4'][0].get_north():
                        # here we assign the value to possible_moves 
                        print("1 versus 4 is a double flip with ",inv_card_index)
                        pos_1_checks[inv_card_index] = [inv_card_power,1]

                        if self.board_status['pos_2'][0] != 'empty' and two_check==False: # card present
                            two_check = True 
                            if self.board_status['pos_2'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_east() > self.board_status['pos_2'][0].get_east():
                                    # here we assign the value to possible_moves 
                                    print("1 versus 2 is a double flip with ",inv_card_index)
                                    pos_1_checks[inv_card_index] = [inv_card_power,2]

            # pos 2 check 
            if self.board_status['pos_2'][0] != 'empty' and two_check==False: # card present 
                if self.board_status['pos_2'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_east() > self.board_status['pos_2'][0].get_east():
                        # here we assign the value to possible_moves 
                        print("1 versus 2 is a double flip with ",inv_card_index)
                        pos_1_checks[inv_card_index] = [inv_card_power,1]
        
        self.possible_moves['pos_1'] = pos_1_checks
        print("checking possible moves")
        print(self.possible_moves)

    def pos_2_attack(self):
        ''' position 2 attack assessment method
        in this case pos 2 will fight pos 1 and pos 5'''
        pos_2_checks = {} # define dictionary which will contain potential attacks for each card
        
        for inv_card in self.inventory: 
            five_check = False # bool to not repeat 5 checks in a double scoring situation 
            inv_card_power = inv_card.card_power() # assses cards power/score
            inv_card_index = self.inventory.index(inv_card)# assign an index to card being assessed 
            # pos 1 check 
            if self.board_status['pos_1'][0] != 'empty': # card present 
                if self.board_status['pos_1'][0].get_colour() != inv_card.get_colour(): 
                    if inv_card.get_west() > self.board_status['pos_1'][0].get_east():
                        # here we assign the value to possible_moves 
                        print("2 versus 1 is a flip with ",inv_card_index)
                        pos_2_checks[inv_card_index] = [inv_card_power,1]

                        # double check for pos 5 
                        if self.board_status['pos_5'][0] != 'empty': # card present
                            five_check = True # don't check again 
                            if self.board_status['pos_5'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_south() > self.board_status['pos_5'][0].get_north():
                                    print("2 versus 5 is a double flip with ",inv_card_index)
                                    pos_2_checks[inv_card_index] = [inv_card_power,2]

            # pos 5 check 
            if self.board_status['pos_5'][0] != 'empty' and five_check == False: # card present and not been checked already
                    if self.board_status['pos_5'][0] != 'empty': # card present 
                        if self.board_status['pos_5'][0].get_colour() != inv_card.get_colour():
                            if inv_card.get_south() > self.board_status['pos_5'][0].get_north():
                                print("2 versus 5 is a double flip with ",inv_card_index)
                                pos_2_checks[inv_card_index] = [inv_card_power,1]

        self.possible_moves['pos_2'] = pos_2_checks # add the checks to the possible_moves attribute 

    def pos_3_attack(self):
        ''' pos 3 will attack 0,4 and 6 '''
        pos_3_checks={}
        for inv_card in self.inventory:
            inv_card_power = inv_card.card_power() # assses cards power/score
            inv_card_index = self.inventory.index(inv_card)# assign an index to card being assessed 
            four_check = False
            six_check = False

            # pos 0 check 
            if self.board_status['pos_0'][0] != 'empty': # card present 
                if self.board_status['pos_0'][0].get_colour() != inv_card.get_colour(): # colour is opposite - fight! 
                    if inv_card.get_north() > self.board_status['pos_0'][0].get_south():
                        print("3 versus 0 is a flip with ",inv_card_index)
                        # here we assign the value to possible_moves 
                        pos_3_checks[inv_card_index] = [inv_card_power,1]
                        # another if statement here for the double case for pos 4 

                        # pos 4 - double check
                        print("first 4 check on double")
                        print()
                        if self.board_status['pos_4'][0] != 'empty': # card present
                            four_check = True
                            print("initial 4 check not empty passed")
                            if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour(): 
                                if inv_card.get_east() > self.board_status['pos_4'][0].get_west():
                                    # here we assign the value to possible_moves 
                                    print("3 versus 4 is a double flip with ",inv_card_index)
                                    pos_3_checks[inv_card_index] = [inv_card_power,2]
                                    
                                    # another if statement here for the triple case?
                                    print("triple case")
                                    if self.board_status['pos_6'][0] != 'empty' and six_check == False: # card present
                                        two_check = True
                                        if self.board_status['pos_6'][0].get_colour() != inv_card.get_colour():
                                            if inv_card.get_south() > self.board_status['pos_6'][0].get_north():
                                                # here we assign the value to possible_moves 
                                                print("1 versus 2 is a triple flip with ",inv_card_index)
                                                pos_3_checks[inv_card_index] = [inv_card_power,3]


            # pos 4 check
            if self.board_status['pos_4'][0] != 'empty' and four_check==False: # card present
                if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour(): 
                    if inv_card.get_east() > self.board_status['pos_4'][0].get_west():
                        # here we assign the value to possible_moves 
                        print("3 versus 4 is a flip with ",inv_card_index)
                        pos_3_checks[inv_card_index] = [inv_card_power,1]

                        if self.board_status['pos_6'][0] != 'empty' and six_check==False: # card present
                            six_check = True 
                            if self.board_status['pos_6'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_south() > self.board_status['pos_6'][0].get_north():
                                    # here we assign the value to possible_moves 
                                    print("3 versus 6 is a double flip with ",inv_card_index)
                                    pos_1_checks[inv_card_index] = [inv_card_power,2]

            # pos 6 check 
            if self.board_status['pos_6'][0] != 'empty' and six_check==False: # card present 
                if self.board_status['pos_6'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_south() > self.board_status['pos_6'][0].get_north():
                        # here we assign the value to possible_moves 
                        print("3 versus 6 is a flip with ",inv_card_index)
                        pos_3_checks[inv_card_index] = [inv_card_power,1]

        self.possible_moves['pos_3'] = pos_3_checks
        print("checking possible moves")
        print(self.possible_moves)

            
    def pos_4_attack(self):
        ''' this might be tricky -
        4 positions to attack - 
        1,3,5 and 7 '''
        pos_4_checks={}

        for inv_card in self.inventory:
            three_check = False
            five_check= False
            seven_check= False
            inv_card_power = inv_card.card_power() # assses cards power/score
            inv_card_index = self.inventory.index(inv_card)# assign an index to card being assessed

            # pos 1 check 
            if self.board_status['pos_1'][0] != 'empty': # card present
                if self.board_status['pos_1'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_north() > self.board_status['pos_1'][0].get_south():
                        print("4 versus 1 is a flip with ",inv_card_index)
                        pos_4_checks[inv_card_index] = [inv_card_power,1]

                        # check for nested double case pos 3 
                        if self.board_status['pos_3'][0] != 'empty': # card present
                            three_check = True
                            if self.board_status['pos_3'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_west() > self.board_status['pos_3'][0].get_east():
                                    print("4 versus 3 is a double flip with ",inv_card_index)
                                    pos_4_checks[inv_card_index] = [inv_card_power,2]

                                    # check for triple nested for pos 5 
                                    if self.board_status['pos_5'][0] != 'empty': # card present 
                                        five_check = True
                                        if self.board_status['pos_5'][0].get_colour() != inv_card.get_colour():
                                            if inv_card.get_west() > self.board_status['pos_5'][0].get_east():
                                                print("4 versus 5 is a triple flip with ",inv_card_index)
                                                pos_4_checks[inv_card_index] = [inv_card_power,3]

                                                # check for quadruple nested for pos 7
                                                if self.board_status['pos_7'][0] != 'empty': # card present
                                                    seven_check = True
                                                    if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                                                        if inv_card.get_south() > self.board_status['pos_7'][0].get_north():
                                                            print("4 versus 7 is a quadruple flip with ",inv_card_index)
                                                            pos_4_checks[inv_card_index] = [inv_card_power,4]

            # pos 3 check
            if self.board_status['pos_3'][0] != 'empty' and three_check == False: # card present
                three_check = True
                if self.board_status['pos_3'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_west() > self.board_status['pos_3'][0].get_east():
                        print("4 versus 3 is a single flip with ",inv_card_index)
                        pos_4_checks[inv_card_index] = [inv_card_power,1]

                        # check for nested double for pos 5 
                        if self.board_status['pos_5'][0] != 'empty' and five_check == False: # card present
                            five_check = True
                            if self.board_status['pos_5'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_east() > self.board_status['pos_5'][0].get_west():
                                    print("4 versus 5 is a double flip with ",inv_card_index)
                                    pos_4_checks[inv_card_index] = [inv_card_power,2]

                                    # check for nested triple with position 7 
                                    if self.board_status['pos_7'][0] != 'empty' and seven_check == False: # card present
                                        seven_check = True
                                        if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                                            if inv_card.get_south() > self.board_status['pos_7'][0].get_north():
                                                print("4 versus 7 is a triple flip with ",inv_card_index)
                                                pos_4_checks[inv_card_index] = [inv_card_power,3] 


            # pos 5 check 
            if self.board_status['pos_5'][0] != 'empty' and five_check == False: # card present  
                five_check = True
                if self.board_status['pos_5'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_east() > self.board_status['pos_5'][0].get_west():
                        print("4 versus 5 is a single flip with ",inv_card_index)
                        pos_4_checks[inv_card_index] = [inv_card_power,1]

                        # nested check for double for pos 7 

                        if self.board_status['pos_7'][0] != 'empty' and seven_check == False: # card present
                            seven_check = True
                            if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_south() > self.board_status['pos_7'][0].get_north():
                                    print("4 versus 7 is a double flip with ",inv_card_index)
                                    pos_4_checks[inv_card_index] = [inv_card_power,2] 

            # pos 7 check
            if self.board_status['pos_7'][0] != 'empty' and seven_check == False: # card present 
                if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_south() > self.board_status['pos_7'][0].get_north():
                        print("4 versus 7 is a single flip with ",inv_card_index)
                        pos_4_checks[inv_card_index] = [inv_card_power,1]

        self.possible_moves['pos_4'] = pos_4_checks
        print("checking possible moves")
        print(self.possible_moves)

    def pos_5_attack(self):
        ''' 5 attackes 2,4 and 8'''
        pos_5_checks = {}

        for inv_card in self.inventory:
            four_check = False
            eight_check= False
            inv_card_power = inv_card.card_power() # assses cards power/score
            inv_card_index = self.inventory.index(inv_card)# assign an index to card being assessed

            # pos 2 check
            if self.board_status['pos_2'][0] != 'empty': # card present
                if self.board_status['pos_2'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_north() > self.board_status['pos_2'][0].get_south():
                        print("5 versus 2 is a single flip with ",inv_card_index)
                        pos_5_checks[inv_card_index] = [inv_card_power,1]

                        # nested double case for 4
                        if self.board_status['pos_4'][0] != 'empty': # card present
                            four_check = True 
                            if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_west() > self.board_status['pos_4'][0].get_east():
                                    print("5 versus 4 is a double flip with ",inv_card_index)
                                    pos_5_checks[inv_card_index] = [inv_card_power,2]

                                    # nested triple case for 8
                                    if self.board_status['pos_8'][0] != 'empty': # card present 
                                        eight_check = True
                                        if self.board_status['pos_8'][0].get_colour() != inv_card.get_colour():
                                            if inv_card.get_south() > self.board_status['pos_8'][0].get_north():
                                                print("5 versus 8 is a triple flip with ",inv_card_index)
                                                pos_5_checks[inv_card_index] = [inv_card_power,3]

            # pos 4 check
            if self.board_status['pos_4'][0] != 'empty' and four_check == False: # card present
                four_check = True 
                if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_west() > self.board_status['pos_4'][0].get_east():
                        print("5 versus 4 is a single flip with ",inv_card_index)
                        pos_5_checks[inv_card_index] = [inv_card_power,1]

                        # double check for pos 8
                        if self.board_status['pos_8'][0] != 'empty' and eight_check == False:
                            eight_check = True
                            if self.board_status['pos_8'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_south() > self.board_status['pos_8'][0].get_north():
                                    print("5 versus 8 is a double flip with ",inv_card_index)
                                    pos_5_checks[inv_card_index] = [inv_card_power,2]

            # pos 8 check 
            if self.board_status['pos_8'][0] != 'empty' and eight_check == False: # card present
                if self.board_status['pos_8'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_south() > self.board_status['pos_8'][0].get_north():
                        print("5 versus 8 is a single flip with ",inv_card_index)
                        pos_5_checks[inv_card_index] = [inv_card_power,1]

        self.possible_moves['pos_5'] = pos_5_checks
        print("checking possible moves")
        print(self.possible_moves)


    def pos_6_attack(self):
        ''' 6 attacks 3 and 7'''
        pos_6_checks={}
        for inv_card in self.inventory:
            seven_check = False
            inv_card_power = inv_card.card_power() # assses cards power/score
            inv_card_index = self.inventory.index(inv_card)# assign an index to card being assessed

            # pos 3 check
            if self.board_status['pos_3'][0] != 'empty':
                if self.board_status['pos_3'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_north() > self.board_status['pos_3'][0].get_south():
                        print("6 versus 3 is a single flip with ",inv_card_index)
                        pos_6_checks[inv_card_index] = [inv_card_power,1]

                        # check for nested double case for pos 7
                        if self.board_status['pos_7'][0] != 'empty': 
                            seven_check = True
                            if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_east() > self.board_status['pos_7'][0].get_west():
                                    print("6 versus 7 is a double flip with ",inv_card_index)
                                    pos_6_checks[inv_card_index] = [inv_card_power,2]

            # pos 7 check
            if self.board_status['pos_7'][0] != 'empty' and seven_check == False:
                print("checks")
                print(self.board_status['pos_7'][0],inv_card.get_colour()) 
                if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_east() > self.board_status['pos_7'][0].get_west():
                        print("6 versus 7 is a single flip with ",inv_card_index)
                        pos_6_checks[inv_card_index] = [inv_card_power,1]
        
        self.possible_moves['pos_6'] = pos_6_checks
        print("checking possible moves")
        print(self.possible_moves)

    def pos_7_attack(self):
        ''' 7 attacks 6, 4 and 8 '''
        pos_7_checks = {}
        for inv_card in self.inventory:
            four_check = False
            eight_check = False
            inv_card_power = inv_card.card_power() # assses cards power/score
            inv_card_index = self.inventory.index(inv_card)# assign an index to card being assessed

            # pos 6 check 
            if self.board_status['pos_6'][0] != 'empty':
                if self.board_status['pos_6'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_west() > self.board_status['pos_6'][0].get_east():
                        print("7 versus 6 is a single flip with ",inv_card_index)
                        pos_7_checks[inv_card_index] = [inv_card_power,1]

                        # nested case for double at pos 4 
                        if self.board_status['pos_4'][0] != 'empty':
                            four_check= True
                            if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_north() > self.board_status['pos_4'][0].get_south():
                                    print("7 versus 4 is a double flip with ",inv_card_index)
                                    pos_7_checks[inv_card_index] = [inv_card_power,2]

                                    # nested triple case at pos 8 
                                    if self.board_status['pos_8'][0] != 'empty':
                                        eight_check = True
                                        if self.board_status['pos_8'][0].get_colour() != inv_card.get_colour():
                                            if inv_card.get_east() > self.board_status['pos_8'][0].get_west():
                                                print("7 versus 8 is a triple flip with ",inv_card_index)
                                                pos_7_checks[inv_card_index] = [inv_card_power,3]

            # pos 4 check 
            if self.board_status['pos_4'][0] != 'empty' and four_check == False:
                four_check= True
                if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_north() > self.board_status['pos_4'][0].get_south():
                        print("7 versus 4 is a single flip with ",inv_card_index)
                        pos_7_checks[inv_card_index] = [inv_card_power,1]

                        # nested double case for pos 8
                        if self.board_status['pos_8'][0] != 'empty':
                            eight_check = True
                            if self.board_status['pos_8'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_east() > self.board_status['pos_8'][0].get_west():
                                    print("7 versus 8 is a double flip with ",inv_card_index)
                                    pos_7_checks[inv_card_index] = [inv_card_power,2] 

            # pos 8 check 
            if self.board_status['pos_8'][0] != 'empty' and eight_check == False:  
                print("pos 7 attack, pos 8 check")
                print(self.board_status['pos_8'][0].get_colour())

                if self.board_status['pos_8'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_east() > self.board_status['pos_8'][0].get_west():
                        print("7 versus 8 is a double flip with ",inv_card_index)
                        pos_7_checks[inv_card_index] = [inv_card_power,2] 

        self.possible_moves['pos_7'] = pos_7_checks
        print("checking possible moves")
        print(self.possible_moves)

    def pos_8_attack(self):
        ''' 8 attacks 5 and 7'''
        pos_8_checks={}

        for inv_card in self.inventory:
            seven_check = False
            inv_card_power = inv_card.card_power() # assses cards power/score
            inv_card_index = self.inventory.index(inv_card)# assign an index to card being assessed

            # pos 5 check
            if self.board_status['pos_5'][0] != 'empty': 
                if self.board_status['pos_5'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_north() > self.board_status['pos_5'][0].get_south():
                        print("8 versus 5 is a single flip with ",inv_card_index)
                        pos_8_checks[inv_card_index] = [inv_card_power,1]

                        # nested double case for pos 7
                        if self.board_status['pos_7'][0] != 'empty':
                            seven_check = True
                            if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_west() > self.board_status['pos_7'][0].get_east():
                                    print("8 versus 7 is a double flip with ",inv_card_index)
                                    pos_8_checks[inv_card_index] = [inv_card_power,2]

            # pos 7 check 
            if self.board_status['pos_7'][0] != 'empty' and seven_check == False:
                seven_check == True
                if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_west() > self.board_status['pos_7'][0].get_east():
                        print("8 versus 7 is a single flip with ",inv_card_index)
                        pos_8_checks[inv_card_index] = [inv_card_power,1]
        self.possible_moves['pos_8'] = pos_8_checks
        print("checking possible moves")
        print(self.possible_moves)

    


# tests 

# check if deck builds and we have alternating colours - yes 
deck_test = Deck()


# define some players 
blue_player = Player()
red_player = CPU()

deck_test.deal_to_player(blue_player)
deck_test.deal_to_player(red_player)

#for card in blue_player.inventory:
#    print(card.get_colour())
#    card.show_compass_values()

#for card in red_player.inventory:
#    print(card.get_colour()) # colours correct
#    card.show_compass_values() # shows cards values on the poles 

# test if our attack method works? 

# initalise board 
board = Board()


# checks - max out blue card stats - minimise red card stats and test all combat
# max out the attacking poles stats 
print("Blue card before")
blue_player.inventory[0].show_compass_values()
blue_player.inventory[0].set_west(1)
blue_player.inventory[0].set_south(1)
blue_player.inventory[0].set_north(1)
blue_player.inventory[0].set_east(1)
print("Blue card after")
blue_player.inventory[0].show_compass_values()

blue_player.inventory[1].set_west(1)
blue_player.inventory[1].set_south(1)
blue_player.inventory[1].set_north(1)
blue_player.inventory[1].set_east(1)

blue_player.inventory[2].set_west(1)
blue_player.inventory[2].set_south(1)
blue_player.inventory[2].set_north(1)
blue_player.inventory[2].set_east(1)

blue_player.inventory[3].set_west(1)
blue_player.inventory[3].set_south(1)
blue_player.inventory[3].set_north(1)
blue_player.inventory[3].set_east(1)

blue_player.inventory[4].set_west(1)
blue_player.inventory[4].set_south(1)
blue_player.inventory[4].set_north(1)
blue_player.inventory[4].set_east(1)


# red card - these should be defeated by blue - minimise stats for debugging 
print("red before")
red_player.inventory[1].show_compass_values()
red_player.inventory[1].set_east(9)
red_player.inventory[1].set_north(9)
red_player.inventory[1].set_south(9)
red_player.inventory[1].set_west(9)

print("red after")
red_player.inventory[1].show_compass_values()

red_player.inventory[0].set_east(9)
red_player.inventory[0].set_north(9)
red_player.inventory[0].set_south(9)
red_player.inventory[0].set_west(9)

red_player.inventory[2].set_east(9)
red_player.inventory[2].set_north(9)
red_player.inventory[2].set_south(9)
red_player.inventory[2].set_west(9)

red_player.inventory[3].set_east(9)
red_player.inventory[3].set_north(9)
red_player.inventory[3].set_south(9)
red_player.inventory[3].set_west(9)

red_player.inventory[4].set_east(9)
red_player.inventory[4].set_north(9)
red_player.inventory[4].set_south(9)
red_player.inventory[4].set_west(9)



board.accept_card('pos_7',blue_player.inventory[0])


board.state_of_board()

print(board.ret_board_in_play())

red_player.make_move(board)

