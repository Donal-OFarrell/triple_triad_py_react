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

class Player():
    '''Represents a player of Triple Triad (Squall v AI eventually) '''
    def __init__(self,colour):
        self.colour = colour
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

    def deal_to_player(self,player): # pass player object to the class
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

    def state_of_board(self):
        ''' displays the baord in it's current state'''
        print(self.positions)
        
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



# test all - done all combat works! 
# define scoring 
# introduce ability to view state of board visually 
# create ai 




        
# is it going to be an issue where the check is a compound check? ie a position wont have an attribute until a card is placed there 
# could split it onto different lines 


    
# check if it changes colour 
       

    #def display_board

# tests 

# check if deck builds and we have alternating colours - yes 
deck_test = Deck()
#print(deck_test.cards[0].get_colour())
#j=0
#for card in deck_test.cards:
#    print (j,card.get_colour())
#    j +=1 

# define some players 
blue_player = Player('blue')
red_player = Player('red')

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
blue_player.inventory[0].set_west(9)
blue_player.inventory[0].set_south(9)
blue_player.inventory[0].set_north(9)
blue_player.inventory[0].set_east(9)
print("Blue card after")
blue_player.inventory[0].show_compass_values()


# red card - these should be defeated by blue - minimise stats for debugging 
print("red before")
red_player.inventory[1].show_compass_values()
red_player.inventory[1].set_east(1)
red_player.inventory[1].set_north(1)
red_player.inventory[1].set_south(1)
red_player.inventory[1].set_west(1)

print("red after")
red_player.inventory[1].show_compass_values()

red_player.inventory[0].set_east(1)
red_player.inventory[0].set_north(1)
red_player.inventory[0].set_south(1)
red_player.inventory[0].set_west(1)

red_player.inventory[2].set_east(1)
red_player.inventory[2].set_north(1)
red_player.inventory[2].set_south(1)
red_player.inventory[2].set_west(1)

red_player.inventory[3].set_east(1)
red_player.inventory[3].set_north(1)
red_player.inventory[3].set_south(1)
red_player.inventory[3].set_west(1)


######### pos_0 attacking pos 1 checks
# place red card [1] on pos_1 
#print(board.get_positions())
#board.accept_card('pos_1',red_player.inventory[1])
#print(board.get_positions())

#print("pos1 card colour")
#print(board.get_positions()['pos_1'][0].get_colour()) # it's red 

# let's attack it 

#board.accept_card('pos_0',blue_player.inventory[0])

#print("pos 1 card colour after fight")
#print(board.get_positions()['pos_1'][0].get_colour()) # blue now - excellent - hardcoded but still great work!


#board.state_of_board()

######### check position 1 combat 

# place red card [1] on pos_3 
#print(board.get_positions())
board.accept_card('pos_5',red_player.inventory[0])
#print(board.get_positions())

board.accept_card('pos_7',red_player.inventory[1])

#board.accept_card('pos_8',red_player.inventory[2])

#board.accept_card('pos_7',red_player.inventory[3])

#card colour
print(board.get_positions()['pos_5'][0].get_colour()) # it's red 
print(board.get_positions()['pos_7'][0].get_colour()) # it's red 
#print(board.get_positions()['pos_8'][0].get_colour()) # it's red 
#print(board.get_positions()['pos_7'][0].get_colour()) # it's red 


# now generate the attack 
board.accept_card('pos_8',blue_player.inventory[0])

print(board.get_positions()['pos_5'][0].get_colour()) # it's red 
print(board.get_positions()['pos_7'][0].get_colour()) # it's red 
#print(board.get_positions()['pos_8'][0].get_colour()) # it's red 
#print(board.get_positions()['pos_7'][0].get_colour()) # it's red 


