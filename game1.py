# need to download assets from github - background, music, etc.
# pygame is a 2d graphics library that allows us to create 2d games
import pygame
# need the operating system to help us define the path to the images/sounds
import os
# initialize font library
pygame.font.init()
# initialize sound effect library
pygame.mixer.init()

# make the main surface - or window
# everything in pygame that we create is known as a surface
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Caption of window
pygame.display.set_caption("First Game!")


# variable for RGB white
WHITE = (255, 255, 255)
BLACK = (0, 0, 0 )
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
# health font
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT= pygame.font.SysFont('comicsans', 100)

# creER_FONT ate a border - x, y , width height
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10,  HEIGHT)

# bullet sound
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

# frames per second, should be consistent for each comp
FPS = 60
# velocity - how much we want our spaceship to move, pixels
VEL = 5
# bullet velocity
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# events if our spaceship is hit
YELLOW_HIT = pygame.USEREVENT + 1
# if both were 1, they would both be the same event
# we need a unique event ID
RED_HIT = pygame.USEREVENT + 2

# load the yellow and red space ship image from the Assets file
YELLOW_SPACE_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
# resizing and rotation
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACE_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT )), 90)

RED_SPACE_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACE_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT )), 270)

# load in our space background, rescale image
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


# take as an argument what I want to draw
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # fill this window with color with SPACE background
    WIN.blit(SPACE, (0,0))
    # create rectangular border in the middle
    pygame.draw.rect(WIN, BLACK, BORDER)
    # text display
    red_health_text = HEALTH_FONT.render(" Red Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Yellow Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # use blit when you want to draw the surface onto the screen
    # 2nd element is the position on the screen
    # 0,0 is at the top left hand corner
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))


    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # update the display
    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    # yellow space ship
    # make sure we cant move off screen
    if keys_pressed[pygame.K_a] and (yellow.x - VEL) > 0:  # left key, a, for yellow spaceship
        # move us to the left. subtract from our current x value
        yellow.x -= VEL
    # need to make sure the rectangle is not over the border, including ts width
    if keys_pressed[pygame.K_d] and (yellow.x + VEL + yellow.width) < BORDER.x:  # right key
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and (yellow.y - VEL) > 0:  # up key
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and (yellow.y + VEL + yellow.height) < (HEIGHT - 10):  # down key
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    # red spaceship
    if keys_pressed[pygame.K_LEFT] and (red.x - VEL) > BORDER.x + BORDER.width:  # left key
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and (red.x + VEL + red.width) < WIDTH:  # right key
        red.x += VEL
    if keys_pressed[pygame.K_UP] and (red.y - VEL) > 0:  # up key
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and (red.y + VEL + red.height) < (HEIGHT - 10):  # down key
        red.y += VEL

# handle the collision of the bullets
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        # yellow bullets are coming from the left to the right
        bullet.x += BULLET_VEL
        # did yellow bullets collide with the red ship?
        # colliderect only works if both objects are rectangles
        if red.colliderect(bullet):
            # we now need to tell the main loop that a collision has occurred
            pygame.event.post(pygame.event.Event(RED_HIT))
            # remove the bullet from the list, if it has collided
            yellow_bullets.remove(bullet)
        # check if the bullets are off screen
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        # did red bullets collide with the yellow ship?
        if yellow.colliderect(bullet):
            # we now need to tell the main loop that a collision has occurred
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            # remove the bullet from the list, if it has collided
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# you win text
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    # puts text directly in middle of screen
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    # delay for 5000 milliseconds
    pygame.time.delay(5000)


# our main function - that contains the loop
def main():
    # create 2 rectangles for each spaceship so we can control where they're moving to
    # red space ship is on the right, yellow on the left
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # empty list for our bullets
    red_bullets = []
    yellow_bullets = []

    # health
    red_health = 10
    yellow_health = 10

    # clock for FPS
    clock = pygame.time.Clock()
    # set up a while loop - a game loop
    run = True
    while run:
        # run this  while loop according to the FPS, so 60 times per sec
        clock.tick(FPS)
        # for each of the different events in pygame
        for event in pygame.event.get():
            # first event is to check if the user quit the window
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # bullet firing - left control and right control
            if event.type == pygame.KEYDOWN:
                # bullet from the left goes to the right
                # only 3 bullets fired on screen
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    # x, y, width, height
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    #sound effect
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    # x, y, width, height
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # if space shit has been hit
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        # pass the winner text
        if winner_text != "":
            draw_winner(winner_text)
            break

        #print(red_bullets, yellow_bullets)
        # movement of spaceships
        # allows for multiple keys to be pressed at the same time
        # or if the key is still being pressed to register it
        keys_pressed = pygame.key.get_pressed()
        # pass the keys being pressed and the yellow function
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    # restart the game
    main()

# calling our main function, if we run this file directly (for ex: dont run if file is imported)
if __name__ == "__main__":
    main()