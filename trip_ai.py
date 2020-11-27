#### YOU DON'T NEED IT TO BE PERFECT - JUST VIABLE

# trip ai should flip cards when available (especially if multis are available) - default agression 
# in the event where a flip is not available - trip ai should be capable of playing a sensible defensive card
# trip ai should be as efficent/conservative as possible with inventory 

# going to need an efficient way to read the board 
# going to need a way to read the inventory

# for empty squares on board - these are options 
# search for blue (player) cards 
# target these for attack 

# could store max north,east,west,south - attack options - or better yet arrays/dicts of attack poles 
# eg north_vals=[4,7,9,2]
# assess eg south opponent vulnerabilities 
# select most conservative kill - based on overall card value (cumulative score based on sum of poles)
# execute kill 

# a defensive move should take the weakest edges of your card and place them at the edges of the board 
# strong edges should be exposed to play 
# in situations where kills arent available 
# 'dead' cards -player or AI - should be considered an edge 

## issues 
# sometimes the most conserative option is not optimal 
# is there a way to asses a kill with the least amount of exposure to the attacking card after the move (the defensive model)
# ie defense priority after viable kill strategies are assessed - least exposure afterwards 