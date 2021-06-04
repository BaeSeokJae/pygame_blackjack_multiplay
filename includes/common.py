import sys
import os
import pygame

MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, os.path.join(MAIN_DIR, 'includes'))

from .globals import *
from .playingcard import PlayingCard

"""
테이블에 1p 플레이어의 카드를 플로팅함
"""
def plot_players_1p_hands(screen,
                       player_pos_start,
                       player_hands_1p, 
                       double_downs, 
                       hands_status_1p):

    player_x_pos, player_y_pos = player_pos_start
    image_db = ImageDB.get_instance()
    for index_x, hand in enumerate(player_hands_1p):
        for index_y, card in enumerate(hand):

            image = BlackJackCardFormatter.get_instance(IMAGE_PATH_CARDS).get_string(card)

            if index_y == 2 and len(hand) == 3 and double_downs[index_x]:
                screen.blit(pygame.transform.rotate(image_db.get_image(image), 90),
                (player_x_pos, player_y_pos))
            else:
                screen.blit(image_db.get_image(image), (player_x_pos, player_y_pos))
            player_x_pos += GAP_BETWEEN_CARDS
            player_y_pos -= 14
        
        x_offset = -50
        y_offset = -40
        if index_x == 0:
            hand = 'first_hand_'
        else:
            hand = 'second_hand_'
        
        if hands_status_1p[hand + 'blackjack']:
            screen.blit(image_db.get_image(IMAGE_PATH + 'blackjack.png'),
            (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status_1p[hand + 'win']:
            screen.blit(image_db.get_image(IMAGE_PATH + 'you_win.png'),
            (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status_1p[hand + 'push']:
            screen.blit(image_db.get_image(IMAGE_PATH + 'push.png'),
            (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status_1p[hand + 'loose']:
            screen.blit(image_db.get_image(IMAGE_PATH + 'you_loose.png'),
            (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status_1p[hand + 'busted']:
            screen.blit(image_db.get_image(IMAGE_PATH + 'busted.png'),
            (player_x_pos + x_offset, player_y_pos + y_offset))
        player_x_pos, player_y_pos = player_pos_start
        player_x_pos += GAP_BETWEEN_SPLIT

"""
테이블에 2p 플레이어의 카드를 플로팅함
"""
def plot_players_2p_hands(screen,
                       player_pos_start,
                       player_hands_2p, 
                       double_downs, 
                       hands_status_2p):

    player_x_pos, player_y_pos = player_pos_start
    image_db = ImageDB.get_instance()
    for index_x, hand in enumerate(player_hands_2p):
        for index_y, card in enumerate(hand):

            image = BlackJackCardFormatter.get_instance(IMAGE_PATH_CARDS).get_string(card)

            if index_y == 2 and len(hand) == 3 and double_downs[index_x]:
                screen.blit(pygame.transform.rotate(image_db.get_image(image), 90),
                (player_x_pos, player_y_pos))
            else:
                screen.blit(image_db.get_image(image), (player_x_pos, player_y_pos))
            player_x_pos += GAP_BETWEEN_CARDS
            player_y_pos -= 14
        
        x_offset = -50
        y_offset = -40
        if index_x == 0:
            hand = 'first_hand_'
        else:
            hand = 'second_hand_'
        
        if hands_status_2p[hand + 'blackjack']:
            screen.blit(image_db.get_image(IMAGE_PATH + 'blackjack.png'),
            (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status_2p[hand + 'win']:
            screen.blit(image_db.get_image(IMAGE_PATH + 'you_win.png'),
            (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status_2p[hand + 'push']:
            screen.blit(image_db.get_image(IMAGE_PATH + 'push.png'),
            (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status_2p[hand + 'loose']:
            screen.blit(image_db.get_image(IMAGE_PATH + 'you_loose.png'),
            (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status_2p[hand + 'busted']:
            screen.blit(image_db.get_image(IMAGE_PATH + 'busted.png'),
            (player_x_pos + x_offset, player_y_pos + y_offset))
        player_x_pos, player_y_pos = player_pos_start
        player_x_pos += GAP_BETWEEN_SPLIT

"""
딜러에게 모든 카드를 게임 테이블에 배치하고 
첫 번째 카드를 숨겨야하는 경우 해당 카드에 대한 카드를 다시 배치합니다.
"""
def plot_dealers_hand(screen,
                      dealer_card_start_pos,
                      dealer_cards,
                      first_card_hidden):
    dealer_x_pos, dealer_y_pos = dealer_card_start_pos
    image_db = ImageDB.get_instance()
    for card in dealer_cards:
        if first_card_hidden is True:
            screen.blit(image_db.get_image(IMAGE_PATH_CARDS + CARDBACK_FILENAME),
            (dealer_x_pos, dealer_y_pos))
        else:
            image = BlackJackCardFormatter.get_instance(IMAGE_PATH_CARDS).get_string(card)
            screen.blit(image_db.get_image(image), (dealer_x_pos, dealer_y_pos))
        first_card_hidden = False
        dealer_x_pos += GAP_BETWEEN_CARDS
        dealer_y_pos += 14
"""
플레이어가 클릭하고 베팅을 할 때 사용할 칩을 게임 보드에 배치
"""
def plot_chips_1p(screen, player_cash_1p, chips_image_width, visible):
    chips_x_pos, chips_y_pos = CHIPS_START_POS
    gap = chips_image_width + GAP_BETWEEN_CHIPS
    image_db = ImageDB.get_instance()
    if visible:
        if player_cash_1p >= 5:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_5_FILENAME_ON),
            (chips_x_pos, chips_y_pos))
        if player_cash_1p >= 10:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_10_FILENAME_ON),
            (chips_x_pos, chips_y_pos))
        if player_cash_1p >= 50:
            chips_x_pos -= gap
            chips_y_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_50_FILENAME_ON),
            (chips_x_pos, chips_y_pos))
        if player_cash_1p >= 100:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_100_FILENAME_ON),
            (chips_x_pos, chips_y_pos))
    else:
        if player_cash_1p >= 5:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_5_FILENAME_OFF),
            (chips_x_pos, chips_y_pos))
        if player_cash_1p >= 10:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_10_FILENAME_OFF),
            (chips_x_pos, chips_y_pos))
        if player_cash_1p >= 50:
            chips_x_pos -= gap
            chips_y_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_50_FILENAME_OFF),
            (chips_x_pos, chips_y_pos))
        if player_cash_1p >= 100:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_100_FILENAME_OFF),
            (chips_x_pos, chips_y_pos))

def plot_chips_2p(screen, player_cash_2p, chips_image_width, visible):
    chips_x_pos, chips_y_pos = CHIPS_START_POS
    chips_x_pos += 730
    gap = chips_image_width + GAP_BETWEEN_CHIPS
    image_db = ImageDB.get_instance()
    if visible:
        if player_cash_2p >= 5:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_5_FILENAME_ON),
            (chips_x_pos, chips_y_pos))
        if player_cash_2p >= 10:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_10_FILENAME_ON),
            (chips_x_pos, chips_y_pos))
        if player_cash_2p >= 50:
            chips_x_pos -= gap
            chips_y_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_50_FILENAME_ON),
            (chips_x_pos, chips_y_pos))
        if player_cash_2p >= 100:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_100_FILENAME_ON),
            (chips_x_pos, chips_y_pos))
    else:
        if player_cash_2p >= 5:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_5_FILENAME_OFF),
            (chips_x_pos, chips_y_pos))
        if player_cash_2p >= 10:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_10_FILENAME_OFF),
            (chips_x_pos, chips_y_pos))
        if player_cash_2p >= 50:
            chips_x_pos -= gap
            chips_y_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_50_FILENAME_OFF),
            (chips_x_pos, chips_y_pos))
        if player_cash_2p >= 100:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_100_FILENAME_OFF),
            (chips_x_pos, chips_y_pos))
"""
플레이어 베팅 스택에서 사용할 수있는 모든 베팅 더미를 플로팅
split 또는 double down이있는 경우 1 ~ 4 개의 더마가 될 수 있음.
"""
def plot_bets_1p(screen, player_bets_1p):
    image_db = ImageDB.get_instance()
    chip_x_pos = 380
    chip_y_pos = 360
    for bet in player_bets_1p:
        for chip in bet:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + 'chip_{0}_w85h85.png'.format(chip)),
            (chip_x_pos, chip_y_pos))
            chip_y_pos += 8
        chip_y_pos = 360
        chip_x_pos += 50

def plot_bets_2p(screen, player_bets_2p):
    image_db = ImageDB.get_instance()
    chip_x_pos = 548
    chip_y_pos = 360
    for bet in player_bets_2p:
        for chip in bet:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + 'chip_{0}_w85h85.png'.format(chip)),
            (chip_x_pos, chip_y_pos))
            chip_y_pos += 8
        chip_y_pos = 360
        chip_x_pos += 50
"""
보드내의 모든 버튼을 배치함
button_status와 On / Off에 따른 다른 이미지 배치로 클릭 가능 여부를 판단할 수 있음
"""
def plot_buttons(screen, button_status):
    button_x_pos, button_y_pos = BUTTONS_START_POS
    image_db = ImageDB.get_instance()
    if button_status.undo_bet_1p is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + UNDO_BET_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + UNDO_BET_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.play is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + PLAY_BUTTON_FILENAME_ON),
        (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + PLAY_BUTTON_FILENAME_OFF),
        (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.undo_bet_2p is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + UNDO_BET_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + UNDO_BET_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    # if button_status.hit is True:
    #     screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_FILENAME_ON),
    #                 (button_x_pos, button_y_pos))
    # else:
    #     screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_FILENAME_OFF),
    #                 (button_x_pos, button_y_pos))
    # button_x_pos += GAP_BETWEEN_BUTTONS

    # if button_status.stand is True:
    #     screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + STAND_BUTTON_FILENAME_ON),
    #                 (button_x_pos, button_y_pos))
    # else:
    #     screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + STAND_BUTTON_FILENAME_OFF),
    #                 (button_x_pos, button_y_pos))
    # button_x_pos += GAP_BETWEEN_BUTTONS

    # if button_status.split is True:
    #     screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + SPLIT_BUTTON_FILENAME_ON),
    #                 (button_x_pos, button_y_pos))
    # else:
    #     screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + SPLIT_BUTTON_FILENAME_OFF),
    #                 (button_x_pos, button_y_pos))
    # button_x_pos += GAP_BETWEEN_BUTTONS

    # if button_status.double_down is True:
    #     screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + DOUBLE_DOWN_BUTTON_FILENAME_ON),
    #                 (button_x_pos, button_y_pos))
    # else:
    #     screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + DOUBLE_DOWN_BUTTON_FILENAME_OFF),
    #                 (button_x_pos, button_y_pos))
    # button_x_pos += GAP_BETWEEN_BUTTONS

"""
결과에 따른 메시지를 띄워주기 위한 메소드
Player is busted 24 <- 와 같은 형식
"""
def plot_results_1p(screen, text_font, message):
    assert isinstance(message, str)
    text_to_plot = text_font.render(message, False, GOLD_COLOR)
    x_pos, y_pos = STATUS_START_POS
    screen.blit(text_to_plot, (x_pos, y_pos + 50))
    
"""
결과에 따른 메시지를 띄워주기 위한 메소드
Player is busted 24 <- 와 같은 형식
"""
def plot_results_2p(screen, text_font, message):
    assert isinstance(message, str)
    text_to_plot = text_font.render(message, False, GOLD_COLOR)
    x_pos, y_pos = STATUS_START_POS
    screen.blit(text_to_plot, (x_pos + 665, y_pos + 50))

"""
플레이어가 가지고 있는 카드의 점수를 계산합니다.
규칙. 
1. 우선 모든 카드를 10으로 취급합니다.
2. 카드가 에이스이고 현재 패의 총 점수가 17 점 이상 21 점 미만인 경우 
    플레이어는 에이스를 1점의 소프트에이스로 판단해야합니다.
"""
def get_value_of_players_hand(hand):
    assert isinstance(hand, list)
    summary = 0
    num_of_soft_aces = 0
    for card in hand:
        assert isinstance(card, PlayingCard)
        rank = card.get_rank()
        if rank > 10:
            summary += 10
        elif rank == 1 and summary <= 10:
            summary += 11
            num_of_soft_aces += 1
        else:
            summary += rank
        
        if num_of_soft_aces and summary > 21:
            summary -= 10
            num_of_soft_aces -= 1
    return summary

"""
딜러가 가지고 있는 카드의 점수를 계산합니다.
규칙. 
1. 우선 모든 카드를 10으로 취급합니다.
2. 카드가 에이스이고 현재 패의 총 점수가 17 점 이상 21 점 미만인 경우 
    딜러는 에이스를 1점의 소프트에이스로 판단해야합니다.
"""
def get_value_of_dealers_hand(hand):
    assert isinstance(hand, list)
    summary = 0
    hard_ace = 0
    for card in hand:
        assert isinstance(card, PlayingCard)
        rank = card.get_rank()
        if rank > 10:
            summary += 10
        elif rank == 1:
            if 17 <= (summary + 11) < 22:
                summary += 11
            else:
                hard_ace = 1
                summary += 1
                continue
        else:
            summary += rank
        if hard_ace and 17 <= (summary + hard_ace * 10) < 22:
            summary += 10
    return summary
"""
딜러가 가지고 있는 카드집의 카드가 18% 이하인지를 판단하는 함수.
18%이하일시 게임 진행이 불가능하기 때문
"""
def is_cut_passed(shoe_of_decks):
    status = False
    if shoe_of_decks is None or shoe_of_decks.length() < (NUM_OF_DECKS * 52 * 0.18):
        status = True
    return status

"""
플레이어가 초기에 배당받은 2장의 카드를 스플릿 할 수 있는지 판단하는 함수
스플릿 조건
1. 카드가 2장이여야함
2. 2장의 카드가 같은 값이여야함
3. 위의 조건 충족시 True값 리턴
"""
def is_possible_split(player_cards):
    if len(player_cards) != 2:
        return False
    if player_cards[0].get_rank() != player_cards[1].get_rank():
        return False
    else:
        return True

"""
플레이어가 카드를 스플릿했을때 더블 배팅이 가능한 금액을 보유하고 있는지 판단하는 함수
판단 조건
1. 기존 배팅금액보다 현재 보유 금액이 많아야함
위의 조건 충족시 True 리턴
"""
def can_double_bet(player_bets_1p, player_cash_1p):
    if player_cash_1p < sum(player_bets_1p[0]):
        return False
    else:
        return True

class CommenVariables:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
    
    def __init__(self):
        self.done = None
        self.screen = None
        self.shoe_of_decks = None
        # 1p
        self.player_hands_1p = None
        self.player_deal_1p = None
        self.player_hit_1p = None
        self.player_cash_1p = None
        self.player_bets_1p = None
        self.hands_status_1p_ = None
        # 2p
        self.player_hands_2p = None
        self.player_deal_2p = None
        self.player_hit_2p = None
        self.player_cash_2p = None
        self.player_bets_2p = None
        self.hands_status_2p = None
        # common
        
        self.double_downs = None
        self.dealer_cards = None
        self.dealer_last_hand = None
        self.bets_pos = None
        self.game_rounds = None
        self.text_font = None
        self.first_card_hidden = None
        self.pause_time = None
        self.button_image_width = None
        self.button_image_height = None
        self.chips_image_width = None
        self.chips_image_height = None

class ButtonStatus:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.play = False
        self.undo_bet_1p = False
        self.undo_bet_2p = False
        self.hit = False
        self.stand = False
        self.split = False
        self.double_down = False

    def reset(self):
        self.play = False
        self.undo_bet_1p = False
        self.undo_bet_2p = False
        self.hit = False
        self.stand = False
        self.split = False
        self.double_down = False

class ImageDB:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.image_lib = {}

    def get_image(self, path):
        image = self.image_lib.get(path)
        if image is None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path)
            self.image_lib[path] = image
        return image

class ButtonCollideArea:
    instance = None

    @classmethod
    def get_instance(cls, common_vars):
        if cls.instance is None:
            cls.instance = cls(common_vars)
        return cls.instance

    def __init__(self, common_vars):
        button_x_pos, button_y_pos = BUTTONS_START_POS

        self.undo_bet_button_area = pygame.Rect(
            button_x_pos,
            button_y_pos,
            common_vars.button_image_width,
            common_vars.button_image_height
            )
        button_x_pos += GAP_BETWEEN_BUTTONS

        self.play_button_area = pygame.Rect(
            button_x_pos, 
            button_y_pos,
            common_vars.button_image_width, 
            common_vars.button_image_height
            )
        button_x_pos += GAP_BETWEEN_BUTTONS

        # self.hit_button_area = pygame.Rect(
        #     button_x_pos,
        #     button_y_pos,
        #     common_vars.button_image_width,
        #     common_vars.button_image_height
        #     )
        # button_x_pos += GAP_BETWEEN_BUTTONS

        # self.stand_button_area = pygame.Rect(
        #     button_x_pos,
        #     button_y_pos,
        #     common_vars.button_image_width,
        #     common_vars.button_image_height
        #     )
        # button_x_pos += GAP_BETWEEN_BUTTONS

        # self.split_button_area = pygame.Rect(
        #     button_x_pos,
        #     button_y_pos,
        #     common_vars.button_image_width,
        #     common_vars.button_image_height
        #     )
        # button_x_pos += GAP_BETWEEN_BUTTONS

        # self.double_down_button_area = pygame.Rect(
        #     button_x_pos,
        #     button_y_pos,
        #     common_vars.button_image_width,
        #     common_vars.button_image_height
        #     )

class ChipsCollideArea:
    instance = None

    @classmethod
    def get_instance(cls, common_vars):
        if cls.instance is None:
            cls.instance = cls(common_vars)
        return cls.instance
    
    def __init__(self, common_vars):
        chips_x_pos, chips_y_pos = CHIPS_START_POS
        gap = common_vars.chips_image_width + GAP_BETWEEN_CHIPS

        self.chip_5_area_1p = pygame.Rect(
            chips_x_pos,
            chips_y_pos,
            common_vars.chips_image_width,
            common_vars.chips_image_height
        )
        chips_x_pos += gap

        self.chip_10_area_1p = pygame.Rect(
            chips_x_pos,
            chips_y_pos,
            common_vars.chips_image_width,
            common_vars.chips_image_height
        )
        chips_x_pos -= gap
        chips_y_pos += gap

        self.chip_50_area_1p = pygame.Rect(
            chips_x_pos,
            chips_y_pos,
            common_vars.chips_image_width,
            common_vars.chips_image_height
        )
        chips_x_pos += gap

        self.chip_100_area_1p = pygame.Rect(
            chips_x_pos,
            chips_y_pos,
            common_vars.chips_image_width,
            common_vars.chips_image_height
        )

        self.chip_5_area_2p = pygame.Rect(
            chips_x_pos + 630,
            chips_y_pos - 90,
            common_vars.chips_image_width,
            common_vars.chips_image_height
        )
        chips_x_pos += gap

        self.chip_10_area_2p = pygame.Rect(
            chips_x_pos + 630,
            chips_y_pos - 90,
            common_vars.chips_image_width,
            common_vars.chips_image_height
        )
        chips_x_pos -= gap
        chips_y_pos += gap

        self.chip_50_area_2p = pygame.Rect(
            chips_x_pos + 630,
            chips_y_pos - 90,
            common_vars.chips_image_width,
            common_vars.chips_image_height
        )
        chips_x_pos += gap

        self.chip_100_area_2p = pygame.Rect(
            chips_x_pos + 630,
            chips_y_pos - 90,
            common_vars.chips_image_width,
            common_vars.chips_image_height
        )

"""
PlayingCard에서 사용될 메소드 모음입니다.
"""
class BlackJackCardFormatter:
    instance = None

    #  instance가 None이면 instance를 반환하고 그렇지 않으면 기존 인스턴스를 반환합니다.
    @classmethod
    def get_instance(cls, path=""):
        if cls.instance is None:
            cls.instance = cls(path)
        return cls.instance
    
    # 싱글 톤 객체를 인스턴스화하고 정수 값과 해당 문자열 사이의 매핑을 숫자 또는 이름으로 보유하는 속성에 순위를 매 깁니다.
    def __init__(self, path):
        self.path = path
        self.card_rank = ["Invalid", "ace", "2", "3", "4", "5", "6", "7",
                          "8", "9", "10", "jack", "queen", "king"]
        self.card_suit = ["spades", "clubs", "diamonds", "hearts"]
    
    # rank와  suit의 문자열 값을 <rank>_of_<suit>.png 형태의 숫자형으로 변환 후 반환
    # 인스턴스 생성에 경로가 제공된 경우 <path> / <rank> _of_ <suit> .png 형태로 반환하게 됩니다.
    def get_string(self, card):
        image = self.path + self.card_rank[card.get_rank()] + "_of_" \
            + self.card_suit[card.get_suit()] + ".png"

        return image
    
    def get_rank(self, card):
        rank = self.card_rank[card.get_rank()]
        return rank