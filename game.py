import pygame
import os

pygame.init()


def get_asset_file(filename):
    return os.path.join(ASSETS_FOLDER, filename)


# TODO: look into subsurface for optimization
def get_image_at(spritesheet, rect):
    image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
    image.blit(spritesheet, (0, 0), rect)
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
    YELLOW_GREEN = (154, 205, 50)

class Wind:
    pass

class Slab:
    def __init__(self, rect):
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(Color.YELLOW_GREEN)
        self.position = (self.rect.x, self.rect.y)

    def render(self, display):
        display.blit(self.image, self.position)


class Grass:

    def __init__(self, position):
        self.__sprites = []
        self.__sprite_index = 0
        self.__frames = 0
        self.position = position

    def update(self):
        pass

    def render(self, display):
        pass

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
    JUMPING_START = apply_image_transform(pygame.rect.Rect(103, 30, 13, 14))
    JUMPING_MID = apply_image_transform(pygame.rect.Rect(120, 27, 15, 11))
    JUMPING_END = apply_image_transform(pygame.rect.Rect(138, 32, 15, 11))

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
        self.position = start_position
        self.velocity = [0, 0]
        self.__frames = 0
        self.__group_index = 0
        self.__direction_index = 0
        self.__sprite_index = 0
        self.__sprites = [
            Goat.GROUP_STANDING,
            Goat.GROUP_WALKING,
            Goat.GROUP_JUMPING,
            Goat.GROUP_EATING,
            Goat.GROUP_FLOWER
            ]
        self.__is_moving_horizontally = False
        self.__is_grounded = True
        self.image = self.__sprite
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1] - self.rect.height

        self.__debug_surface = pygame.Surface((self.rect.width, self.rect.height))
        self.__debug_surface.fill(Color.RED)

    def update_draw_position(self):
        self.image = self.__sprite
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1] - self.rect.height
        self.__debug_surface = pygame.Surface((self.rect.width, self.rect.height))
        self.__debug_surface.fill(Color.RED)

    @property
    def is_moving_horizontally(self):
        return self.__is_moving_horizontally

    @is_moving_horizontally.setter
    def is_moving_horizontally(self, moving):
        if self.is_grounded:
            if moving:
                self.__group_index = 1
            else:
                self.__group_index = 0
        self.update_indices()
        self.__is_moving_horizontally = moving

    @property
    def is_grounded(self):
        return self.__is_grounded

    @is_grounded.setter
    def is_grounded(self, grounded):
        # reset the sprite index to ensure we start at the beginning of the jump
        if self.__is_grounded and not grounded:
            self.__group_index = 2
            self.__sprite_index = 0
        self.__is_grounded = grounded

    @property
    def direction(self):
        return self.__direction_index

    def update_indices(self):
        self.__sprite_index = self.__sprite_index % len(self.__direction())

    def turn_right(self):
        self.__direction_index = 0
        self.update_indices()

    def turn_left(self):
        self.__direction_index = 1
        self.update_indices()

    def __group(self):
        return self.__sprites[self.__group_index]

    def __direction(self):
        return self.__sprites[self.__group_index][self.__direction_index]

    @property
    def __sprite(self):
        return self.__sprites[self.__group_index][self.__direction_index][self.__sprite_index]

    def update(self):
        self.__frames += 1
        if self.__frames >= 12:
            self.__sprite_index = (self.__sprite_index + 1) % len(self.__direction())
            self.update_draw_position()
            self.__frames = 0

    def render(self, display):

        display.blit(self.__debug_surface, (self.rect.x, self.rect.y))
        display.blit(self.__sprite, (self.rect.x, self.rect.y))


def is_entity_on_ground(entity, slabs):
    entity_rect = entity.rect.copy()
    entity_rect.y += 2
    for slab in slabs:
        if entity_rect.colliderect(slab.rect):
            return True
    return False


def run_game():
    pygame.display.set_caption('The Grass is Always Greener - Ludum Dare 38 - Theme: A Small World')
    # pygame.display.set_icon(Player.SPRITE_DEATH)

    # initialize the mixer for sound to work
    # pygame.mixer.music.load(get_asset_file('background_music.ogg'))
    # pygame.mixer.music.play(-1)

    # clock for keeping track of time, ticks, and frames per second
    clock = pygame.time.Clock()
    goat = Goat([15, 15])
    grass_left = Grass((15, 400))
    grass_right = Grass((780, 400))
    ground = Slab(pygame.Rect(0, 250, 800, 350))
    wall = Slab(pygame.Rect(400, 0, 15, 250))
    slabs = [ground, wall]
    done = False
    while not done:
        clock.tick(60)
        display.fill(Color.LIGHT_SKY_BLUE)

        goat.is_grounded = is_entity_on_ground(goat, slabs)
        if goat.is_grounded:
            goat.velocity[0] = 0

        # handle input
        events = pygame.event.get()
        keys_pressed = pygame.key.get_pressed()
        goat.is_moving_horizontally = keys_pressed[pygame.K_a] or keys_pressed[pygame.K_d]
        for event in events:
            # handle clicking the X on the game window
            if event.type == pygame.QUIT:
                print('received a quit request')
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_a:
                    goat.turn_left()
                    print('a pressed')
                if event.key == pygame.K_d:
                    goat.turn_right()
                    print('d pressed')
                if event.key == pygame.K_e:
                    print('e pressed')
                if event.key == pygame.K_SPACE and goat.is_grounded:
                    goat.is_grounded = False
                    goat.velocity[1] = -2
                    print('space pressed')

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    if goat.is_moving_horizontally:
                        goat.turn_right()
                    print('a released')
                if event.key == pygame.K_d:
                    if goat.is_moving_horizontally:
                        goat.turn_left()
                    print('d released')
                if event.key == pygame.K_e:
                    print('e released')
                if event.key == pygame.K_SPACE:
                    print('space released')

            # goat is moving right
        if goat.is_moving_horizontally and goat.direction == 0:
            goat.velocity[0] = 1
        elif goat.is_moving_horizontally and goat.direction == 1:
            goat.velocity[0] = -1
        elif not goat.is_moving_horizontally:
            goat.velocity[0] = 0

        if goat.velocity[1] == 0:
            goat.velocity[1] = 1
        else:
            goat.velocity[1] += 0.15

        # update
        goat.rect.x += goat.velocity[0]
        for slab in slabs:
            # if there is a collision
            if goat.rect.colliderect(slab.rect):

                # player collides with a platform on their right
                if slab.rect.left < goat.rect.right < slab.rect.right:
                    goat.rect.right = slab.rect.left

                # player collides with a platform on their left
                elif slab.left < goat.rect.left < slab.rect.right:
                    goat.rect.left = slab.rect.right

                goat.velocity[0] = 0

        goat.rect.y += goat.velocity[1]
        for slab in slabs:
            if goat.rect.colliderect(slab.rect):

                # player collides with a platform on their head
                if goat.velocity[1] < 0:
                    goat.rect.top = slab.rect.bottom

                # player collides standing on a platform
                elif goat.velocity[1] > 0:
                    goat.rect.bottom = slab.rect.top

                goat.velocity[1] = 0

        goat.position[0] = goat.rect.x
        goat.position[1] = goat.rect.bottom

        # -- update player
        goat.update()
        # -- update particles
        # -- update grass

        # render
        # -- render background
        for slab in slabs:
            slab.render(display)
        # -- render foreground
        # -- render grass
        # -- render player
        goat.render(display)

        # -- render debug

        pygame.display.flip()


if __name__ == '__main__':
    run_game()
