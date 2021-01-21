import pprint

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
    def __init__(self,board):
        self.inventory = [] 
        self.board = board 

    def play_card(self,position,card,card_index):
        ''' Plays a card for the player.
        Complies with the board rules by invoking board.accept_card().
        After a card id played it is removed from the players inventory. '''
        self.board.accept_card(position,card) # play the card 
        self.inventory.pop(card_index) # remove this card from the Players inventory 


    def get_player_colour(self):
        return self.colour

    def show_inventory(self):
        for card in self.inventory:
            card.show_compass_values()

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



# each card can occupy a position on the board R1: 0,1,2  R2: 3,4,5  R3: 7,8,9
# board has become sort of a game class too - but the board's magic I guess :P 
class Board():
    board_spaces = 9 
    spaces_filled = 0 # when this equals above game is over 

    def __init__(self):
        self.positions = {'pos_0':['empty',self.pos_0_combat],'pos_1':['empty',self.pos_1_combat],'pos_2':['empty',self.pos_2_combat],
        'pos_3':['empty',self.pos_3_combat],'pos_4':['empty',self.pos_4_combat],'pos_5':['empty',self.pos_5_combat],
        'pos_6':['empty',self.pos_6_combat],'pos_7':['empty',self.pos_7_combat],'pos_8':['empty',self.pos_8_combat]}
        self.blue_score = 5
        self.red_score = 5
        

    def adjust_scores(self,winning_colour):
        print("---------------------reached adjust_scores")
        print(winning_colour)
        if winning_colour == 'blue':

            self.blue_score = self.blue_score + 1
            self.red_score = self.red_score - 1

        elif winning_colour == 'red':

            self.red_score = self.red_score + 1
            self.blue_score = self.blue_score - 1





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
        ''' displays the board in it's current state'''
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
                board_dict[key] = [card,card.return_compass_values(),card.get_colour()]

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
                    
                    # carry out score changes 
                    print("winning_colour", self.positions['pos_0'][0].get_colour())
                    self.adjust_scores(self.positions['pos_0'][0].get_colour())

                    print("0 flipped 1") # debug checks 
        # TO DO: adjust score for red/blue player 

        # fight 3 
        if self.positions['pos_3'][0] != 'empty':
            if self.positions['pos_3'][0].get_colour() != self.positions['pos_0'][0].get_colour(): 
                if self.positions['pos_0'][0].get_south() > self.positions['pos_3'][0].get_north():
                    print("0 fighting 3")
                    self.positions['pos_3'][0].set_colour(self.positions['pos_0'][0].get_colour()) # again opposite of placed card 

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_0'][0].get_colour())
                    self.adjust_scores(self.positions['pos_0'][0].get_colour())


                    print("0 flipped 3") # to colour

    def pos_1_combat(self):
        ''' 1 fights 0, 4 and 2'''
        # fight 0
        if self.positions['pos_0'][0] != 'empty':
            if self.positions['pos_0'][0].get_colour() != self.positions['pos_1'][0].get_colour():
                if self.positions['pos_1'][0].get_west() > self.positions['pos_0'][0].get_east():
                    
                    print("1 fighting 0")
                    self.positions['pos_0'][0].set_colour(self.positions['pos_1'][0].get_colour()) # flip the card to attacking cards colour
                    # carry out score changes 
                    print("winning_colour", self.positions['pos_1'][0].get_colour())
                    self.adjust_scores(self.positions['pos_1'][0].get_colour()) 


                    print("1 flipped 0")
        # fight 2
        if self.positions['pos_2'][0] != 'empty':
            if self.positions['pos_2'][0].get_colour() != self.positions['pos_1'][0].get_colour():
                if self.positions['pos_1'][0].get_east() > self.positions['pos_2'][0].get_west():
                    print("1 fighting 2")
                    self.positions['pos_2'][0].set_colour(self.positions['pos_1'][0].get_colour()) # flip the card to attacking cards colour

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_1'][0].get_colour())
                    self.adjust_scores(self.positions['pos_1'][0].get_colour())



                    print("1 flipped 2")

        # fight 4 
        if self.positions['pos_4'][0] != 'empty':
            if self.positions['pos_4'][0].get_colour() != self.positions['pos_1'][0].get_colour():
                if self.positions['pos_1'][0].get_south() > self.positions['pos_4'][0].get_north():
                    print("1 fighting 4")
                    self.positions['pos_4'][0].set_colour(self.positions['pos_1'][0].get_colour()) # flip the card to attacking cards colour 
                    
                    # carry out score changes 
                    print("winning_colour", self.positions['pos_1'][0].get_colour())
                    self.adjust_scores(self.positions['pos_1'][0].get_colour())

                    
                    print("1 flipped 4")

    def pos_2_combat(self):
        ''' 2 fights 5 and 1'''
        # fight 1
        if self.positions['pos_1'][0] != 'empty':
            if self.positions['pos_1'][0].get_colour() != self.positions['pos_2'][0].get_colour():
                if self.positions['pos_2'][0].get_west() > self.positions['pos_1'][0].get_east(): 
                    print("2 fighting 1")
                    self.positions['pos_1'][0].set_colour(self.positions['pos_2'][0].get_colour()) # flip the card to attacking cards colour
                    
                    # carry out score changes 
                    print("winning_colour", self.positions['pos_2'][0].get_colour())
                    self.adjust_scores(self.positions['pos_2'][0].get_colour())


                    print("2 flipped 1")
        # fight 5 
        if self.positions['pos_5'][0] != 'empty': 
            if self.positions['pos_5'][0].get_colour() != self.positions['pos_2'][0].get_colour():
                if self.positions['pos_2'][0].get_south() > self.positions['pos_5'][0].get_north():
                    print("2 fighting 5")
                    self.positions['pos_5'][0].set_colour(self.positions['pos_2'][0].get_colour()) # flip the card to attacking cards colour
                    # carry out score changes 
                    print("winning_colour", self.positions['pos_2'][0].get_colour())
                    self.adjust_scores(self.positions['pos_2'][0].get_colour())                   


                    print("2 flipped 5")

    def pos_3_combat(self):
        ''' 3 fights 0,4 and 6'''
        # fight 0 
        if self.positions['pos_0'][0] != 'empty':
            if self.positions['pos_0'][0].get_colour() != self.positions['pos_3'][0].get_colour():
                if self.positions['pos_3'][0].get_north() > self.positions['pos_0'][0].get_south():
                    print("3 fighting 0")
                    self.positions['pos_0'][0].set_colour(self.positions['pos_3'][0].get_colour()) # flip the card to attacking cards colour
                    # carry out score changes 
                    print("winning_colour", self.positions['pos_3'][0].get_colour())
                    self.adjust_scores(self.positions['pos_3'][0].get_colour())


                    print("3 flipped 0")

        #fight 4 
        if self.positions['pos_4'][0] != 'empty':
            if self.positions['pos_4'][0].get_colour() != self.positions['pos_3'][0].get_colour():
                if self.positions['pos_3'][0].get_east() > self.positions['pos_4'][0].get_west():
                    print("3 fighting 4")
                    self.positions['pos_4'][0].set_colour(self.positions['pos_3'][0].get_colour()) # flip the card to attacking cards colour
                    # carry out score changes 
                    print("winning_colour", self.positions['pos_3'][0].get_colour())
                    self.adjust_scores(self.positions['pos_3'][0].get_colour())


                    print("3 flipped 4")
        
        # fight 6 
        if self.positions['pos_6'][0] != 'empty':
            if self.positions['pos_6'][0].get_colour() != self.positions['pos_3'][0].get_colour():
                if self.positions['pos_3'][0].get_south() > self.positions['pos_6'][0].get_north():
                    print("3 fighting 6")
                    self.positions['pos_6'][0].set_colour(self.positions['pos_3'][0].get_colour()) # flip the card to attacking cards colour

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_3'][0].get_colour())
                    self.adjust_scores(self.positions['pos_3'][0].get_colour())


                    print("3 flipped 6")

    def pos_4_combat(self):
        ''' 4 fights 1,3,5 and 7 '''
        # fight 1 
        if self.positions['pos_1'][0] != 'empty':
            if self.positions['pos_1'][0].get_colour() != self.positions['pos_4'][0].get_colour():
                if self.positions['pos_4'][0].get_north() > self.positions['pos_1'][0].get_south():
                    print("4 fighting 1")
                    self.positions['pos_1'][0].set_colour(self.positions['pos_4'][0].get_colour()) # flip the card to attacking cards colour

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_4'][0].get_colour())
                    self.adjust_scores(self.positions['pos_4'][0].get_colour())


                    print("4 flipped 1")
        # fight 3 
        if self.positions['pos_3'][0] != 'empty':
            if self.positions['pos_3'][0].get_colour() != self.positions['pos_4'][0].get_colour():
                if self.positions['pos_4'][0].get_west() > self.positions['pos_3'][0].get_east():
                    print("4 fighting 3")
                    self.positions['pos_3'][0].set_colour(self.positions['pos_4'][0].get_colour()) # flip the card to attacking cards colour

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_4'][0].get_colour())
                    self.adjust_scores(self.positions['pos_4'][0].get_colour())                    


                    print("4 flipped 3")

        # fight 5 
        if self.positions['pos_5'][0] != 'empty':
            if self.positions['pos_5'][0].get_colour() != self.positions['pos_4'][0].get_colour():
                if self.positions['pos_4'][0].get_east() > self.positions['pos_5'][0].get_west():
                    print("4 fighting 5")
                    self.positions['pos_5'][0].set_colour(self.positions['pos_4'][0].get_colour()) # flip the card to attacking cards colour

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_4'][0].get_colour())
                    self.adjust_scores(self.positions['pos_4'][0].get_colour())


                    print("4 flipped 5")

        # fight 7 
        if self.positions['pos_7'][0] != 'empty':
            if self.positions['pos_7'][0].get_colour() != self.positions['pos_4'][0].get_colour():
                if self.positions['pos_4'][0].get_south() > self.positions['pos_7'][0].get_north():
                    print("4 fighting 7")
                    self.positions['pos_7'][0].set_colour(self.positions['pos_4'][0].get_colour()) # flip the card to attacking cards colour
                    # carry out score changes 
                    print("winning_colour", self.positions['pos_4'][0].get_colour())
                    self.adjust_scores(self.positions['pos_4'][0].get_colour())


                    print("4 flipped 7") 


    def pos_5_combat(self):
        ''' 5 fights 2,4 and 8 '''
        # fight 2 
        if self.positions['pos_2'][0] != 'empty':
            if self.positions['pos_2'][0].get_colour() != self.positions['pos_5'][0].get_colour():
                if self.positions['pos_5'][0].get_north() > self.positions['pos_2'][0].get_south():
                    print("5 fighting 2")
                    self.positions['pos_2'][0].set_colour(self.positions['pos_5'][0].get_colour()) # flip the card to attacking cards colour

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_5'][0].get_colour())
                    self.adjust_scores(self.positions['pos_5'][0].get_colour())



                    print("5 flipped 2")
        
        # fight 4 
        if self.positions['pos_4'][0] != 'empty':
            if self.positions['pos_4'][0].get_colour() != self.positions['pos_5'][0].get_colour():
                if self.positions['pos_5'][0].get_west() > self.positions['pos_4'][0].get_east():
                    print("5 fighting 4")
                    self.positions['pos_4'][0].set_colour(self.positions['pos_5'][0].get_colour()) # flip the card to attacking cards colour

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_5'][0].get_colour())
                    self.adjust_scores(self.positions['pos_5'][0].get_colour())


                    print("5 flipped 4")

        # fight 8 
        if self.positions['pos_8'][0] != 'empty':
            if self.positions['pos_8'][0].get_colour() != self.positions['pos_5'][0].get_colour():
                if self.positions['pos_5'][0].get_south() > self.positions['pos_8'][0].get_north():
                    print("5 fighting 8")
                    self.positions['pos_8'][0].set_colour(self.positions['pos_5'][0].get_colour()) # flip the card to attacking cards colour

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_5'][0].get_colour())
                    self.adjust_scores(self.positions['pos_5'][0].get_colour())


                    print("5 flipped 8")

    def pos_6_combat(self):
        ''' 6 fights 3 and 7 '''
        # fight 3 
        if self.positions['pos_3'][0] != 'empty':
            if self.positions['pos_3'][0].get_colour() != self.positions['pos_6'][0].get_colour():
                if self.positions['pos_6'][0].get_north() > self.positions['pos_3'][0].get_south():
                    print("6 fighting 3")
                    self.positions['pos_3'][0].set_colour(self.positions['pos_6'][0].get_colour()) # flip the card to attacking cards colour
                    # carry out score changes 
                    print("winning_colour", self.positions['pos_6'][0].get_colour())
                    self.adjust_scores(self.positions['pos_6'][0].get_colour())
 
                    print("6 flipped 3")

        # fight 7 
        if self.positions['pos_7'][0] != 'empty':
            if self.positions['pos_7'][0].get_colour() != self.positions['pos_6'][0].get_colour():
                if self.positions['pos_6'][0].get_east() > self.positions['pos_7'][0].get_west():
                    print("6 fighting 7")
                    self.positions['pos_7'][0].set_colour(self.positions['pos_6'][0].get_colour()) # flip the card to attacking cards colour

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_6'][0].get_colour())
                    self.adjust_scores(self.positions['pos_6'][0].get_colour())


                    print("6 flipped 7")

    def pos_7_combat(self):
        '''7 fights 6, 4 and 8 '''
        # fight 6 
        if self.positions['pos_6'][0] != 'empty':
            if self.positions['pos_6'][0].get_colour() != self.positions['pos_7'][0].get_colour():
                if self.positions['pos_7'][0].get_west() > self.positions['pos_6'][0].get_east():
                    print("7 fighting 6")
                    self.positions['pos_6'][0].set_colour(self.positions['pos_7'][0].get_colour()) # flip the card to attacking cards colour

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_7'][0].get_colour())
                    self.adjust_scores(self.positions['pos_7'][0].get_colour())


                    print("7 flipped 6")
        # fight 4
        if self.positions['pos_4'][0] != 'empty':
            if self.positions['pos_4'][0].get_colour() != self.positions['pos_7'][0].get_colour():
                if self.positions['pos_7'][0].get_north() > self.positions['pos_4'][0].get_south():
                    print("7 fighting 4")
                    self.positions['pos_4'][0].set_colour(self.positions['pos_7'][0].get_colour()) # flip the card to attacking cards colour

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_7'][0].get_colour())
                    self.adjust_scores(self.positions['pos_7'][0].get_colour())



                    print("7 flipped 4")

        # fight 8 
        if self.positions['pos_8'][0] != 'empty':
            if self.positions['pos_8'][0].get_colour() != self.positions['pos_7'][0].get_colour():
                if self.positions['pos_7'][0].get_east() > self.positions['pos_8'][0].get_west():
                    print("7 fighting 8")
                    self.positions['pos_8'][0].set_colour(self.positions['pos_7'][0].get_colour()) # flip the card to attacking cards colour

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_7'][0].get_colour())
                    self.adjust_scores(self.positions['pos_7'][0].get_colour())                


                    print("7 flipped 8")

    def pos_8_combat(self):
        '''8 fights 7 and 5 '''
        # fight 7 
        if self.positions['pos_7'][0] != 'empty':
            if self.positions['pos_7'][0].get_colour() != self.positions['pos_8'][0].get_colour():
                if self.positions['pos_8'][0].get_west() > self.positions['pos_7'][0].get_east():
                    print("8 fighting 7")
                    self.positions['pos_7'][0].set_colour(self.positions['pos_8'][0].get_colour()) # flip the card to attacking cards colour

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_8'][0].get_colour())
                    self.adjust_scores(self.positions['pos_8'][0].get_colour())

                    
                    print("8 flipped 7")
        
        # fight 5 
        if self.positions['pos_5'][0] != 'empty':
            if self.positions['pos_5'][0].get_colour() != self.positions['pos_8'][0].get_colour():
                if self.positions['pos_8'][0].get_north() > self.positions['pos_5'][0].get_south():
                    print("8 fighting 5")
                    self.positions['pos_5'][0].set_colour(self.positions['pos_8'][0].get_colour()) # flip the card to attacking cards colour

                    # carry out score changes 
                    print("winning_colour", self.positions['pos_8'][0].get_colour())
                    self.adjust_scores(self.positions['pos_8'][0].get_colour())

                    print("8 flipped 5")


class CPU():
    '''CPU class which plays versus a player '''
    colour = 'red'

    def __init__(self,board):
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
        self.board = board # not delighted about this - need to refactor attributes and methods
        self.board_status = {}
        self.is_board_empty = False
        self.spaces_in_play = {}
        self.occupied_spaces = {}
        self.possible_moves = {} # possible attacking moves in the event of an attacking option 
        self.defensive_map={'pos_0':self.pos_0_defense, 
                      'pos_1':self.pos_1_defense,
                      'pos_2':self.pos_2_defense,
                      'pos_3':self.pos_3_defense,
                      'pos_4':self.pos_4_defense,
                      'pos_5':self.pos_5_defense,
                      'pos_6':self.pos_6_defense,
                      'pos_7':self.pos_7_defense,
                      'pos_8':self.pos_8_defense}
        self.defensive_moves={}
        

    def add_to_inventory(self,card):
        self.inventory.append(card)

    def get_inventory(self):
        return self.inventory 

    def show_inventory(self):
        for card in self.inventory:
            card.show_compass_values()

    def get_player_colour(self):
        return self.colour


    def play_card(self,position,card,card_index):
        ''' CPU play card method.
        It will place the card on the board complying with the boards rules 
        (this is dictated by invoking boards accept card method).
        It will then remove that card from the CPUs inventory'''
        self.board.accept_card(position,card) # play the card 
        self.inventory.pop(card_index) # remove this card from the CPU inventory 


    def assess_board(self):
        self.board_status = self.board.ret_board_in_play() ## investigate this when less tired
        print("board_status - check if this is broken")
        print(self.board_status) 

        
        empty = self.board.get_spaces_filled()
        print("checking empty == self.board.get_spaces_filled() - that looks weird to me already")
        print(empty)

        if empty == 0: # need to address this 
            self.is_board_empty = True

        self.spaces_in_play = {}
             
        for key,value in self.board_status.items():
            if value[0] == 'empty':
                self.spaces_in_play[key] = value
            else:
                self.occupied_spaces[key] = value
                #self.spaces_in_play[key] = value

        print("spaces in play after assess board")
        print(self.spaces_in_play) # this is broken !!!!!!!!!!!!!!



    def make_move(self):
        ''' this is the CPU brain '''
        
        print("CPU assessinng board")
        self.assess_board()


        if self.is_board_empty:
            self.defensive_opener()  # defensive opener invoked in the case of an empty board (i.e opening move)

        else: # initiate search for attacks
            print("board not empty, searching for attacks")
            attack_options = self.spaces_in_play.keys()
            print(attack_options)

            for option in attack_options: 
                self.attack_map[option]() # invoke the attack moves to populate possible moves attribute 

            print()

            valid_attacks = {}

            for option in attack_options:
                if self.possible_moves[option] != {}: # remove any non attacking positions - could just reapply to attribute 
                    valid_attacks[option] = self.possible_moves[option] 


            if valid_attacks != {}: # provided there are attacks available 

                print("double triple checks") # search for doubles/triples
                valid_attack_positions = valid_attacks.keys()

                pos_dubs_trips={}
                doubles_triples={}
                triple_quad_bool = False
                double_bool = False

                for pos in valid_attack_positions:
                    attacks = valid_attacks[pos] # attacks for that position 

                    inv_card_keys = list(attacks.keys())
                    for key in inv_card_keys: 
                        attack_values = attacks[key]
                        if attack_values[1] > 2:
                            if double_bool:
                                doubles_triples = {} # if there has been doubles already then erase them
                            doubles_triples[key] = attack_values 
                            triple_quad_bool = True # if we have triples or quads - ignore doubles 
                        if attack_values[1] > 1 and triple_quad_bool == False: # otherwise we have doubles so add them in 
                             doubles_triples[key] = attack_values
                             double_bool = True    
                    if doubles_triples != {}:
                        pos_dubs_trips[pos] = doubles_triples
                    doubles_triples = {}


                # if the above has been altered then there are doubles or triples and we should ignore the singles and update valid_attacks 
                if pos_dubs_trips != {}:
                     valid_attacks = pos_dubs_trips

                print("from valid attacks we have - assess defensive footprint of each")
                valid_attack_keys = list(valid_attacks.keys())

                for position in valid_attack_keys:
                    self.defensive_map[position](self.inventory) # this should invoke the method - which should then popluate defensive_moves 
                    #### I think here we just pass the relevant inventory for each position 
                    #### verify that indices hold true 
                    #### if not may need to invoke ids for the cards 

                print("checking for attack with no defensive considerations thereafter - prioritise these")
                pos_to_attack = '' # the position to attack in the case of no defense to consider 

                for position in valid_attack_keys:
                    if self.defensive_moves[position] == []: # if it's an empty array for that position - 
                        pos_to_attack = position # then thats' the position we attack
                        break # exit the loop on satisfying above 
                
                if pos_to_attack != '': # then extract the powers of the cards and choose the lowest - then play this one 
                    cards=valid_attacks[pos_to_attack]

                    card_keys = list(cards.keys())

                    lowest_power_card = valid_attacks[pos_to_attack][card_keys[0]] # select the first one 

                    power_of_lowest = lowest_power_card[0]

                    no_def_attack = {pos_to_attack:''} # placeholder for the position of the eventual card to attack 

                    for card in card_keys:
                        if valid_attacks[pos_to_attack][card][0] < power_of_lowest:
                            lowest_power_card = valid_attacks[pos_to_attack][card]

                        no_def_attack = {pos_to_attack:[card,lowest_power_card]}


                    no_def_pos = list(no_def_attack.keys())
                    no_def_pos = no_def_pos[0]

                    no_def_card_index = no_def_attack[no_def_pos][1][1]

                    no_def_card = self.inventory[no_def_card_index]

                    self.play_card(no_def_pos,no_def_card,no_def_card_index) # play no defense card if available 


                   
                # else pick the card with the best defesne 
                else: # there are no defense free attacks 
                    print("arrived at attacks with defensive considerations")

                    POI = list(self.defensive_moves.keys()) # positions of interest for attack/defense 
                    # I think this should be valid attacks 
                    print("valid_attacks", valid_attacks)
                    print("POI", POI)
                    print("self.defensive_moves")
                    pprint.pprint(self.defensive_moves)

                    # need to repopulate defensive moves here from valid attacks 
                    # so you could just loop through and drop the invalid keys 

                    for pos in POI:
                        valid_attack_inv_cards = list(valid_attacks[pos].keys()) # these are the valid keys 
                        print("valid_attack_inv_cards", valid_attack_inv_cards)
                        # need to drop all invalid keys from self.defensive_moves

                    # poi then needs the cards that can produce flips 
                    # self.defensive_map[pos](inv_cards that can produce a flip)
                    #### I think here we just pass the relevant inventory for each position

                    sections = []

                    concatenated_positions = {}

                    for pos in POI: 
                        # can have up to three positions to sum
                        section = self.defensive_moves[pos] # each position 

                        if len(section) > 1:
                            # get the keys for one
                            inv_cards = list(section[0].keys())
            
                            # define base dictionary 
                            dict_1 = section[0]

                            if len(section) == 2:
                                dict_2 = section[1] # define the second dictionary
                                for index in inv_cards:
                                    dict_1[index].append(dict_2.get(index, {})) # add the dictionaries together for each inv card/position

                                for index in inv_cards:
                                    sum_dispar = [dict_1[index][1] + dict_1[index][2][1], abs(dict_1[index][1] - dict_1[index][2][1])] # calculate sum and disparity
                                    dict_1[index] = [sum_dispar[0] - sum_dispar[1],2] # sum - disparity is ther ultimate measure - highest sum and lowest disparity is the best card 

                            if len(section) == 3: 
                                dict_2 = section[1] # define the second dictionary
                                dict_3 = section[2] # define the third dictionary

                                for index in inv_cards:
                                    dict_1[index].append(dict_2.get(index, {})) 

                                for index in inv_cards:
                                    dict_1[index].append(dict_3.get(index, {})) # add all of the dictionaries together one after the other 

                                # initially need to find the highest and lowest end member poles for calculations
                                # for index in inv_cards:
                                    # add to temp array the following values 
                                    # [1], [2][1], [3][1]
                                    # calc max and min ==> minus these two figures for disparity
                                    # sum all 3 for sum 
                                    # calc sum - disparity  
                                for index in inv_cards:
                                    pole_values = [dict_1[index][1], dict_1[index][2][1], dict_1[index][3][1]]
                                    max_pole = max(pole_values)
                                    min_pole = min(pole_values)
                                    disparity = max_pole - min_pole
                                    poles_sum = sum(pole_values)
                                    sum_minus_disparity = poles_sum - disparity
                                    # now assign it 
                                    dict_1[index] = [sum_minus_disparity,3] #also add division factor 
                                       
                            
                            concatenated_positions[pos] = dict_1


                    for pos in concatenated_positions.keys():
                        self.defensive_moves[pos]  = concatenated_positions[pos] 

                    # process here maybe? 
                    print("self.defensive_moves after initial processing")
                    pprint.pprint(self.defensive_moves)

                    # if type(self.defensive_moves) 
                    #  is_list = then you take the max of the poles 
                    #  is_dict - then again take the max of the dictionary 
                    # for multi pole defensive cards - divide by the number of poles /2 | /3 - if that is above the top single value - play that 
                    
                    is_list = type([])
                    is_dict = type({})

                    for pos in self.defensive_moves.keys():
                        # loop through the intended positions to attack
                        intended_attacks = self.defensive_moves[pos] # - consider refactor 
                        if type(intended_attacks) == is_list:
                            # get max 

                            #inv_cards = list(intended_attacks[0].keys())
                            # what about here????????????
                            inv_cards = list(valid_attacks[pos].keys()) # these are the valid keys

                            max_val = [inv_cards[0],intended_attacks[0][inv_cards[0]][1]] # intitiate max_val variable 
                            
                            for index in inv_cards: # loop through and find max_val
                                if intended_attacks[0][index][1] > max_val[1]:
                                    max_val = [index,intended_attacks[0][index][1]]

                            self.defensive_moves[pos] = max_val # why use this attribute? It's confusing - why not something new like attack with defense move


                        elif type(intended_attacks) == is_dict: 
                            #inv_cards = list(intended_attacks.keys())
                            inv_cards = list(valid_attacks[pos].keys()) # these are the valid keys
                            division_factor = intended_attacks[inv_cards[0]][1] # define division factor (how many poles to divide by)

                            max_val = [inv_cards[0],intended_attacks[inv_cards[0]][0]]


                            # loop through and get max
                            first_highest = True
                            for index in inv_cards:
                                if intended_attacks[index][0] > intended_attacks[inv_cards[0]][0]:
                                    first_highest = False
                                    max_val = [index, intended_attacks[index][0]/division_factor] # divide by divsion factor
                            
                            if first_highest:
                                max_val = [inv_cards[0],intended_attacks[inv_cards[0]][0]/division_factor] # still need to divide the entry if the first is highest
                                   

                            self.defensive_moves[pos] = max_val

                    positions = list(self.defensive_moves.keys())

                    top_pick= self.defensive_moves[positions[0]][1]
                    selection = {positions[0]: self.defensive_moves[positions[0]]}


                    for pos in positions:
                        if self.defensive_moves[pos][1] > top_pick:
                            top_pick = self.defensive_moves[pos][1]
                            selection = {pos:self.defensive_moves[pos]}
                        
                    position_list = list(selection.keys())
                    position = position_list[0]

                    
                    card_index = selection[position][0]

                    card = self.inventory[selection[position][0]]

                    # play the card 

                    self.play_card(position,card,card_index)


                    # revert defensive_moves to {}
                    self.defensive_moves = {}
 

            # In the event of no available attacks 
            else: #
                print()
                print("No attacks available - making a defensive move")
                print("attack_options", attack_options)

                # change this 
                for option in attack_options:  
                    self.defensive_map[option](self.inventory) # defensive moves populated here - no inventory left - that's why !!!!!!!!!!

                #for option in self.spaces_in_play:
                #    self.defensive_map[option](self.inventory)

                print("defensive_moves priot to POI")
                pprint.pprint(self.defensive_moves)


                POI = list(self.defensive_moves.keys()) # positions of interest for attack/defense

                sections = []

                concatenated_positions = {}

                for pos in POI: 
                    # can have up to three positions to sum
                    section = self.defensive_moves[pos] # each position 

                    # if section.length() > 1
                    if len(section) > 1:
                        # get the keys for one
                        inv_cards = list(section[0].keys())
            #            print("inv_cards",inv_cards)
                        
                        # define base dictionary 
                        dict_1 = section[0]

                        if len(section) == 2:
                            dict_2 = section[1] # define the second dictionary
                            for index in inv_cards:
                                dict_1[index].append(dict_2.get(index, {})) # add the dictionaries together for each inv card/position

                            for index in inv_cards:
                                sum_dispar = [dict_1[index][1] + dict_1[index][2][1], abs(dict_1[index][1] - dict_1[index][2][1])] # calculate sum and disparity
                                dict_1[index] = [sum_dispar[0] - sum_dispar[1],2] # sum - disparity 

                        if len(section) == 3:
                            dict_2 = section[1] # define the second dictionary
                            dict_3 = section[2] # define the third dictionary

                            for index in inv_cards:
                                dict_1[index].append(dict_2.get(index, {})) 

                            for index in inv_cards:
                                dict_1[index].append(dict_3.get(index, {})) # add all of the dictionaries together one after the other 

                            # initially need to find the highest and lowest end member poles for calculations
                            # for index in inv_cards:
                                # add to temp array the following values 
                                # [1], [2][1], [3][1]
                                # calc max and min ==> minus these two figures for disparity
                                # sum all 3 for sum 
                                # calc sum - disparity  
                            for index in inv_cards:
                                pole_values = [dict_1[index][1], dict_1[index][2][1], dict_1[index][3][1]]
                                max_pole = max(pole_values)
                                min_pole = min(pole_values)
                                disparity = max_pole - min_pole
                                poles_sum = sum(pole_values)
                                sum_minus_disparity = poles_sum - disparity
                                # now assign it 
                                dict_1[index] = [sum_minus_disparity,3] #also add division factor 
                                    
                        
                        concatenated_positions[pos] = dict_1


                for pos in concatenated_positions.keys():
                    self.defensive_moves[pos]  = concatenated_positions[pos] 

                is_list = type([])
                is_dict = type({})

                # here there's likely an meoty array or two - is this erroneous - or should we just remove them? 

                print("checking 1079 - self.defensive_moves - just before checks")
                pprint.pprint(self.defensive_moves)
                for pos in self.defensive_moves.keys():
                    # loop through the intended positions to attack
                    intended_attacks = self.defensive_moves[pos] # consider refactor
                    if type(intended_attacks) == is_list and intended_attacks != []:
                        # get max 
            #            print("intended_attacks single array case",intended_attacks)
                        print("error 1079 - some positions are empty for defensive moves positions - why - how is it built - does it get edited along the way? ")
                        print(intended_attacks)
                        inv_cards = list(intended_attacks[0].keys())
            #            print("inv_cards",inv_cards)
                        #max_val = {inv_cards[0]:intended_attacks[inv_cards[0]]} # need to get this right
                        
                        #print("inv_cards[0]",inv_cards[0])
                        #print("*-*intended_attacks[0][inv_cards[0]][1]*-*",intended_attacks[0][inv_cards[0]][1])
                        max_val = [inv_cards[0],intended_attacks[0][inv_cards[0]][1]]
                        print("max_val", max_val)
                        
                        for index in inv_cards:
                            if intended_attacks[0][index][1] > max_val[1]:
                                max_val = [index,intended_attacks[0][index][1]]
            #                    print("max val after change in array")
            #                    print(max_val)
                            # now loop through and find the maximum 

                        
                        self.defensive_moves[pos] = max_val
            #            print("defensive moves after changes")
            #            pprint.pprint(self.defensive_moves)

                    
                    elif type(intended_attacks) == is_dict:
                        #print("intended_attacks in division factor error checks")
                        #print(intended_attacks)
                        # get max and divide by appropriate value 
            #            print("intended_attacks dict case",intended_attacks)
                        inv_cards = list(intended_attacks.keys())
            #            print("inv cards dict",inv_cards)
                        division_factor = intended_attacks[inv_cards[0]][1] # define division factor (how many poles to divide by)
                        #print("checking division factor and type", division_factor, type(division_factor))
            #            print("division factor", division_factor)

                        max_val = [inv_cards[0],intended_attacks[inv_cards[0]][0]]
            #            print("max val dict case")

                        # loop through and get max
                        first_highest = True
                        for index in inv_cards:
                            if intended_attacks[index][0] > intended_attacks[inv_cards[0]][0]:
                                first_highest = False
            #                    print("checking dict max val value",intended_attacks[index][0])
            #                    print("checking division factor",division_factor)
            #                    print("checking calculation",intended_attacks[index][0]/division_factor)
                                max_val = [index, intended_attacks[index][0]/division_factor] # divide by divsion factor
                        
                        if first_highest:
                            #print("checking first_highest case and what's being divided and it's type", intended_attacks[inv_cards[0]][0], type(intended_attacks[inv_cards[0]][0]))
                            max_val = [inv_cards[0],intended_attacks[inv_cards[0]][1]/division_factor] # still need to divide the entry if the first is highest
                               

                        self.defensive_moves[pos] = max_val
        #                print("defensive moves after changes in dict case")
        #                pprint.pprint(self.defensive_moves)
                         

                # play the appropriate card and revert defensive_moves and possible_moves to {}                 
        #        print("***making top pick for defense***")

                ########

                print("reached defense in no attack situation")
                pprint.pprint(self.defensive_moves)
                positions = list(self.defensive_moves.keys())

                top_pick= 0
                selection = {positions[0]: self.defensive_moves[positions[0]]}
                best_card = False   

        #        print("top_pick",top_pick)
        #        print("selection",selection)

                for pos in positions:
                    if self.defensive_moves[pos] != []: # change here to accomodate empty list 
                        if self.defensive_moves[pos][1] > top_pick:
                            top_pick = self.defensive_moves[pos][1]
                            selection = {pos:self.defensive_moves[pos]}
                            best_card = True 
                            
                if best_card: 
                    position_list = list(selection.keys())
                    position = position_list[0]
            #        print("position",position)
                    
                    #need to play last card here !!!!
                    
                    card_index = selection[position][0]
            #        print("card_index",card_index)
                    card = self.inventory[selection[position][0]]
            #        print("card",card)
            #
                    # play the card 
            #        print(self.board.ret_board_in_play())
                    self.play_card(position,card,card_index)
            #        print(self.board.ret_board_in_play())
            #
                    # revert defensive_moves to {}
                    self.defensive_moves = {}
                else: 
                    position = positions[0]
                    card = self.inventory[0]
                    card_index = 0

                    self.play_card(position,card,card_index)


                

    def defensive_opener(self):
        ''' if the CPU plays first it plays a defensive move in one of the four corners (least exposed poles)
        biggest sum is played - with an inclusion of disparity to reduce imbalance eg 9 exposed along with a 2'''

        print("defensive opener invoked")

        corners= ['pos_0','pos_2','pos_6','pos_8']
        
        for option in corners:
        #    print(option)
            self.defensive_map[option](self.inventory) # add all the options 
        #pprint.pprint(self.defensive_moves)
        
        # first of all break down how to use/digest this info 
        
        sum_disparity = {} # card 

        for option in corners:
            pos_0 = self.defensive_moves[option] # loop through each  
 

            pos_0_dict_1 = pos_0[0] 
            pos_0_dict_2 = pos_0[1]

        #    print("pos_0_dict_1",pos_0_dict_1)
        #    print("pos_0_dict_2",pos_0_dict_2)

            for k in pos_0_dict_1.keys():
        #        print(k)
                pos_0_dict_1[k].append(pos_0_dict_2.get(k, {})) # add the dictionaries together for each inv card/position 

        #    pprint.pprint(pos_0_dict_1)  

            for k in pos_0_dict_1:
                sum_dispar = [pos_0_dict_1[k][1] + pos_0_dict_1[k][2][1], abs(pos_0_dict_1[k][1] - pos_0_dict_1[k][2][1])] # calculate sum and disparity
        #        print("sum_dispar",sum_dispar)
                pos_0_dict_1[k] = sum_dispar[0] - sum_dispar[1] # sum - disparity is ther ultimate winner - highest sum and lowest disparity is the best card 

            sum_disparity[option] = pos_0_dict_1

        #print("***check sum disaprity")
        #print(sum_disparity)

        # select the card with the largest overall int score 
        # then play that card 

        high_sums = {}

        for option in corners:
        #    print("sum_disparity[option]",sum_disparity[option])
        #    print(max(sum_disparity[option], key=sum_disparity[option].get))
            #high_sums[option] = [max(sum_disparity[option], key=sum_disparity[option].get)]
            high_sums[option] = [max(sum_disparity[option], key=sum_disparity[option].get) ,sum_disparity[option][max(sum_disparity[option], key=sum_disparity[option].get)]]

        #print("***high_sums***")
        #print(high_sums)


        
        top_pick = high_sums['pos_0'] # initiate top pick 
        selection = {'pos_0':top_pick} # initiate selection 

        #print("***top_pick***")
        #print(top_pick)
        

        for pos,card_sum in high_sums.items():
            if card_sum[1] > top_pick[1]: 
                top_pick = card_sum
                selection = {pos:top_pick}
#
        #print("after selection")
        #print(selection)


        position_list = list(selection.keys())
        position = position_list[0]
        #print("position",position)
        
        card_index = selection[position][0]
        #print("card_index",card_index)
        card = self.inventory[selection[position][0]]
        #print("card",card)
#
        # play the card 
        #print(self.board.ret_board_in_play())
        self.play_card(position,card,card_index)
        #print(self.board.ret_board_in_play())
#
        # revert defensive_moves to {} and is_board_empty = False
        self.defensive_moves = {}
        self.is_board_empty = False


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
    #        print("first check")
            if self.board_status['pos_1'][0] != 'empty':
                if self.board_status['pos_1'][0].get_colour() != inv_card.get_colour():
    #                print("colour check passed")
                    if inv_card.get_east() > self.board_status['pos_1'][0].get_west():
    #                    print("0 versus 1 is a flip with ",inv_card_index)
                        # here we assign the value to possible_moves 
                        pos_0_checks[inv_card_index] = [inv_card_power,1] # how to increment score? 
                        # another if statement here for the double case? 
                        if self.board_status['pos_3'][0] != 'empty':
    #                        print("nested boolean")
                            three_check = True
                            if self.board_status['pos_3'][0].get_colour() != inv_card.get_colour(): 
                                if inv_card.get_south() > self.board_status['pos_3'][0].get_north():
    #                                print("Double case for pos 0 with ", inv_card_index)
                                    pos_0_checks[inv_card_index] = [inv_card_power,2]
                                    
            # then a solitary check here for pos 3 check
            if self.board_status['pos_3'][0] != 'empty' and three_check == False: # if the double check has taken place don't run this
                if self.board_status['pos_3'][0].get_colour() != inv_card.get_colour(): 
                    if inv_card.get_south() > self.board_status['pos_3'][0].get_north():
    #                    print("0 versus 3 is a flip with ", inv_card_index)
                        pos_0_checks[inv_card_index] = [inv_card_power,1] 

        self.possible_moves['pos_0'] = pos_0_checks
    #    print("checking possible moves")
    #    print(self.possible_moves)

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
        #                print("1 versus 0 is a flip with ",inv_card_index)
                        # here we assign the value to possible_moves 
                        pos_1_checks[inv_card_index] = [inv_card_power,1]
                        # another if statement here for the double case for pos 4 

                        # pos 4 - double check
        #                print("first 4 check on double")
        #                print()
                        if self.board_status['pos_4'][0] != 'empty': # card present
                            four_check = True
        #                    print("initial 4 check not empty passed")
        #                    print(self.board_status['pos_4'][0].get_colour())
        #                    print(inv_card.get_colour())
                            if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour(): 
        #                        print("colour checks passed")
                                if inv_card.get_south() > self.board_status['pos_4'][0].get_north():
                                    # here we assign the value to possible_moves 
        #                            print("1 versus 4 is a double flip with ",inv_card_index)
                                    pos_1_checks[inv_card_index] = [inv_card_power,2]
                                    
                                    # another if statement here for the triple case?
        #                            print("triple case")
                                    if self.board_status['pos_2'][0] != 'empty' and two_check == False: # card present
                                        two_check = True
                                        if self.board_status['pos_2'][0].get_colour() != inv_card.get_colour():
                                            if inv_card.get_east() > self.board_status['pos_2'][0].get_east():
                                                # here we assign the value to possible_moves 
        #                                        print("1 versus 2 is a triple flip with ",inv_card_index)
                                                pos_1_checks[inv_card_index] = [inv_card_power,3]

                        # pos 2 alternate double check
                        if self.board_status['pos_2'][0] != 'empty' and two_check==False: # card present
                            two_check = True 
                            if self.board_status['pos_2'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_east() > self.board_status['pos_2'][0].get_east():
                                    # here we assign the value to possible_moves 
        #                            print("solo 1 versus 2 is a double flip with ",inv_card_index)
                                    pos_1_checks[inv_card_index] = [inv_card_power,2]

            # pos 4 check
            if self.board_status['pos_4'][0] != 'empty' and four_check==False: # card present
                four_check=True
                if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour(): 
                    if inv_card.get_south() > self.board_status['pos_4'][0].get_north():
                        # here we assign the value to possible_moves 
        #                print("1 versus 4 is a double flip with ",inv_card_index)
                        pos_1_checks[inv_card_index] = [inv_card_power,1]

                        if self.board_status['pos_2'][0] != 'empty' and two_check==False: # card present
                            two_check = True 
                            if self.board_status['pos_2'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_east() > self.board_status['pos_2'][0].get_east():
                                    # here we assign the value to possible_moves 
        #                            print("1 versus 2 is a double flip with ",inv_card_index)
                                    pos_1_checks[inv_card_index] = [inv_card_power,2]

            # pos 2 check 
            if self.board_status['pos_2'][0] != 'empty' and two_check==False: # card present 
                if self.board_status['pos_2'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_east() > self.board_status['pos_2'][0].get_east():
                        # here we assign the value to possible_moves 
    #                    print("1 versus 2 is a double flip with ",inv_card_index)
                        pos_1_checks[inv_card_index] = [inv_card_power,1]
        
        self.possible_moves['pos_1'] = pos_1_checks
    #    print("checking possible moves")
    #    print(self.possible_moves)

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
        #                print("2 versus 1 is a flip with ",inv_card_index)
                        pos_2_checks[inv_card_index] = [inv_card_power,1]

                        # double check for pos 5 
                        if self.board_status['pos_5'][0] != 'empty': # card present
                            five_check = True # don't check again 
                            if self.board_status['pos_5'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_south() > self.board_status['pos_5'][0].get_north():
        #                            print("2 versus 5 is a double flip with ",inv_card_index)
                                    pos_2_checks[inv_card_index] = [inv_card_power,2]

            # pos 5 check 
            if self.board_status['pos_5'][0] != 'empty' and five_check == False: # card present and not been checked already
                    if self.board_status['pos_5'][0] != 'empty': # card present 
                        if self.board_status['pos_5'][0].get_colour() != inv_card.get_colour():
                            if inv_card.get_south() > self.board_status['pos_5'][0].get_north():
    #                            print("2 versus 5 is a double flip with ",inv_card_index)
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
        #                print("3 versus 0 is a flip with ",inv_card_index)
                        # here we assign the value to possible_moves 
                        pos_3_checks[inv_card_index] = [inv_card_power,1]
                        # another if statement here for the double case for pos 4 

                        # pos 4 - double check
        #                print("first 4 check on double")
        #                print()
                        if self.board_status['pos_4'][0] != 'empty': # card present
                            four_check = True
        #                    print("initial 4 check not empty passed")
                            if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour(): 
                                if inv_card.get_east() > self.board_status['pos_4'][0].get_west():
                                    # here we assign the value to possible_moves 
        #                            print("3 versus 4 is a double flip with ",inv_card_index)
                                    pos_3_checks[inv_card_index] = [inv_card_power,2]
                                    
                                    # another if statement here for the triple case?
        #                            print("triple case")
                                    if self.board_status['pos_6'][0] != 'empty' and six_check == False: # card present
                                        two_check = True
                                        if self.board_status['pos_6'][0].get_colour() != inv_card.get_colour():
                                            if inv_card.get_south() > self.board_status['pos_6'][0].get_north():
                                                # here we assign the value to possible_moves 
        #                                        print("1 versus 2 is a triple flip with ",inv_card_index)
                                                pos_3_checks[inv_card_index] = [inv_card_power,3]


            # pos 4 check
            if self.board_status['pos_4'][0] != 'empty' and four_check==False: # card present
                if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour(): 
                    if inv_card.get_east() > self.board_status['pos_4'][0].get_west():
                        # here we assign the value to possible_moves 
        #                print("3 versus 4 is a flip with ",inv_card_index)
                        pos_3_checks[inv_card_index] = [inv_card_power,1]

                        if self.board_status['pos_6'][0] != 'empty' and six_check==False: # card present
                            six_check = True 
                            if self.board_status['pos_6'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_south() > self.board_status['pos_6'][0].get_north():
                                    # here we assign the value to possible_moves 
        #                            print("3 versus 6 is a double flip with ",inv_card_index)
                                    pos_1_checks[inv_card_index] = [inv_card_power,2]

            # pos 6 check 
            if self.board_status['pos_6'][0] != 'empty' and six_check==False: # card present 
                if self.board_status['pos_6'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_south() > self.board_status['pos_6'][0].get_north():
                        # here we assign the value to possible_moves 
    #                    print("3 versus 6 is a flip with ",inv_card_index)
                        pos_3_checks[inv_card_index] = [inv_card_power,1]

        self.possible_moves['pos_3'] = pos_3_checks
    #    print("checking possible moves")
    #    print(self.possible_moves)

            
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
        #                print("4 versus 1 is a flip with ",inv_card_index)
                        pos_4_checks[inv_card_index] = [inv_card_power,1]

                        # check for nested double case pos 3 
                        if self.board_status['pos_3'][0] != 'empty': # card present
                            three_check = True
                            if self.board_status['pos_3'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_west() > self.board_status['pos_3'][0].get_east():
        #                            print("4 versus 3 is a double flip with ",inv_card_index)
                                    pos_4_checks[inv_card_index] = [inv_card_power,2]

                                    # check for triple nested for pos 5 
                                    if self.board_status['pos_5'][0] != 'empty': # card present 
                                        five_check = True
                                        if self.board_status['pos_5'][0].get_colour() != inv_card.get_colour():
                                            if inv_card.get_west() > self.board_status['pos_5'][0].get_east():
        #                                        print("4 versus 5 is a triple flip with ",inv_card_index)
                                                pos_4_checks[inv_card_index] = [inv_card_power,3]

                                                # check for quadruple nested for pos 7
                                                if self.board_status['pos_7'][0] != 'empty': # card present
                                                    seven_check = True
                                                    if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                                                        if inv_card.get_south() > self.board_status['pos_7'][0].get_north():
        #                                                    print("4 versus 7 is a quadruple flip with ",inv_card_index)
                                                            pos_4_checks[inv_card_index] = [inv_card_power,4]

            # pos 3 check
            if self.board_status['pos_3'][0] != 'empty' and three_check == False: # card present
                three_check = True
                if self.board_status['pos_3'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_west() > self.board_status['pos_3'][0].get_east():
    #                    print("4 versus 3 is a single flip with ",inv_card_index)
                        pos_4_checks[inv_card_index] = [inv_card_power,1]

                        # check for nested double for pos 5 
                        if self.board_status['pos_5'][0] != 'empty' and five_check == False: # card present
                            five_check = True
                            if self.board_status['pos_5'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_east() > self.board_status['pos_5'][0].get_west():
    #                                print("4 versus 5 is a double flip with ",inv_card_index)
                                    pos_4_checks[inv_card_index] = [inv_card_power,2]

                                    # check for nested triple with position 7 
                                    if self.board_status['pos_7'][0] != 'empty' and seven_check == False: # card present
                                        seven_check = True
                                        if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                                            if inv_card.get_south() > self.board_status['pos_7'][0].get_north():
    #                                            print("4 versus 7 is a triple flip with ",inv_card_index)
                                                pos_4_checks[inv_card_index] = [inv_card_power,3] 


            # pos 5 check 
            if self.board_status['pos_5'][0] != 'empty' and five_check == False: # card present  
                five_check = True
                if self.board_status['pos_5'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_east() > self.board_status['pos_5'][0].get_west():
    #                    print("4 versus 5 is a single flip with ",inv_card_index)
                        pos_4_checks[inv_card_index] = [inv_card_power,1]

                        # nested check for double for pos 7 

                        if self.board_status['pos_7'][0] != 'empty' and seven_check == False: # card present
                            seven_check = True
                            if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_south() > self.board_status['pos_7'][0].get_north():
    #                                print("4 versus 7 is a double flip with ",inv_card_index)
                                    pos_4_checks[inv_card_index] = [inv_card_power,2] 

            # pos 7 check
            if self.board_status['pos_7'][0] != 'empty' and seven_check == False: # card present 
                if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_south() > self.board_status['pos_7'][0].get_north():
    #                    print("4 versus 7 is a single flip with ",inv_card_index)
                        pos_4_checks[inv_card_index] = [inv_card_power,1]

        self.possible_moves['pos_4'] = pos_4_checks
    #    print("checking possible moves")
    #    print(self.possible_moves)

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
        #                print("5 versus 2 is a single flip with ",inv_card_index)
                        pos_5_checks[inv_card_index] = [inv_card_power,1]

                        # nested double case for 4
                        if self.board_status['pos_4'][0] != 'empty': # card present
                            four_check = True 
                            if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_west() > self.board_status['pos_4'][0].get_east():
        #                            print("5 versus 4 is a double flip with ",inv_card_index)
                                    pos_5_checks[inv_card_index] = [inv_card_power,2]

                                    # nested triple case for 8
                                    if self.board_status['pos_8'][0] != 'empty': # card present 
                                        eight_check = True
                                        if self.board_status['pos_8'][0].get_colour() != inv_card.get_colour():
                                            if inv_card.get_south() > self.board_status['pos_8'][0].get_north():
        #                                        print("5 versus 8 is a triple flip with ",inv_card_index)
                                                pos_5_checks[inv_card_index] = [inv_card_power,3]

            # pos 4 check
            if self.board_status['pos_4'][0] != 'empty' and four_check == False: # card present
                four_check = True 
                if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_west() > self.board_status['pos_4'][0].get_east():
        #                print("5 versus 4 is a single flip with ",inv_card_index)
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
        #print("checking possible moves")
        #print(self.possible_moves)


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
        #                print("6 versus 3 is a single flip with ",inv_card_index)
                        pos_6_checks[inv_card_index] = [inv_card_power,1]

                        # check for nested double case for pos 7
                        if self.board_status['pos_7'][0] != 'empty': 
                            seven_check = True
                            if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_east() > self.board_status['pos_7'][0].get_west():
        #                            print("6 versus 7 is a double flip with ",inv_card_index)
                                    pos_6_checks[inv_card_index] = [inv_card_power,2]

            # pos 7 check
            if self.board_status['pos_7'][0] != 'empty' and seven_check == False:
        #        print("checks")
        #        print(self.board_status['pos_7'][0],inv_card.get_colour()) 
                if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_east() > self.board_status['pos_7'][0].get_west():
                        print("6 versus 7 is a single flip with ",inv_card_index)
                        pos_6_checks[inv_card_index] = [inv_card_power,1]
        
        self.possible_moves['pos_6'] = pos_6_checks
        #print("checking possible moves")
        #print(self.possible_moves)

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
        #                print("7 versus 6 is a single flip with ",inv_card_index)
                        pos_7_checks[inv_card_index] = [inv_card_power,1]

                        # nested case for double at pos 4 
                        if self.board_status['pos_4'][0] != 'empty':
                            four_check= True
                            if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_north() > self.board_status['pos_4'][0].get_south():
        #                            print("7 versus 4 is a double flip with ",inv_card_index)
                                    pos_7_checks[inv_card_index] = [inv_card_power,2]

                                    # nested triple case at pos 8 
                                    if self.board_status['pos_8'][0] != 'empty':
                                        eight_check = True
                                        if self.board_status['pos_8'][0].get_colour() != inv_card.get_colour():
                                            if inv_card.get_east() > self.board_status['pos_8'][0].get_west():
        #                                        print("7 versus 8 is a triple flip with ",inv_card_index)
                                                pos_7_checks[inv_card_index] = [inv_card_power,3]

            # pos 4 check 
            if self.board_status['pos_4'][0] != 'empty' and four_check == False:
                four_check= True
                if self.board_status['pos_4'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_north() > self.board_status['pos_4'][0].get_south():
        #                print("7 versus 4 is a single flip with ",inv_card_index)
                        pos_7_checks[inv_card_index] = [inv_card_power,1]

                        # nested double case for pos 8
                        if self.board_status['pos_8'][0] != 'empty':
                            eight_check = True
                            if self.board_status['pos_8'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_east() > self.board_status['pos_8'][0].get_west():
        #                            print("7 versus 8 is a double flip with ",inv_card_index)
                                    pos_7_checks[inv_card_index] = [inv_card_power,2] 

            # pos 8 check 
            if self.board_status['pos_8'][0] != 'empty' and eight_check == False:  
        #        print("pos 7 attack, pos 8 check")
        #        print(self.board_status['pos_8'][0].get_colour())

                if self.board_status['pos_8'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_east() > self.board_status['pos_8'][0].get_west():
        #                print("7 versus 8 is a double flip with ",inv_card_index)
                        pos_7_checks[inv_card_index] = [inv_card_power,2] 

        self.possible_moves['pos_7'] = pos_7_checks
        #print("checking possible moves")
        #print(self.possible_moves)

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
        #                print("8 versus 5 is a single flip with ",inv_card_index)
                        pos_8_checks[inv_card_index] = [inv_card_power,1]

                        # nested double case for pos 7
                        if self.board_status['pos_7'][0] != 'empty':
                            seven_check = True
                            if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                                if inv_card.get_west() > self.board_status['pos_7'][0].get_east():
        #                            print("8 versus 7 is a double flip with ",inv_card_index)
                                    pos_8_checks[inv_card_index] = [inv_card_power,2]

            # pos 7 check 
            if self.board_status['pos_7'][0] != 'empty' and seven_check == False:
                seven_check == True
                if self.board_status['pos_7'][0].get_colour() != inv_card.get_colour():
                    if inv_card.get_west() > self.board_status['pos_7'][0].get_east():
                        print("8 versus 7 is a single flip with ",inv_card_index)
                        pos_8_checks[inv_card_index] = [inv_card_power,1]
        self.possible_moves['pos_8'] = pos_8_checks
        #print("checking possible moves")
        #print(self.possible_moves)

    def pos_0_defense(self,cards):
        ''' makes a defensive assessment for position 0,
        defense is not just considered when no moves are available,
        an optimal attack considers a move which leaves the attacking card
        least vulnerable to attack  by the ooponent on the next turn '''

        pos_0_defensives= {}

        pos_1_empty = False
        pos_3_empty = False

        #assess neighbours status 
        if self.board_status['pos_1'][0] == 'empty':
            pos_1_empty = True

        if self.board_status['pos_3'][0] == 'empty':
            pos_3_empty = True

        pos_1_defense={}
        pos_3_defense={}

        if pos_1_empty:
            for inv_card in cards: # pass the cards under consideration for defensive moves - all if no attacks - only attack cards in event of offensive move available 
                inv_card_index = self.inventory.index(inv_card)
                pos_1_defense[inv_card_index]=['east_defense',inv_card.get_east()]

        if pos_3_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_3_defense[inv_card_index]=['south_defense',inv_card.get_south()]

        pos_0_defensives =[pos_1_defense,pos_3_defense]
        while {} in pos_0_defensives:
            pos_0_defensives.remove({})

        self.defensive_moves['pos_0'] = pos_0_defensives


    def pos_1_defense(self,cards):
        ''' 1 will consider 0, 2 and 4 '''

        pos_1_defensives= {}

        pos_0_empty = False
        pos_2_empty = False
        pos_4_empty = False

        #assess neighbours status 
        if self.board_status['pos_0'][0] == 'empty':
            pos_0_empty = True

        if self.board_status['pos_2'][0] == 'empty':
            pos_2_empty = True

        if self.board_status['pos_4'][0] == 'empty':
            pos_4_empty = True

        pos_0_defense={}
        pos_2_defense={}
        pos_4_defense={}

        if pos_0_empty:
            for inv_card in cards: # pass the cards under consideration for defensive moves - all if no attacks - only attack cards in event of offensive move available 
                inv_card_index = self.inventory.index(inv_card)
                pos_0_defense[inv_card_index]=['west_defense',inv_card.get_west()]

        if pos_2_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_2_defense[inv_card_index]=['east_defense',inv_card.get_east()]

        if pos_4_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_4_defense[inv_card_index]=['south_defense',inv_card.get_south()]

        pos_1_defensives =[pos_0_defense, pos_2_defense, pos_4_defense] # if one of these are empty it's still included - below will remove the empties 
        while {} in pos_1_defensives:
            pos_1_defensives.remove({})

        self.defensive_moves['pos_1'] = pos_1_defensives

    def pos_2_defense(self,cards):
        ''' 2 will consider 1 and 5 '''

        pos_2_defensives= {}

        pos_1_empty = False
        pos_5_empty = False

        pos_1_defense={}
        pos_5_defense={}


        #assess neighbours status 
        if self.board_status['pos_1'][0] == 'empty':
            pos_1_empty = True

        if self.board_status['pos_5'][0] == 'empty':
            pos_5_empty = True


        if pos_1_empty:
            for inv_card in cards: # pass the cards under consideration for defensive moves - all if no attacks - only attack cards in event of offensive move available 
                inv_card_index = self.inventory.index(inv_card)
                pos_1_defense[inv_card_index]=['west_defense',inv_card.get_west()]

        if pos_5_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_5_defense[inv_card_index]=['south_defense',inv_card.get_south()]

        pos_2_defensives =[pos_1_defense, pos_5_defense]
        while {} in pos_2_defensives:
            pos_2_defensives.remove({})

        self.defensive_moves['pos_2'] = pos_2_defensives


    def pos_3_defense(self,cards):
        ''' 3 will consider 0, 4 and 6 '''

        pos_3_defensives= {}

        pos_0_empty = False
        pos_4_empty = False
        pos_6_empty = False

        #assess neighbours status 
        if self.board_status['pos_0'][0] == 'empty':
            pos_0_empty = True

        if self.board_status['pos_4'][0] == 'empty':
            pos_4_empty = True

        if self.board_status['pos_6'][0] == 'empty':
            pos_6_empty = True

        pos_0_defense={}
        pos_4_defense={}
        pos_6_defense={}
        

        if pos_0_empty:
            for inv_card in cards: # pass the cards under consideration for defensive moves - all if no attacks - only attack cards in event of offensive move available 
                inv_card_index = self.inventory.index(inv_card)
                pos_0_defense[inv_card_index]=['north_defense',inv_card.get_north()]

        if pos_4_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_4_defense[inv_card_index] = ['east_defense',inv_card.get_east()]

        if pos_6_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_6_defense[inv_card_index] = ['south_defense',inv_card.get_south()]


        pos_3_defensives =[pos_0_defense, pos_4_defense, pos_6_defense]
        while {} in pos_3_defensives:
            pos_3_defensives.remove({})
        
        self.defensive_moves['pos_3'] = pos_3_defensives


    def pos_4_defense(self,cards):
        ''' 4 will consider 1,3,5 and 7'''

        pos_4_defensives= {}

        pos_1_empty = False
        pos_3_empty = False
        pos_5_empty = False   
        pos_7_empty = False 

        pos_1_defense={}
        pos_3_defense={}
        pos_5_defense={}
        pos_7_defense={}

        #assess neighbours status 
        if self.board_status['pos_1'][0] == 'empty':
            pos_1_empty = True

        if self.board_status['pos_3'][0] == 'empty':
            pos_3_empty = True

        if self.board_status['pos_5'][0] == 'empty':
            pos_5_empty = True

        if self.board_status['pos_7'][0] == 'empty':
            pos_7_empty = True

        if pos_1_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_1_defense[inv_card_index] = ['north_defense',inv_card.get_north()]

        if pos_3_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_3_defense[inv_card_index] = ['west_defense',inv_card.get_west()]

        if pos_5_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_5_defense[inv_card_index] = ['east_defense',inv_card.get_east()]

        if pos_7_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_7_defense[inv_card_index] = ['south_defense',inv_card.get_south()]

        pos_4_defensives =[pos_1_defense, pos_3_defense, pos_5_defense, pos_7_defense]
        while {} in pos_4_defensives:
            pos_4_defensives.remove({})
        
        self.defensive_moves['pos_4'] = pos_4_defensives


    def pos_5_defense(self,cards):
        ''' 5 will consider 2,4 and 8'''

        pos_5_defensives= {}

        pos_2_empty = False
        pos_4_empty = False
        pos_8_empty = False   
         
        pos_2_defense={}
        pos_4_defense={}
        pos_8_defense={}

        #assess neighbours status 
        if self.board_status['pos_2'][0] == 'empty':
            pos_2_empty = True

        if self.board_status['pos_4'][0] == 'empty':
            pos_4_empty = True

        if self.board_status['pos_8'][0] == 'empty':
            pos_8_empty = True


        if pos_2_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_2_defense[inv_card_index] = ['north_defense',inv_card.get_north()]

        if pos_4_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_4_defense[inv_card_index] = ['west_defense',inv_card.get_west()]

        if pos_8_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_8_defense[inv_card_index] = ['south_defense',inv_card.get_south()]


        pos_5_defensives =[pos_2_defense, pos_4_defense, pos_8_defense]
        while {} in pos_5_defensives:
            pos_5_defensives.remove({})
        
        self.defensive_moves['pos_5'] = pos_5_defensives

    def pos_6_defense(self,cards):
        ''' 6 will consider 3 and 7 '''

        pos_6_defensives= {}

        pos_3_empty = False
        pos_7_empty = False

        pos_3_defense={}
        pos_7_defense={}
   
        #assess neighbours status 
        if self.board_status['pos_3'][0] == 'empty':
            pos_3_empty = True

        if self.board_status['pos_7'][0] == 'empty':
            pos_7_empty = True


        if pos_3_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_3_defense[inv_card_index] = ['north_defense',inv_card.get_north()]

        if pos_7_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_7_defense[inv_card_index] = ['east_defense',inv_card.get_east()]

        pos_6_defensives =[pos_3_defense, pos_7_defense]
        while {} in pos_6_defensives:
            pos_6_defensives.remove({})
        
        self.defensive_moves['pos_6'] = pos_6_defensives

    def pos_7_defense(self,cards):
        ''' 7 will consider 6,4 and 8 '''

        pos_7_defensives= {}

        pos_6_empty = False
        pos_4_empty = False
        pos_8_empty = False   

        pos_6_defense={}
        pos_4_defense={}
        pos_8_defense={}
         

        #assess neighbours status 
        if self.board_status['pos_6'][0] == 'empty':
            pos_6_empty = True

        if self.board_status['pos_4'][0] == 'empty':
            pos_4_empty = True

        if self.board_status['pos_8'][0] == 'empty':
            pos_8_empty = True


        if pos_6_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_6_defense[inv_card_index] = ['west_defense',inv_card.get_west()]

        if pos_4_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_4_defense[inv_card_index] = ['north_defense',inv_card.get_north()]

        if pos_8_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_8_defense[inv_card_index] = ['east_defense',inv_card.get_east()]

        pos_7_defensives =[pos_6_defense, pos_4_defense, pos_8_defense]
        while {} in pos_7_defensives:
            pos_7_defensives.remove({})
        
        self.defensive_moves['pos_7'] = pos_7_defensives

    def pos_8_defense(self,cards):
        ''' 8 will consider 5 and 7 '''

        pos_8_defensives= {}

        pos_5_empty = False
        pos_7_empty = False

        pos_5_defense = {}
        pos_7_defense = {}
   
        #assess neighbours status 
        if self.board_status['pos_5'][0] == 'empty':
            pos_5_empty = True

        if self.board_status['pos_7'][0] == 'empty':
            pos_7_empty = True


        if pos_5_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_5_defense[inv_card_index] = ['north_defense',inv_card.get_north()]

        if pos_7_empty:
            for inv_card in cards: 
                inv_card_index = self.inventory.index(inv_card)
                pos_7_defense[inv_card_index] = ['west_defense',inv_card.get_west()]

        pos_8_defensives =[pos_5_defense, pos_7_defense]
        while {} in pos_8_defensives:
            pos_8_defensives.remove({})
        
        self.defensive_moves['pos_8'] = pos_8_defensives
          


# create a loop to run test games 

#deck = Deck() 
#board = Board()
#blue_player = CPU(board)
#red_player = CPU(board)



#board.state_of_board()
def play_game():
        # instantiations
    deck = Deck() 
    board = Board()
    blue_player = Player(board)
    red_player = CPU(board)

    # deal to CPU and player 
    deck.deal_to_player(blue_player)
    deck.deal_to_player(red_player)

    while board.spaces_filled < 9:
        pprint.pprint(board.ret_board_in_play())


        print("blue Player score",board.blue_score)
        print("red CPU score",board.red_score)

        print("red inv")
        red_player.show_inventory()
        print("blue_inv")
        blue_player.show_inventory()

        player_input = input("play card in format inv_card, pos:  ")

        # cards to be played here 
        # extract message 
        card_pos = player_input.split(',')
        position = card_pos[0]
        index = int(card_pos[1])
        card = blue_player.inventory[index]


        blue_player.play_card(position,card,index)

        pprint.pprint(board.ret_board_in_play())

        print("red inv")
        red_player.show_inventory()
        print("blue_inv")
        blue_player.show_inventory()

        if board.spaces_filled != 9:
            # then red player plays  
            red_player.make_move()

    if board.blue_score > board.red_score:
        print("You win")
    else:
        print("You lose human, CPU wins!")

def play_game_red_first():
        # instantiations
    deck = Deck() 
    board = Board()
    blue_player = Player(board)
    red_player = CPU(board)

    # deal to CPU and player 
    deck.deal_to_player(blue_player)
    deck.deal_to_player(red_player)

    while board.spaces_filled < 9:
        # then red player plays 
        red_player.make_move()



        pprint.pprint(board.ret_board_in_play())


        print("blue Player score",board.blue_score)
        print("red CPU score",board.red_score)

        print("red inv")
        red_player.show_inventory()
        print("blue_inv")
        blue_player.show_inventory()

        player_input = input("play card in format inv_card, pos:  ")

        # cards to be played here 
        # extract message 
        card_pos = player_input.split(',')
        position = card_pos[0]
        index = int(card_pos[1])
        card = blue_player.inventory[index]


        blue_player.play_card(position,card,index)

        pprint.pprint(board.ret_board_in_play())

        print("red inv")
        red_player.show_inventory()
        print("blue_inv")
        blue_player.show_inventory()



    if board.blue_score > board.red_score:
        print("You win")
    else:
        print("You lose human, CPU wins!")

#deck = Deck() 
#board = Board()
#blue_player = CPU(board)
#red_player = CPU(board)

'''

def cpu_v_cpu():
    # instantiations


    # deal to CPU and player 
    deck.deal_to_player(blue_player)
    deck.deal_to_player(red_player)

    while board.spaces_filled < 9:
        
        pprint.pprint(board.ret_board_in_play())

        print("red inv")
        red_player.show_inventory()
        print("blue_inv")
        blue_player.show_inventory()



        # then red player plays 
        red_player.make_move()
        blue_player.make_move()

        pprint.pprint(board.ret_board_in_play())

        print("red inv")
        red_player.show_inventory()
        print("blue_inv")
        blue_player.show_inventory()

'''
#cpu_v_cpu()
play_game()
#play_game_red_first()



#blue_player.play_card('pos_3',blue_player.inventory[0],4)
#blue_player.play_card('pos_1',blue_player.inventory[3],3)

#print("**********blue",board.blue_score)
#print("red",board.red_score)

#red_player.make_move()

#print("Inventory after")
#red_player.show_inventory()

#print("blue",board.blue_score)
#print("red",board.red_score)

#print(board.ret_board_in_play())


#print("blue",board.blue_score)
#print("red",board.red_score)

#board.adjust_scores('blue')

#print("blue",board.blue_score)
#print("red",board.red_score)






# what get's passed to the defensive methods is:
#   if there are attacks we pass those to assess their defense relative to the attack
#   if there are no attacks we pass all the possible spaces and pick the best move 

# tests 

# check if deck builds and we have alternating colours - yes 
#deck_test = Deck()

# initalise board 
#board = Board()

# define some players 
#blue_player = Player(board)
#red_player = CPU(board)

#deck_test.deal_to_player(blue_player)
#deck_test.deal_to_player(red_player)

#for card in blue_player.inventory:
#    print(card.get_colour())
#    card.show_compass_values()

#for card in red_player.inventory:
#    print(card.get_colour()) # colours correct
#    card.show_compass_values() # shows cards values on the poles 

# test if our attack method works? 




# checks - max out blue card stats - minimise red card stats and test all combat
# max out the attacking poles stats 
#print("Blue card before")
#blue_player.inventory[0].show_compass_values()
#blue_player.inventory[0].set_west(1)
#blue_player.inventory[0].set_south(1)
#blue_player.inventory[0].set_north(1)
#blue_player.inventory[0].set_east(1)
#print("Blue card after")
#blue_player.inventory[0].show_compass_values()
#
#blue_player.inventory[1].set_west(1)
#blue_player.inventory[1].set_south(1)
#blue_player.inventory[1].set_north(1)
#blue_player.inventory[4].set_east(9)


# red card - these should be defeated by blue - minimise stats for debugging 
#print("red before")
#red_player.inventory[1].show_compass_values()
#red_player.inventory[1].set_east(9)
#red_player.inventory[1].set_north(9)
#red_player.inventory[1].set_south(9)
#red_player.inventory[1].set_west(9)
#
#print("red after")
#red_player.inventory[1].show_compass_values()

#red_player.inventory[0].set_east(9)
#red_player.inventory[0].set_north(9)
#red_player.inventory[0].set_south(9)
#red_player.inventory[0].set_west(9)
#
#red_player.inventory[2].set_east(9)
#red_player.inventory[2].set_north(9)
#red_player.inventory[2].set_south(9)
#red_player.inventory[2].set_west(9)
#
#red_player.inventory[3].set_east(9)
#red_player.inventory[3].set_north(9)
#red_player.inventory[3].set_south(9)
#red_player.inventory[3].set_west(9)
#
#red_player.inventory[4].set_east(9)
#red_player.inventory[4].set_north(9)
#red_player.inventory[4].set_south(9)
#red_player.inventory[4].set_west(9)



#board.state_of_board()

#print(board.ret_board_in_play())

#print("Inventory before")