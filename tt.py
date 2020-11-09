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

    def get_colour(self):
        return self.blue_or_red 
    
    def set_colour(self,colour): 
        self.blue_or_red = colour

# deck class will generate the deck 
class Deck():
    num_cards = 10
    card_values=[1,2,3,4,5,6,7,8,9]
    cards=[]

    def __init__(self):
        for i in range(0,self.num_cards):
            self.cards.append(Card(i,choice(self.card_values),choice(self.card_values),choice(self.card_values),choice(self.card_values)))

# each card can occupy a position on the board R1: 0,1,2  R2: 3,4,5  R3: 7,8,9
class Board():
    #board_spaces = 9
    def __init__(self):
        self.spaces_filled = 0
        self.positions = {'pos_0':'empty','pos_1':'empty','pos_2':'empty',
                        'pos_3':'empty','pos_4':'empty','pos_5':'empty',
                        'pos_6':'empty','pos_7':'empty','pos_8':'empty'}

    def accept_card(self,position,card):
        ''' card places into position - not very 'oopy' consider revision''' 
        self.positions[position] = card
        self.spaces_filled += 1 # increment board occupancy 

    #def display_board

# tests 

# check if deck builds 
deck_test = Deck()
print(deck_test.cards[0].get_colour())
deck_test.cards[0].set_colour('blue')
print(deck_test.cards[0].get_colour())

# check if board can accept cards into positions on the board 
board_test = Board()
board_test.accept_card('pos_1',deck_test.cards[0])
print("board test")
print(board_test.positions['pos_1'].get_colour())

# game logic 
# if a space is empty a card can be placed in that position
# # if a player (blue) has a higher number next to a lower number of opponent (red) card 
# --> then you flip that card and this adds to that players (initially 5-5) 

# nect we need to simulate the logic of turning/defeating cards on the board 