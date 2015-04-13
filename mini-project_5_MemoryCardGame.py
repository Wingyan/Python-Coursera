# implementation of card game - Memory

import simplegui
import random

NUM_OF_CARDS = 16
CARD_WIDTH = 50
CARD_HEIGHT = 100
width = 0
card = 0
state = 0
firsttry = 0
secondtry = 0
counter = 0


# helper function to initialize globals
def new_game():
    global deck, exposed, CARD_WIDTH, width, card, state, counter, firsttry, secondtry
    deck= []
    exposed = []
    for i in range(NUM_OF_CARDS):
        deck.append(i%8)
        exposed.append(False)
    random.shuffle(deck)
    
    counter = 0
    label.set_text("Turns = " + str(counter))
    
    width = CARD_WIDTH * NUM_OF_CARDS 
    state = 0
    firsttry = None
    secondtry = None
    

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global card, state, firsttry, secondtry, deck, counter
    card = pos[0] // 50
    
    if exposed[card] == False:
        exposed[card] = True
        if state == 0:
            firsttry = card
            state = 1
        elif state == 1:
            secondtry = firsttry
            firsttry = card
            state = 2
        else:
            if deck[secondtry] == deck[firsttry]:
                exposed[firsttry] = True
                exposed[secondtry] = True
            else:
                exposed[firsttry] = False
                exposed[secondtry] = False
            counter += 1
            label.set_text("Turns = " + str(counter))
            firsttry = card
            state = 1
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global CARD_WIDTH, CARD_HEIGHT, deck, exposed, width, card, state
    textpos = 10
    i = 0
    for card in deck:
        xpos = width - (CARD_WIDTH * (len(deck) - i))
        if exposed[i] == True:
            canvas.draw_polygon([(xpos,0), (xpos + CARD_WIDTH,0), (xpos + CARD_WIDTH, CARD_HEIGHT), (xpos, CARD_HEIGHT)], 2, "White")
            canvas.draw_text(str(card), [textpos,70], 48, "White")
        elif exposed[i] == False:
            canvas.draw_polygon([(xpos,0), (xpos + CARD_WIDTH,0), (xpos + CARD_WIDTH, CARD_HEIGHT), (xpos, CARD_HEIGHT)], 2, "White", "Black")
        i += 1
        textpos += CARD_WIDTH


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric