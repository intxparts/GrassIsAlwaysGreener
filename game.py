import pygame
import os

pygame.init()

ASSETS_FOLDER = os.path.join(os.getcwd(), 'Assets')


def get_asset_file(filename):
    return os.path.join(ASSETS_FOLDER, filename)


class Color:
    STEEL_BLUE = (95, 158, 160)
    BLACK = (0, 0, 0)
    AWESOME_GRAY = (49, 49, 49)


class Player:
    pass


def run_game():
    pygame.display.set_caption('The Grass is Always Greener - Ludum Dare 38 - Theme: A Small World')
    # pygame.display.set_icon(Player.SPRITE_DEATH)

    # initialize the display for drawing to the screen
    display = pygame.display.set_mode([800, 600], pygame.DOUBLEBUF, 32)

    # initialize the mixer for sound to work
    # pygame.mixer.music.load(get_asset_file('background_music.ogg'))
    # pygame.mixer.music.play(-1)

    # clock for keeping track of time, ticks, and frames per second
    clock = pygame.time.Clock()

    done = False
    while not done:
        clock.tick(60)
        display.fill(Color.BLACK)

        # handle input
        print('handle input')
        events = pygame.event.get()

        # handle input
        for event in events:
            # handle clicking the X on the game window
            if event.type == pygame.QUIT:
                print('received a quit request')
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_a:
                    pass  # move left
                if event.key == pygame.K_d:
                    pass  # move right
                if event.key == pygame.K_e:
                    pass  # eat
                if event.key == pygame.K_SPACE:
                    pass  # jump

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    pass
                if event.key == pygame.K_d:
                    pass
                if event.key == pygame.K_SPACE:
                    pass
        # update
        # -- update player
        # -- update particles
        # -- update grass

        # render
        # -- render background
        # -- render foreground
        # -- render grass
        # -- render player
        # -- render debug


if __name__ == '__main__':
    run_game()
