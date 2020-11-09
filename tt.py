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



# each card can occupy a position on the board R1: 0,1,2  R2: 3,4,5  R3: 7,8,9
# board has become sort of a game class too - but the board's magic I guess :P 
class Board():
    board_spaces = 9 
    spaces_filled = 0 # when this equals above game is over 
    def __init__(self):
        self.positions = {'pos_0':['empty',self.pos_0_combat],'pos_1':['empty',self.pos_1_combat],'pos_2':'empty',
        'pos_3':'empty','pos_4':'empty','pos_5':'empty',
        'pos_6':'empty','pos_7':'empty','pos_8':'empty'}

    def accept_card(self,position,card):
        ''' card places into position - not very 'oopy' consider revision''' 
        self.positions[position][0] = card # place card 
        
        self.positions[position][1]() # then invoke the combat method for that space 

        self.spaces_filled += 1 # increment board occupancy 
    
    def get_positions(self):
        return self.positions
        
    def pos_0_combat(self):
        if self.positions['pos_1'][0] != 'empty': # then try to attack the card 
            if self.positions['pos_0'][0].get_west() > self.positions['pos_1'][0].get_east(): # if the number is bigger -> then flip the card 
    #  TO DO: create a pointer to array containing two colours - apply the opposite of attacking card
                self.positions['pos_1'][0].set_colour('blue') # flip the card - placeholder red for now 
                print("0 flipped 1") # debug checks 
    # TO DO: adjust score for red/blue player 

        if self.positions['pos_4'] != 'empty': 
            if self.positions['pos_0'][0].get_south() > self.positions['pos_3'][0].get_north():
                self.position['pos_3'].set_colour('red') # again opposite of placed card 
                print("0 flipped 3") # to colour

    def pos_1_combat(self):
        if self.positions['pos_0'] != 'empty':
            print("Placeholder")
    
# check if it changes colour 
       

    #def display_board

# tests 

# check if deck builds and we have alternating colours - yes 
deck_test = Deck()
#print(deck_test.cards[0].get_colour())
j=0
for card in deck_test.cards:
    print (j,card.get_colour())
    j +=1 

# define some players 
blue_player = Player('blue')
red_player = Player('red')

deck_test.deal_to_player(blue_player)
deck_test.deal_to_player(red_player)

for card in blue_player.inventory:
    print(card.get_colour())
    card.show_compass_values()

for card in red_player.inventory:
    print(card.get_colour()) # colours correct
    card.show_compass_values() # shows cards values on the poles 

# test if our attack method works? 

# initalise board 

board = Board()
# max out the attacking poles stats 
print("Blue card before")
blue_player.inventory[0].show_compass_values()
blue_player.inventory[0].set_west(9)
blue_player.inventory[0].set_south(9)
print("Blue card after")
blue_player.inventory[0].show_compass_values()


# these should be defeated by blue 
print("red before")
red_player.inventory[1].show_compass_values()
red_player.inventory[1].set_east(8)
print("red after")
red_player.inventory[1].show_compass_values()



#red_player.inventory[3].set_north(8)

# place red card [1] on pos_1 
print(board.get_positions())
board.accept_card('pos_1',red_player.inventory[1])
print(board.get_positions())

print(board.get_positions()['pos_1'][0].get_colour()) # it's red 

# let's attack it 

board.accept_card('pos_0',blue_player.inventory[0])


print(board.get_positions()['pos_1'][0].get_colour()) # blue now - excellent - hardcoded but still great work!




#deck_test.cards[0].set_colour('blue')
#print(deck_test.cards[0].get_colour())

# check if board can accept cards into positions on the board 
#board_test = Board()
#board_test.accept_card('pos_0',deck_test.cards[0])
#print("board test")
#print(board_test.positions['pos_0'][0].get_colour())
#print(board_test.get_positions())

# game logic 
# if a space is empty a card can be placed in that position
# # if a player (blue) has a higher number next to a lower number of opponent (red) card 
# --> then you flip that card and this adds to that players (initially 5-5) 

# next we need to simulate the logic of turning/defeating cards on the board 

# if card in -> 
# pos 0 north and west are neutral/0 , pos 1 - north neutral , pos 2 - north and east - neutral 
# pos 3 west neutral , pos 4 mothing, pos 5 east neutral 
# pos 6 south and west neutral, 7 south neutral, 8 south and east neutral 

# if neighbour colour != same and touching pole > neighbour pole - 
    # card.colur change 

# how do i program neighbours/ poles? 

# if pos is empty - then you can place card 
# have a method for each position ... 
# so you could have a list card holder and then the function for that position 
# check for neighbours when you place card  

