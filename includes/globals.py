# Paths
IMAGE_PATH = 'images/'
IMAGE_PATH_CARDS = 'images/cards/'
IMAGE_PATH_CHIPS = 'images/casino_chips/'
IMAGE_PATH_BUTTONS = 'images/buttons/'
SOUND_PATH = 'sounds/'
# previously using IMAGE_PATH = "./images/" which works as well

# The card back image used to print the dealers initial hidden card
CARDBACK_FILENAME = "cardback1.png"

# All button images
PLAY_BUTTON_FILENAME_ON = "play_button_blue.png"
PLAY_BUTTON_FILENAME_OFF = "play_button_blue_fade.png"
HIT_BUTTON_FILENAME_ON = "hit_button_blue.png"
HIT_BUTTON_FILENAME_OFF = "hit_button_blue_fade.png"
STAND_BUTTON_FILENAME_ON = "stand_button_blue.png"
STAND_BUTTON_FILENAME_OFF = "stand_button_blue_fade.png"
SPLIT_BUTTON_FILENAME_ON = "split_button_blue.png"
SPLIT_BUTTON_FILENAME_OFF = "split_button_blue_fade.png"
DOUBLE_DOWN_BUTTON_FILENAME_ON = "doubledown_button_blue.png"
DOUBLE_DOWN_BUTTON_FILENAME_OFF = "doubledown_button_blue_fade.png"
UNDO_BET_BUTTON_FILENAME_ON = "undobet_button_blue.png"
UNDO_BET_BUTTON_FILENAME_OFF = "undobet_button_blue_fade.png"
UNDO_BET_2P_BUTTON_FILENAME_ON = "undobet_button_blue_2p.png"
UNDO_BET_2P_BUTTON_FILENAME_OFF = "undobet_button_blue_fade_2p.png"

# All chips images
CHIP_5_FILENAME_ON = "chip_5_w85h85.png"
CHIP_5_FILENAME_OFF = "chip_5_w85h85_fade.png"
CHIP_10_FILENAME_ON = "chip_10_w85h85.png"
CHIP_10_FILENAME_OFF = "chip_10_w85h85_fade.png"
CHIP_50_FILENAME_ON = "chip_50_w85h85.png"
CHIP_50_FILENAME_OFF = "chip_50_w85h85_fade.png"
CHIP_100_FILENAME_ON = "chip_100_w85h85.png"
CHIP_100_FILENAME_OFF = "chip_100_w85h85_fade.png"

# Colors
GAME_BOARD_COLOR = (34, 139,  34)  # Nice TexasHoldem table color
GOLD_COLOR = (255, 215, 0)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
BLUE_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 255, 0)
RED_COLOR = (255, 0, 0)
YELLOW_COLOR = (255, 255, 0)

# Size, positions and gaps between objects on the game board
GAME_BOARD_SIZE = (1024, 600)
GAME_BOARD_X_SIZE = GAME_BOARD_SIZE[0]
GAME_BOARD_Y_SIZE = GAME_BOARD_SIZE[1]
PLAYER_1P_CARD_START_POS = (100, 220)
PLAYER_2P_CARD_START_POS = (830, 220)
DEALER_CARD_START_POS = (int(GAME_BOARD_X_SIZE * 0.455), 70)
CHIPS_START_POS = (50, 360)
BUTTONS_START_POS = (355, 555)
STATUS_START_POS = (30, 15)
GAP_BETWEEN_CARDS = 20
GAP_BETWEEN_CHIPS = 10
GAP_BETWEEN_BUTTONS = 102
GAP_BETWEEN_SPLIT = 190

# Timers in seconds
PAUSE_TIMER1 = 0.5
PAUSE_TIMER2 = 1
PAUSE_TIMER3 = 3

# Misc
NUM_OF_DECKS = 4
LOWEST_BET = 5
DEFAULT_PLAYER_BALANCE = 5000
COUNTING_HELP = True

# Rank
RANK = {}

# Game Status
HIT = "hit"
STAND = "stand"
DOUBLE_DOWN = "double_down"