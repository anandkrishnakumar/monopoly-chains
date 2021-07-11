#!/usr/bin/env python3

# Import the random package
import random

import numpy as np
# Import the matplotlib pyplot package
import matplotlib.pyplot as plt

# A function to generate two random numbers within the range 1 <= i <= 6 and add them together
def rollTwoDice():
    return random.randint(1,6) + random.randint(1,6)

#-------------------------------------------------

# A function to normalise the counters by the sum of the counts
def normalise(counters):

    # Count the total number of entries
    total = 0.
    for counter in counters:
        total = total + counter

    # Divide each counter value by the total
    for i in range(len(counters)):
        counters[i] = counters[i] / total

#-------------------------------------------------

# A function to create a histogram
def plot(x, y):
    pyplot.bar(x, y)
    pyplot.xlabel('Monopoly board square (n)')
    pyplot.ylabel('Probability of landing on square P(n)')
    pyplot.show()

#=================================================

# A class to describe a deck of cards
class Deck:
    def __init__(self, ncards, results):
        # Store the number of cards
        self.ncards = ncards

        # Initialise all cards to have no function
        self.cards = [ None ]*self.ncards

        # Check if the number of results is within range
        nresults = len(results)
        assert nresults <= self.ncards, "Error: to many card types for number of cards."

        # Set the moving cards to be at the front of the deck
        for i in range(nresults):
            self.cards[i] = results[i]

        # Set the next card to be drawn.
        self.nextCard = 0

    #-----------------------------------------------

    def shuffle(self):
        random.shuffle(self.cards)

    #-----------------------------------------------

    def draw(self):
        # Draw the current card
        card = self.cards[self.nextCard]

        # Step to the next place in the list, wrapping around if necessary.
        self.nextCard = self.nextCard + 1
        if self.nextCard >= self.ncards:
            self.nextCard = 0

        # Return the card
        return card

#=================================================

class MonopolySimulation:
    def __init__(self):

        # The position of the chance and community chest squares
        self.chance = [7, 22, 36]
        self.communityChest = [2, 17, 33]

        self.chanceDeck = None
        self.communityChestDeck = None
        self.createCardDecks()

        # The number of squares on the board
        self.nsquares = 40

        # A list to contain the total value rolled.
        self.counters=[0.]*self.nsquares

        # A variable to hold the current position
        self.currentPosition = 0
        
        # to keep track if in jail
        self.inJail = 0
        self.jail = 0
        self.just_visiting = 0

    #-----------------------------------------------

    # Build the card decks
    def createCardDecks(self):

        # Create two lists to hold possible results from picking a card
        chanceResults = []
        communityChestResults = []

        # These are all commands to go to a square
        chanceResults += [ (0, 0) ] # Advance to GO
        chanceResults += [ (0, 11) ] # Advance to Pall Mall
        chanceResults += [ (0, 10) ] # Go to Jail
        chanceResults += [ (0, 15) ] # Take a trip to Marylebone Station
        chanceResults += [ (0, 39) ] # Advance to Mayfair
        chanceResults += [ (0, 24) ] # Advance to Trafalgar square

        # This is an offset
        chanceResults += [ (1, -3) ] # Go back three spaces

        # Now create the deck of cards
        self.chanceDeck = Deck(16, chanceResults) # There are sixteen cards in the deck.
        self.chanceDeck.shuffle() # Call this once at the start of the game.

        # These are all commands to go to a square
        communityChestResults += [ (0, 0) ] # Advance to GO
        communityChestResults += [ (0, 10) ] # Go to Jail
        communityChestResults += [ (2, 0) ] # Pay 10 pounds or take a chance

        # Now create the deck of cards
        self.communityChestDeck = Deck(16, communityChestResults) # There are sixteen cards in the deck.
        self.communityChestDeck.shuffle() # Call this once at the start of the game.

    #-----------------------------------------------

    def movePlayer(self):
        # roll the dice
        totalValue = rollTwoDice()
        
        if self.inJail in [1, 2]:
            if totalValue < 12:
                self.inJail += 1
                self.jail += 1
                return
        elif self.inJail == 3:
            if totalValue < 12:
                self.inJail = 0
                self.just_visiting += 1
                return

        # Move the player to the next position
        self.currentPosition = self.currentPosition + totalValue

        # If the player has moved past the last square, wrap the board around.
        if self.currentPosition >= self.nsquares:
            self.currentPosition = self.currentPosition - self.nsquares

        # Check that the value is within range, to protect the list index limits.
        assert self.currentPosition >= 0 and self.currentPosition < self.nsquares, "Error: current position is out of range."

        # Count the current position on the board
        if self.currentPosition == 10:
            self.just_visiting += 1
        self.counters[self.currentPosition] = self.counters[self.currentPosition] + 1.

    #-----------------------------------------------

    def evaluateCard(self, card):
        # If the card does not move the player
        if card == None:
            return

        # The type of action and the setting that is associated with it
        (typeOfAction, setting) = card

        # A command to move to a square
        if typeOfAction == 0:
            self.currentPosition = setting
            self.counters[self.currentPosition] = self.counters[self.currentPosition] + 1.    # Count the current position
            return

        # A command to apply an offset
        elif typeOfAction == 1:
            self.currentPosition = self.currentPosition + setting
            self.counters[self.currentPosition] = self.counters[self.currentPosition] + 1.    # Count the current position
            return

        # A command to take a chance
        elif typeOfAction == 2:
            if random.random() > 0.5: # Player chooses chance 1/2 the time at random
                self.evaluateCard(self.chanceDeck.draw())
            return
        
        if self.currentPosition == 10:
            self.inJail = 1
            self.jail += 1

        assert False, "Error: card action %d is out of range" % typeOfAction

    #-----------------------------------------------

    def checkAction(self):

        # Check if the player has landed on a chance square
        for i in self.chance:
            if i == self.currentPosition:
                self.evaluateCard(self.chanceDeck.draw())
                return

        # Check if the player has landed on a community chest square
        for i in self.communityChest:
            if i == self.currentPosition:
                self.evaluateCard(self.communityChestDeck.draw())
                return

        # Check if the player should go to jail
        if self.currentPosition == 30:
            self.currentPosition = 10 # Send them to the jail square
            self.inJail = 1
            self.jail += 1
            self.counters[self.currentPosition] = self.counters[self.currentPosition] + 1.    # Count the current position
            return

    #-----------------------------------------------

    def play(self, nRolls):
        # Print a message
        # print("Rolling two dice " + str(nRolls) + " times...")

        # Roll the dice
        for i in range(nRolls):
            # Move the player and count the square the player landed on
            self.movePlayer()

            # Check if the player has landed on an action square
            # If the player has landed on a square, then move them as necessary
            # and count the square that they land on.
            self.checkAction()

def simulate(nRolls=1000000):
    # Set the number of rolls
    nRolls = nRolls
    m = MonopolySimulation()
    m.play(nRolls)
    counters = np.array(m.counters)
    counters[30] = m.jail
    counters[10] = m.just_visiting
    
    # Total probability is always defined as 1.
    # Therefore, have to divide by the total number of counted values.
    # normalise(counters)
    counters /= nRolls
    
    # # Now print out the probabilities for each of the combinations
    # print("The probabilities of landing on a given Monopoly square after " + str(nRolls) + " rolls")
    # for i in range(len(counters)):
    #     # Need to add one, since Python counts from zero.
    #     print(" P("+str(i)+")="+str(counters[i]))
    # print("where P(n) is the probability of landing on the nth Monopoly board square")
    
    # # Create a bar chart display
    # plot(range(len(counters)),counters)
    
    return counters

def n_rolls_prob(n):
    simulation_probs = np.zeros((10000, 40))
    for i in range(10000):
        simulation_probs[i] = simulate(n)
    # AFTER n DICE ROLLs
    return np.mean(simulation_probs, 0)


#Lets rank our probabilities for the tiles
Names = ['Go','Old Kent Road','Chest 1','Whitechapel Road','Income Tax','Station 1',
          'The Angel Islington','Chance 1','Euston Road','Pentonville Road','Just Visiting',
          'Pall Mall','Utility 1','Whitehall','Northumberland Avenue','Station 2',
          'Bow Street','Chest 2','Marlborough Street','Vine Street','Free Parking',
          'Strand','Chance 2','Fleet Street','Trafalgar Square','Station 3','Leicester Squre',
          'Coventry Street','Utility 2','Picadilly','Jail','Regent Street','Oxford Street',
          'Chest 3','Bond Street','Station4','Chance 3','Park Lane','Super Tax','Mayfair']

Colours = ['lavender','tab:brown','lavender','tab:brown','lavender','k','c','lavender','c','c','lavender','m','lavender','m','m',
            'k','tab:orange','lavender','tab:orange','tab:orange','lavender','r','lavender','r','r','k','yellow',
            'yellow','lavender','yellow','lavender','g','g','lavender','g','k','lavender','b','lavender','b']

##################################### n turns plots

# fig, ax = plt.subplots(2, 2)
# fig.set_size_inches(34.5, 21.5)

# probs = n_rolls_prob(1)
# ax[0, 0].bar(range(len(probs)),probs,color=Colours)
# ax[0, 0].set_xticks(range(len(probs)))
# ax[0, 0].set_xticklabels(Names, rotation=90, fontsize=22)
# ax[0, 0].get_yaxis().set_visible(False)

# probs = n_rolls_prob(2)
# ax[0, 1].bar(range(len(probs)),probs,color=Colours)
# ax[0, 1].set_xticks(range(len(probs)))
# ax[0, 1].set_xticklabels(Names, rotation=90, fontsize=22)
# ax[0, 1].get_yaxis().set_visible(False)

# probs = n_rolls_prob(3)
# ax[1, 0].bar(range(len(probs)),probs,color=Colours)
# ax[1, 0].set_xticks(range(len(probs)))
# ax[1, 0].set_xticklabels(Names, rotation=90, fontsize=22)
# ax[1, 0].get_yaxis().set_visible(False)

# probs = n_rolls_prob(4)
# ax[1, 1].bar(range(len(probs)),probs,color=Colours)
# ax[1, 1].set_xticks(range(len(probs)))
# ax[1, 1].set_xticklabels(Names, rotation=90, fontsize=22)
# ax[1, 1].get_yaxis().set_visible(False)

# fig.tight_layout()
# fig.savefig("4turns_probs.pdf", bbox_inches='tight', pad_inches = 0)
    
##################################### FINAL PLOT
probs = simulate()
fig, ax = plt.subplots()
fig.set_size_inches(16.5, 10.5)
ax.bar(range(len(probs)), probs, color=Colours)
ax.set_xticks(range(len(probs)))
ax.set_xticklabels(Names, rotation=90, fontsize=22)
ax.tick_params(axis='y', labelsize=22)

fig.tight_layout()
fig.savefig("comp_probs.pdf", bbox_inches='tight', pad_inches=0)