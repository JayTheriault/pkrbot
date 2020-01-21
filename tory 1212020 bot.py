'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
import random
# from deuces.card import Card 
# from deuces import Evaluator

from pprint import pprint

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

        self.nodes = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
        self.edges = []

        self.handRankingDict = PreFlopStrat(True)
        self.carddict = PreFlopStrat()

        self.straights = []



        # card_strength = {v:self.values.index(v) for v in self.values}
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

        self.preflop = 0
        
        myraise=0
        myother=1
        theirraise=0
        theirother=1
        myaggression=(myraise/(myraise+myother))
        theiraggression=(theirraise/(theirraise+theirother))

        deltaaggression=myaggression-theiraggression


        total_continue_cost=1
        total_times=1
        av_continue_cost=(total_continue_cost/total_times)
        

        if round_num == NUM_ROUNDS:
            pprint(self.straights)

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

        self.updateCardStrength(my_delta, game_state, previous_state, street, my_cards, opp_cards)
        

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

        pot_after_continue = my_contribution + opp_contribution + continue_cost



        if ShakeOpponent()==True:
            if CallAction in legal_actions:
                return CallAction
        elif ShakeOpponent()==False:
            if RaiseAction in legal_actions:
                return RaiseAction(max_raise-1)



        my_max=0
        my_opp=0
        their_max=0
        their_opp=0



        total_continue_cost+=continue_cost
        total_times+=1



        if RaiseAction in legal_actions:
            min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise
            min_cost = min_raise - my_pip  # the cost of a minimum bet/raise
            max_cost = max_raise - my_pip  # the cost of a maximum bet/raise
        

        # if game_state.round_num == NUM_ROUNDS:
        #     print(self.edges)
        if my_stack == 0:
            return CheckAction()
        # cards = my_cards
        # if street==0 and self.preflop == 0:#pre flop strategy
            
        #     if cards[0][0]==cards[1][0]:#pairs
        #         return RaiseAction(pot_after_continue/2)
            
        #     if cards[0][0]==self.values[12] or cards[1][0]==self.values[12]: #rwhenever there is an Ace
        #         return RaiseAction(pot_after_continue/2)

        #     elif cards[0][1]!=cards[1][1]:#different suit absolutes
        #         if self.values.index(cards[0][0])+self.values.index(cards[1][0])<10:#folding on low values
        #             return CheckAction() if CheckAction in legal_actions else FoldAction()
        #         elif self.values.index(cards[0][0])+self.values.index(cards[1][0])>16:
        #             return RaiseAction(pot_after_continue/2)

        #         elif cards[0][0]==self.values[8] and cards[1][0]==self.values[3]:
        #             return CheckAction() if CheckAction in legal_actions else FoldAction()
        #         elif cards[0][0]==self.values[3] and cards[1][0]==self.values[8]:
        #             return CheckAction() if CheckAction in legal_actions else FoldAction()

        #         elif cards[0][0]==self.values[8] and cards[1][0]==self.values[2]:
        #             return RaiseAction(pot_after_continue/2)
        #         elif cards[0][0]==self.values[2] and cards[1][0]==self.values[8]:
        #             return RaiseAction(pot_after_continue/2)
        #         elif cards[0][0]==self.values[7] and cards[1][0]==self.values[3]:
        #             return RaiseAction(pot_after_continue/2)
        #         elif cards[0][0]==self.values[3] and cards[1][0]==self.values[7]:
        #             return RaiseAction(pot_after_continue/2)

        #     elif  cards[0][1]==cards[1][1]:#same suit absolutes
        #         if cards[0][0]==self.values[0] or cards[1][0]==self.values[0]:
        #             if self.values.index(cards[0][0])+self.values.index(cards[1][0]) < 9: #folding on low values
        #                 return CheckAction() if CheckAction in legal_actions else FoldAction()

        #         elif self.values.index(cards[0][0])+self.values.index(cards[1][0])>11:#raising high
        #             return RaiseAction(pot_after_continue/2)
        #         elif cards[0][0]==self.values[1] or cards[1][0]==self.values[1]:
        #             if self.values.index(cards[0][0])+self.values.index(cards[1][0])<11:
        #                 if self.values.index(cards[0][0])+self.values.index(cards[1][0])>4:
        #                     return CheckAction() if CheckAction in legal_actions else FoldAction()
        #         elif cards[0][0]==self.values[6] and cards[1][0]==self.values[5]:
        #             return RaiseAction(pot_after_continue/2)
        #         elif cards[0][0]==self.values[5] and cards[1][0]==self.values[6]:
        #             return RaiseAction(pot_after_continue/2)
        #         elif cards[0][0]==self.values[5] and cards[1][0]==self.values[4]:
        #             return RaiseAction(pot_after_continue/2)
        #         elif cards[0][0]==self.values[4] and cards[1][0]==self.values[5]:
        #             return RaiseAction(pot_after_continue/2)

        #     elif active==True:#big blind
               
        #        return CheckAction() if CheckAction in legal_actions else CallAction()

        #     else:#small blind

        #         return RaiseAction(pot_after_continue/2) #maybe call under 10 value

        #     self.preflop += 1

        # elif street == 0 and self.preflop > 0:
        #     return CheckAction() if CheckAction in legal_actions else CallAction()


        # else:
        #     #after flop
        #     if street == 3:
        #         if self.checkFlush(my_cards, board_cards) or self.check3ofKind(my_cards, board_cards) or self.check2Pair(my_cards, board_cards) or (self.checkPair(my_cards, board_cards) != False and self.values.index(self.checkPair(my_cards, board_cards)) >= 9):
        #             return RaiseAction(max_raise)

        #     if self.checkFlush(my_cards, board_cards) or self.check3ofKind(my_cards, board_cards):
        #         return RaiseAction(pot_after_continue)
        #     elif self.checkPair(my_cards, board_cards):
        #         return RaiseAction(pot_after_continue/2)
        #     elif self.values.index(self.highCard(my_cards, [])) >10:
        #         return CallAction() if continue_cost < my_contribution else FoldAction()

        highCard = self.highCard(my_cards, [])

        lowCard = my_cards[0][0] if my_cards[0][0] != highCard else my_cards[1][0]

        suited = 's' if my_cards[0][1] == my_cards[1][1] else 'o'

        starting_amount=35



        shifty=ShiftOpponent()





        starting_amount=starting_amount+8*(deltaaggression)
        starting_amount=starting_amount+(continue_cost-av_continue_cost)/25
        starting_amount=starting_amount+shifty




        if street!=0:
            if active==True: #ur big blind
                if continue_cost==max_raise:
                    theirraise+=1
                else:
                    theirother+=1



        if RaiseAction in legal_actions:
            if continue_cost==max_raise:
                #if they have a strong hand
                theirraise+=1
                starting_amount+=10
            
            elif continue_cost<(max_raise):
                #if they have a really good hand
                theirother+=1
                starting_amount+=10*(1-((max_raise-continue_cost)/max_raise))
            

        if my_stack == 0:
            myother+=1
            return CheckAction()



        if RaiseAction in legal_actions:
            
            if street != 0:
                if self.check3ofKind(my_cards, board_cards) or self.checkFlush(my_cards, board_cards):
                    myraise+=1
                    return RaiseAction(max_raise) 
                elif self.check2Pair(my_cards, board_cards) and self.highCard(my_cards, []) in self.check2Pair(my_cards, board_cards):
                    myraise+=1
                    return RaiseAction(max_raise)
                elif self.checkPair(my_cards, board_cards) and self.highCard(my_cards, []) in self.checkPair(my_cards, board_cards):
                    myraise+=1
                    return RaiseAction(max_raise)

                if continue_cost == 0:
                    myraise+=1
                    return RaiseAction(min_raise)
            else:
                if self.carddict[(self.values.index(lowCard), self.values.index(highCard)), suited]>starting_amount:
                    myraise+=1
                    return RaiseAction(max_raise)
                elif continue_cost < 5:
                    myother+=1
                    return CheckAction() if CheckAction in legal_actions else CallAction()


        if CallAction in legal_actions:
            
            if street != 0:
                if self.check3ofKind(my_cards, board_cards) or self.checkFlush(my_cards, board_cards):
                    myother+=1
                    return CallAction()
                elif self.check2Pair(my_cards, board_cards) and self.highCard(my_cards, []) in self.check2Pair(my_cards, board_cards):
                    myother+=1
                    return CallAction()
                # elif self.checkPair(my_cards, board_cards) and self.highCard(my_cards, []) in self.checkPair(my_cards, board_cards):
                #     return CallAction()
            # else:
            #     if self.carddict[(self.values.index(lowCard), self.values.index(highCard)), suited]>starting_amount:
            #         return CallAction()

        if CheckAction in legal_actions:
                    myother+=1
            return CheckAction()
        
        myother+=1
        return FoldAction()


    def checkFlush(self, cards, board_cards):
        '''
        Returns True if there is a flush, False otherwise
        '''
        clubs = []
        diamonds = []
        hearts = []
        spades = []

        for card in cards:
            if card[1] == 'c':
                clubs += card[0]
            elif card[1] == 'd':
                diamonds += card[0]
            elif card[1] == 'h':
                hearts += card[0]
            else:
                spades += card[0]

        for card in board_cards:
            if card[1] == 'c':
                clubs += card[0]
            elif card[1] == 'd':
                diamonds += card[0]
            elif card[1] == 'h':
                hearts += card[0]
            else:
                spades += card[0]

        if len(clubs) >= 5:
            return clubs
        elif len(diamonds) >= 5:
            return diamonds
        elif len(spades) >= 5:
            return spades
        elif len(hearts) >= 5:
            return hearts
        return False

    def checkPair(self, cards, board_cards):
        '''
        returns first found pair and False if no pair
        '''  
        if cards == []:
            return False
        if cards[0][0] == cards[1][0]:
            return cards[0][0]
        
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
        if cards == []:
            return False
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
        if cards == []:
            return False

        if cards[0][0] == cards[1][0]:
            for card in board_cards:
                if cards[0][0] == card[0]:
                    return cards[0][0]
        else:
            card0 = 1
            card1 = 1
            for card in board_cards:
                if card[0] == cards[0][0]:
                    card0 += 1
                if card[0] == cards[1][0]:
                    card1 += 1
            if card0 >= 3:
                return cards[0][0]
            if card1 >= 3:
                return cards[1][0]
        return False

    def highCard(self, cards, board_cards):
        high_card = self.values[0]
        for card in cards:
            if self.values.index(card[0]) > self.values.index(high_card):
                high_card = card[0]
        for card in board_cards:
            if self.values.index(card[0]) > self.values.index(high_card):
                high_card = card[0]
        return high_card

    def checkStraight(self, cards, board_cards):
        return False


    def updateCardStrength(self, my_delta, game_state, previous_state, street, my_cards, opp_cards):
        board_cards = previous_state.deck[:street]

        my_high = self.highCard(my_cards, [])
        opp_high = self.highCard(opp_cards, [])
        board_high = self.highCard([], board_cards)

        my_pair = self.checkPair(my_cards, board_cards)
        opp_pair = self.checkPair(opp_cards, board_cards)

        my_2pair = self.check2Pair(my_cards, board_cards)
        opp_2pair = self.check2Pair(opp_cards, board_cards)

        my_3ofKind = self.check3ofKind(my_cards, board_cards)
        opp_3ofKind = self.check3ofKind(opp_cards, board_cards)

        my_straight = self.checkStraight(my_cards, board_cards)
        opp_straight = self.checkStraight(opp_cards, board_cards)

        my_flush = self.checkFlush(my_cards, board_cards)
        opp_flush = self.checkFlush(opp_cards, board_cards)

        my_fullHouse = True if my_3ofKind != False and my_2pair != False else False
        opp_fullHouse = True if opp_3ofKind != False and opp_2pair != False else False

        my_4ofKind = False
        opp_4ofKind = False #TODO

        my_straightFlush = True if my_straight and my_flush else False
        opp_straightFlush = True if opp_straight and opp_flush else False

        my_besthand = opp_besthand = None
        if my_straightFlush != False:
            my_besthand = 'sf' 
        elif my_fullHouse != False:
            my_besthand = 'fh'
        elif my_flush != False:
            my_besthand = 'f'
        elif my_straight != False:
            my_besthand = 's'
        elif my_3ofKind != False:
            my_besthand = '3'
        elif my_2pair != False:
            my_besthand = '2'
        elif my_pair != False:
            my_besthand = '1'
        else:
            my_besthand = 'h'

        if opp_straightFlush != False:
            opp_besthand = 'sf' 
        elif opp_fullHouse != False:
            opp_besthand = 'fh'
        elif opp_flush != False:
            opp_besthand = 'f'
        elif opp_straight != False:
            opp_besthand = 's'
        elif opp_3ofKind != False:
            opp_besthand = '3'
        elif opp_2pair != False:
            opp_besthand = '2'
        elif opp_pair != False:
            opp_besthand = '1'
        else:
            opp_besthand = 'h'
        

        if opp_cards == []:
            pass
        elif my_flush != False or opp_flush != False:

            if my_flush != False and opp_flush != False:
                my_flush_highcard = self.highCard([], my_flush)
                opp_flush_highcard = self.highCard([], opp_flush)

                if my_delta == 0:
                    if my_flush_highcard != opp_flush_highcard:
                        print('some crazy shit just happened', my_cards, opp_cards, board_cards)
                elif my_delta > 0:
                    if self.values.index(my_flush_highcard) < self.values.index(opp_flush_highcard):
                        self.values = swapPositions(self.values, my_flush_highcard, opp_flush_highcard)
                        print('fl1', my_cards, opp_cards, board_cards)
                elif my_delta < 0:
                    if self.values.index(my_flush_highcard) > self.values.index(opp_flush_highcard):
                        self.values = swapPositions(self.values, my_flush_highcard, opp_flush_highcard)
                        print('fl2', my_cards, opp_cards, board_cards)



        elif my_delta == 0:
            # see if we have different pairs -> straight
            if my_pair != opp_pair and my_2pair == False:

                

                #if we don't share any cards, then the board must be a straight
                if my_cards[0][0] != opp_cards[0][0] and my_cards[0][0] != opp_cards[1][0] and my_cards[1][0] != opp_cards[0][0] and my_cards[1][0] != opp_cards[1][0]:
                    print('board straight', board_cards)
                    self.straights.append(([], [], board_cards))
                else:
                    print('shared straight', my_cards, opp_cards, board_cards)              #STRAIGHT
                    self.straights.append((my_cards, opp_cards, board_cards))


            #neither of us has a pair
            elif my_besthand == 'h' and opp_besthand == 'h' and my_high != opp_high:

                if my_cards[0][0] != opp_cards[0][0] and my_cards[0][0] != opp_cards[1][0] and my_cards[1][0] != opp_cards[0][0] and my_cards[1][0] != opp_cards[1][0]:
                    print('board straight', board_cards)
                    self.straights.append(([], [], board_cards))
                else:
                    print('shared straight', my_cards, opp_cards, board_cards)              #STRAIGHT
                    self.straights.append((my_cards, opp_cards, board_cards))


                #add new high card code here
        elif my_delta > 0:
            #test if we both have pairs
            if my_besthand == '1' and opp_besthand == '1' and my_pair != opp_pair:
                #if my pair is 'lower', switch it with 'higher' one
                if self.values.index(my_pair) + 4 < self.values.index(opp_pair):
                    print('my straight', my_cards, opp_cards, board_cards)                     #STRAIGHT
                    self.straights.append((my_cards, [], board_cards))
                elif self.values.index(my_pair) < self.values.index(opp_pair):
                    self.values = swapPositions(self.values, my_pair, opp_pair)
                    print('pos1', my_cards, opp_cards, board_cards)
            #test if we both have high cards only
            elif my_besthand == 'h' and opp_besthand == 'h' and my_high != opp_high:
                #if my high card is 'lower', switch it with 'higher' one
                if self.values.index(my_high) + 4 < self.values.index(opp_high):
                    print('my straight', my_cards, opp_cards, board_cards)                     #STRAIGHT
                    self.straights.append((my_cards, [], board_cards))
                elif self.values.index(my_high) < self.values.index(opp_high):
                    self.values = swapPositions(self.values, my_high, opp_high)
                    print('pos2', my_cards, opp_cards, board_cards)

            #TODO check if hand strength doesn't amkes sense --> implies straight

            pass
        elif my_delta < 0:
            #test is we both have pairs
            if my_besthand == '1' and opp_besthand == '1' and my_pair != opp_pair:
                #if opp pair is 'lower', switch it with 'higher' one
                if self.values.index(my_pair) - 4 > self.values.index(opp_pair):
                    print('opp straight', my_cards, opp_cards, board_cards)                     #STRAIGHT
                    self.straights.append(([], opp_cards, board_cards))
                elif self.values.index(my_pair) > self.values.index(opp_pair):
                    self.values = swapPositions(self.values, opp_pair, my_pair)
                    print('neg1', my_cards, opp_cards, board_cards)
            #test if we both have high cards only
            elif my_besthand == 'h' and opp_besthand == 'h' and my_high != opp_high:
                #if opp high card is 'lower', switch it with 'higher' one
                if self.values.index(my_high) - 4 > self.values.index(opp_high):
                    print('opp straight', my_cards, opp_cards, board_cards)                     #STRAIGHT
                    self.straights.append(([], opp_cards, board_cards))
                elif self.values.index(my_high) > self.values.index(opp_high):
                    self.values = swapPositions(self.values, opp_high, my_high)
                    print('neg2', my_cards, opp_cards, board_cards)


        #__________________________________________new idea partial order shit goes here_____________________________________


        #kicker card goes forever need to implement those methods later

        if my_besthand == '1' and opp_besthand == '1' and my_pair != opp_pair and opp_cards != []:
            if my_delta == 0:
                pass
            elif my_delta > 0:
                edge = (my_pair, opp_pair, game_state.round_num, 'pp') 
                if edge not in self.edges: 
                    self.edges.append(edge)
                    # print('edges = ' + str(self.edges))
            elif my_delta < 0:
                edge = (opp_pair, my_pair, game_state.round_num, 'pn')
                if edge not in self.edges:
                    self.edges.append(edge)
                    # print('edges = ' + str(self.edges))

        if my_besthand == 'h' and opp_besthand == 'h' and my_high != opp_high and opp_cards != []:
            if my_delta == 0:
                pass
            elif my_delta > 0:
                edge = (my_high, opp_high, game_state.round_num, 'hp') #FIX LATER
                if edge not in self.edges:
                    self.edges.append(edge)
                    # print('edges = ' + str(self.edges))
            elif my_delta < 0:
                edge = (opp_high, my_high, game_state.round_num, 'hn')
                if edge not in self.edges:
                    self.edges.append(edge)
                    # print('edges = ' + str(self.edges))





    def determineHandStrength(self, my_cards, board_cards, active):
        big_blind = bool(active) #small blind has position advantage
        pass

    def determinePlayerRange(self, board_cards, Opp = True):
        pass


    def HeadsUpStrategyJay(self, game_state, round_state, active):
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

        pot_after_continue = my_contribution + opp_contribution + continue_cost

        if RaiseAction in legal_actions:
            min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise
            min_cost = min_raise - my_pip  # the cost of a minimum bet/raise
            max_cost = max_raise - my_pip  # the cost of a maximum bet/raise




def PreFlopStrat(Jay = False):
    """filled with pre flop values"""
    if Jay:
        handRankingDict = {}

        card1=[0,1,2,3,4,5,6,7,8,9,10,11,12]
        card1.reverse()
        card2=[0,1,2,3,4,5,6,7,8,9,10,11,12]
        card2.reverse()

        cardcombos=[]

        handcombos=[]



        carddict={}
        for card in card1:
            for cards in card2:
                if (cards,card) not in cardcombos:
                    cardcombos.append((card,cards))
        #print(cardcombos)
        sameopp=["s","o"]
        for combo in cardcombos:
            for sign in sameopp:

                if sign == 's' and combo[0] == combo[1]:
                    pass
                else:
                    handcombos.append((combo,sign))

        #
        #pprint(handcombos)

        hand_strength = [1,8,12,10,14,11,15,13,19,18,25,21,32,24,36,31,42,30,41,35,49,38,53,46,59,
            2,16,23,20,26,22,33,29,40,37,51,44,58,50,62,54,69,60,74,63,80,71,86,
            3,28,39,34,47,43,56,52,68,61,77,67,81,72,89,76,93,82,98,88,105,
            4,45,57,55,70,65,79,75,92,85,102,90,107,95,111,97,116,104,121,
            5,64,78,73,91,84,101,96,112,106,122,108,125,114,131,118,135,
            6,83,99,94,109,103,120,113,130,123,140,126,144,132,149,
            7,100,117,110,127,119,137,129,148,139,157,142,159,
            9,115,133,124,141,134,151,143,160,152,165,
            17,128,145,138,154,147,162,156,167,
            27,136,153,146,151,155,166,
            48,150,164,158,168,
            66,163,169,
            87]

        for index in range(len(hand_strength)):
                handRankingDict[handcombos[index]] = hand_strength[index]

        # d_view = [ (v,k) for k,v in handRankingDict.items()]
        # d_view.sort() # natively sort tuples by first element
        # for v,k in d_view:
        #     print("%s: %d" % (k,v))
        return handRankingDict

    card1=[0,1,2,3,4,5,6,7,8,9,10,11,12]
    card2=[0,1,2,3,4,5,6,7,8,9,10,11,12]
    cardcombos=[]
    
    handcombos=[]
    
    
    
    carddict={}
    for card in card1:
        for cards in card2:
            if (cards,card) not in cardcombos:
                cardcombos.append((card,cards))
    #print(cardcombos)
    sameopp=["s","o"]
    for sign in sameopp:
        for combo in cardcombos:
            handcombos.append((combo,sign))
    
    
    #print(handcombos)
    
    
    
    
    
    pre_flop_val_list=[50,1.7,1.8,2,2,2.1,2.5,3.7,6.5,8.8,13,19,48,50,10,13,7.1,2.5,2.7,4.9,8,11,14,20,50,50,24,16,14,10,7,11,14,16,26,50,50,29,24,19,14,12,16,24,32,50,50,36,31,27,25,19,29,36,50,50,43,36,36,32,20,49,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,1.4,1.4,1.5,1.5,1.6,2,2,3,5,7,12,29,50,2,2,2,2,2,2,3,5,7.5,13,32,50,2,2,2,2,3,4,5,8,13,35,50,2,3,3,4,4,6,9,14,37,50,11,7,5,6,7,10,15,35,50,16,11,10,9,10,16,41,50,21,18,14,13,19,43,50,32,29,24,24,45,50,46,46,50,50,50,50,50,50,50,50,50,50,50,50]
    
    #print(len(pre_flop_val_list))
    for i in range(182):
        carddict[handcombos[i]]=pre_flop_val_list[i]

    return carddict

def swapPositions(list, pos1, pos2): 
    
    p1 = list.index(pos1)  
    p2 = list.index(pos2)
    if p1 > p2+1:
        list[p1], list[p1-1] = list[p1-1], list[p1]
        list[p2+1], list[p2] = list[p2], list[p2+1] 
        print(pos2, pos1)
    elif p2 > p1 + 1:
        list[p1], list[p1+1] = list[p1+1], list[p1]
        list[p2-1], list[p2] = list[p2], list[p2-1] 
        print(pos1, pos2)
    else:
        list[p1], list[p2] = list[p2], list[p1]
        if p1 > p2:
            print(pos2, pos1)
        else:
            print(pos1, pos2)

    print(list)
    return list



def ShakeOpponent():
    number=random.random()
    if number>.99:
        return True
    elif number<.01:
        return False
    else:
        return None
def ShiftOpponent():
    number=random.gauss(0,1)
    shift_constant=5*number
    return shift_constant






if __name__ == '__main__':
    run_bot(Player(), parse_args())


 