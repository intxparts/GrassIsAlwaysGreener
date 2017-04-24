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
display = pygame.display.set_mode([320, 240], pygame.DOUBLEBUF, 32)
ASSETS_FOLDER = os.path.join(os.getcwd(), 'Assets')
SPRITE_SHEET = pygame.image.load(get_asset_file('goats.png')).convert_alpha()
WORLD = pygame.image.load(get_asset_file('world.png'))


def apply_image_transform(rect):
    return pygame.transform.scale2x(get_image_at(SPRITE_SHEET, rect))


class Color:
    STEEL_BLUE = (95, 158, 160)
    BLACK = (0, 0, 0)
    AWESOME_GRAY = (49, 49, 49)
    LIGHT_SKY_BLUE = (135, 206, 250)
    RED = (255, 0, 0)
    YELLOW_GREEN = (154, 205, 50)


class Flower:
    SPRITE = apply_image_transform(pygame.Rect(38, 60, 3, 5))
    SOUND = pygame.mixer.Sound(get_asset_file('flowerappearing.ogg'))

    def __init__(self):
        self.display = False
        self.position = (235, 135)

    def render(self, display):
        if self.display:
            display.blit(Flower.SPRITE, self.position)


class EatingParticles:
    SPRITE1 = apply_image_transform(pygame.Rect(0, 69, 8, 11))
    SPRITE2 = apply_image_transform(pygame.Rect(8, 69, 10, 11))
    SPRITE3 = apply_image_transform(pygame.Rect(18, 69, 11, 11))
    SOUND = pygame.mixer.Sound(get_asset_file('eating.ogg'))

    def __init__(self):
        self.active = False
        self.__sprites = [EatingParticles.SPRITE1, EatingParticles.SPRITE2, EatingParticles.SPRITE3]
        self.__sprite_index = 0
        self.__frames = 0

    def update(self):
        if self.active:
            self.__frames += 1
            if self.__frames >= 32:
                self.__sprite_index = (self.__sprite_index + 1) % len(self.__sprites)
                self.__frames = 0

    @property
    def current_image(self):
        return self.__sprites[self.__sprite_index]


class HappyBubble:
    SPRITE = apply_image_transform(pygame.Rect(136, 0, 154, 18))

    def __init__(self):
        self.display = False


class HungerBubble:
    SPRITE = apply_image_transform(pygame.Rect(115, 0, 19, 18))

    def __init__(self):
        self.__frames = 0
        self.display = True

    def update(self):
        if self.display:
            self.__frames += 1
            if self.__frames >= 200:
                self.display = False


class Bridge:
    SPRITE = apply_image_transform(pygame.Rect(55, 69, 46, 2))
    DEBRIS_1 = apply_image_transform(pygame.Rect(61, 81, 14, 12))
    DEBRIS_2 = apply_image_transform(pygame.Rect(80, 77, 25, 17))
    BREAKING_SOUND = pygame.mixer.Sound(get_asset_file('boulderbreakingwood.ogg'))

    def __init__(self):
        self.position = (121, 143)
        self.__debris_particles = [Bridge.DEBRIS_1, Bridge.DEBRIS_2]
        self.__debris_position = [(42 + self.position[0], 2 + self.position[1]), (42 + self.position[0], 2 + self.position[1])]
        self.image = Bridge.SPRITE
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.__is_broken = False
        self.__display_debris = False
        self.__debris_index = 0
        self.__frames = 0

    @property
    def is_broken(self):
        return self.__is_broken

    @is_broken.setter
    def is_broken(self, broken):
        if broken:
            self.__display_debris = True
            Bridge.BREAKING_SOUND.play(0)
        self.__is_broken = broken

    def update(self):
        if self.is_broken:
            self.__frames += 1
            if self.__frames > 16:
                if self.__debris_index == 1:
                    self.__display_debris = False
                else:
                    self.__debris_index += 1

    def render(self, display):
        if not self.is_broken:
            display.blit(self.image, self.position)
        if self.__display_debris:
            display.blit(self.__debris_particles[self.__debris_index], self.__debris_position[self.__debris_index])
        # debug = pygame.Surface((self.rect.width, self.rect.height))
        # debug.fill(Color.YELLOW_GREEN)
        # display.blit(debug, (self.rect.x, self.rect.y))


class Boulder:
    SPRITE = apply_image_transform(pygame.Rect(121, 62, 34, 36))

    def __init__(self):
        self.position = [140, -80]
        self.active = False
        self.image = Boulder.SPRITE
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.velocity = (0, 10)

    def render(self, display):
        if self.active:
            display.blit(self.SPRITE, (self.rect.x, self.rect.y))


class Wind:
    SPRITE1 = apply_image_transform(pygame.Rect(0, 80, 28, 13))
    SPRITE2 = apply_image_transform(pygame.Rect(27, 80, 28, 13))
    SPRITE3 = apply_image_transform(pygame.Rect(28, 67, 27, 13))
    SOUND = pygame.mixer.Sound(get_asset_file('strongestwind.ogg'))

    def __init__(self):
        self.position = (102, 90)
        self.active = False
        self.__frames = 0
        self.__sprite_index = 0
        self.__sprites = [Wind.SPRITE1, Wind.SPRITE2, Wind.SPRITE3]

    def update(self):
        if self.active:
            self.__frames += 1
            if self.__frames >= 10:
                self.__sprite_index = (self.__sprite_index + 1) % len(self.__sprites)

    def render(self, display):
        if self.active:
            display.blit(self.__sprites[self.__sprite_index], self.position)


class Slab:
    def __init__(self, rect):
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(Color.YELLOW_GREEN)
        self.position = (self.rect.x, self.rect.y)

    def render(self, display):
        display.blit(self.image, self.position)


class Grass:

    ALIVE_1 = apply_image_transform(pygame.rect.Rect(48, 50, 21, 4))
    ALIVE_2 = apply_image_transform(pygame.rect.Rect(76, 50, 21, 4))
    ALIVE_3 = apply_image_transform(pygame.rect.Rect(104, 50, 21, 4))

    DEAD_1 = apply_image_transform(pygame.rect.Rect(48, 58, 21, 4))
    DEAD_2 = apply_image_transform(pygame.rect.Rect(76, 58, 21, 4))
    DEAD_3 = apply_image_transform(pygame.rect.Rect(103, 58, 21, 4))

    def __init__(self, position, alive):
        self.__sprites = [
            [Grass.ALIVE_1, Grass.ALIVE_2, Grass.ALIVE_3, Grass.ALIVE_2],
            [Grass.DEAD_1, Grass.DEAD_2, Grass.DEAD_3, Grass.DEAD_2]
            ]
        self.rect = pygame.Rect(position[0], position[1], 42, 8)
        self.__sprite_index = 0
        self.__living_index = 0
        self.__frames = 0
        self.position = position
        self.is_alive = alive
        self.is_windy = False

    @property
    def is_alive(self):
        return self.__living_index == 0

    @is_alive.setter
    def is_alive(self, alive):
        if alive:
            self.__living_index = 0
        else:
            self.__living_index = 1

    def update(self):
        self.__frames += 1
        frame_threshold = 12
        if self.is_windy:
            frame_threshold = 3
        if self.__frames >= frame_threshold:
            self.__sprite_index = (self.__sprite_index + 1) % len(self.__sprites[self.__living_index])
            self.__frames = 0

    def render(self, display):
        display.blit(self.__sprites[self.__living_index][self.__sprite_index], self.position)


class Goat:

    def generate_left_image_group(right_image_group):
        left_image_group = []
        for i in right_image_group:
            left_image_group.append(pygame.transform.flip(i, True, False))
        return left_image_group

    GRUNT_SOUND = pygame.mixer.Sound(get_asset_file('goatgrunt.ogg'))
    STANDING_NORMAL = apply_image_transform(pygame.rect.Rect(26, 31, 16, 12))
    STANDING_CROUCHED = apply_image_transform(pygame.rect.Rect(8, 32, 16, 11))

    WALKING_TOGETHER = apply_image_transform(pygame.rect.Rect(44, 32, 14, 11))
    WALKING_SEPARATE = apply_image_transform(pygame.rect.Rect(78, 31, 15, 12))

    # FIX THESE
    JUMPING_START = apply_image_transform(pygame.rect.Rect(103, 30, 13, 14))
    JUMPING_MID = apply_image_transform(pygame.rect.Rect(120, 27, 15, 11))
    JUMPING_END = apply_image_transform(pygame.rect.Rect(138, 32, 15, 11))

    FLOWER_STANDING = apply_image_transform(pygame.rect.Rect(26, 14, 16, 12))
    FLOWER_CROUCHED = apply_image_transform(pygame.rect.Rect(8, 15, 16, 11))

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
            Goat.GROUP_FLOWER
            ]
        self.__is_happy = False
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
            elif self.is_happy:
                self.__group_index = 3
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
            self.__frames = 0
        self.__is_grounded = grounded

    @property
    def is_happy(self):
        return self.__is_happy

    @is_happy.setter
    def is_happy(self, happy):
        self.__is_happy = happy
        if happy:
            self.__group_index = 3
            self.__sprite_index = 0
            self.update_indices()

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
        frame_threshold = 12
        if self.is_grounded and not self.is_moving_horizontally:
            frame_threshold = 24

        if self.is_grounded:
            if self.__frames >= frame_threshold:
                self.__sprite_index = (self.__sprite_index + 1) % len(self.__direction())
                self.update_draw_position()
                self.__frames = 0
        else:
            if self.velocity[1] < -0.9:
                self.__sprite_index = 0
            elif -0.9 <= self.velocity[1] <= 0.9:
                self.__sprite_index = 1
            else:
                self.__sprite_index = 2

    def render(self, display):
        # display.blit(self.__debug_surface, (self.rect.x, self.rect.y))
        display.blit(self.__sprite, (self.rect.x, self.rect.y))


def is_entity_on_ground(entity, slabs):
    entity_rect = entity.rect.copy()
    entity_rect.bottom += 1
    for slab in slabs:
        if entity_rect.colliderect(slab.rect):
            if slab.rect.top <= entity_rect.bottom <= slab.rect.top + 3:
                return True
    return False


def check_collision_x(goat, entities):
    for slab in entities:
        # if there is a collision
        if goat.rect.colliderect(slab.rect):

            # player collides with a platform on their right
            if slab.rect.left < goat.rect.right < slab.rect.right:
                goat.rect.right = slab.rect.left

            # player collides with a platform on their left
            elif slab.rect.left < goat.rect.left < slab.rect.right:
                goat.rect.left = slab.rect.right

            goat.velocity[0] = 0


def check_collision_y(goat, entities):
    for slab in entities:
        if goat.rect.colliderect(slab.rect):
            # player collides with a platform on their head
            if slab.rect.top < goat.rect.top < slab.rect.bottom:
                goat.rect.top = slab.rect.bottom

            # player collides standing on a platform
            elif slab.rect.top < goat.rect.bottom < slab.rect.bottom:
                goat.rect.bottom = slab.rect.top

            goat.velocity[1] = 0


def handle_fallthrough_collision_x(goat, entities):
    pass  # nothing to do here


def handle_fallthrough_collision_y(goat, entities):
    for slab in entities:
        if goat.rect.colliderect(slab.rect) and goat.velocity[1] > 0:
            # player collides standing on a platform
            if slab.rect.top < goat.rect.bottom < slab.rect.top + 1:
                goat.rect.bottom = slab.rect.top
                goat.velocity[1] = 0


def run_game():
    pygame.display.set_caption('Grass is Always Greener')
    pygame.display.set_icon(Goat.STANDING_NORMAL)

    # initialize the mixer for sound to work
    # pygame.mixer.music.load(get_asset_file('background_music.ogg'))
    # pygame.mixer.music.play(-1)

    # clock for keeping track of time, ticks, and frames per second
    clock = pygame.time.Clock()
    hunger = HungerBubble()
    happy = HappyBubble()
    goat = Goat([64, 143])
    bridge = Bridge()
    eating = EatingParticles()
    wind = Wind()
    flower = Flower()
    boulder = Boulder()
    grass_left = Grass((66, 135), alive = False)
    grass_right = Grass((232, 135), alive = True)
    disable_controls = False
    ending_timer = 0
    fallthrough_slabs = [
        Slab(pygame.Rect(209, 195, 21, 3)),
        Slab(pygame.Rect(292, 151, 15, 3)),
        Slab(pygame.Rect(208, 142, 109, 3)),
        Slab(pygame.Rect(192, 212, 16, 3)),
        Slab(pygame.Rect(209, 195, 21, 3)),
        Slab(pygame.Rect(244, 160, 15, 3))
        ]
    slabs = [
        Slab(pygame.Rect(0, 0, 12, 190)),
        Slab(pygame.Rect(5, 101, 59, 4)),
        Slab(pygame.Rect(64, 27, 3, 74)),
        Slab(pygame.Rect(0, 88, 67, 15)),
        Slab(pygame.Rect(0, 143, 124, 97)),
        Slab(pygame.Rect(121, 143, 3, 97)),
        Slab(pygame.Rect(120, 231, 166, 16)),
        Slab(pygame.Rect(262, 166, 44, 80)),
        Slab(pygame.Rect(306, 143, 14, 27)),
        Slab(pygame.Rect(310, 25, 20, 200)),
        Slab(pygame.Rect(232, 181, 54, 53)),
        Slab(pygame.Rect(250, 172, 21, 12))
    ]
    # fallthrough_slabs = [Slab(pygame.Rect(140, 170, 50, 10))]
    # ground = Slab(pygame.Rect(0, 210, 320, 10))
    # slabs = [ground, Slab(pygame.Rect(0, 175, 20, 10))]
    pygame.mixer.music.load(get_asset_file('background.ogg'))
    pygame.mixer.music.play(-1)
    event_index = 0
    done = False
    while not done:
        clock.tick(60)
        display.fill(Color.LIGHT_SKY_BLUE)
        display.blit(WORLD, (0, 0))

        if disable_controls:
            ending_timer += 1
            if ending_timer >= 460:
                done = True

        goat_on_bridge = not bridge.is_broken and is_entity_on_ground(goat, [bridge])

        goat.is_grounded = is_entity_on_ground(goat, slabs) or is_entity_on_ground(goat, fallthrough_slabs) or goat_on_bridge
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
                    # print('a pressed')
                if event.key == pygame.K_d:
                    goat.turn_right()
                    # print('d pressed')
                if event.key == pygame.K_e:
                    if goat.rect.colliderect(grass_right.rect):
                        if event_index == 0:
                            grass_right.is_alive = False
                            grass_left.is_alive = True
                            goat.GRUNT_SOUND.play(0)
                            wind.SOUND.play(0)
                            wind.active = True
                            grass_left.is_windy = True
                            grass_right.is_windy = True
                            event_index += 1
                        if event_index == 2:
                            flower.display = False
                            happy.display = True
                            goat.is_happy = True
                            eating.active = True
                            disable_controls = True
                            eating.SOUND.play(0)
                            event_index += 1
                    if goat.rect.colliderect(grass_left.rect):
                        if event_index == 1:
                            goat.GRUNT_SOUND.play(0)
                            grass_right.is_alive = True
                            grass_left.is_alive = False
                            wind.SOUND.stop()
                            wind.active = False
                            grass_left.is_windy = False
                            grass_right.is_windy = False
                            boulder.active = True
                            flower.display = True
                            flower.SOUND.play(0)
                            event_index += 1

                    # print('e pressed')
                if event.key == pygame.K_SPACE and goat.is_grounded:
                    goat.is_grounded = False
                    if wind.active:
                        goat.velocity[1] = -1
                    else:
                        goat.velocity[1] = -2
                    # print('space pressed')

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    if goat.is_moving_horizontally:
                        goat.turn_right()
                    # print('a released')
                if event.key == pygame.K_d:
                    if goat.is_moving_horizontally:
                        goat.turn_left()
                    # print('d released')
                if event.key == pygame.K_e:
                    pass
                    # print('e released')
                if event.key == pygame.K_SPACE:
                    pass
                    # print('space released')

        wind_friction = 0
        if wind.active:
            wind_friction = 1
            # goat is moving right
        if goat.is_moving_horizontally and goat.direction == 0:
            goat.velocity[0] = 2 - wind_friction
        elif goat.is_moving_horizontally and goat.direction == 1:
            goat.velocity[0] = -2 + wind_friction
        elif not goat.is_moving_horizontally:
            goat.velocity[0] = 0

        if goat.is_grounded:
            goat.velocity[1] = 0
        else:
            goat.velocity[1] += 0.15

        if boulder.active:
            boulder.rect.y += boulder.velocity[1]
            if boulder.rect.colliderect(bridge.rect):
                bridge.is_broken = True

            if boulder.rect.y > 240:
                boulder.active = False

        # update
        goat.rect.x += goat.velocity[0]
        check_collision_x(goat, slabs)
        if not bridge.is_broken:
            check_collision_x(goat, [bridge])
        handle_fallthrough_collision_x(goat, fallthrough_slabs)

        goat.rect.y += goat.velocity[1]
        check_collision_y(goat, slabs)
        if not bridge.is_broken:
            check_collision_y(goat, [bridge])
        handle_fallthrough_collision_y(goat, fallthrough_slabs)

        goat.position[0] = goat.rect.x
        goat.position[1] = goat.rect.bottom
        # end disable controls

        hunger.update()
        wind.update()
        goat.update()
        grass_left.update()
        grass_right.update()
        bridge.update()
        eating.update()

        # for slab in slabs:
        #     slab.render(display)

        # for slab in fallthrough_slabs:
        #     slab.render(display)

        goat.render(display)
        grass_left.render(display)
        grass_right.render(display)
        flower.render(display)
        bridge.render(display)
        wind.render(display)
        boulder.render(display)
        if happy.display:
            display.blit(HappyBubble.SPRITE, (goat.rect.right + 5, goat.rect.top - (goat.rect.height + 10)))
        if hunger.display:
            display.blit(hunger.SPRITE, (goat.rect.right + 5, goat.rect.top - (goat.rect.height + 10)))
        if eating.active:
            if goat.direction == 0:
                display.blit(eating.current_image, (goat.rect.right - 10, goat.rect.top + 5))
            else:
                display.blit(eating.current_image, (goat.rect.left - 10, goat.rect.top + 5))
        pygame.display.flip()


if __name__ == '__main__':
    run_game()
