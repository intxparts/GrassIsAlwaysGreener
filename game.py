import pygame
import os

pygame.init()


def get_asset_file(filename):
    return os.path.join(ASSETS_FOLDER, filename)


# TODO: look into subsurface for optimization
def get_image_at(spritesheet, rect):
    image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
    image.blit(spritesheet, (0, 0), rect)
    # image = pygame.transform.scale2x(image)
    return image


# initialize the display for drawing to the screen
display = pygame.display.set_mode([800, 600], pygame.DOUBLEBUF, 32)
ASSETS_FOLDER = os.path.join(os.getcwd(), 'Assets')
SPRITE_SHEET = pygame.image.load(get_asset_file('goats.png')).convert_alpha()


class Color:
    STEEL_BLUE = (95, 158, 160)
    BLACK = (0, 0, 0)
    AWESOME_GRAY = (49, 49, 49)
    LIGHT_SKY_BLUE = (135, 206, 250)
    RED = (255, 0, 0)


class Goat:

    STANDING_NORMAL = pygame.transform.scale2x(get_image_at(SPRITE_SHEET, pygame.rect.Rect(26, 31, 16, 12)))
    STANDING_NORMAL_LEFT = pygame.transform.flip(STANDING_NORMAL, True, False)

    def __init__(self, start_position):
        self.__position = start_position
        self.image = Goat.STANDING_NORMAL
        self.rect = self.image.get_rect()

        self.__debug_surface = pygame.Surface((self.rect.width, self.rect.height))
        self.__debug_surface.fill(Color.RED)

    @property
    def position(self):
        return self.__position

    def update(self):
        pass

    def render(self, display):
        display.blit(self.__debug_surface, self.__position)
        display.blit(Goat.STANDING_NORMAL, self.__position)


def run_game():
    pygame.display.set_caption('The Grass is Always Greener - Ludum Dare 38 - Theme: A Small World')
    # pygame.display.set_icon(Player.SPRITE_DEATH)

    # initialize the mixer for sound to work
    # pygame.mixer.music.load(get_asset_file('background_music.ogg'))
    # pygame.mixer.music.play(-1)

    # clock for keeping track of time, ticks, and frames per second
    clock = pygame.time.Clock()
    goat = Goat((250, 250))
    done = False
    while not done:
        clock.tick(60)
        display.fill(Color.LIGHT_SKY_BLUE)

        # handle input
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
                    print('a pressed')
                if event.key == pygame.K_d:
                    print('d pressed')
                if event.key == pygame.K_e:
                    print('e pressed')
                if event.key == pygame.K_SPACE:
                    print('space pressed')

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    print('a released')
                if event.key == pygame.K_d:
                    print('d released')
                if event.key == pygame.K_e:
                    print('e released')
                if event.key == pygame.K_SPACE:
                    print('space released')
        # update
        # -- update player
        # -- update particles
        # -- update grass

        # render
        # -- render background
        # -- render foreground
        # -- render grass
        # -- render player
        goat.render(display)

        # -- render debug

        pygame.display.flip()


if __name__ == '__main__':
    run_game()
