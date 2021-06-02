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
        common_vars.hands_status = {
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
            # TODO: 사운드 파일 쪽 / 나중에 추가할지 말지 고민
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
                        
                    elif  button_collide_instance.undo_bet_button_area.\
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
        if is_cut_passed(common_vars.shoe_of_decks):
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)
        
        # 게임이 시작됨에 따라 더이상 칩을 배팅할 수 없게 하기 위하여 Visible이였던 칩 상태를 안보이게 hidden으로 바꿈
        plot_chips_1p(common_vars.screen, common_vars.player_cash_1p, common_vars.chips_image_width, False)
        plot_chips_2p(common_vars.screen, common_vars.player_cash_2p, common_vars.chips_image_width, False)

        # TODO: 사운드 파일 쪽 / 나중에 추가할지 말지 고민
        # sound_db = SoundDB.get_instance()
        # card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        first_hand = 0 # 플레이어가 한장의 카드를 들 고 있어야 함
        if len(common_vars.dealer_cards) < 2:
            # 딜러의 카드가 2장의 카드를 들고 있어야 함으로 잠시 딜레이 시간을 두고 다음 카드를 주기 위함
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
            # TODO: player_2p 추가 필요
            value_of_players_2p_hand = get_value_of_players_hand(common_vars.player_hands_2p[0])
            # 21점으로 blackjack임과 동시에 카드가 2장 이상일 시 split을 할 수 없는 조건을 검
            if value_of_players_1p_hand == 21 and len(common_vars.player_hands_1p) != 2:
                common_vars.first_card_hidden = False
                # 만약 딜러도 21점으로 동점일 시 드로우 처리하고 돈을 돌려 받음
                if value_of_dealers_hand == 21:
                    common_vars.pause_time = PAUSE_TIMER3
                    plot_results_1p(common_vars.screen, common_vars.text_font, 'Push')
                    common_vars.hands_status['first_hand_push'] = True
                    common_vars.player_cash_1p += sum(common_vars.player_bets_1p[0])
                else:
                    common_vars.pause_time = PAUSE_TIMER3
                    plot_results_1p(common_vars.screen, common_vars.text_font, 'Black Jack!')
                    common_vars.hands_status['first_hand_blackjack'] = True
                    common_vars.player_cash_1p += sum(common_vars.player_bets_1p[0])
                    common_vars.player_cash_1p += int(sum(common_vars.player_bets_1p[0]) * 1.5)
                # 플레이어가 이겼을시 black jack멘트와 함께 기존 배팅금 + 1.5배의 배당금을 받게됨
                if value_of_players_2p_hand == 21:
                    common_vars.pause_time = PAUSE_TIMER3
                    plot_results_2p(common_vars.screen, common_vars.text_font, 'Black Jack!')
                    common_vars.hands_status['first_hand_blackjack'] = True
                    common_vars.player_cash_2p += sum(common_vars.player_bets_2p[0])
                    common_vars.player_cash_2p += int(sum(common_vars.player_bets_2p[0]) * 1.5)
                else:
                    common_vars.pause_time = PAUSE_TIMER3
                    plot_results_1p(common_vars.screen, common_vars.text_font, 'Black Jack!')
                    common_vars.hands_status['first_hand_blackjack'] = True
                    common_vars.player_cash_2p += sum(common_vars.player_bets_2p[0])
                    common_vars.player_cash_2p += int(sum(common_vars.player_bets_2p[0]) * 1.5)
                
                # 전광판에 딜러의 마지막 점수를 띄우기 위해 저장
                common_vars.dealer_last_hand = value_of_dealers_hand
                common_vars.pause_time = PAUSE_TIMER3
                # 게임이 종료되었으니 버튼들의 상태 초기화 및 게임 설정 기존 설정으로 초기화
                button_status.reset()
                self.next_state(InitialState)
            # 만약 플레이어의 카드가 2장이 아니고 스플릿을 할 수 있다면
            elif len(common_vars.player_hands_1p) != 2 and is_possible_split(common_vars.player_hands_1p[0]):
                # 스플릿이 가능한 상태를 판단하기 위해 먼저 double bet이 가능한지 판단 후 True False로 스플릿 가능한 상태 판단
                button_status.split = can_double_bet(common_vars.player_bets_1p, common_vars.player_cash_1p)
                button_status.hit = True
            # 위의 모든 조건을 충족하지 않고 일단 게임을 진행해야 될 시 hit값을 true로 설정
            else:
                button_status.hit = True
        else:
            button_status.hit = True
            button_status.stand = True
            button_status.double_down = can_double_bet(common_vars.player_bets_1p, common_vars.player_cash_1p)
            value_of_players_1p_hand = get_value_of_players_hand(common_vars.player_hands_1p[0])
            value_of_players_2p_hand = get_value_of_players_hand(common_vars.player_hands_1p[0])

        button_collide_instance = ButtonCollideArea.get_instance(common_vars)
        # 버튼 상태 반영
        plot_buttons(common_vars.screen, button_status)

        # print(common_vars.player_hands_1p[0], len(common_vars.dealer_cards) == 2)
        # bettingResult = betResult(value_of_players_hand)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common_vars.done = True
            if event.type == pygame.KEYDOWN:
                mouse_position = pygame.mouse.get_pos()
                value_of_players_1p_hand = get_value_of_players_hand(common_vars.player_hands_1p[0])
                value_of_players_2p_hand = get_value_of_players_hand(common_vars.player_hands_2p[0])
                # TODO:
                player_1p = betting(common_vars.player_hands_1p[0], common_vars.dealer_cards[1], value_of_players_1p_hand)
                player_2p = betting(common_vars.player_hands_2p[0], common_vars.dealer_cards[1], value_of_players_2p_hand)
                if button_status.hit and player_1p == "hit" and player_2p == "hit":
                    # card_sound.play()
                    card = common_vars.shoe_of_decks.pop()
                    common_vars.player_hands_1p[first_hand].append(card)
                    card = common_vars.shoe_of_decks.pop()
                    common_vars.player_hands_2p[first_hand].append(card)
                    button_status.split = False
                    button_status.double_down = False
                    self.next_state(PlayerHitState)
                elif button_status.stand and player_1p == "stand" and player_2p == "stand":
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

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         common_vars.done = True
        #     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        #         mouse_position = pygame.mouse.get_pos()
        #         value_of_players_hand = get_value_of_players_hand(common_vars.player_hands_1p[0])
        #         if button_status.hit and button_collide_instance.hit_button_area.\
        #                 collidepoint(mouse_position[0], mouse_position[1]):
        #             # card_sound.play()
        #             card = common_vars.shoe_of_decks.pop()
        #             common_vars.player_hands_1p[first_hand].append(card)
        #             button_status.split = False
        #             button_status.double_down = False
        #             self.next_state(PlayerHitState)
        #         elif button_status.stand and button_collide_instance.stand_button_area.\
        #                 collidepoint(mouse_position[0], mouse_position[1]):
        #             self.next_state(DealerInitState)
        #         elif button_status.double_down and button_collide_instance.double_down_button_area.\
        #                 collidepoint(mouse_position[0], mouse_position[1]):
        #             common_vars.player_cash_1p -= sum(common_vars.player_bets_1p[0])
        #             common_vars.player_bets_1p.append(common_vars.player_bets_1p[0])
        #             # card_sound.play()
        #             card = common_vars.shoe_of_decks.pop()
        #             common_vars.player_hands_1p[first_hand].append(card) # Pull a third card
        #             common_vars.double_downs[first_hand] = True
        #             button_status.double_down = False
        #             self.next_state(DealerInitState)
        #         elif button_status.split and button_collide_instance.split_button_area.\
        #                 collidepoint(mouse_position[0], mouse_position[1]):
        #             common_vars.player_cash_1p -= sum(common_vars.player_bets_1p[0])
        #             common_vars.player_bets_1p.append(common_vars.player_bets_1p[0])
        #             # button_status.split = False
        #             button_status.reset()
        #             self.next_state(SplitState)

        plot_bets_1p(common_vars.screen, common_vars.player_bets_1p)

        plot_bets_2p(common_vars.screen, common_vars.player_bets_2p)

        plot_buttons(common_vars.screen, button_status)
      
        plot_players_1p_hands(common_vars.screen,
                           PLAYER_1P_CARD_START_POS,
                           common_vars.player_hands_1p,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_players_2p_hands(common_vars.screen,
                           PLAYER_2P_CARD_START_POS,
                           common_vars.player_hands_2p,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


"""
처음 두 장의 카드를 두 손으로 나눕니다.
각 핸드에 새 카드를 뽑고 플레이어가 양손에 21 개를 얻을 수있을만큼 운이 좋다면 딜러 핸드를 향해 더블 블랙 잭 또는 타이를 위해 평가하십시오.
그렇지 않으면 다음 상태 'PlayerHitState'로 이동합니다.
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
                # 두장의 카드로 둘다 21을 맞췄을 시
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
                           common_vars.hands_status)

        plot_players_2p_hands(common_vars.screen,
                           PLAYER_2P_CARD_START_POS,
                           common_vars.player_hands_2p,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)

class PlayerHitState(State):
    _current_hand = 0

    def __call__(self, common_vars, button_status):
        if is_cut_passed(common_vars.shoe_of_decks):
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)
        
        plot_chips_1p(common_vars.screen, common_vars.player_cash_1p, common_vars.chips_image_width, False)
        plot_chips_2p(common_vars.screen, common_vars.player_cash_2p, common_vars.chips_image_width, False)

        # TODO: 사운드 파일 쪽 / 나중에 추가할지 말지 고민
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
        
        value_of_players_1p_hand = get_value_of_players_hand(common_vars.player_hands_1p[self._current_hand])
        value_of_players_2p_hand = get_value_of_players_hand(common_vars.player_hands_2p[self._current_hand])
        # 1P와 2P가 둘다 21이상으로 busted 당할 시
        if value_of_players_1p_hand > 21:
            common_vars.pause_time = PAUSE_TIMER3
            plot_results_1p(common_vars.screen, common_vars.text_font,
            'Player is busted {0}'.format(value_of_players_1p_hand))
            if value_of_players_2p_hand > 21:
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_2p(common_vars.screen, common_vars.text_font,
                'Player is busted {0}'.format(value_of_players_2p_hand))
                if num_of_hands_2p == 1:
                    common_vars.hands_status['first_hand_busted'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                elif self._current_hand == 0:
                    common_vars.hands_status['first_hand_busted'] = True
                    button_status.double_down = True
                    self._current_hand += 1
                elif self._current_hand == 1 and common_vars.hands_status['first_hand_busted']:
                    common_vars.hands_status['second_hand_busted'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                else:
                    common_vars.hands_status['second_hand_busted'] = True
                    self._current_hand = 0
                    self.next_state(DealerInitState)
            if num_of_hands_1p == 1:
                common_vars.hands_status['first_hand_busted'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            elif self._current_hand == 0:
                common_vars.hands_status['first_hand_busted'] = True
                button_status.double_down = True
                self._current_hand += 1
            elif self._current_hand == 1 and common_vars.hands_status['first_hand_busted']:
                common_vars.hands_status['second_hand_busted'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                common_vars.hands_status['second_hand_busted'] = True
                self._current_hand = 0
                self.next_state(DealerInitState)
        # 1p와 2p가 21점이 딱 맞을 시
        elif value_of_players_1p_hand == 21:
            if value_of_players_2p_hand == 21:
                if num_of_hands_2p == 2 and self._current_hand == 0:
                    self._current_hand += 1
                else:
                    self._current_hand = 0
                    self.next_state(DealerInitState)
            if num_of_hands_1p == 2 and self._current_hand == 0:
                self._current_hand += 1
            else:
                self._current_hand = 0
                self.next_state(DealerInitState)
        else:
            # Create detectable areas for the buttons, used when mouse is clicked
            button_collide_instance = ButtonCollideArea.get_instance(common_vars)
            plot_buttons(common_vars.screen, button_status)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    common_vars.done = True
                if event.type == pygame.KEYDOWN:
                    player_1p = betting(common_vars.player_hands_1p[0], common_vars.dealer_cards[1], value_of_players_1p_hand)
                    player_2p = betting(common_vars.player_hands_2p[0], common_vars.dealer_cards[1], value_of_players_2p_hand)
                    mouse_position = pygame.mouse.get_pos()
                    if player_1p == "hit":
                        if player_2p == "hit":
                            card = common_vars.shoe_of_decks.pop()
                            common_vars.player_hands_2p[self._current_hand].append(card)
                            button_status.double_down = False
                        # card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands_1p[self._current_hand].append(card)
                        button_status.double_down = False
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
                    elif player_1p == "stand":
                        if player_2p == "stand":
                            if num_of_hands_2p == 2 and self._current_hand == 0:
                                self._current_hand += 1
                                button_status.double_down = True
                            else:
                                self._current_hand = 0
                        if num_of_hands_1p == 2 and self._current_hand == 0:
                            # One hand left to handle
                            self._current_hand += 1
                            button_status.double_down = True
                        else:
                            self._current_hand = 0
                            self.next_state(DealerInitState)
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         common_vars.done = True
            #     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #         mouse_position = pygame.mouse.get_pos()
            #         if button_collide_instance.hit_button_area.collidepoint(mouse_position[0], mouse_position[1]):
            #             # card_sound.play()
            #             card = common_vars.shoe_of_decks.pop()
            #             common_vars.player_hands_1p[self._current_hand].append(card)
            #             button_status.double_down = False
            #         elif button_status.double_down and button_collide_instance.double_down_button_area.\
            #                 collidepoint(mouse_position[0], mouse_position[1]):
            #             common_vars.double_downs[self._current_hand] = True
            #             common_vars.player_cash_1p -= sum(common_vars.player_bets_1p[0])
            #             common_vars.player_bets_1p.append(common_vars.player_bets_1p[0])
            #             # card_sound.play()
            #             card = common_vars.shoe_of_decks.pop()
            #             common_vars.player_hands_1p[self._current_hand].append(card)
            #             if num_of_hands == 2 and self._current_hand == 0:
            #                 # One hand left to handle
            #                 self._current_hand += 1
            #             else:
            #                 self._current_hand = 0
            #                 button_status.double_down = False
            #                 self.next_state(DealerInitState)
            #         elif button_collide_instance.stand_button_area.collidepoint(mouse_position[0], mouse_position[1]):
            #             if num_of_hands == 2 and self._current_hand == 0:
            #                 # One hand left to handle
            #                 self._current_hand += 1
            #                 button_status.double_down = True
            #             else:
            #                 self._current_hand = 0
            #                 self.next_state(DealerInitState)

        plot_bets_1p(common_vars.screen, common_vars.player_bets_1p)

        plot_bets_2p(common_vars.screen, common_vars.player_bets_2p)

        plot_buttons(common_vars.screen, button_status)

        plot_players_1p_hands(common_vars.screen,
                           PLAYER_1P_CARD_START_POS,
                           common_vars.player_hands_1p,
                           common_vars.double_downs,
                           common_vars.hands_status)
        common_vars.pause_tiem = PAUSE_TIMER2
        plot_players_2p_hands(common_vars.screen,
                           PLAYER_2P_CARD_START_POS,
                           common_vars.player_hands_2p,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)

class DealerInitState(State):
    _current_hand = 0

    def __call__(self, common_vars, button_status):
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

        if value_of_dealer_hand == 21:
            if value_of_player_1p_hand < 21:
                if value_of_player_2p_hand < 21:
                    common_vars.pause_time = PAUSE_TIMER3
                    plot_results_2p(common_vars.screen, common_vars.text_font,'Dealer has {0}, Player has {1}'.format(value_of_dealer_hand, value_of_player_2p_hand))
                    # if num_of_hands_2p == 1:
                    #     common_vars.hands_status['first_hand_loose'] = True
                    #     self._current_hand = 0
                    #     button_status.reset()
                    #     self.next_state(InitialState)
                    # elif num_of_hands_2p == 2 and self._current_hand == 0:
                    #     common_vars.player_bets_1p.pop()
                    #     self._current_hand += 1
                    #     common_vars.hands_status['first_hand_loose'] = True
                    # else:
                    #     common_vars.hands_status['second_hand_loose'] = True
                    #     self._current_hand = 0
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_1p(common_vars.screen, common_vars.text_font,'Dealer has {0}, Player has {1}'.format(value_of_dealer_hand, value_of_player_1p_hand))
                if num_of_hands_1p == 1:
                    common_vars.hands_status['first_hand_loose'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                elif num_of_hands_1p == 2 and self._current_hand == 0:
                    common_vars.player_bets_1p.pop()
                    self._current_hand += 1
                    common_vars.hands_status['first_hand_loose'] = True
                else:
                    common_vars.hands_status['second_hand_loose'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_status(InitialState)
            else:
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_1p(common_vars.screen, common_vars.text_font,
                'Both dealer and player has 21, a push')
                plot_results_2p(common_vars.screen, common_vars.text_font,
                'Both dealer and player has 21, a push')
                common_vars.player_cash_1p += sum(common_vars.player_bets_1p.pop())
                common_vars.player_cash_2p += sum(common_vars.player_bets_2p.pop())
                if num_of_hands_1p == 1 or self._current_hand == 1:
                    if num_of_hands_2p or self._current_hand == 1:
                        common_vars.hands_status['first_hand_push'] = True
                        self._current_hand = 0
                    common_vars.hands_status['first_hand_push'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                else:
                    self._current_hand += 1
                    common_vars.hands_status['first_hand_push'] = True
        elif value_of_dealer_hand > 15 and value_of_dealer_hand > value_of_player_1p_hand and value_of_dealer_hand > value_of_player_2p_hand:
            common_vars.pause_time = PAUSE_TIMER3
            plot_results_1p(common_vars.screen, common_vars.text_font,
            'Dealer wins with {0} over player {1}'.format(value_of_dealer_hand, value_of_player_1p_hand))
            plot_results_2p(common_vars.screen, common_vars.text_font,
            'Dealer wins with {0} over player {1}'.format(value_of_dealer_hand, value_of_player_2p_hand))
            if num_of_hands_1p == 1 or self._current_hand == 1:
                if num_of_hands_2p or self._current_hand == 1:
                    common_vars.hands_status['first_hand_loose'] = True
                    self._current_hand = 0
                common_vars.hands_status['first_hand_loose'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # First hand in split mode, step to next hand
                self._current_hand += 1
                common_vars.hands_status['first_hand_loose'] = True
        elif value_of_player_1p_hand > 21:
            if value_of_player_2p_hand > 21:
                common_vars.pause_time = PAUSE_TIMER3
                plot_results_2p(common_vars.screen, common_vars.text_font,
                'Player is busted with {0}'.format(value_of_player_2p_hand))
            # Player is busted from previous state (possibly at a double down)
            common_vars.pause_time = PAUSE_TIMER3
            plot_results_1p(common_vars.screen, common_vars.text_font,
            'Player is busted with {0}'.format(value_of_player_1p_hand))
            if num_of_hands_1p == 1 or self._current_hand == 1:
                # Only one player hand or last hand evaluated
                common_vars.hands_status['first_hand_busted'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # First hand in split mode, step to next hand
                self._current_hand += 1
                common_vars.hands_status['first_hand_busted'] = True
        else:
            self._current_hand = 0
            self.next_state(DealerHitState)

        plot_bets_1p(common_vars.screen, common_vars.player_bets_1p)

        plot_bets_2p(common_vars.screen, common_vars.player_bets_2p)

        plot_buttons(common_vars.screen, button_status)

        plot_players_1p_hands(common_vars.screen,
                           PLAYER_1P_CARD_START_POS,
                           common_vars.player_hands_1p,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_players_2p_hands(common_vars.screen,
                           PLAYER_2P_CARD_START_POS,
                           common_vars.player_hands_2p,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)

class DealerHitState(State):
    _current_hand = 0

    def __call__(self, common_vars, button_status):
        if is_cut_passed(common_vars.shoe_of_decks):
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)
        
        plot_chips_1p(common_vars.screen, common_vars.player_cash_1p, common_vars.chips_image_width, False)
        plot_chips_2p(common_vars.screen, common_vars.player_cash_2p, common_vars.chips_image_width, False)

        # TODO: 사운드 파일 쪽 / 나중에 추가할지 말지 고민
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
            card = common_vars.shoe_of_decks.pop()
            common_vars.dealer_cards.append(card)
            common_vars.pause_time = PAUSE_TIMER2
        elif value_of_dealer_hand < 17 and value_of_dealer_hand < value_of_player_hand_1p:
            # card_sound.play()
            card = common_vars.shoe_of_decks.pop()
            common_vars.dealer_cards.append(card)
            common_vars.pause_time = PAUSE_TIMER2
        elif value_of_player_hand_1p > 21 or 22 > value_of_dealer_hand > value_of_player_hand_1p:
            common_vars.pause_time = PAUSE_TIMER3
            if value_of_player_hand_1p > 21:
                if value_of_player_hand_2p > 21:
                    plot_results_2p(common_vars.screen, common_vars.text_font,
                    'Player is busted {0}'.format(value_of_player_hand_2p))
                plot_results_1p(common_vars.screen, common_vars.text_font,
                'Player is busted {0}'.format(value_of_player_hand_1p))
                if self._current_hand == 0:
                    common_vars.hands_status['first_hand_busted'] = True
                else:
                    common_vars.hands_status['second_hand_busted'] = True
            else:
                plot_results_1p(common_vars.screen, common_vars.text_font,
                'Dealer wins with {0} over player {1}'.format(value_of_dealer_hand, value_of_player_hand_1p))
                plot_results_2p(common_vars.screen, common_vars.text_font,
                'Dealer wins with {0} over player {1}'.format(value_of_dealer_hand, value_of_player_hand_2p))
                if self._current_hand == 0:
                    common_vars.hands_status['first_hand_loose'] = True
                else:
                    common_vars.hands_status['second_hand_loose'] = True
            # Pop one bet pile from the player which is lost
            common_vars.player_bets_1p.pop()
            common_vars.player_bets_2p.pop()
            if common_vars.double_downs[self._current_hand]:
                common_vars.player_bets_1p.pop()
                # common_vars.player_bets_2p.pop()
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
        elif value_of_dealer_hand == value_of_player_hand_1p:
            # 플레이어와 딜러의 점수가 값으면 push함
            common_vars.pause_time = PAUSE_TIMER3
            plot_results_1p(common_vars.screen, common_vars.text_font,
            'A push dealer has {0}, player has {1}'.format(value_of_dealer_hand, value_of_player_hand_1p))
            if self._current_hand == 0:
                common_vars.hands_status["first_hand_push"] = True
            else:
                common_vars.hands_status['second_hand_push'] = True
            
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
            # 플레이어와 딜러의 점수가 값으면 push함
            common_vars.pause_time = PAUSE_TIMER3
            plot_results_2p(common_vars.screen, common_vars.text_font,
            'A push dealer has {0}, player has {1}'.format(value_of_dealer_hand, value_of_player_hand_2p))
            if self._current_hand == 0:
                common_vars.hands_status["first_hand_push"] = True
            else:
                common_vars.hands_status['second_hand_push'] = True
            
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
            # Player wins this hand
            if self._current_hand == 0:
                common_vars.hands_status['first_hand_win'] = True
            else:
                common_vars.hands_status['second_hand_win'] = True
            common_vars.pause_time = PAUSE_TIMER3
            plot_results_1p(common_vars.screen, common_vars.text_font,
            "Player wins with {0} over dealer {1}".format(value_of_player_hand_1p, value_of_dealer_hand))
            plot_results_2p(common_vars.screen, common_vars.text_font,
            "Player wins with {0} over dealer {1}".format(value_of_player_hand_1p, value_of_dealer_hand))
            common_vars.player_cash_1p += sum(common_vars.player_bets_1p.pop()) * 2
            common_vars.player_cash_2p += sum(common_vars.player_bets_2p.pop()) * 2
            if common_vars.double_downs[self._current_hand]:
                # Doubled down hand, add additional win
                common_vars.player_cash_1p += sum(common_vars.player_bets_1p.pop()) * 2
                common_vars.player_cash_2p += sum(common_vars.player_bets_2p.pop()) * 2
            common_vars.dealer_last_hand = value_of_dealer_hand
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
        
        plot_bets_1p(common_vars.screen, common_vars.player_bets_1p)

        plot_bets_2p(common_vars.screen, common_vars.player_bets_2p)

        plot_buttons(common_vars.screen, button_status)

        plot_players_1p_hands(common_vars.screen,
                               PLAYER_1P_CARD_START_POS,
                               common_vars.player_hands_1p,
                               common_vars.double_downs,
                               common_vars.hands_status)

        plot_players_2p_hands(common_vars.screen,
                           PLAYER_2P_CARD_START_POS,
                           common_vars.player_hands_2p,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
        DEALER_CARD_START_POS,
        common_vars.dealer_cards,
        common_vars.first_card_hidden)
"""
플레이어가 돈이 없는 상태
x버튼을 누르기 전까지는 상태를 유지하고 누를시 게임을 종료할 수 있음
"""
class FinalState(State):
    def __call__(self, common_vars, button_status):
        account_text = common_vars.text_font.render("Game Over, you're out of money", False, GOLD_COLOR)
        common_vars.screen.blit(account_text, (5, GAME_BOARD_Y_SIZE - 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common_vars.done = True