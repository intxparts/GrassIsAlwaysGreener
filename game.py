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

    def generate_left_image_group(right_image_group):
        left_image_group = []
        for i in right_image_group:
            left_image_group.append(pygame.transform.flip(i, True, False))
        return left_image_group

    def apply_image_transform(rect):
        return pygame.transform.scale2x(get_image_at(SPRITE_SHEET, rect))

    STANDING_NORMAL = apply_image_transform(pygame.rect.Rect(26, 31, 16, 12))
    STANDING_CROUCHED = apply_image_transform(pygame.rect.Rect(8, 32, 16, 11))

    WALKING_TOGETHER = apply_image_transform(pygame.rect.Rect(44, 32, 14, 11))
    WALKING_SEPARATE = apply_image_transform(pygame.rect.Rect(78, 31, 15, 12))

    # FIX THESE
    JUMPING_START = apply_image_transform(pygame.rect.Rect(26, 31, 16, 12))
    JUMPING_MID = apply_image_transform(pygame.rect.Rect(26, 31, 16, 12))
    JUMPING_END = apply_image_transform(pygame.rect.Rect(26, 31, 16, 12))

    EATING_STANDING = apply_image_transform(pygame.rect.Rect(26, 31, 16, 12))
    EATING_CROUCHED = apply_image_transform(pygame.rect.Rect(26, 31, 16, 12))

    FLOWER_STANDING = apply_image_transform(pygame.rect.Rect(26, 31, 16, 12))
    FLOWER_CROUCHED = apply_image_transform(pygame.rect.Rect(26, 31, 16, 12))

    GROUP_STANDING_RIGHT = [STANDING_NORMAL, STANDING_CROUCHED]
    GROUP_STANDING_LEFT = generate_left_image_group(GROUP_STANDING_RIGHT)
    GROUP_STANDING = [GROUP_STANDING_RIGHT, GROUP_STANDING_LEFT]
    GROUP_JUMPING_RIGHT = [JUMPING_START, JUMPING_MID, JUMPING_END]
    GROUP_JUMPING_LEFT = generate_left_image_group(GROUP_JUMPING_RIGHT)
    GROUP_JUMPING = [GROUP_JUMPING_RIGHT, GROUP_JUMPING_LEFT]
    GROUP_WALKING_RIGHT = [
        STANDING_NORMAL,
        WALKING_TOGETHER,
        # STANDING_CROUCHED,
        WALKING_SEPARATE
        ]
    GROUP_WALKING_LEFT = generate_left_image_group(GROUP_WALKING_RIGHT)
    GROUP_WALKING = [GROUP_WALKING_RIGHT, GROUP_WALKING_LEFT]
    GROUP_EATING_RIGHT = [EATING_STANDING, EATING_CROUCHED]
    GROUP_EATING_LEFT = generate_left_image_group(GROUP_EATING_RIGHT)
    GROUP_EATING = [GROUP_EATING_RIGHT, GROUP_EATING_LEFT]
    GROUP_FLOWER_RIGHT = [FLOWER_STANDING, FLOWER_CROUCHED]
    GROUP_FLOWER_LEFT = generate_left_image_group(GROUP_FLOWER_RIGHT)
    GROUP_FLOWER = [GROUP_FLOWER_RIGHT, GROUP_FLOWER_LEFT]

    def __init__(self, start_position):
        self.__position = start_position
        self.__frames = 0
        self.__group_index = 1
        self.__direction_index = 0
        self.__sprite_index = 0
        self.__sprites = [
            Goat.GROUP_STANDING,
            Goat.GROUP_WALKING,
            Goat.GROUP_JUMPING,
            Goat.GROUP_EATING,
            Goat.GROUP_FLOWER
            ]

        self.image = self.__sprite
        self.rect = self.image.get_rect()
        self.rect.x = self.__position[0]
        self.rect.y = self.__position[1] - self.rect.height

        self.__debug_surface = pygame.Surface((self.rect.width, self.rect.height))
        self.__debug_surface.fill(Color.RED)

    def update_draw_position(self):
        self.image = self.__sprite
        self.rect = self.image.get_rect()
        self.rect.x = self.__position[0]
        self.rect.y = self.__position[1] - self.rect.height
        self.__debug_surface = pygame.Surface((self.rect.width, self.rect.height))
        self.__debug_surface.fill(Color.RED)

    @property
    def position(self):
        return self.__position

    def __group(self):
        return self.__sprites[self.__group_index]

    def __direction(self):
        return self.__sprites[self.__group_index][self.__direction_index]

    @property
    def __sprite(self):
        return self.__sprites[self.__group_index][self.__direction_index][self.__sprite_index]

    def update(self):
        pass

    def render(self, display):
        self.__frames += 1
        if self.__frames >= 20:
            self.__sprite_index = (self.__sprite_index + 1) % len(self.__direction())
            self.update_draw_position()
            self.__frames = 0
        display.blit(self.__debug_surface, (self.rect.x, self.rect.y))
        display.blit(self.__sprite, (self.rect.x, self.rect.y))


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
