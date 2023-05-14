import pygame
import copy
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900
FPS = 60
BG_COLOR = (0, 0, 0)

pygame.display.set_caption('CBC Blackjack!')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
active = False
results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...']
hand_outcome = 0
game_records = [0, 0, 0] # win / loss / push
player_score = 0
dealer_score = 0
initial_deal = False

player_hand = []
dealer_hand = []

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4

#######################################
# deal cards by selecting randomly from deck, and make function for one card at a time
#######################################
def deal_cards(current_hand, current_deck):

    card_index = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card_index - 1])
    current_deck.pop(card_index - 1)

    return current_hand, current_deck

#######################################
# pass in player or dealer hand and get best score possible
#######################################
def calculate_score(hand):
    # calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        # for 2,3,4,5,6,7,8,9 - just add the number to total
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        # for 10 and face cards, add 10
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces start by adding 11, we'll check if we need to reduce afterwards
        elif hand[i] == 'A':
            hand_score += 11
    # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score

#######################################
# draw game conditions and buttons
#######################################
def draw_game(active, record, result):
    button_list = []
    # initially on startup (not active) only option is to deal new hand
    if not active:
        # create the "DEAL HAND" button
        deal = pygame.draw.rect(screen, (255, 255, 255), [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, (0, 255, 0), [150, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, (0, 0, 0))
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)
    # once game started, show the HIT and STAND buttons and win/loss records
    else:
        # create the "HIT" button
        hit = pygame.draw.rect(screen, (255, 255, 255), [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, (0, 255, 0), [0, 700, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, (0, 0, 0))
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)

        # create the "STAND" button
        stand = pygame.draw.rect(screen, (255, 255, 255), [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, (0, 255, 0), [300, 700, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, (0, 0, 0))
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)
        
        # create the WIN/LOSS/DRAWS Text
        score_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, (255, 255, 255))
        screen.blit(score_text, (15, 840))

    # if there is an outcome for the hand that was played, display a restart button and tell user what happened
    if result != 0:
        screen.blit(font.render(results[result], True, (255, 255, 255)), (15, 25))

        # create the "NEW HAND" button
        deal = pygame.draw.rect(screen, (255, 255, 255), [150, 220, 300, 100], 0, 5)
        pygame.draw.rect(screen, (0, 255, 0), [150, 220, 300, 100], 3, 5)
        pygame.draw.rect(screen, (0, 0, 0), [153, 223, 294, 94], 3, 5)
        deal_text = font.render('NEW HAND', True, (0, 0, 0))
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)
    return button_list

run = True
while run: # basic game loop

    # run game at our framerate and fill screen with bg color
    timer.tick(FPS)
    screen.fill(BG_COLOR)

    # initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            player_hand, game_deck = deal_cards(player_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False

    # once game is activated, and dealt, calculate scores and display cards
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)

    buttons = draw_game(active, game_records, outcome)

    # listen for basic events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False # exit the game
        if event.type == pygame.MOUSEBUTTONUP: # player clicked something
            if not active:
                if buttons[0].collidepoint(event.pos):
                    # player clicked the "DEAL" button
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    player_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
            else:
                # if player can hit, allow them to draw a card
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                # allow player to end turn (stand)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0

    # if player busts, automatically end turn - treat like a stand
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    #outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    pygame.display.flip()

pygame.quit()