# from pygame import mouse
import sys
import os

from pygame.event import get_grab

MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, os.path.join(MAIN_DIR, 'includes'))

from .common import *
from .carddecks import CardDecks
from myFile import *
from .playingcard import PlayingCard

class State(object):
    def next_state(self, state):
        self.__class__ = state

    def get_state(self):
        temp = str(self.__class__).strip('\'>').split('.')
        return temp[2]

class InitialState(State):
    def __call__(self, common_vars, button_status):
        print("--------------------------------")
        common_vars.hands_status_1p = {
            'first_hand_blackjack': False,
            'first_hand_win': False,
            'first_hand_push': False,
            'first_hand_loose': False,
            'first_hand_busted': False,
            'second_hand_blackjack': False,
            'second_hand_win': False,
            'second_hand_push': False,
            'second_hand_loose': False,
            'second_hand_busted': False
        }
        common_vars.hands_status_2p = {
            'first_hand_blackjack': False,
            'first_hand_win': False,
            'first_hand_push': False,
            'first_hand_loose': False,
            'first_hand_busted': False,
            'second_hand_blackjack': False,
            'second_hand_win': False,
            'second_hand_push': False,
            'second_hand_loose': False,
            'second_hand_busted': False
        }
        common_vars.player_hands_1p = []
        common_vars.player_hands_2p = []
        hand_instance_1p = []
        hand_instance_2p = []
        common_vars.player_hands_1p.append(hand_instance_1p)
        common_vars.player_hands_2p.append(hand_instance_2p)
        common_vars.player_bets_1p = []
        common_vars.player_bets_2p = []
        common_vars.bets_pos = []
        common_vars.game_rounds += 1
        common_vars.double_downs = [False, False]
        common_vars.first_card_hidden = True
        button_status.reset()
        self.next_state(BettingStatus)

class BettingStatus(State):
    print("BettingStatus")
    _current_bet_1p = []
    _current_bet_2p = []
    _chips_visible_1p = True
    _chips_visible_2p = True

    def __call__(self, common_vars, button_status):
        if common_vars.player_cash_1p >= LOWEST_BET or sum(self._current_bet_1p) > 0 or sum(self._current_bet_2p) > 0:
            plot_chips_1p(
                common_vars.screen, 
                common_vars.player_cash_1p, 
                common_vars.chips_image_width,
                self._chips_visible_1p
                )

            plot_chips_2p(
                common_vars.screen, 
                common_vars.player_cash_2p, 
                common_vars.chips_image_width,
                self._chips_visible_2p
                )
            
            if sum(self._current_bet_1p) > 0:
                button_status.play = True
                button_status.undo_bet_1p = True
            else:
                button_status.play = False
                button_status.undo_bet_1p = False
            
            if sum(self._current_bet_2p) > 0:
                button_status.play = True
                button_status.undo_bet_2p = True
            else:
                button_status.play = False
                button_status.undo_bet_2p = False
            
            plot_buttons(common_vars.screen, button_status)

            button_collide_instance = ButtonCollideArea.get_instance(common_vars)
            chips_collide_instance = ChipsCollideArea.get_instance(common_vars)
            # TODO: ????????? ?????? ??? / ????????? ???????????? ?????? ??????
            # sound_db = SoundDB.get_instance()
            # chip_sound = sound_db.get_sound(SOUND_PATH + 'chipsstack.wav')
            temp_bet_list_1p = []
            temp_bet_list_2p = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    common_vars.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_position = pygame.mouse.get_pos()
                    if button_collide_instance.play_button_area.collidepoint(mouse_position[0], mouse_position[1])\
                            and sum(self._current_bet_1p) > 0 and sum(self._current_bet_2p) > 0:

                        common_vars.player_bets_1p.append(self._current_bet_1p)
                        common_vars.player_bets_2p.append(self._current_bet_2p)
                        common_vars.dealer_cards = []
                        common_vars.first_card_hidden = True
                        common_vars.player_deal_1p = False
                        common_vars.player_hit_1p = False
                        button_status.play = False
                        button_status.undo_bet_1p = False
                        button_status.undo_bet_2p = False

                        self._current_bet_1p = []
                        self._current_bet_2p = []
                        self._chips_visible_1p = True
                        self._chips_visible_2p = True
                        self.next_state(DealingState)
                    elif button_collide_instance.undo_bet_button_area.\
                            collidepoint(mouse_position[0], mouse_position[1])\
                            and sum(self._current_bet_1p) > 0:
                        # chip,sound.play()
                        common_vars.player_cash_1p += self._current_bet_1p.pop()
                        
                    elif  button_collide_instance.undo_bet_2p_button_area.\
                            collidepoint(mouse_position[0], mouse_position[1])\
                            and sum(self._current_bet_2p) > 0:
                        # chip,sound.play()
                        common_vars.player_cash_2p += self._current_bet_2p.pop()

                    if len(self._current_bet_1p) < 14:
                        self._chips_visible_1p = True
                        if chips_collide_instance.chip_5_area_1p.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash_1p >= 5:
                            # chip_sound.play()
                            self._current_bet_1p.append(5)
                            common_vars.player_cash_1p -= 5
                        elif chips_collide_instance.chip_10_area_1p.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash_1p >= 10:
                            # chip_sound.play()
                            self._current_bet_1p.append(10)
                            common_vars.player_cash_1p -= 10
                        elif chips_collide_instance.chip_50_area_1p.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash_1p >=50:
                            # chip_sound.play()
                            self._current_bet_1p.append(50)
                            common_vars.player_cash_1p -= 50
                        elif chips_collide_instance.chip_100_area_1p.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash_1p >=100:
                            # chip_sound.play()
                            self._current_bet_1p.append(100)
                            common_vars.player_cash_1p -= 100
                    else:
                        self._chips_visible_1p = False
                    
                    if len(self._current_bet_2p) < 14:
                        self._chips_visible_2p = True
                        if chips_collide_instance.chip_5_area_2p.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash_2p >= 5:
                            # chip_sound.play()
                            self._current_bet_2p.append(5)
                            common_vars.player_cash_2p -= 5
                        elif chips_collide_instance.chip_10_area_2p.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash_2p >= 10:
                            # chip_sound.play()
                            self._current_bet_2p.append(10)
                            common_vars.player_cash_2p -= 10
                        elif chips_collide_instance.chip_50_area_2p.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash_2p >=50:
                            # chip_sound.play()
                            self._current_bet_2p.append(50)
                            common_vars.player_cash_2p -= 50
                        elif chips_collide_instance.chip_100_area_2p.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash_2p >=100:
                            # chip_sound.play()
                            self._current_bet_2p.append(100)
                            common_vars.player_cash_2p -= 100
                    else:
                        self._chips_visible_2p = False
            temp_bet_list_1p.append(self._current_bet_1p)
            temp_bet_list_2p.append(self._current_bet_2p)
            plot_bets_1p(common_vars.screen, temp_bet_list_1p)
            plot_bets_2p(common_vars.screen, temp_bet_list_2p)
        else:
            self.next_state(FinalState)

class DealingState(State):
    def __call__(self, common_vars, button_status):
        print("DealingState")
        if is_cut_passed(common_vars.shoe_of_decks):
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)
        
        # ????????? ???????????? ?????? ????????? ?????? ????????? ??? ?????? ?????? ????????? Visible????????? ??? ????????? ???????????? hidden?????? ??????
        plot_chips_1p(common_vars.screen, common_vars.player_cash_1p, common_vars.chips_image_width, False)
        plot_chips_2p(common_vars.screen, common_vars.player_cash_2p, common_vars.chips_image_width, False)

        # TODO: ????????? ?????? ??? / ????????? ???????????? ?????? ??????
        # sound_db = SoundDB.get_instance()
        # card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        player_1p_win = 0
        player_2p_win = 0
        first_hand = 0 # ??????????????? ????????? ????????? ??? ??? ????????? ???
        if len(common_vars.dealer_cards) < 2:
            # ????????? ????????? 2?????? ????????? ?????? ????????? ????????? ?????? ????????? ????????? ?????? ?????? ????????? ?????? ??????
            common_vars.pause_time = PAUSE_TIMER1
            if not common_vars.player_hands_1p[first_hand]:
                # card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands_1p[first_hand].append(card)

            elif not common_vars.player_hands_2p[first_hand]:
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands_2p[first_hand].append(card)

            elif not common_vars.dealer_cards:
                # card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.dealer_cards.append(card)

            elif len(common_vars.player_hands_1p[first_hand]) == 1:
                # card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands_1p[first_hand].append(card)

            elif len(common_vars.player_hands_2p[first_hand]) == 1:
                # card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands_2p[first_hand].append(card)

            elif len(common_vars.dealer_cards) == 1:
                # card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.dealer_cards.append(card)

        elif not button_status.hit:
            common_vars.pause_time = 0
            value_of_dealers_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
            value_of_players_1p_hand = get_value_of_players_hand(common_vars.player_hands_1p[0])
            value_of_players_2p_hand = get_value_of_players_hand(common_vars.player_hands_2p[0])
            # 21????????? blackjack?????? ????????? ????????? 2??? ????????? ??? split??? ??? ??? ?????? ????????? ???
            if value_of_players_1p_hand == 21 and len(common_vars.player_hands_1p) != 2:
                common_vars.first_card_hidden = False
                # ?????? 2P??? ???????????????
                if value_of_players_2p_hand == 21 and len(common_vars.player_hadns_2p_) != 2:
                    # ?????? ????????? 21????????? ????????? ??? push ???????????? ?????? ?????? ??????
                    if value_of_dealers_hand == 21:
                        common_vars.pause_time = PAUSE_TIMER3
                        
                        # TODO: ?????? ???????????????
                        plot_results_1p(common_vars.screen, common_vars.text_font, 'Push')
                        plot_results_2p(common_vars.screen, common_vars.text_font, 'Push')
                        # ????????? ????????? push ???????????? ?????? True??? ??????
                        common_vars.hands_status_1p['first_hand_push'] = True
                        common_vars.hands_status_2p['first_hand_push'] = True
                        # ?????? ????????????
                        common_vars.player_cash_1p += sum(common_vars.player_bets_1p[0])
                        common_vars.player_cash_2p += sum(common_vars.player_bets_2p[0])
                        # ???????????? ????????? ????????? ????????? ????????? ?????? ?????? 
                        common_vars.dealer_last_hand = value_of_dealers_hand
                        common_vars.pause_time = PAUSE_TIMER3
                        # ????????? ?????????????????? ???????????? ?????? ????????? ??? ?????? ?????? ?????? ???????????? ?????????
                        button_status.reset()
                        self.next_state(InitialState)
                    # ????????? 21?????? ????????? ???????????? ???????????? ??????????????? ???????????? ??????
                    else:
                        common_vars.pause_time = PAUSE_TIMER3
                        plot_results_1p(common_vars.screen, common_vars.text_font, 'Black Jack!')
                        plot_results_2p(common_vars.screen, common_vars.text_font, 'Black Jack!')
                        common_vars.hands_status_1p['first_hand_blackjack'] = True
                        common_vars.hands_status_2p['first_hand_blackjack'] = True
                        common_vars.player_cash_1p += sum(common_vars.player_bets_1p[0])
                        common_vars.player_cash_1p += int(sum(common_vars.player_bets_1p[0]) * 1.5)
                        common_vars.player_cash_2p += sum(common_vars.player_bets_2p[0])
                        common_vars.player_cash_2p += int(sum(common_vars.player_bets_2p[0]) * 1.5)

                        # ???????????? ????????? ????????? ????????? ????????? ?????? ?????? 
                        common_vars.dealer_last_hand = value_of_dealers_hand
                        common_vars.pause_time = PAUSE_TIMER3
                        # ????????? ?????????????????? ???????????? ?????? ????????? ??? ?????? ?????? ?????? ???????????? ?????????
                        button_status.reset()
                        self.next_state(InitialState)
                # 1P??? ?????????, 2P??? ?????????
                else:
                    # ?????? ????????? ???????????????
                    # ?????? ?????? ?????? ???
                    # 1p??? ?????? ???????????? 2p??? ??? ????????? ??????
                    if value_of_dealers_hand == 21:
                        print("304 / value_of_dealers_hand == 21")
                        common_vars.pause_time = PAUSE_TIMER3
                        # TODO: ?????? ???????????????
                        plot_results_1p(common_vars.screen, common_vars.text_font, 'Push')
                        plot_results_2p(common_vars.screen, common_vars.text_font, 'Loose')
                        # ????????? ????????? push ???????????? ?????? True??? ??????
                        common_vars.hands_status_1p['first_hand_push'] = True
                        # ????????? ????????? push ???????????? ?????? True??? ??????
                        common_vars.hands_status_2p['first_hand_loose'] = True
                        # ?????? ????????????
                        common_vars.player_cash_1p += sum(common_vars.player_bets_1p[0])
                        # ???????????? ????????? ????????? ????????? ????????? ?????? ?????? 
                        common_vars.dealer_last_hand = value_of_dealers_hand
                        common_vars.pause_time = PAUSE_TIMER3
                        # ????????? ?????????????????? ???????????? ?????? ????????? ??? ?????? ?????? ?????? ???????????? ?????????
                        button_status.reset()
                        self.next_state(InitialState)
                    # ????????? 21?????? ????????? ???????????? ???????????? ??????????????? ???????????? ???????????????
                    # 2P??? ???????????? ???????????? ????????? ?????? ???????????????
                    else:
                        print("324")
                        common_vars.pause_time = PAUSE_TIMER3
                        plot_results_1p(common_vars.screen, common_vars.text_font, 'Black Jack!')
                        common_vars.hands_status_1p['first_hand_blackjack'] = True
                        print(player_1p_win)
                        if player_1p_win == 0:
                            player_1p_win += 1
                            common_vars.player_cash_1p += sum(common_vars.player_bets_1p[0])
                            common_vars.player_cash_1p += int(sum(common_vars.player_bets_1p[0]) * 1.5)

            elif value_of_players_2p_hand == 21 and len(common_vars.player_hands_2p) != 2:
                common_vars.first_card_hidden = False
                # ?????? 2P??? ???????????????
                if value_of_players_1p_hand == 21 and len(common_vars.player_hadns_1p_) != 2:
                    # ?????? ????????? 21????????? ????????? ??? push ???????????? ?????? ?????? ??????
                    if value_of_dealers_hand == 21:
                        common_vars.pause_time = PAUSE_TIMER3
                        # TODO: ?????? ???????????????
                        plot_results_1p(common_vars.screen, common_vars.text_font, 'Push')
                        plot_results_2p(common_vars.screen, common_vars.text_font, 'Push')
                        # ????????? ????????? push ???????????? ?????? True??? ??????
                        common_vars.hands_status_1p['first_hand_push'] = True
                        common_vars.hands_status_2p['first_hand_push'] = True
                        # ?????? ????????????
                        common_vars.player_cash_1p += sum(common_vars.player_bets_1p[0])
                        common_vars.player_cash_2p += sum(common_vars.player_bets_2p[0])
                        # ???????????? ????????? ????????? ????????? ????????? ?????? ?????? 
                        common_vars.dealer_last_hand = value_of_dealers_hand
                        common_vars.pause_time = PAUSE_TIMER3
                        # ????????? ?????????????????? ???????????? ?????? ????????? ??? ?????? ?????? ?????? ???????????? ?????????
                        button_status.reset()
                        self.next_state(InitialState)
                    # ????????? 21?????? ????????? ???????????? ???????????? ??????????????? ???????????? ??????
                    else:
                        common_vars.pause_time = PAUSE_TIMER3
                        plot_results_1p(common_vars.screen, common_vars.text_font, 'Black Jack!')
                        plot_results_2p(common_vars.screen, common_vars.text_font, 'Black Jack!')
                        common_vars.hands_status_1p['first_hand_blackjack'] = True
                        common_vars.hands_status_2p['first_hand_blackjack'] = True
                        common_vars.player_cash_1p += sum(common_vars.player_bets_1p[0])
                        common_vars.player_cash_1p += int(sum(common_vars.player_bets_1p[0]) * 1.5)
                        common_vars.player_cash_2p += sum(common_vars.player_bets_2p[0])
                        common_vars.player_cash_2p += int(sum(common_vars.player_bets_2p[0]) * 1.5)

                        # ???????????? ????????? ????????? ????????? ????????? ?????? ?????? 
                        common_vars.dealer_last_hand = value_of_dealers_hand
                        common_vars.pause_time = PAUSE_TIMER3
                        # ????????? ?????????????????? ???????????? ?????? ????????? ??? ?????? ?????? ?????? ???????????? ?????????
                        button_status.reset()
                        self.next_state(InitialState)
                        
                # 2P??? ?????????, 1P??? ?????????
                else:
                    # ?????? ????????? ???????????????
                    if value_of_dealers_hand == 21:
                        common_vars.pause_time = PAUSE_TIMER3
                        # TODO: ?????? ???????????????
                        plot_results_2p(common_vars.screen, common_vars.text_font, 'Push')
                        # ????????? ????????? push ???????????? ?????? True??? ??????
                        common_vars.hands_status_2p['first_hand_push'] = True
                        # ?????? ????????????
                        common_vars.player_cash_2p += sum(common_vars.player_bets_1p[0])
                    # ????????? 21?????? ????????? ???????????? ???????????? ??????????????? ???????????? ??????
                    else:
                        print("2p??? ?????????????????? 1p??? ????????????.")
                        common_vars.pause_time = PAUSE_TIMER3
                        plot_results_2p(common_vars.screen, common_vars.text_font, 'Black Jack!')
                        common_vars.hands_status_2p['first_hand_blackjack'] = True
                        if player_2p_win == 0:
                            player_2p_win += 1
                        common_vars.player_cash_2p += sum(common_vars.player_bets_2p[0])
                        common_vars.player_cash_2p += int(sum(common_vars.player_bets_2p[0]) * 1.5)

            # ?????? ??????????????? ????????? 2?????? ????????? ???????????? ??? ??? ?????????
            elif len(common_vars.player_hands_1p) != 2 and is_possible_split(common_vars.player_hands_1p[0]):
                # ???????????? ????????? ????????? ???????????? ?????? ?????? double bet??? ???????????? ?????? ??? True False??? ????????? ????????? ?????? ??????
                button_status.split = can_double_bet(common_vars.player_bets_1p, common_vars.player_cash_1p)
                button_status.hit = True
            # ?????? ?????? ????????? ???????????? ?????? ?????? ????????? ???????????? ??? ??? hit?????? true??? ??????
            else:
                button_status.hit = True
        else:
            button_status.hit = True
            button_status.stand = True
            button_status.double_down = can_double_bet(common_vars.player_bets_1p, common_vars.player_cash_1p)
            value_of_players_1p_hand = get_value_of_players_hand(common_vars.player_hands_1p[0])
            value_of_players_2p_hand = get_value_of_players_hand(common_vars.player_hands_2p[0])

        # ?????? ?????? ??????
        plot_buttons(common_vars.screen, button_status)

        # print(common_vars.player_hands_1p[0], len(common_vars.dealer_cards) == 2)
        # bettingResult = betResult(value_of_players_hand)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common_vars.done = True
            if event.type == pygame.KEYDOWN:
                value_of_players_1p_hand = get_value_of_players_hand(common_vars.player_hands_1p[0])
                value_of_players_2p_hand = get_value_of_players_hand(common_vars.player_hands_2p[0])
                # TODO:
                player_1p = betting(common_vars.player_hands_1p[0], common_vars.dealer_cards[1], value_of_players_1p_hand)
                player_2p = betting(common_vars.player_hands_2p[0], common_vars.dealer_cards[1], value_of_players_2p_hand)
                # 2p??? ?????? ???????????? ??????????????? 1p??? ?????? ??????
                if common_vars.hands_status_2p['first_hand_blackjack'] == True:
                    if player_1p == HIT:
                        # card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_1p[first_hand].append(card)
                        button_status.split = False
                        button_status.double_down = False
                        self.next_state(PlayerHitState)
                    elif player_1p == STAND:
                        self.next_state(DealerInitState)
                    elif button_status.double_down:
                        common_vars.player_cash_1p -= sum(common_vars.player_bets_1p[0])
                        common_vars.player_bets_1p.append(common_vars.player_bets_1p[0])
                        # card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_1p[first_hand].append(card) # Pull a third card
                        common_vars.double_downs[first_hand] = True
                        button_status.double_down = False
                        self.next_state(DealerInitState)
                    elif button_status.split:
                        common_vars.player_cash_1p -= sum(common_vars.player_bets_1p[0])
                        common_vars.player_bets_1p.append(common_vars.player_bets_1p[0])
                        # button_status.split = False
                        button_status.reset()
                        self.next_state(SplitState)
                # 1p??? ?????? ???????????? ??????????????? 2p??? ?????? ??????
                elif common_vars.hands_status_1p['first_hand_blackjack'] == True:
                    if player_2p == HIT:
                        print("player_2p == HIT")
                        # card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_2p[first_hand].append(card)
                        button_status.split = False
                        button_status.double_down = False
                        self.next_state(PlayerHitState)
                    elif player_2p == STAND:
                        print("player_2p == STAND")
                        self.next_state(DealerInitState)
                    elif button_status.double_down:
                        common_vars.player_cash_2p -= sum(common_vars.player_bets_2p[0])
                        common_vars.player_bets_2p.append(common_vars.player_bets_2p[0])
                        # card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_2p[first_hand].append(card) # Pull a third card
                        common_vars.double_downs[first_hand] = True
                        button_status.double_down = False
                        self.next_state(DealerInitState)
                    elif button_status.split:
                        common_vars.player_cash_2p -= sum(common_vars.player_bets_2p[0])
                        common_vars.player_bets_2p.append(common_vars.player_bets_2p[0])
                        # button_status.split = False
                        button_status.reset()
                        self.next_state(SplitState)
                # ??? ??? ???????????? ?????? ???????????? ???????????? ?????? ??????
                else:
                    if player_1p == HIT and player_2p == HIT:
                        print("player_1p == HIT and player_2p == HIT")
                        # card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_1p[first_hand].append(card)
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_2p[first_hand].append(card)
                        button_status.split = False
                        button_status.double_down = False
                        self.next_state(PlayerHitState)
                    elif player_1p == HIT and player_2p == STAND:
                        print("player_1p == HIT and player_2p == STAND")
                        # card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_1p[first_hand].append(card)
                        button_status.split = False
                        button_status.double_down = False
                        self.next_state(PlayerHitState)
                    elif player_1p == STAND and player_2p == HIT:
                        print("player_1p == STAND and player_2p == HIT")
                        # card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_2p[first_hand].append(card)
                        button_status.split = False
                        button_status.double_down = False
                        self.next_state(PlayerHitState)
                    elif player_1p == STAND and player_2p == STAND:
                        print("505 / player_1p == STAND and player_2p == STAND")
                        self.next_state(DealerInitState)
                    elif button_status.double_down:
                        common_vars.player_cash_1p -= sum(common_vars.player_bets_1p[0])
                        common_vars.player_bets_1p.append(common_vars.player_bets_1p[0])
                        # card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_1p[first_hand].append(card) # Pull a third card
                        common_vars.double_downs[first_hand] = True
                        button_status.double_down = False
                        self.next_state(DealerInitState)
                    elif button_status.split:
                        common_vars.player_cash_1p -= sum(common_vars.player_bets_1p[0])
                        common_vars.player_bets_1p.append(common_vars.player_bets_1p[0])
                        # button_status.split = False
                        button_status.reset()
                        self.next_state(SplitState)

        plot_bets_1p(common_vars.screen, common_vars.player_bets_1p)

        plot_bets_2p(common_vars.screen, common_vars.player_bets_2p)

        plot_buttons(common_vars.screen, button_status)

        plot_players_1p_hands(common_vars.screen,
                           PLAYER_1P_CARD_START_POS,
                           common_vars.player_hands_1p,
                           common_vars.double_downs,
                           common_vars.hands_status_1p)

        plot_players_2p_hands(common_vars.screen,
                           PLAYER_2P_CARD_START_POS,
                           common_vars.player_hands_2p,
                           common_vars.double_downs,
                           common_vars.hands_status_2p)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


"""
?????? ??? ?????? ????????? ??? ????????? ????????????.
??? ????????? ??? ????????? ?????? ??????????????? ????????? 21 ?????? ?????? ??????????????? ?????? ????????? ?????? ????????? ?????? ?????? ?????? ??? ?????? ????????? ?????? ??????????????????.
????????? ????????? ?????? ?????? 'PlayerHitState'??? ???????????????.
"""
class SplitState(State):
    def __call__(self, common_vars, button_status):
        if is_cut_passed(common_vars.shoe_of_decks):
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)
        
        plot_chips_1p(common_vars.screen, common_vars.player_cash_1p, common_vars.chips_image_width, False)
        plot_chips_2p(common_vars.screen, common_vars.player_cash_2p, common_vars.chips_image_width, False)
        plot_buttons(common_vars.screen, button_status)

        # sound_db = SoundDB.get_instance()
        # card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        first_hand = 0
        second_hand = 1
        if len(common_vars.player_hands_1p) == 1:
            hand_instance = []
            common_vars.player_hands_1p.append(hand_instance)
            common_vars.player_hands_1p[second_hand].append(common_vars.player_hands_1p[first_hand].pop())
        
        if len(common_vars.player_hands_1p[second_hand]) != 2:
            # Fill up each hand with one additional card
            common_vars.puase_time = PAUSE_TIMER1
            if len(common_vars.player_hands_1p[first_hand]) < 2:
                # card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands_1p[first_hand].append(card)
            elif len(common_vars.player_hands_1p[second_hand]) < 2:
                # card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands_1p[second_hand].append(card)
        else: 
            # Both hands have now two cards, let's evaluate
            value_of_players_hands = 0
            for hand in common_vars.player_hands_1p:
                value_of_players_hands += get_value_of_players_hand(hand)
            if value_of_players_hands != 42:
                # Not two times 21 or the answer to the meaning of life, continue to next state
                button_status.hit = True
                button_status.stand = True
                button_status.double_down = can_double_bet(common_vars.player_bets_1p, common_vars.player_cash_1p)
                self.next_state(PlayerHitState)
            else:
                # ????????? ????????? ?????? 21??? ????????? ???
                value_of_dealer_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
                common_vars.dealer_last_hand = value_of_dealer_hand
                sum_of_bets = 0
                for bet in common_vars.player_bets_1p:
                    sum_of_bets += sum(bet)
                if get_value_of_dealers_hand == 21:
                    plot_results_1p(common_vars.screen, common_vars.text_font, 'Push')
                    common_vars.player_hands_1p['first_hand_push'] = True
                    common_vars.player_hands_1p['second_hand_push'] = True
                    common_vars.player_cash_1p += sum_of_bets
                else:
                    plot_results_1p(common_vars.screen, common_vars.text_font, 'Double Black Jack!')
                    common_vars.player_hands_1p['first_hand_blackjack'] = True
                    common_vars.player_hands_1p['second_hand_blackjack'] = True
                    common_vars.player_cash_1p += sum_of_bets
                    common_vars.player_cash_1p += int(sum_of_bets * 1.5)
                common_vars.pause_time = PAUSE_TIMER3
                button_status.reset()
                self.next_state(InitialState)
        plot_bets_1p(common_vars.screen, common_vars.player_bets_1p)

        plot_bets_2p(common_vars.screen, common_vars.player_bets_2p)

        plot_players_1p_hands(common_vars.screen,
                           PLAYER_1P_CARD_START_POS,
                           common_vars.player_hands_1p,
                           common_vars.double_downs,
                           common_vars.hands_status_1p)

        plot_players_2p_hands(common_vars.screen,
                           PLAYER_2P_CARD_START_POS,
                           common_vars.player_hands_2p,
                           common_vars.double_downs,
                           common_vars.hands_status_2p)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)

class PlayerHitState(State):
    _current_hand = 0

    def __call__(self, common_vars, button_status):
        print("PlayerHitState")
        if is_cut_passed(common_vars.shoe_of_decks):
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)
        # ?????? ??? ??? ???????????? ??????
        plot_chips_1p(common_vars.screen, common_vars.player_cash_1p, common_vars.chips_image_width, False)
        plot_chips_2p(common_vars.screen, common_vars.player_cash_2p, common_vars.chips_image_width, False)

        # TODO: ????????? ?????? ??? / ????????? ???????????? ?????? ??????
        # sound_db = SoundDB.get_instance()
        # card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        num_of_hands_1p = len(common_vars.player_hands_1p)
        num_of_hands_2p = len(common_vars.player_hands_2p)

        if num_of_hands_1p == 2 and num_of_hands_2p == 2:
            image_db = ImageDB.get_instance()
            if self._current_hand == 0:
                common_vars.screen.blit(image_db.get_image(IMAGE_PATH + 'hand.png'), (100, 315))
            else:
                common_vars.screen.blit(image_db.get_image(IMAGE_PATH + 'hand.png'), (100 + GAP_BETWEEN_SPLIT, 315))
        # ??????????????? ?????? ?????? ????????? ??????
        value_of_players_1p_hand = get_value_of_players_hand(common_vars.player_hands_1p[self._current_hand])
        value_of_players_2p_hand = get_value_of_players_hand(common_vars.player_hands_2p[self._current_hand])
        # ?????? 1P??? bust ?????????
        if value_of_players_1p_hand > 21:
            print("664 / playerhitstate / value_of_players_1p_hand > 21")
            common_vars.pause_time = PAUSE_TIMER3
            plot_results_1p(common_vars.screen, common_vars.text_font,
            'Player is busted {0}'.format(value_of_players_1p_hand))
            # ????????? 2p??? ????????? ?????? ???
            if value_of_players_2p_hand > 21:
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_2p(common_vars.screen, common_vars.text_font,
                'Player is busted {0}'.format(value_of_players_2p_hand))
                print("PlayerHitState?????? 1p ??????????????? 2p ????????? ????????? ??????")
                if num_of_hands_2p == 1:
                    common_vars.hands_status_2p['first_hand_busted'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                elif self._current_hand == 0:
                    common_vars.hands_status_2p['first_hand_busted'] = True
                    button_status.double_down = True
                    self._current_hand += 1
                elif self._current_hand == 1 and common_vars.hands_status_2p['first_hand_busted']:
                    common_vars.hands_status_2p['second_hand_busted'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                else:
                    print("DealerInitState??? ???????????? ??????")
                    common_vars.hands_status_2p['second_hand_busted'] = True
                    self._current_hand = 0
                    self.next_state(DealerInitState)
            if num_of_hands_1p == 1:
                print("699 / PlayerHitState / num_of_hands_1p == 1")
                common_vars.hands_status_1p['first_hand_busted'] = True
                self._current_hand = 0
                # button_status.reset()
                # self.next_state(InitialState)
            elif self._current_hand == 0:
                print("705 / PlayerHitState / self._current_hand == 0")
                common_vars.hands_status_1p['first_hand_busted'] = True
                button_status.double_down = True
                self._current_hand += 1
            elif self._current_hand == 1 and common_vars.hands_status_1p['first_hand_busted']:
                print("705 / PlayerHitState / self._current_hand == 1 and common_vars.hands_status_1p['first_hand_busted']")
                common_vars.hands_status_1p['second_hand_busted'] = True
                self._current_hand = 0
                # button_status.reset()
                # self.next_state(InitialState)
            else:
                print("PlayerHitState / else")
                common_vars.hands_status_1p['second_hand_busted'] = True
                # self._current_hand = 0
                # self.next_state(DealerInitState)
            
        # ?????? 1p??? ???????????? 2p??? ????????? ???
        elif value_of_players_2p_hand > 21:
            print("PlayerHitState?????? 2p ????????? ????????? ??????")
            common_vars.pause_time = PAUSE_TIMER3
            plot_results_2p(common_vars.screen, common_vars.text_font,
            'Player is busted {0}'.format(value_of_players_2p_hand))
            # ?????? ????????? 1p??? ??????
            if value_of_players_1p_hand > 21:
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_1p(common_vars.screen, common_vars.text_font,
                'Player is busted {0}'.format(value_of_players_1p_hand))
                if num_of_hands_1p == 1:
                    common_vars.hands_status_1p['first_hand_busted'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                elif self._current_hand == 0:
                    common_vars.hands_status_1p['first_hand_busted'] = True
                    button_status.double_down = True
                    self._current_hand += 1
                elif self._current_hand == 1 and common_vars.hands_status_1p['first_hand_busted']:
                    common_vars.hands_status_1p['second_hand_busted'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                else:
                    common_vars.hands_status_1p['second_hand_busted'] = True
                    self._current_hand = 0
                    self.next_state(DealerInitState)
            print(num_of_hands_2p)
            if num_of_hands_2p == 1:
                common_vars.hands_status_2p['first_hand_busted'] = True
                self._current_hand = 0
                # button_status.reset()
                # self.next_state(InitialState)
            elif self._current_hand == 0:
                common_vars.hands_status_2p['first_hand_busted'] = True
                button_status.double_down = True
                self._current_hand += 1
            elif self._current_hand == 1 and common_vars.hands_status_2p['first_hand_busted']:
                common_vars.hands_status_2p['second_hand_busted'] = True
                self._current_hand = 0
                # button_status.reset()
                # self.next_state(InitialState)
            else:
                common_vars.hands_status_2p['second_hand_busted'] = True
                self._current_hand = 0
                self.next_state(DealerInitState)
            # elif value_of_players_1p_hand < 21:
            #     self.next_state(DealerInitState)
            
        # 1p??? 2p??? 21?????? ??? ?????? ???
        elif value_of_players_1p_hand == 21 and value_of_players_2p_hand == 21:
            print("769 / value_of_players_1p_hand == 21")
            # if value_of_players_2p_hand == 21:
            #     print("1p??? 2p ?????? 21???")
            #     if num_of_hands_2p == 2 and self._current_hand == 0:
            #         self._current_hand += 1
            #     else:
            #         self._current_hand = 0
            #         self.next_state(DealerInitState)
            if num_of_hands_1p == 2 and num_of_hands_2p == 2 and self._current_hand == 0:
                self._current_hand += 1
            else:
                self._current_hand = 0
                self.next_state(DealerInitState)
        # 1p??? ????????? 2p??? ?????? ???
        # elif value_of_players_2p_hand == 21:
        #     print("784 / value_of_players_2p_hand == 21")
        #     if value_of_players_1p_hand == 21:
        #         if num_of_hands_1p == 2 and self._current_hand == 0:
        #             self._current_hand += 1
        #         else:
        #             self._current_hand = 0
        #             self.next_state(DealerInitState)
        #     if num_of_hands_2p == 2 and self._current_hand == 0:
        #         self._current_hand += 1
        #     else:
        #         self._current_hand = 0
        #         self.next_state(DealerInitState)
        # else:
            # Create detectable areas for the buttons, used when mouse is clicked
        plot_buttons(common_vars.screen, button_status)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common_vars.done = True
            if event.type == pygame.KEYDOWN:
                player_1p = betting(common_vars.player_hands_1p[0], common_vars.dealer_cards[1], value_of_players_1p_hand)
                player_2p = betting(common_vars.player_hands_2p[0], common_vars.dealer_cards[1], value_of_players_2p_hand)
                # 2p??? ?????? ????????? ?????? Busted ?????? ??????????????? 1p??? ?????? ??????
                if value_of_players_2p_hand == 21 or value_of_players_2p_hand > 21:
                    print("812 / value_of_players_2p_hand == 21 or value_of_players_2p_hand > 21")
                    print("1p:", player_1p,"2p:", player_2p)
                    if player_1p == "hit":
                        # card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_1p[self._current_hand].append(card)
                        button_status.double_down = False
                    elif player_1p == "stand":
                        if num_of_hands_1p == 2 and self._current_hand == 0:
                            # One hand left to handle
                            self._current_hand += 1
                            button_status.double_down = True
                        else:
                            self._current_hand = 0
                            self.next_state(DealerInitState)
                    elif button_status.double_down:
                        common_vars.double_downs[self._current_hand] = True
                        common_vars.player_cash_1p -= sum(common_vars.player_bets_1p[0])
                        common_vars.player_bets_1p.append(common_vars.player_bets_1p[0])
                        # card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_1p[self._current_hand].append(card)
                        if num_of_hands_1p == 2 and self._current_hand == 0:
                            # One hand left to handle
                            self._current_hand += 1
                        else:
                            self._current_hand = 0
                            button_status.double_down = False
                            self.next_state(DealerInitState)
                    # 1p??? ?????? ???????????? ??????????????? 2p??? ?????? ??????
                elif value_of_players_1p_hand == 21 or value_of_players_1p_hand > 21:
                    print("838 / value_of_players_1p_hand == 21")
                    print("1p:", player_1p,"2p:", player_2p)
                    if player_2p == "hit":
                        # card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_2p[self._current_hand].append(card)
                        button_status.double_down = False
                    elif player_2p == "stand":
                        if num_of_hands_2p == 2 and self._current_hand == 0:
                            # One hand left to handle
                            self._current_hand += 1
                            button_status.double_down = True
                        else:
                            self._current_hand = 0
                            self.next_state(DealerInitState)
                    elif button_status.double_down:
                        common_vars.double_downs[self._current_hand] = True
                        common_vars.player_cash_2p -= sum(common_vars.player_bets_2p[0])
                        common_vars.player_bets_2p.append(common_vars.player_bets_2p[0])
                        # card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_2p[self._current_hand].append(card)
                        if num_of_hands_2p == 2 and self._current_hand == 0:
                            # One hand left to handle
                            self._current_hand += 1
                        else:
                            self._current_hand = 0
                            button_status.double_down = False
                            self.next_state(DealerInitState)
                # 1p 2p ??? ??? ????????? ???????????? ??? ???
                else:
                    if player_1p == HIT and player_2p == HIT:
                        print("player_1p == HIT and player_2p == HIT")
                        # card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_1p[self._current_hand].append(card)
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_2p[self._current_hand].append(card)
                        button_status.double_down = False
                    elif player_1p == HIT and player_2p == STAND:
                        print("player_1p == HIT and player_2p == STAND")
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_1p[self._current_hand].append(card)
                        button_status.double_down = False
                    elif player_1p == STAND and player_2p == HIT:
                        print("player_1p == STAND and player_2p == HIT")
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_2p[self._current_hand].append(card)
                        button_status.double_down = False
                    elif player_1p == STAND and player_2p == STAND:
                        print("887 / player_1p == STAND and player_2p == STAND")
                        if num_of_hands_1p == 2 and num_of_hands_2p == 2 and self._current_hand == 0:
                        # One hand left to handle
                            self._current_hand += 1
                            button_status.double_down = True
                        else:
                            self._current_hand = 0
                            self.next_state(DealerInitState)

        plot_bets_1p(common_vars.screen, common_vars.player_bets_1p)

        plot_bets_2p(common_vars.screen, common_vars.player_bets_2p)

        plot_buttons(common_vars.screen, button_status)

        plot_players_1p_hands(common_vars.screen,
                           PLAYER_1P_CARD_START_POS,
                           common_vars.player_hands_1p,
                           common_vars.double_downs,
                           common_vars.hands_status_1p)
        # common_vars.pause_tiem = PAUSE_TIMER2
        plot_players_2p_hands(common_vars.screen,
                           PLAYER_2P_CARD_START_POS,
                           common_vars.player_hands_2p,
                           common_vars.double_downs,
                           common_vars.hands_status_2p)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)

class DealerInitState(State):
    _current_hand = 0

    def __call__(self, common_vars, button_status):
        print("DealerInitState")
        if is_cut_passed(common_vars.shoe_of_decks):
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)
        
        plot_chips_1p(common_vars.screen, common_vars.player_cash_1p, common_vars.chips_image_width, False)
        plot_chips_2p(common_vars.screen, common_vars.player_cash_2p, common_vars.chips_image_width, False)

        common_vars.first_card_hidden = False
        num_of_hands_1p = len(common_vars.player_hands_1p)
        num_of_hands_2p = len(common_vars.player_hands_2p)
        value_of_dealer_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
        common_vars.dealer_last_hand = value_of_dealer_hand
        value_of_player_1p_hand = get_value_of_players_hand(common_vars.player_hands_1p[self._current_hand])
        value_of_player_2p_hand = get_value_of_players_hand(common_vars.player_hands_2p[self._current_hand])
        print("941")
        if value_of_dealer_hand == 21:
            print("value_of_dealer_hand == 21")
            if value_of_player_1p_hand < 21:
                print("value_of_player_1p_hand < 21")
                if value_of_player_2p_hand < 21:
                    print("value_of_player_2p_hand < 21")
                    common_vars.pause_time = PAUSE_TIMER3
                    plot_results_2p(common_vars.screen, common_vars.text_font,
                    'Dealer has {0}, Player has {1}'.format(value_of_dealer_hand, value_of_player_2p_hand))
                    if num_of_hands_2p == 1:
                        common_vars.hands_status_2p['first_hand_loose'] = True
                        self._current_hand = 0
                        button_status.reset()
                        self.next_state(InitialState)
                    elif num_of_hands_2p == 2 and self._current_hand == 0:
                        common_vars.player_bets_2p.pop()
                        self._current_hand += 1
                        common_vars.hands_status_2p['first_hand_loose'] = True
                    else:
                        common_vars.hands_status_2p['second_hand_loose'] = True
                        self._current_hand = 0
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_1p(common_vars.screen, common_vars.text_font,
                'Dealer has {0}, Player has {1}'.format(value_of_dealer_hand, value_of_player_1p_hand))
                if num_of_hands_1p == 1:
                    common_vars.hands_status_1p['first_hand_loose'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                elif num_of_hands_1p == 2 and self._current_hand == 0:
                    common_vars.player_bets_1p.pop()
                    self._current_hand += 1
                    common_vars.hands_status_1p['first_hand_loose'] = True
                else:
                    common_vars.hands_status_1p['second_hand_loose'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_status(InitialState)
            elif value_of_player_2p_hand < 21:
                print("value_of_player_2p_hand < 21")
                if value_of_player_1p_hand < 21:
                    print("value_of_player_1p_hand < 21")
                    common_vars.pause_time = PAUSE_TIMER3
                    plot_results_1p(common_vars.screen, common_vars.text_font,
                    'Dealer has {0}, Player has {1}'.format(value_of_dealer_hand, value_of_player_1p_hand))
                    if num_of_hands_1p == 1:
                        common_vars.hands_status_1p['first_hand_loose'] = True
                        self._current_hand = 0
                        button_status.reset()
                        self.next_state(InitialState)
                    elif num_of_hands_1p == 2 and self._current_hand == 0:
                        common_vars.player_bets_1p.pop()
                        self._current_hand += 1
                        common_vars.hands_status_1p['first_hand_loose'] = True
                    else:
                        common_vars.hands_status_1p['second_hand_loose'] = True
                        self._current_hand = 0
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_2p(common_vars.screen, common_vars.text_font,
                'Dealer has {0}, Player has {1}'.format(value_of_dealer_hand, value_of_player_2p_hand))
                if num_of_hands_2p == 1:
                    common_vars.hands_status_2p['first_hand_loose'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                elif num_of_hands_2p == 2 and self._current_hand == 0:
                    common_vars.player_bets_2p.pop()
                    self._current_hand += 1
                    common_vars.hands_status_2p['first_hand_loose'] = True
                else:
                    common_vars.hands_status_2p['second_hand_loose'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_status(InitialState)
            else:
                print("DealerInitState / value_of_player_1p_hand")
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_1p(common_vars.screen, common_vars.text_font,
                'Both dealer and player has 21, a push')
                plot_results_2p(common_vars.screen, common_vars.text_font,
                'Both dealer and player has 21, a push')
                common_vars.player_cash_1p += sum(common_vars.player_bets_1p.pop())
                common_vars.player_cash_2p += sum(common_vars.player_bets_2p.pop())
                if num_of_hands_1p == 1 or self._current_hand == 1:
                    if num_of_hands_2p or self._current_hand == 1:
                        common_vars.hands_status_2p['first_hand_push'] = True
                        self._current_hand = 0
                    common_vars.hands_status_1p['first_hand_push'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                elif num_of_hands_2p == 1 or self._current_hand == 1:
                    if num_of_hands_1p or self._current_hand == 1:
                        common_vars.hands_status_1p['first_hand_push'] = True
                        self._current_hand = 0
                    common_vars.hands_status_2p['first_hand_push'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                else:
                    self._current_hand += 1
                    common_vars.hands_status_1p['first_hand_push'] = True
                    common_vars.hands_status_2p['first_hand_push'] = True
        elif value_of_dealer_hand > 15 and value_of_dealer_hand > value_of_player_1p_hand:
            print("value_of_dealer_hand > 15 and value_of_dealer_hand > value_of_player_1p_hand")
            if value_of_dealer_hand > value_of_player_2p_hand:
                print("value_of_dealer_hand > value_of_player_2p_hand:")
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_2p(common_vars.screen, common_vars.text_font,
                'Dealer wins with {0} over player {1}'.format(value_of_dealer_hand, value_of_player_2p_hand))
                if num_of_hands_2p or self._current_hand == 1:
                    common_vars.hands_status_2p['first_hand_loose'] = True
                    self._current_hand = 0
                else:
                # First hand in split mode, step to next hand
                    self._current_hand += 1
                    common_vars.hands_status_2p['first_hand_loose'] = True
            plot_results_1p(common_vars.screen, common_vars.text_font,
            'Dealer wins with {0} over player {1}'.format(value_of_dealer_hand, value_of_player_1p_hand))
            if num_of_hands_1p == 1 or self._current_hand == 1:
                common_vars.hands_status_1p['first_hand_loose'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # First hand in split mode, step to next hand
                self._current_hand += 1
                common_vars.hands_status_1p['first_hand_loose'] = True
        elif value_of_dealer_hand > 15 and value_of_dealer_hand > value_of_player_2p_hand:
            print("value_of_dealer_hand > 15 and value_of_dealer_hand > value_of_player_2p_hand:")
            if value_of_dealer_hand > value_of_player_1p_hand:
                print("value_of_dealer_hand > value_of_player_1p_hand:")
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_1p(common_vars.screen, common_vars.text_font,
                'Dealer wins with {0} over player {1}'.format(value_of_dealer_hand, value_of_player_1p_hand))
                if num_of_hands_1p or self._current_hand == 1:
                    common_vars.hands_status_1p['first_hand_loose'] = True
                    self._current_hand = 0
                else:
                # First hand in split mode, step to next hand
                    self._current_hand += 1
                    common_vars.hands_status_1p['first_hand_loose'] = True
            plot_results_2p(common_vars.screen, common_vars.text_font,
            'Dealer wins with {0} over player {1}'.format(value_of_dealer_hand, value_of_player_2p_hand))
            if num_of_hands_2p == 1 or self._current_hand == 1:
                common_vars.hands_status_2p['first_hand_loose'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # First hand in split mode, step to next hand
                self._current_hand += 1
                common_vars.hands_status_2p['first_hand_loose'] = True
        elif value_of_player_1p_hand > 21:
            print("1094 / value_of_player_1p_hand > 21")
            if value_of_player_2p_hand > 21:
                print("value_of_player_2p_hand > 21")
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_2p(common_vars.screen, common_vars.text_font,
                'Player is busted with {0}'.format(value_of_player_2p_hand))
                common_vars.hands_status_2p['first_hand_busted'] = True
                if num_of_hands_2p == 1 or self._current_hand == 1:
                    common_vars.hands_status_2p['first_hand_busted'] = True
                    self._current_hand = 0
                else:
                # First hand in split mode, step to next hand
                    self._current_hand += 1
                    common_vars.hands_status_2p['first_hand_busted'] = True
            else:
                self.next_state(DealerHitState)
            # elif value_of_player_2p_hand > value_of_dealer_hand:
            #     print("value_of_player_2p_hand > value_of_dealer_hand")
            #     common_vars.pause_time = PAUSE_TIMER3
            #     plot_results_2p(common_vars.screen, common_vars.text_font,
            #     "Player wins with {0} over dealer {1}".format(value_of_player_2p_hand, value_of_dealer_hand))
            # Player is busted from previous state (possibly at a double down)
            common_vars.pause_time = PAUSE_TIMER3
            plot_results_1p(common_vars.screen, common_vars.text_font,
            'Player is busted with {0}'.format(value_of_player_1p_hand))
            if num_of_hands_1p == 1 or self._current_hand == 1:
                # Only one player hand or last hand evaluated
                common_vars.hands_status_1p['first_hand_busted'] = True
                self._current_hand = 0
                # button_status.reset()
                # self.next_state(InitialState)
            else:
                # First hand in split mode, step to next hand
                self._current_hand += 1
                common_vars.hands_status_1p['first_hand_busted'] = True
        elif value_of_player_2p_hand > 21:
            print("value_of_player_2p_hand > 21:")
            if value_of_player_1p_hand > 21:
                print("value_of_player_1p_hand > 21:")
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_1p(common_vars.screen, common_vars.text_font,
                'Player is busted with {0}'.format(value_of_player_1p_hand))
                common_vars.hands_status_1p['first_hand_busted'] = True
            elif value_of_player_1p_hand > value_of_dealer_hand:
                self._current_hand = 0
                self.next_state(DealerHitState)
            # Player is busted from previous state (possibly at a double down)
            common_vars.pause_time = PAUSE_TIMER3
            plot_results_2p(common_vars.screen, common_vars.text_font,
            'Player is busted with {0}'.format(value_of_player_2p_hand))
            if num_of_hands_1p == 1 or self._current_hand == 1:
                if num_of_hands_2p == 1 or self._current_hand == 1:
                    common_vars.hands_status_2p['first_hand_busted'] = True
                    self._current_hand = 0
                # Only one player hand or last hand evaluated
                common_vars.hands_status_1p['first_hand_busted'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # First hand in split mode, step to next hand
                self._current_hand += 1
                common_vars.hands_status_2p['first_hand_busted'] = True
        else:
            print("1142")
            self._current_hand = 0
            self.next_state(DealerHitState)

        plot_bets_1p(common_vars.screen, common_vars.player_bets_1p)

        plot_bets_2p(common_vars.screen, common_vars.player_bets_2p)

        plot_buttons(common_vars.screen, button_status)

        plot_players_1p_hands(common_vars.screen,
                           PLAYER_1P_CARD_START_POS,
                           common_vars.player_hands_1p,
                           common_vars.double_downs,
                           common_vars.hands_status_1p)

        plot_players_2p_hands(common_vars.screen,
                           PLAYER_2P_CARD_START_POS,
                           common_vars.player_hands_2p,
                           common_vars.double_downs,
                           common_vars.hands_status_2p)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)

class DealerHitState(State):
    _current_hand = 0

    def __call__(self, common_vars, button_status):
        print("DealerHitState")
        if is_cut_passed(common_vars.shoe_of_decks):
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)
        
        plot_chips_1p(common_vars.screen, common_vars.player_cash_1p, common_vars.chips_image_width, False)
        plot_chips_2p(common_vars.screen, common_vars.player_cash_2p, common_vars.chips_image_width, False)

        # TODO: ????????? ?????? ??? / ????????? ???????????? ?????? ??????
        # sound_db = SoundDB.get_instance()
        # card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        num_of_hands_1p = len(common_vars.player_hands_1p)
        num_of_hands_2p = len(common_vars.player_hands_2p)
        value_of_dealer_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
        common_vars.dealer_last_hand = value_of_dealer_hand
        value_of_player_hand_1p = get_value_of_players_hand(common_vars.player_hands_1p[self._current_hand])
        value_of_player_hand_2p = get_value_of_players_hand(common_vars.player_hands_2p[self._current_hand])

        if value_of_dealer_hand < 16:
            # card_sound.play()
            print("value_of_dealer_hand < 16")
            card = common_vars.shoe_of_decks.pop()
            common_vars.dealer_cards.append(card)
            common_vars.pause_time = PAUSE_TIMER2
        elif value_of_dealer_hand < 17 and value_of_dealer_hand < value_of_player_hand_1p or value_of_dealer_hand < value_of_player_hand_2p:
            print("value_of_dealer_hand < 17 and value_of_dealer_hand < value_of_player_hand_1p or value_of_dealer_hand < value_of_player_hand_2p")
            # card_sound.play()
            card = common_vars.shoe_of_decks.pop()
            common_vars.dealer_cards.append(card)
            common_vars.pause_time = PAUSE_TIMER2
        elif value_of_player_hand_1p > 21 or 22 > value_of_dealer_hand > value_of_player_hand_1p:
            print("value_of_player_hand_1p > 21 or 22 > value_of_dealer_hand > value_of_player_hand_1p")
            common_vars.pause_time = PAUSE_TIMER3
            if value_of_player_hand_1p > 21:
                print("value_of_player_hand_1p > 21")
                if value_of_player_hand_2p > 21 or 22 > value_of_dealer_hand > value_of_player_hand_2p:
                    print("value_of_player_hand_2p > 21 or 22 > value_of_dealer_hand > value_of_player_hand_2p")
                    if value_of_player_hand_2p > 21:
                        print("value_of_player_hand_2p > 21")
                        plot_results_2p(common_vars.screen, common_vars.text_font,
                        'Player is busted {0}'.format(value_of_player_hand_2p))
                        if self._current_hand == 0:
                            common_vars.hands_status_2p['first_hand_busted'] = True
                        else:
                            common_vars.hands_status_2p['second_hand_busted'] = True
                    else:
                        print("value_of_player_hand_2p > 21 / else")
                        plot_results_2p(common_vars.screen, common_vars.text_font,
                        'Dealer wins with {0} over player {1}'.format(value_of_dealer_hand, value_of_player_hand_2p))
                        if self._current_hand == 0:
                            common_vars.hands_status_2p['first_hand_loose'] = True
                        else:
                            common_vars.hands_status_2p['second_hand_loose'] = True
                elif value_of_player_hand_2p > value_of_dealer_hand:
                    print(value_of_player_hand_2p > value_of_dealer_hand)
                    common_vars.pause_time = PAUSE_TIMER3
                    plot_results_2p(common_vars.screen, common_vars.text_font,
                    "Player wins with {0} over dealer {1}".format(value_of_player_hand_2p, value_of_dealer_hand))
                    if self._current_hand == 0:
                        common_vars.hands_status_2p['first_hand_win'] = True
                    else:
                        common_vars.hands_status_2p['second_hand_win'] = True
                        common_vars.player_cash_2p += sum(common_vars.player_bets_2p.pop()) * 2
                elif value_of_dealer_hand == value_of_player_hand_2p:
                    print("1236 / value_of_dealer_hand == value_of_player_hand_2p")
                    # ??????????????? ????????? ????????? ????????? push???
                    common_vars.pause_time = PAUSE_TIMER3
                    plot_results_2p(common_vars.screen, common_vars.text_font,
                    'A push dealer has {0}, player has {1}'.format(value_of_dealer_hand, value_of_player_hand_2p))
                    if self._current_hand == 0:
                        common_vars.hands_status_2p["first_hand_push"] = True
                    else:
                        common_vars.hands_status_2p['second_hand_push'] = True
                    common_vars.player_cash_2p += sum(common_vars.player_bets_2p.pop())
                plot_results_1p(common_vars.screen, common_vars.text_font,
                'Player is busted {0}'.format(value_of_player_hand_1p))
                if self._current_hand == 0:
                    common_vars.hands_status_1p['first_hand_busted'] = True
                else:
                    common_vars.hands_status_1p['second_hand_busted'] = True
            else:
                print("value_of_player_hand_1p > 21 / else")
                if value_of_player_hand_2p > 21 or 22 > value_of_dealer_hand > value_of_player_hand_2p:
                    print("value_of_player_hand_2p > 21 or 22 > value_of_dealer_hand > value_of_player_hand_2p")
                    if value_of_player_hand_2p > 21:
                        print("value_of_player_hand_2p > 21")
                        plot_results_2p(common_vars.screen, common_vars.text_font,
                        'Player is busted {0}'.format(value_of_player_hand_2p))
                        if self._current_hand == 0:
                            common_vars.hands_status_2p['first_hand_busted'] = True
                        else:
                            common_vars.hands_status_2p['second_hand_busted'] = True
                    else:
                        print("value_of_player_hand_2p > 21 / else")
                        plot_results_2p(common_vars.screen, common_vars.text_font,
                        'Dealer wins with {0} over player {1}'.format(value_of_dealer_hand, value_of_player_hand_2p))
                        if self._current_hand == 0:
                            common_vars.hands_status_2p['first_hand_loose'] = True
                        else:
                            common_vars.hands_status_2p['second_hand_loose'] = True
                elif value_of_player_hand_2p > value_of_dealer_hand:
                    print("value_of_player_hand_2p > value_of_dealer_hand")
                    common_vars.pause_time = PAUSE_TIMER3
                    plot_results_2p(common_vars.screen, common_vars.text_font,
                    "Player wins with {0} over dealer {1}".format(value_of_player_hand_2p, value_of_dealer_hand))
                    if self._current_hand == 0:
                        common_vars.hands_status_2p['first_hand_win'] = True
                    else:
                        common_vars.hands_status_2p['second_hand_win'] = True
                        common_vars.player_cash_2p += sum(common_vars.player_bets_2p.pop()) * 2
                elif value_of_dealer_hand == value_of_player_hand_2p:
                    print("1283 / value_of_dealer_hand == value_of_player_hand_2p")
                    # ??????????????? ????????? ????????? ????????? push???
                    common_vars.pause_time = PAUSE_TIMER3
                    plot_results_2p(common_vars.screen, common_vars.text_font,
                    'A push dealer has {0}, player has {1}'.format(value_of_dealer_hand, value_of_player_hand_2p))
                    if self._current_hand == 0:
                        common_vars.hands_status_2p["first_hand_push"] = True
                    else:
                        common_vars.hands_status_2p['second_hand_push'] = True
                    common_vars.player_cash_2p += sum(common_vars.player_bets_2p.pop())
                plot_results_1p(common_vars.screen, common_vars.text_font,
                'Dealer wins with {0} over player {1}'.format(value_of_dealer_hand, value_of_player_hand_1p))
                if self._current_hand == 0:
                    common_vars.hands_status_1p['first_hand_loose'] = True
                else:
                    common_vars.hands_status_1p['second_hand_loose'] = True
            # Pop one bet pile from the player which is lost
            common_vars.player_bets_1p.pop()
            common_vars.player_bets_2p.pop()
            if common_vars.double_downs[self._current_hand]:
                common_vars.player_bets_1p.pop()
                common_vars.player_bets_2p.pop()
            common_vars.pause_time = PAUSE_TIMER3
            if num_of_hands_1p == 1 or self._current_hand == 1:
                # We're done if there is one player hand only or second hand has been evaluated
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            elif num_of_hands_2p == 1 or self._current_hand == 1:
                # We're done if there is one player hand only or second hand has been evaluated
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # First hand in split mode evaluated, let's switch to second hand
                self._current_hand += 1
        elif value_of_player_hand_2p > 21 or 22 > value_of_dealer_hand > value_of_player_hand_2p:
            print("value_of_player_hand_2p > 21 or 22 > value_of_dealer_hand > value_of_player_hand_2p")
            common_vars.pause_time = PAUSE_TIMER3
            if value_of_player_hand_2p > 21:
                print("value_of_player_hand_2p > 21")
                if value_of_player_hand_1p > 21 or 22 > value_of_dealer_hand > value_of_player_hand_1p:
                    print("value_of_player_hand_1p > 21 or 22 > value_of_dealer_hand > value_of_player_hand_1p")
                    if value_of_player_hand_1p > 21:
                        print("value_of_player_hand_1p > 21")
                        plot_results_1p(common_vars.screen, common_vars.text_font,
                        'Player is busted {0}'.format(value_of_player_hand_1p))
                        if self._current_hand == 0:
                            common_vars.hands_status_1p['first_hand_busted'] = True
                        else:
                            common_vars.hands_status_1p['second_hand_busted'] = True
                    elif value_of_player_hand_1p > value_of_dealer_hand:
                        print("1330 /value_of_player_hand_1p > value_of_dealer_hand")
                        common_vars.pause_time = PAUSE_TIMER3
                        plot_results_1p(common_vars.screen, common_vars.text_font,
                        "Player wins with {0} over dealer {1}".format(value_of_player_hand_1p, value_of_dealer_hand))
                        if self._current_hand == 0:
                            common_vars.hands_status_1p['first_hand_win'] = True
                        else:
                            common_vars.hands_status_1p['second_hand_win'] = True
                        common_vars.player_cash_1p += sum(common_vars.player_bets_1p.pop()) * 2
                    else:
                        print("1340 / value_of_player_hand_1p > value_of_dealer_hand / else")
                        plot_results_1p(common_vars.screen, common_vars.text_font,
                        'Dealer wins with {0} over player {1}'.format(value_of_dealer_hand, value_of_player_hand_1p))
                        if self._current_hand == 0:
                            common_vars.hands_status_1p['first_hand_loose'] = True
                        else:
                            common_vars.hands_status_1p['second_hand_loose'] = True
                elif value_of_player_hand_2p > value_of_dealer_hand:
                    print("value_of_player_hand_2p > value_of_dealer_hand")
                    common_vars.pause_time = PAUSE_TIMER3
                    plot_results_2p(common_vars.screen, common_vars.text_font,
                    "Player wins with {0} over dealer {1}".format(value_of_player_hand_2p, value_of_dealer_hand))
                    if self._current_hand == 0:
                        common_vars.hands_status_2p['first_hand_win'] = True
                    else:
                        common_vars.hands_status_2p['second_hand_win'] = True
                        common_vars.player_cash_2p += sum(common_vars.player_bets_2p.pop()) * 2
                plot_results_2p(common_vars.screen, common_vars.text_font,
                'Player is busted {0}'.format(value_of_player_hand_2p))
                if self._current_hand == 0:
                    common_vars.hands_status_2p['first_hand_busted'] = True
                else:
                    common_vars.hands_status_2p['second_hand_busted'] = True
            else:
                print("Dealer win")
                plot_results_2p(common_vars.screen, common_vars.text_font,
                'Dealer wins with {0} over player {1}'.format(value_of_dealer_hand, value_of_player_hand_2p))
                if self._current_hand == 0:
                    common_vars.hands_status_2p['first_hand_loose'] = True
                else:
                    common_vars.hands_status_2p['second_hand_loose'] = True
            # Pop one bet pile from the player which is lost
            common_vars.player_bets_1p.pop()
            common_vars.player_bets_2p.pop()
            if common_vars.double_downs[self._current_hand]:
                common_vars.player_bets_1p.pop()
                common_vars.player_bets_2p.pop()
            common_vars.pause_time = PAUSE_TIMER3
            if num_of_hands_1p == 1 or self._current_hand == 1:
                # We're done if there is one player hand only or second hand has been evaluated
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            elif num_of_hands_2p == 1 or self._current_hand == 1:
                # We're done if there is one player hand only or second hand has been evaluated
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # First hand in split mode evaluated, let's switch to second hand
                self._current_hand += 1
                ####################
        elif value_of_dealer_hand == value_of_player_hand_1p:
            print("value_of_dealer_hand == value_of_player_hand_1p")
            if value_of_dealer_hand == value_of_player_hand_2p:
                print("1400 / value_of_dealer_hand == value_of_player_hand_2p")
                # ??????????????? ????????? ????????? ????????? push???
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_2p(common_vars.screen, common_vars.text_font,
                'A push dealer has {0}, player has {1}'.format(value_of_dealer_hand, value_of_player_hand_2p))
                if self._current_hand == 0:
                    common_vars.hands_status_2p["first_hand_push"] = True
                else:
                    common_vars.hands_status_2p['second_hand_push'] = True
                common_vars.player_cash_2p += sum(common_vars.player_bets_2p.pop())
            # ??????????????? ????????? ????????? ????????? push???
            common_vars.pause_time = PAUSE_TIMER3
            plot_results_1p(common_vars.screen, common_vars.text_font,
            'A push dealer has {0}, player has {1}'.format(value_of_dealer_hand, value_of_player_hand_1p))
            if self._current_hand == 0:
                common_vars.hands_status_1p["first_hand_push"] = True
            else:
                common_vars.hands_status_1p['second_hand_push'] = True
            
            if num_of_hands_1p == 1 or self._current_hand == 1:
                # We're done if there is one player hand only or second hand has been evaluated
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                self._current_hand += 1
            
            # Pay back one bet to player
            common_vars.player_cash_1p += sum(common_vars.player_bets_1p.pop())
            if common_vars.double_downs[self._current_hand]:
                # nd pay back the second bet pile for this hand which has been doubled down'ed
                common_vars.player_cash_1p += sum(common_vars.player_bets_1p.pop())
        elif value_of_dealer_hand == value_of_player_hand_2p:
            print("1433 / value_of_dealer_hand == value_of_player_hand_2p")
            if value_of_dealer_hand == value_of_player_hand_1p:
                print("value_of_dealer_hand == value_of_player_hand_1p")
                # ??????????????? ????????? ????????? ????????? push???
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_1p(common_vars.screen, common_vars.text_font,
                'A push dealer has {0}, player has {1}'.format(value_of_dealer_hand, value_of_player_hand_1p))
                if self._current_hand == 0:
                    common_vars.hands_status_1p["first_hand_push"] = True
                else:
                    common_vars.hands_status_1p['second_hand_push'] = True
                common_vars.player_cash_1p += sum(common_vars.player_bets_1p.pop())
            elif value_of_dealer_hand < value_of_player_hand_1p:
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_1p(common_vars.screen, common_vars.text_font,
                "Player wins with {0} over dealer {1}".format(value_of_player_hand_1p, value_of_dealer_hand))
                if self._current_hand == 0:
                    common_vars.hands_status_1p['first_hand_win'] = True
                else:
                    common_vars.hands_status_1p['second_hand_win'] = True
                common_vars.player_cash_1p += sum(common_vars.player_bets_1p.pop()) * 2
            # ??????????????? ????????? ????????? ????????? push???
            common_vars.pause_time = PAUSE_TIMER3
            plot_results_2p(common_vars.screen, common_vars.text_font,
            'A push dealer has {0}, player has {1}'.format(value_of_dealer_hand, value_of_player_hand_2p))
            if self._current_hand == 0:
                common_vars.hands_status_2p["first_hand_push"] = True
            else:
                common_vars.hands_status_2p['second_hand_push'] = True
            
            if num_of_hands_2p == 1 or self._current_hand == 1:
                # We're done if there is one player hand only or second hand has been evaluated
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                self._current_hand += 1
            
            # Pay back one bet to player
            common_vars.player_cash_2p += sum(common_vars.player_bets_2p.pop())
            if common_vars.double_downs[self._current_hand]:
                # nd pay back the second bet pile for this hand which has been doubled down'ed
                common_vars.player_cash_2p += sum(common_vars.player_bets_2p.pop())
        else:
            if value_of_player_hand_1p > value_of_dealer_hand or value_of_dealer_hand > 21:
                print("1473 / value_of_player_hand_1p > value_of_dealer_hand")
                if value_of_player_hand_2p > 21 or 22 > value_of_dealer_hand > value_of_player_hand_2p:
                    print("value_of_player_hand_2p > 21 or 22 > value_of_dealer_hand > value_of_player_hand_2p")
                    if value_of_player_hand_2p > 21:
                        print("value_of_player_hand_2p > 21")
                        plot_results_2p(common_vars.screen, common_vars.text_font,
                        'Player is busted {0}'.format(value_of_player_hand_2p))
                        if self._current_hand == 0:
                            common_vars.hands_status_2p['first_hand_busted'] = True
                        else:
                            common_vars.hands_status_2p['second_hand_busted'] = True
                    elif value_of_player_hand_2p > value_of_dealer_hand:
                        print("value_of_player_hand_2p > value_of_dealer_hand")
                        common_vars.pause_time = PAUSE_TIMER3
                        plot_results_2p(common_vars.screen, common_vars.text_font,
                        "Player wins with {0} over dealer {1}".format(value_of_player_hand_2p, value_of_dealer_hand))
                        if self._current_hand == 0:
                            common_vars.hands_status_2p['first_hand_win'] = True
                        else:
                            common_vars.hands_status_2p['second_hand_win'] = True
                        common_vars.player_cash_2p += sum(common_vars.player_bets_2p.pop()) * 2
                    else:
                        print("value_of_player_hand_2p > value_of_dealer_hand / else")
                        plot_results_2p(common_vars.screen, common_vars.text_font,
                        'Dealer wins with {0} over player {1}'.format(value_of_dealer_hand, value_of_player_hand_2p))
                        if self._current_hand == 0:
                            common_vars.hands_status_2p['first_hand_loose'] = True
                        else:
                            common_vars.hands_status_2p['second_hand_loose'] = True
                elif value_of_player_hand_2p > value_of_dealer_hand or value_of_dealer_hand > 21:
                    print("value_of_player_hand_2p > value_of_dealer_hand or value_of_dealer_hand > 21")
                    common_vars.pause_time = PAUSE_TIMER3
                    plot_results_2p(common_vars.screen, common_vars.text_font,
                    "Player wins with {0} over dealer {1}".format(value_of_player_hand_2p, value_of_dealer_hand))
                    if self._current_hand == 0:
                        common_vars.hands_status_2p['first_hand_win'] = True
                    else:
                        common_vars.hands_status_2p['second_hand_win'] = True
                    common_vars.player_cash_2p += sum(common_vars.player_bets_2p.pop()) * 2
            # Player wins this hand
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_1p(common_vars.screen, common_vars.text_font,
                "Player wins with {0} over dealer {1}".format(value_of_player_hand_1p, value_of_dealer_hand))
                if self._current_hand == 0:
                    common_vars.hands_status_1p['first_hand_win'] = True
                else:
                    common_vars.hands_status_1p['second_hand_win'] = True

                if common_vars.hands_status_1p['first_hand_blackjack'] == False:
                    common_vars.player_cash_1p += sum(common_vars.player_bets_1p.pop()) * 2

                if common_vars.double_downs[self._current_hand]:
                    # Doubled down hand, add additional win
                    common_vars.player_cash_1p += sum(common_vars.player_bets_1p.pop()) * 2
            common_vars.dealer_last_hand = value_of_dealer_hand
            if num_of_hands_1p == 1 and num_of_hands_2p == 1 or self._current_hand == 1:
                # We're done if there is one player hand only or second hand has been evaluated
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # First hand in split mode evaluated, let's switch to second hand
                self._current_hand += 1
        
        plot_bets_1p(common_vars.screen, common_vars.player_bets_1p)

        plot_bets_2p(common_vars.screen, common_vars.player_bets_2p)

        plot_buttons(common_vars.screen, button_status)

        plot_players_1p_hands(common_vars.screen,
                               PLAYER_1P_CARD_START_POS,
                               common_vars.player_hands_1p,
                               common_vars.double_downs,
                               common_vars.hands_status_1p)

        plot_players_2p_hands(common_vars.screen,
                               PLAYER_2P_CARD_START_POS,
                               common_vars.player_hands_2p,
                               common_vars.double_downs,
                               common_vars.hands_status_2p)

        plot_dealers_hand(common_vars.screen,
        DEALER_CARD_START_POS,
        common_vars.dealer_cards,
        common_vars.first_card_hidden)
"""
??????????????? ?????? ?????? ??????
x????????? ????????? ???????????? ????????? ???????????? ????????? ????????? ????????? ??? ??????
"""
class FinalState(State):
    def __call__(self, common_vars, button_status):
        print("FinalState")
        account_text = common_vars.text_font.render("Game Over, you're out of money", False, GOLD_COLOR)
        common_vars.screen.blit(account_text, (5, GAME_BOARD_Y_SIZE - 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common_vars.done = True