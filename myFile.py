from includes.common import *

def betting(player_hands_1p, dealer_hands, total_rank):
    player_first_card = BlackJackCardFormatter.get_instance().get_rank(player_hands_1p[0])
    player_second_card = BlackJackCardFormatter.get_instance().get_rank(player_hands_1p[1])
    dealer_card = BlackJackCardFormatter.get_instance().get_rank(dealer_hands)
    # 함수 쓰세요
        # player_hands_1p = KQJ(player_hands_1p)
    if (len(player_hands_1p) == 2):
        print("플레이어:", player_first_card, "," , player_second_card)
        print("딜러: ", dealer_card)
    else:
        player_third_card = BlackJackCardFormatter.get_instance().get_rank(player_hands_1p[2])
        print("플레이어:", player_first_card, "," , player_second_card, "," , player_third_card)
        print("딜러: ", dealer_card)
    if (total_rank >= 17):
        return "stand"
    else:
        return "hit"
