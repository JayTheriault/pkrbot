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
        
        values = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']

        card_strength = {v:values.index(v) for v in values}
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
            
        
        if street==0:#pre flop strategy
            
            if cards[0][0]==cards[1][0]:#pairs
                return RaiseAction()
            
             if cards[0][0]==self.values[12] or cards[1][0]==self.values[12]:#rwhenever there is an Ace
                    return RaiseAction()

            elif cards[0][1]!=cards[1][1]:#different suit absolutes
                if self.values.index[cards[0][0]]+self.values.index[cards[1][0]]<10:#folding on low values
                    return FoldAction()
                elif self.values.index[cards[0][0]]+self.values.index[cards[1][0]]>16:
                    return RaiseAction()

                elif cards[0][0]==self.values[8] and cards[1][0]==self.values[3]:
                    return FoldAction()
                elif cards[0][0]==self.values[3] and cards[1][0]==self.values[8]:
                    return FoldAction()

                elif cards[0][0]==self.values[8] and cards[1][0]==self.values[2]:
                    return RaiseAction()
                elif cards[0][0]==self.values[2] and cards[1][0]==self.values[8]:
                    return RaiseAction()
                elif cards[0][0]==self.values[7] and cards[1][0]==self.values[3]:
                    return RaiseAction()
                elif cards[0][0]==self.values[3] and cards[1][0]==self.values[7]:
                    return RaiseAction()








            elif  cards[0][1]==cards[1][1]:#same suit absolutes
                if cards[0][0]==self.values[0] or if cards[1][0]==self.values[0]:
                    if self.values.index[cards[0][0]]+self.values.index[cards[1][0]]<9#folding on low values
                        return FoldAction()

                elif self.values.index[cards[0][0]]+self.values.index[cards[1][0]]>11:#raising high
                    return RaiseAction()
                elif cards[0][0]==self.values[1] or cards[1][0]==self.values[1]:
                    if self.values.index[cards[0][0]]+self.values.index[cards[1][0]]<11:
                        if self.values.index[cards[0][0]]+self.values.index[cards[1][0]]>4:
                            return FoldAction()
                elif cards[0][0]==self.values[6] and cards[1][0]==self.values[5]:
                    return RaiseAction()
                elif cards[0][0]==self.values[5] and cards[1][0]==self.values[6]:
                    return RaiseAction()
                elif cards[0][0]==self.values[5] and cards[1][0]==self.values[4]:
                    return RaiseAction()
                elif cards[0][0]==self.values[4] and cards[1][0]==self.values[5]:
                    return RaiseAction()




#code to be copied in small and big for kings w 2-8 w opposite


            elif active==True:#big blind
               
                return CallAction()

            else:#small blind

                return RaiseAction() #maybe call under 10 value


            #yellow=[jack opp 7-10, diff 13 and up, same 5 and 4]
            #red=[ rest of diff, same 2 and 3]
            #green=[rest of same]
            #if cards[0][0]==self.values[0] and cards[1][0]==self.values[10] and cards[0][1]==cards[1][1]:
            #small blind goes second
            #call=match check=next raise=big fold=quit
            #green raise
            #yellow small raie big call
            #light orange small call red call
            #dark orange small call red fold
            #red fold fold











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



    def updateCardStrength(self, my_delta, previous_state, street, my_cards, opp_cards):
        board_cards = previous_state.deck[:street]
        
        if self.checkFlush(my_cards, board_cards) or self.checkFlush(opp_cards, board_cards):
            print('flush')
            print(my_cards, opp_cards, board_cards)
            pass

        if my_delta == 0:
            #check for same high card
            #share high card or high pair

            #check for pairs, if either of us has pair that both don't have we know there must be a straight

            #check if we have the same high card, if so then do nothing

            #if different high cards swap highest card with highest shared card
            pass
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







def CreateValueDict():
    """all u need to do is plug in the values found online"""
    
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
    
    
    
    
    
    vallist=[]
    
    #print(len(pre_flop_val_list))
    for i in range(182):
        carddict[handcombos[i]]=vallist[i]

    return carddict







def PreFlopStrat():
    """filled with pre flop values"""


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
    
    
    
    
    
    pre_flop_val_list=[50, 1.7,1.8,2,2,2.1,2.5,3.7,6.5,8.8,13,19,48,50,10,13,7.1,2.5,2.7,4.9,8,11,14,20,50,50,24,16,14,10,7,11,14,16,26,50,50,29,24,19,14,12,16,24,32,50,50,36,31,27,25,19,29,36,50,50,43,36,36,32,20,49,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,1.4,1.4,1.5,1.5,1.6,2,2,3,5,7,12,29,50,2,2,2,2,2,2,3,5,7.5,13,32,50,2,2,2,2,3,4,5,8,13,35,50,2,3,3,4,4,6,9,14,37,50,11,7,5,6,7,10,15,35,50,16,11,10,9,10,16,41,50,21,18,14,13,19,43,50,32,29,24,24,45,50,46,46,50,50,50,50,50,50,50,50,50,50,50,50]
    
    #print(len(pre_flop_val_list))
    for i in range(182):
        carddict[handcombos[i]]=pre_flop_val_list[i]

    return carddict​






if __name__ == '__main__':
    run_bot(Player(), parse_args())



