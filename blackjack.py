import os
import sys
import random
import click

__author__ = "Andrew Hariri"
__email___ = "hariria@usc.edu"

# Ascii inpsired by @see https://codereview.stackexchange.com/questions/82103/ascii-fication-of-playing-cards

blackjackASCII = """
$$$$$$$\  $$\        $$$$$$\   $$$$$$\  $$\   $$\   $$$$$\  $$$$$$\   $$$$$$\  $$\   $$\ 
$$  __$$\ $$ |      $$  __$$\ $$  __$$\ $$ | $$  |  \__$$ |$$  __$$\ $$  __$$\ $$ | $$  |
$$ |  $$ |$$ |      $$ /  $$ |$$ /  \__|$$ |$$  /      $$ |$$ /  $$ |$$ /  \__|$$ |$$  / 
$$$$$$$\ |$$ |      $$$$$$$$ |$$ |      $$$$$  /       $$ |$$$$$$$$ |$$ |      $$$$$  /  
$$  __$$\ $$ |      $$  __$$ |$$ |      $$  $$<  $$\   $$ |$$  __$$ |$$ |      $$  $$<   
$$ |  $$ |$$ |      $$ |  $$ |$$ |  $$\ $$ |\$$\ $$ |  $$ |$$ |  $$ |$$ |  $$\ $$ |\$$\  
$$$$$$$  |$$$$$$$$\ $$ |  $$ |\$$$$$$  |$$ | \$$\\$$$$$$  |$$ |  $$ |\$$$$$$  |$$ | \$$\ 
\_______/ \________|\__|  \__| \______/ \__|  \__|\______/ \__|  \__| \______/ \__|  \__|
"""

class Card:

    # Constructor for card, takes a value and suit
    def __init__(self, valueAndSuit):
        self.value = valueAndSuit[0:valueAndSuit.find(":")]
        self.suit = valueAndSuit[valueAndSuit.find(":") + 1:]
        self.largeCard = []
        self.setLargeCard()
        if (self.suit == "♠"):
            self.suitString = "spades"
        elif (self.suit == "♦"):
            self.suitString = "diamonds"
        elif (self.suit == "♥"):
            self.suitString = "hearts"
        else:
            self.suitString = "clubs"

    # gets the value
    def getValue(self):
        return self.value
    
    # Prints a large version of the card
    def setLargeCard(self):
        self.largeCard.append('┌─────────┐')
        self.largeCard.append(f'│{"1" if self.value == "10" else " "}{"0" if self.value == "10" else self.value}       │') 
        self.largeCard.append('│         │')
        self.largeCard.append('│         │')
        self.largeCard.append(f'│    {self.suit}    │')
        self.largeCard.append('│         │')
        self.largeCard.append('│         │')
        self.largeCard.append(f'│      {"1" if self.value == "10" else " "}{"0" if self.value == "10" else self.value} │')
        self.largeCard.append('└─────────┘')

    # Prints 
    def printLargeCard(self):
        for x in self.largeCard:
            print(x)
    
    # Get numerical value of the card
    def getNumValue(self):
        if (self.value.isnumeric()):
            return int(self.value)
        elif (self.value == "A"):
            return 1
        else:
            return 10
    
    # print card as a message
    def printCardString(self):
        print(self.value + " of " + self.suitString)

    # announce card 
    def sayCard(self):
        os.system(f"say {self.printCardString()}")


# Method to initialize the deck with 52 unique cards
def initializeDeck():
    deck = []
    cardValues = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['♠', '♦', '♥', '♣']
    for cardValue in cardValues:
        for suit in suits:
            deck.append(cardValue + ":" + suit)
    return deck

# Print the deck
def printDeck(deck):
    for x in range(0, 9):
        for card in deck:
            print(card.largeCard[x] + "    ", end="")
        print("")

# Print the dealer deck
def printDealerDeck(deck):
    for x in range(0, 9):
        index = 0
        while(index != len(deck)):
            if (index == 0):
                print("***********" + "    ", end="")
            else:
                print(deck[index].largeCard[x] + "    ", end="")
            index += 1
        print("")



# core play logic function
def playLogic():
    print("hello and welcome to blackjack")
    while(input("press 'q' to quit or any other key to continue: ") != 'q'):
        deck = initializeDeck()
        userHand = []
        userNumAces = 0
        userTotal = 0
        dealerHand = []
        dealerNumAces = 0
        dealerTotal = 0
        print("dealing cards...")
        

        # start of round
        for x in range(4):
            randomNumber = random.randint(0, len(deck) - 1)
            card = Card(deck[randomNumber])
            if x % 2 == 0:
                userHand.append(card)
                userTotal += card.getNumValue()
                if card.getValue() == "A":
                    userNumAces += 1
            else:
                dealerHand.append(card)
                dealerTotal += card.getNumValue()
                if card.getValue() == "A":
                    dealerNumAces += 1
            del deck[randomNumber]
        
        print("--------------------- DEALER'S HAND -----------------------", end="\n\n")
        printDealerDeck(dealerHand)
        print("\n----------------------- YOUR HAND -------------------------", end="\n\n")
        printDeck(userHand)

        # stay or hit for user
        while(userTotal < 21):
            if (userTotal == 11 and userNumAces > 0):
                userTotal += 10
                break
            hitOrStay = input("would you like to hit or stay? For hit type 'h', for stay type 's': ")
            if (hitOrStay == 's'):
                break
            elif (hitOrStay == 'h'):
                randomNumber = random.randint(0, len(deck))
                card = Card(deck[randomNumber])
                userHand.append(card)
                del deck[randomNumber]
                if card.getValue() == "A":
                    dealerNumAces += 1
                    if (userTotal == 10):
                        userTotal += 11
                        break
                userTotal += card.getNumValue()
                printDeck(userHand)
            else:
                print("your input was incorrectly formatted, please try again...")
        
        if (userTotal <= 10 and userNumAces > 0):
            userTotal += 10
            userNumAces -= 1
        
        if (userTotal == 21):
            print("Congrats, you got 21 perfectly! You win")
            continue

        elif (userTotal > 21):
            print("You went bust! Would you like to play again?")
        
        else:
            print("\n--------------------- DEALER'S HAND -----------------------", end="\n\n")
            # stay or hit for user
            while(dealerTotal < 17):
                randomNumber = random.randint(0, len(deck))
                card = Card(deck[randomNumber])
                dealerHand.append(card)
                del deck[randomNumber]
                if card.getValue() == "A":
                    dealerNumAces += 1
                    if (dealerTotal == 10 ):
                        dealerTotal += 11
                dealerTotal += card.getNumValue()
                printDealerDeck(dealerHand)
                if (dealerTotal <= 10 and dealerNumAces > 0):
                    dealerNumAces -= 1
                    dealerTotal += 10
            if(dealerTotal == 21):
                printDeck(dealerHand)
                print("Dealer got 21 and wins", end="\n\n")
            elif (dealerTotal > 21 and userTotal > 21):
                printDeck(dealerHand)
                print("you both lose!")
            elif (dealerTotal > 21 and userTotal <= 21):
                printDeck(dealerHand)
                print("You win!")
            elif (dealerTotal < userTotal):
                printDeck(dealerHand)
                print("You win!")
            elif (dealerTotal > userTotal):
                printDeck(dealerHand)
                print("Dealer wins")
            elif (dealerTotal == userTotal):
                printDeck(dealerHand)
                print("You tie")

        

        
        


if __name__ == "__main__":
    print(blackjackASCII)
    # os.system("say Hello my name is Andrea!")
    playLogic()