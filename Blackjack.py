# blackjack

import random
suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

# Card class

class Card:

	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

	def __str__(self):
		return f'{self.rank} of {self.suit}'

# Deck class

class Deck:

	def __init__(self):
		self.deck = []
		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit, rank))
	# shuffle function
	def shuffle(self):
		random.shuffle(self.deck)
	# deal card function, removes one card from the deck
	def deal_card(self):
		return self.deck.pop()

# Player hand Class

class Hand:

	def __init__(self):
		self.cards = []
		self.value = 0
		self.aces = 0

	def add_card(self, card):

		self.cards.append(card)
		self.value += values[card.rank]

		if card.rank == 'Ace':
			self.aces += 1

	# function to adjust for ace if needed
	def adjust_ace(self):

		while self.aces > 0 and self.value > 21:
			self.value -= 10
			self.aces -= 1

# chips Class

class Chips:

	def __init__(self):
		self.total = 100
		self.bet = 0

	def win_bet(self):
		self.total = self.total + self.bet

	def lose_bet(self):
		self.total = self.total - self.bet
		if self.total <= 0:
			print('Out of chips. You might owe money...')
		else:
			print(self.total)

# GENERAL FUNCTIONS #

def take_bet(chips):

	while chips.bet == 0:
		chips.bet = int(input('How many chips would you like to bet? Enter a numeric value higher than 0: '))

		if chips.bet > chips.total:
			print(f'Not enough chips. You have {chips.total} chips remaining.')
			chips.bet = 0

def hit(deck, hand):

	hand.add_card(deck.deal_card())
	hand.adjust_ace()

def hit_or_stand(deck, hand):

	# make more specific with a tuple/list and indexing
	global playing

	while True:
		hit_choice = input('Would you like to hit or stand? Enter H or S? ')

		if hit_choice[0].lower() == 'h':
			hit(deck, hand)
		elif hit_choice[0].lower() == 's':
			print("Player stands, Dealer's turn.")
			playing = False
		else:
			print('Try again, enter h or s')
			continue
		break

# PLAYER/DEALER SHOW HAND FUNCTIONS #

def show_some(player, dealer):

	# Player Info
	print("Player Info:")
	print("Cards:")
	print(*player.cards, sep='\n')
	print(f"Card Value: {player.value}\n")

	# Dealer Info
	print("Dealer Info:")
	print('Cards:')
	print('<hidden>', *dealer.cards[1:], sep='\n')

def show_all(player, dealer):

	# Player Info
	print("Player Info:")
	print("Cards:")
	print(*player.cards, sep='\n')
	print(f"Card Value: {player.value}\n")

	# Dealer Info
	print("Dealer Info:")
	print("Cards:")
	print(*dealer.cards, sep='\n')
	print(f"Card Value: {dealer.value}")

# END GAME OUTCOMES #

def player_wins(player, dealer, chips):

	print('Player wins!')
	chips.win_bet()

def player_busts(player, dealer, chips):

	print('Player busts!')
	chips.lose_bet()

def dealer_wins(player, dealer, chips):

	print('Dealer wins!')
	chips.lose_bet()

def dealer_busts(player, dealer, chips):

	print('Dealer busts!')
	chips.win_bet()

def push(player, dealer):
	print('Dealer and player tie! Game pushes.')

# GAME LOGIC #

while True:

	print('Welcome to Blackjack!')

	deck = Deck()
	deck.shuffle()

	# player setup
	player_hand = Hand()
	player_hand.add_card(deck.deal_card())
	player_hand.add_card(deck.deal_card())

	player_chips = Chips()

	# dealer setup
	dealer_hand = Hand()
	dealer_hand.add_card(deck.deal_card())
	dealer_hand.add_card(deck.deal_card())

	# bet
	take_bet(player_chips)

	# show hands, one dealer card is hidden
	show_some(player_hand, dealer_hand)

	while playing:

		hit_or_stand(deck, player_hand)

		show_some(player_hand, dealer_hand)

		if player_hand.value > 21:
			player_busts(player_hand, dealer_hand, player_chips)
			break

	# dealer has to hit until 17 or bust
	if player_hand.value <= 21:

		while dealer_hand.value < 17:
			hit(deck, dealer_hand)

		show_all(player_hand, dealer_hand)

		# END GAME #
		if dealer_hand.value > 21:
			dealer_busts(player_hand, dealer_hand, player_chips)
		elif dealer_hand.value > player_hand.value:
			dealer_wins(player_hand, dealer_hand, player_chips)
		elif dealer_hand.value < player_hand.value:
			player_wins(player_hand, dealer_hand, player_chips)
		else:
			push(player_hand, dealer_hand)

	# player winnings/losses
	print(f"Player's winnings: {player_chips.total}")

	# play again check
	new_game = input("Play again? Y or N: ")

	if new_game[0].lower() == 'y':
		playing = True
		continue
	else:
		print('Thanks for playing!')
		break
