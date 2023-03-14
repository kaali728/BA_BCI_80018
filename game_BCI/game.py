import pygame
import random
import socket


# Initialize Pygame
pygame.init()

# Set up the display
display_width = 800
display_height = 600
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Brain-controlled game")

# Set up the character
character_width = 50
character_height = 50
character_x = display_width / 2 - character_width / 2
character_y = display_height / 2 - character_height / 2

# Set up the obstacles
obstacle_width = 50
obstacle_height = 50
obstacle_x = random.randrange(0, display_width - obstacle_width)
obstacle_y = -obstacle_height
obstacle_speed = 5

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Set up the font
font = pygame.font.SysFont(None, 25)

# Set up the clock
clock = pygame.time.Clock()


host = socket.gethostname()
port = 8080

s = socket.socket()
s.connect((host, port))
# Main game loop
def game_loop():
    global character_x, character_y, obstacle_x, obstacle_speed, obstacle_y, action, s
    game_exit = False
    score = 0

    while not game_exit:
        action = s.recv(1024).decode('utf-8')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
        if action == "winkL":
            character_x -= 10
        elif action == "winkR":
            character_x += 10
        elif action == "smile":
            character_y -= 10
        elif action == "blink":
            character_y += 10

        # Controll with keyboard
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         game_exit = True
        #     elif event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT:
        #             character_x -= 10
        #         elif event.key == pygame.K_RIGHT:
        #             character_x += 10
        #         elif event.key == pygame.K_UP:
        #             character_y -= 10
        #         elif event.key == pygame.K_DOWN:
        #             character_y += 10

        # Update the obstacles
        obstacle_y += obstacle_speed
        if obstacle_y > display_height:
            obstacle_x = random.randrange(0, display_width - obstacle_width)
            obstacle_y = -obstacle_height
            score += 1

        # Check for collisions
        if character_y < obstacle_y + obstacle_height:
            if character_x > obstacle_x and character_x < obstacle_x + obstacle_width or character_x + character_width > obstacle_x and character_x + character_width < obstacle_x + obstacle_width:
                game_over(score)

        # Draw the character and obstacles
        game_display.fill(white)
        pygame.draw.rect(game_display, black, [character_x, character_y, character_width, character_height])
        pygame.draw.rect(game_display, red, [obstacle_x, obstacle_y, obstacle_width, obstacle_height])

        # Draw the score
        score_text = font.render("Score: " + str(score), True, black)
        game_display.blit(score_text, [0, 0])

        pygame.display.update()

        # Limit the frame rate
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    quit()


# Game over function
def game_over(score):
    game_display.fill(white)
    message = font.render("Game over! Your score was " + str(score), True, black)
    game_display.blit(message,
                      [display_width / 2 - message.get_width() / 2, display_height / 2 - message.get_height() / 2])
    pygame.display.update()
    pygame.time.wait(2000)
    game_loop()

if __name__ == '__main__':
    # Start the game loop
    game_loop()