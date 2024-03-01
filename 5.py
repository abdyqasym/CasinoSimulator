import pygame
import random
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)

pygame.init()

background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (800, 600))

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Casino Simulator")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

GAME_MENU = 0
GAME_BLACKJACK = 1
GAME_ROULETTE = 2
game_state = GAME_MENU

player_cards = []
computer_cards = []
game_over = False

roulette_number = None
player_number = None
bet_amount = 0
result_text = ""

def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_main_menu():
    screen.blit(background_image, (0, 0))
    draw_text("Casino Simulator", 250, 50)
    pygame.draw.rect(screen, BLACK, (300, 200, 200, 100), 2)
    draw_text("Blackjack", 330, 230)
    pygame.draw.rect(screen, BLACK, (300, 350, 200, 100), 2)
    draw_text("Roulette", 330, 380)

def draw_blackjack():
    screen.blit(background_image, (0, 0))
    draw_text("Blackjack Game", 250, 50)
    draw_text("Your Cards:", 50, 150)
    for i, card in enumerate(player_cards):
        draw_text(str(card), 50 + i * 50, 180)
    draw_text("Computer's Cards:", 50, 250)
    for i, card in enumerate(computer_cards):
        draw_text(str(card), 50 + i * 50, 280)
    player_score = sum(player_cards)
    computer_score = sum(computer_cards)
    draw_text(f"Your Score: {player_score}", 50, 350)
    draw_text(f"Computer's Score: {computer_score}", 50, 400)
    if game_over:
        if player_score == computer_score:
            draw_text("It's a draw!", 250, 450)
        elif player_score > 21:
            draw_text("You went over. You lose!", 250, 450)
        elif computer_score > 21:
            draw_text("Computer went over. You win!", 250, 450)
        elif player_score > computer_score:
            draw_text("You win!", 250, 450)
        else:
            draw_text("You lose!", 250, 450)
    pygame.draw.rect(screen, BLACK, (50, 500, 100, 50), 2)
    draw_text("Hit", 80, 515)
    pygame.draw.rect(screen, BLACK, (200, 500, 100, 50), 2)
    draw_text("Stand", 220, 515)

def draw_roulette():
    screen.blit(background_image, (0, 0))
    draw_text("Roulette Game", 270, 50)
    pygame.draw.circle(screen, BLACK, (400, 300), 200, 2)
    for i in range(0, 37):
        if i == 0:
            color = GREEN
        else:
            color = BLACK
        pygame.draw.circle(screen, color, (int(400 + 160 * math.cos(i * 2 * math.pi / 37)), int(300 + 160 * math.sin(i * 2 * math.pi / 37))), 20)
        draw_text(str(i), int(400 + 160 * math.cos(i * 2 * math.pi / 37)) - 10, int(300 + 160 * math.sin(i * 2 * math.pi / 37)) - 10)

def handle_input():
    global game_state, player_cards, computer_cards, game_over
    global player_number, bet_amount, roulette_number, result_text

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if player_number is None:
                    try:
                        player_number = int(input("Choose a number (from 0 to 36): "))
                        if not (0 <= player_number <= 36):
                            raise ValueError
                    except ValueError:
                        print("Invalid input. Please choose a number from 0 to 36.")
                        player_number = None
                elif bet_amount == 0:
                    try:
                        bet_amount = int(input("Enter the bet amount: "))
                        if bet_amount <= 0:
                            raise ValueError
                    except ValueError:
                        print("Invalid input. Please enter a positive bet amount.")
                        bet_amount = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if game_state == GAME_MENU:
                if 300 <= mouse_x <= 500:
                    if 200 <= mouse_y <= 300:
                        game_state = GAME_BLACKJACK
                        player_cards = [random.randint(1, 11), random.randint(1, 11)]
                        computer_cards = [random.randint(1, 11)]
                    elif 350 <= mouse_y <= 450:
                        game_state = GAME_ROULETTE
            elif game_state == GAME_BLACKJACK:
                if 50 <= mouse_x <= 150 and 500 <= mouse_y <= 550:
                    player_cards.append(random.randint(1, 11))
                elif 200 <= mouse_x <= 300 and 500 <= mouse_y <= 550:
                    game_over = True
            elif game_state == GAME_ROULETTE:
                if 700 <= mouse_x <= 770 and 50 <= mouse_y <= 80:
                    if player_number is not None and bet_amount > 0:
                        roulette_number = random.randint(0, 36)
                        if roulette_number == player_number:
                            result_text = "Congratulations! You won " + str(bet_amount * 36) + "!"
                        else:
                            result_text = "Sorry, you lost."
                        player_number = None
                        bet_amount = 0

def dealer_play():
    global computer_cards
    while sum(computer_cards) < 17:
        computer_cards.append(random.randint(1, 11))
        screen.fill(GREEN)
        draw_blackjack()
        pygame.display.flip()

running = True
while running:
    screen.fill(GREEN)

    handle_input()

    if game_state == GAME_MENU:
        draw_main_menu()
    elif game_state == GAME_BLACKJACK:
        draw_blackjack()
        if game_over:
            dealer_play()
            game_over = False
    elif game_state == GAME_ROULETTE:
        draw_roulette()

    if game_state == GAME_BLACKJACK and game_over:
        draw_text(result_text, 250, 500)

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
