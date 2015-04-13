# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        hand = ''
        for item in self.cards:
            hand += item.get_suite() + item.get_rank() + ' '
        return "Hand: "

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        number_of_aces = 0
        for each_card in self.cards:
            if each_card.get_rank() == 'A':
                number_of_aces += 1               
            value += VALUES[each_card.get_rank()]
        
        if number_of_aces > 0:
            if value + 10 < 21:
                return value + 10
            else:
                return value
        return value
   
    def draw(self, canvas, pos): 
        # draw a hand on the canvas
        for c in self.cards:
            c.draw(canvas,  pos)
            pos[0] += CARD_SIZE[0] * 1.1
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards=[]	
        for i in SUITS:
            for j in RANKS:
                card=Card(i, j)
                self.cards.append(card)

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        s = ''
        for card in self.cards:
            s += str(card) + ' '
        return 'Deck Contains: ' + string


#define event handlers for buttons
def deal():
    global outcome, in_play, score, result, dealer, player, deck
    
    #if in_play: #if the Deal button is hit during a game player loses
    #    score = score - 1
    #    outcome = "You lose!"
    #else:
    #    outcome = "Hit or stand?"
    
    result = ''
    outcome = 'Hit or  Stand?'
    if in_play: # if deal is presses between game, player looses
        score -= 1
        print result    
    
    player = Hand()
    dealer = Hand()
    deck = Deck()
    deck.shuffle()
    
    for i in range(0, 2): #deal two cards to each 
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
    
    in_play = True
    

def hit():
    global in_play, player, deck, outcome, score
    
    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())
    
    # if busted, assign a message to outcome, update in_play and score
    if player.get_value() > 21:
        outcome = "Busted! You Deal again?"
        score -= 1
        in_play = False
 
   
     
def stand():  
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global outcome, in_play, dealer, player, game_deck, score
    
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        if player.get_value() > dealer.get_value() or dealer.get_value() > 21:
            score = score + 1
            outcome = "Player wins! Deal again?"
        else:
            score = score - 1
            outcome = "Dealer wins! Deal again?"
    in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
   
    global outcome, score, dealer, player
    
    canvas.draw_text('Blackjack!', (220, 40), 36, 'Red', 'monospace')
    canvas.draw_text('Dealer', (100, 125), 24, 'Black', 'monospace')
    dealer.draw(canvas, [100, 150])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (136, 200), CARD_BACK_SIZE)
    canvas.draw_text('Player', (100, 375), 24, 'Black', 'monospace')
    player.draw(canvas, [100, 400])
    canvas.draw_text(outcome, (150, 300), 24, 'White', 'monospace')
    canvas.draw_text('Score: ' + str(score), (350, 125), 24, 'Red', 'monospace')
 


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric