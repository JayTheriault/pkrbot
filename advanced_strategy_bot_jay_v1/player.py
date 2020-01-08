'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot


class Player(Bot):
    '''
    A pokerbot.
    '''

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''
        
        self.values = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']

        card_strength = {v:self.values.index(v) for v in self.values}
        #creates dictionary to see what cards win

        #create a directed graph with 13 nodes and if a certain card beats another add a node

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        my_cards = round_state.hands[active]  # your cards
        big_blind = bool(active)  # True if you are the big blind
        pass

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        previous_state = terminal_state.previous_state  # RoundState before payoffs
        street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        my_cards = previous_state.hands[active]  # your cards
        opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed

        self.updateCardStrength(my_delta, previous_state, street, my_cards, opp_cards)
        

    def get_action(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your action.
        '''
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, river, or turn respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot

        if RaiseAction in legal_actions:
            min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise
            min_cost = min_raise - my_pip  # the cost of a minimum bet/raise
            max_cost = max_raise - my_pip  # the cost of a maximum bet/raise
        

        



        if CheckAction in legal_actions:  # check-call
            return CheckAction()
        return CallAction()


    def checkFlush(self, cards, board_cards):
        '''
        Returns True if there is a flush, False otherwise

        '''
        clubs = diamonds = hearts = spades = 0

        for card in range(len(cards)):
            if cards[card][1] == 'c':
                clubs += 1
            elif cards[card][1] == 'd':
                diamonds += 1
            elif cards[card][1] == 'h':
                hearts += 1
            else:
                spades += 1

        for card in range(len(board_cards)):
            if board_cards[card][1] == 'c':
                clubs += 1
            elif board_cards[card][1] == 'd':
                diamonds += 1
            elif board_cards[card][1] == 'h':
                hearts += 1
            else:
                spades += 1

        # print('test')

        if clubs >= 5 or diamonds >= 5 or spades >= 5 or hearts >= 5:
            return True
        return False

    def checkPair(self, cards, board_cards):
        '''
        returns first found pair and False if no pair

        '''
        if cards[0][0] == cards[1][0]:
            return True
        
        for card in board_cards:
            if cards[0][0] == card[0]:
                return card[0]
            if cards[1][0] == card[0]:
                return card[0]

            for card1 in board_cards:
                for card2 in board_cards:
                    if card1[0] == card2[0] and card1 != card2:
                        return card[0]
        return False

    def check2Pair(self, cards, board_cards):
        pairs = []
        poss_values = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
        if cards[0][0] == cards[1][0]:
            if cards[0][0] in poss_values:
                pairs.append(cards[0][0])
                poss_values.remove(cards[0][0])
        
        for card in board_cards:
            if cards[0][0] == card[0]:
                if card[0] in poss_values:
                    pairs.append(card[0])
                    poss_values.remove(card[0])
            if cards[1][0] == card[0]:
                if card[0] in poss_values:
                    pairs.append(card[0])
                    poss_values.remove(card[0])

            for card1 in board_cards:
                for card2 in board_cards:
                    if card1[0] == card2[0] and card1 != card2 and card1[0] in poss_values:
                        pairs.append(card1[0])
                        poss_values.remove(card1[0])
        if len(pairs) < 2:
            return False
        return pairs

    def check3ofKind(self, cards, board_cards):
        return None

    def checkFullHouse(self, cards, board_cards):
        if self.check2Pair(cards, board_cards) and self.check3ofKind(cards, board_cards):
            return True
        return False

    def highCard(self, cards, board_cards):
        high_card = cards[0][0]
        if self.values.index(cards[1][0]) > self.values.index(high_card):
            high_card = cards[1][0]
        for card in board_cards:
            if self.values.index(card[0]) > self.values.index(high_card):
                high_card = card[0]
        return high_card


    def updateCardStrength(self, my_delta, previous_state, street, my_cards, opp_cards):
        board_cards = previous_state.deck[:street]
        
        print(self.check2Pair(my_cards, board_cards))
        if self.check2Pair(my_cards, board_cards) != False:
            print(my_cards, opp_cards, board_cards)

        if self.checkFlush(my_cards, board_cards) or self.checkFlush(opp_cards, board_cards):
            print('flush')
            print(my_cards, opp_cards, board_cards)

        elif my_delta == 0:
            # print('tie')
            # print(my_cards, opp_cards, board_cards)
            if self.checkPair(my_cards, board_cards) != self.checkPair(opp_cards, board_cards) and self.check2Pair(my_cards, board_cards) == False:
                #check for pairs, if either of us has pair that both don't have we know there must be a straight
                #straight?
                pass
            elif self.checkPair(my_cards, board_cards) == False and self.checkPair(opp_cards, board_cards) == False:
                if self.highCard(my_cards, board_cards) != self.highCard(opp_cards, board_cards):
                    if self.values.index(self.highCard(my_cards, board_cards)) > self.values.index(self.highCard(opp_cards, board_cards)):
                        #swap my high card with higest shared card
                        pass
                    else:
                        #swap opp high card with highest shared card
                        pass
                #swap value of my highest card with highest shared card value iff I think my highest card is better than highest shared card
        elif my_delta >= 0:
            #see how my hand is better than opp hand, update cards as needed

            #check if both of us have pairs
            #if so update highest card

            #check if hand strength doesn't amkes sense --> implies straight
            pass
        elif my_delta <= 0:
            #see how opp hand is better than my hand, update cards as needed
            pass


    def determineHandStrength(self, my_cards, board_cards, active):
        big_blind = bool(active) #small blind has position advantage
        pass

    def determinePlayerRange(self, board_cards, Opp = True):
        pass




if __name__ == '__main__':
    run_bot(Player(), parse_args())



 