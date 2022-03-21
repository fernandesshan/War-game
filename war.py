# This is a War Game between two virtual players
import random

# used tuple for suits and ranks because we know it won't change
suits = ('Hearts', 'Clubs', 'Diamonds', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}


# CARD class is used to hold property of a single card
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


'''DECK class is used to 
- create a new deck
- shuffle the cards in the deck
- deal one card from the deck'''


class Deck:
    def __init__(self):
        # New deck created once per game
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)

    def shuffle(self):
        # shuffles card in place and returns None
        random.shuffle(self.all_cards)

    def deal_one(self):
        # removes one card from top of the deck of all_cards
        return self.all_cards.pop()


'''PLAYER class is used to
- create a new player
- hold cards in hand of each player
- remove one card from cards_in_hand for each player
- add card to cards_in_hand for each player '''


class Player:
    def __init__(self, name):
        self.name = name
        self.cards_in_hand = []

    def __str__(self):
        return f'Player {self.name} has {len(self.cards_in_hand)} cards'

    def remove_one_card(self):
        # removes one card that was added first to the list
        return self.cards_in_hand.pop(0)

    ''' Extend is used if more than 1 card is added 
        because we want only elements to add not nested lists to cards in hand.
        Can't use only extend because extend need a list to add, not a single element. '''

    def add_cards(self, cards):
        """ Check if cards parameter is a list(in case of multiple cards after a war).
            We know cards_in_hand is a list pre-defined.
            Can check with type([]) alternatively"""
        if type(self.cards_in_hand) == type(cards):
            self.cards_in_hand.extend(cards)
        else:
            self.cards_in_hand.append(cards)


''' Check if players have sufficient cards (additional 5 cards) in hand, in case of war '''


def check_none_won(p1, p2):
    # global game_on
    if len(p1.cards_in_hand) <= 6:
        print(f"\n{p1.name} has insufficient cards to declare war. {p2.name} won. Game Over!")
        # game_on = False
        return False
    elif len(p2.cards_in_hand) <= 6:
        print(f"\n{p2.name} has insufficient cards to declare war. {p1.name} won. Game Over!")
        # game_on = False
        return False
    else:
        return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    '''
    We assume that game_on is True which means players have sufficient cards to play at the beginning
    We assume that War will happen in the 1st round because this will handle the case of consecutive war cases
    round_num is used to see the number of round the game is played
    '''
    game_on = True
    in_war = True
    round_num = 0

    # Create two virtual players
    player1 = Player('Shan')
    player2 = Player('Andu')

    # create a new deck and shuffle it. Done once per game
    deck = Deck()
    deck.shuffle()

    ''' split deck of cards between 2 players
       range(26) is used since a deck has 52 cards/ 2 player = 26 '''
    for i in range(26):
        player1.add_cards(deck.deal_one())
        player2.add_cards(deck.deal_one())

    ''' game_on will be false if any one player wins '''
    while game_on:
        round_num += 1
        print(f"\nRound {round_num} ")

        '''card1 and card2 are the cards on table from player 1 and player 2 respectively.
           These cards will reset after each round. '''
        card1 = []
        card2 = []

        ''' in_war will be false if values of both player cards are not same '''
        while in_war:
            # Error (print(card1) was showing memory location not str value like 'Two of Diamonds'):
            # because had used deal_one from deck class without()
            card1.append(player1.remove_one_card())
            card2.append(player2.remove_one_card())

            ''' card[-1] (i.e the last cards in the card list) 
            is used to compare the latest card added to the table when the war occurred '''
            print(f'Player 1- {player1.name} card is : ', card1[-1])
            print(f'Player 2- {player2.name}  card is : ', card2[-1])

            '''If Player 1 last card is higher, add cards to player1'''
            if card1[-1].value > card2[-1].value:
                print(f'In round {round_num}, player 1 {player1.name} won')
                '''Error: [[],[]]
                   Add card1 and card 2 individually. Else when at war, will give error to add array of array 
                   Eg. adding player1.add_cards[card1,card2] where card2=[c1,c2,..list of cards to add]'''
                player1.add_cards(card1)
                player1.add_cards(card2)
                print(f'Players cards after round {round_num} = {len(player1.cards_in_hand)}, {len(player2.cards_in_hand)}')
                in_war = False
                # break

            elif card1[-1].value < card2[-1].value:
                '''Error: if comments place above elif, got invalid syntax error
                If Player 2 is higher, add cards to player2 '''
                print(f'In round {round_num}, player 2 {player2.name} won')
                '''Error: [[],[]]
                   Add card1 and card 2 individually. Else when at war, will give error to add array of array 
                   Eg. adding player2.add_cards[card1,card2] where card2=[c1,c2,..list of cards to add]'''
                player2.add_cards(card1)
                player2.add_cards(card2)
                print(
                    f'Players cards  after round {round_num} = {len(player1.cards_in_hand)} , {len(player2.cards_in_hand)} ')
                in_war = False
                # break

            else:
                print(f'\nWAR! Place additional 5 cards on the table')
                # print(f'Players cards  after round {round_num} = {len(player1.cards_in_hand)} , {len(player2.cards_in_hand)} ')
                for num in range(5):
                    card1.append(player1.remove_one_card())
                    card2.append(player2.remove_one_card())
        in_war = True
        game_on = check_none_won(player1, player2)
