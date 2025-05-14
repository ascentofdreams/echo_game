import pygame
import os
import sys


class Echo(pygame.sprite.Sprite):
    def __init__(self, echo_type, pos_x, pos_y):
        super().__init__(echo_group, all_sprites)
        self.image = load_image(f'echo/{echo_type}.png')
        if echo_type in {0, 4, 8, 12, 16}:
            self.rect = self.image.get_rect().move(pos_x - wall_width, pos_y - wall_height)
            self.pos = pos_x - wall_width, pos_y - wall_height
        elif echo_type in {1, 5, 9, 13, 17}:
            self.rect = self.image.get_rect().move(pos_x - wall_width, pos_y)
            self.pos = pos_x - wall_width, pos_y + wall_height
        elif echo_type in {2, 6, 10, 14, 18}:
            self.rect = self.image.get_rect().move(pos_x, pos_y - wall_height)
            self.pos = pos_x + wall_width, pos_y - wall_height
        elif echo_type in {3, 7, 11, 15, 19}:
            self.rect = self.image.get_rect().move(pos_x, pos_y)
            self.pos = pos_x + wall_width, pos_y + wall_height
        self.distance = 0
        self.echo_type = echo_type
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, time):
        pos = 100
        orientation_movement = {0: ['-', '-', pos / 50, pos / 50, 2, 1],
                                1: ['-', '+', pos / 50, pos / 50, 3, 0],
                                2: ['+', '-', pos / 50, pos / 50, 0, 3],
                                3: ['+', '+', pos / 50, pos / 50, 1, 2],

                                4: ['-', '-', pos / 50, pos / 30, 6, 5],
                                5: ['-', '+', pos / 50, pos / 30, 7, 4],
                                6: ['+', '-', pos / 50, pos / 30, 4, 7],
                                7: ['+', '+', pos / 50, pos / 30, 5, 6],

                                8: ['-', '-', pos / 30, pos / 50, 10, 9],
                                9: ['-', '+', pos / 30, pos / 50, 11, 8],
                                10: ['+', '-', pos / 30, pos / 50, 8, 11],
                                11: ['+', '+', pos / 30, pos / 50, 9, 10],

                                12: ['-', '-', pos / 100, pos / 50, 14, 13],
                                13: ['-', '+', pos / 100, pos / 50, 15, 12],
                                14: ['+', '-', pos / 100, pos / 50, 12, 15],
                                15: ['+', '+', pos / 100, pos / 50, 13, 14],

                                16: ['-', '-', pos / 50, pos / 100, 18, 17],
                                17: ['-', '+', pos / 50, pos / 100, 19, 16],
                                18: ['+', '-', pos / 50, pos / 100, 16, 19],
                                19: ['+', '+', pos / 50, pos / 100, 17, 18]}
        movement = orientation_movement[self.echo_type]
        lst_collided_wall = list(filter(lambda wall: pygame.sprite.collide_mask(self, wall), walls_group))
        lst_collided_angle = list(filter(lambda angle: pygame.sprite.collide_mask(self, angle), angles_group))
        if not (lst_collided_wall + lst_collided_angle):
            self.rect = self.rect.move(float(f'{movement[0]}{movement[2]}'),
                                       float(f'{movement[1]}{movement[3]}'))
            self.distance += time
            pos_x, pos_y = self.pos
            self.pos = pos_x + float(f'{movement[0]}{movement[2]}'), pos_y + float(f'{movement[1]}{movement[3]}')
        elif lst_collided_wall:
            pos_x, pos_y = self.pos
            if self.echo_type in {0, 4, 8, 12, 16}:
                self.pos = pos_x, pos_y + wall_height
            elif self.echo_type in {1, 5, 9, 13, 17}:
                self.pos = pos_x, pos_y - wall_height
            elif self.echo_type in {2, 6, 10, 14, 18}:
                self.pos = pos_x, pos_y + wall_height
            elif self.echo_type in {3, 7, 11, 15, 19}:
                self.pos = pos_x, pos_y - wall_height
            self.echo_type = movement[5]
            movement = orientation_movement[self.echo_type]
            self.image = load_image(f'echo/{self.echo_type}.png')
            self.rect = self.rect.move(float(f'{movement[0]}{movement[2]}'),
                                       float(f'{movement[1]}{movement[3]}'))
        # elif lst_collided_angle:
        #     pos_x, pos_y = self.pos
        #     angle = lst_collided_angle[0]
        #     if angle.rect.x <= pos_x <= angle.rect.x + angle.rect.w:
        #         self.echo_type = movement[5]
        #         movement = orientation_movement[self.echo_type]
        #         self.image = load_image(f'echo/{self.echo_type}.png')
        #         self.rect = self.rect.move(float(f'{movement[0]}{movement[2]}'),
        #                                    float(f'{movement[1]}{movement[3]}'))
        #         print(pos_x, pos_y, angle.rect, 'y')
        #     elif (angle.rect.y <= pos_y <= angle.rect.y + angle.rect.h)\
        #             and (pos_x <= angle.rect.x + angle.rect.w or pos_x >= angle.rect.x + angle.rect.w):
        #         self.echo_type = movement[4]
        #         movement = orientation_movement[self.echo_type]
        #         self.image = load_image(f'echo/{self.echo_type}.png')
        #         self.rect = self.rect.move(float(f'{movement[0]}{movement[2]}'),
        #                                    float(f'{movement[1]}{movement[3]}'))
        #         print(pos_x, pos_y, angle.rect, 'x')


class Angles(pygame.sprite.Sprite):
    def __init__(self, angle_type, pos_x, pos_y):
        super().__init__(angles_group, all_sprites)
        self.image = angle_images[angle_type]
        self.rect = self.image.get_rect().move(
            wall_width * pos_x, wall_height * pos_y)
        self.position = angle_type
        self.mask = pygame.mask.from_surface(self.image)


class Walls(pygame.sprite.Sprite):
    def __init__(self, wall_type, pos_x, pos_y):
        super().__init__(walls_group, all_sprites)
        if pos_y <= max_level_y // 2:
            self.image = wall_images[f"{wall_type}_up"]
        else:
            self.image = wall_images[f"{wall_type}_down"]
        self.rect = self.image.get_rect().move(
            wall_width * pos_x, wall_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


# def reflection_echo(self, wall_group, angle_group, echo_type):
#     global lst_collided
#     lst_reflect = []
#     if collide[0] not in {0, 12, 13, 17, 18, 22, 23, 27, 28, 32, 33, 45}:
#         lst_reflect = list(filter(lambda t: collide[0] - 1 <= t[0] <= collide[0] + 1, enumerate(walls_group)))
#     elif collide[0] in {0, 13, 18, 23, 28, 33}:
#         lst_reflect = list(filter(lambda t: collide[0] <= t[0] <= collide[0] + 1, enumerate(walls_group)))
#     elif collide[0] in {12, 17, 22, 27, 32, 45}:
#         lst_reflect = list(filter(lambda t: collide[0] - 1 <= t[0] <= collide[0], enumerate(walls_group)))
#     if collide[0] in {17, 18, 27, 28}:
#         angles = {17: 'angle_left_up', 18: 'angle_right_up', 27: 'angle_left_down', 28: 'angle_right_down'}
#         self.image = load_image(f"angles/{angles[collide[0]]}.png")
#         lst_collided.append(collide[1])
#     else:
#         if index in {0, 2, 4, 6, 8, 10, 12, 14}:
#             if collide_y:
#                 for wall_reflect in lst_reflect:
#                     wall_reflect[1].image = load_image("walls/reflection_down.png")
#                     lst_collided.append(wall_reflect[1])
#             elif collide_x:
#                 if index in {0, 4, 8, 12}:
#                     for wall_reflect in lst_reflect:
#                         wall_reflect[1].image = load_image("walls/reflection_right.png")
#                         lst_collided.append(wall_reflect[1])
#                 else:
#                     for wall_reflect in lst_reflect:
#                         wall_reflect[1].image = load_image("walls/reflection_left.png")
#                         lst_collided.append(wall_reflect[1])
#         elif index in {1, 3, 5, 7, 9, 11, 13, 15}:
#             if collide_y:
#                 for wall_reflect in lst_reflect:
#                     wall_reflect[1].image = load_image("walls/reflection_up.png")
#                     lst_collided.append(wall_reflect[1])
#             elif collide_x:
#                 if index in {1, 5, 9, 13}:
#                     for wall_reflect in lst_reflect:
#                         wall_reflect[1].image = load_image("walls/reflection_right.png")
#                         lst_collided.append(wall_reflect[1])
#                 else:
#                     for wall_reflect in lst_reflect:
#                         wall_reflect[1].image = load_image("walls/reflection_left.png")
#                         lst_collided.append(wall_reflect[1])


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, orientation_player):
        super().__init__(player_group, all_sprites)
        self.image = player_images[orientation_player]
        self.pos = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            wall_width * pos_x + wall_width // 2 - self.image.get_rect().w // 2,
            wall_height * pos_y + wall_height // 2 - self.image.get_rect().h // 2)
        self.index = 1
        self.player_move = False

    def move(self, orientation_move):
        pos_x, pos_y = self.pos
        if stand:
            Footprints(pos_x, pos_y, orientation)
        else:
            Footprints(pos_x, pos_y, orientation, self.index)
        if orientation_move == 'up':
            if orientation != 'down':
                if pos_y > 0 and level_map[pos_y - 1][pos_x] == '.':
                    self.pos = pos_x, pos_y - 1
                    self.player_move = True
            else:
                self.image = player_images[orientation_move]
        if orientation_move == 'down':
            if orientation != 'up':
                if pos_y < level_y and level_map[pos_y + 1][pos_x] == '.':
                    self.pos = pos_x, pos_y + 1
                    self.player_move = True
            else:
                self.image = player_images[orientation_move]
        if orientation_move == 'left':
            if orientation != 'right':
                if pos_x > 0 and level_map[pos_y][pos_x - 1] == '.':
                    self.pos = pos_x - 1, pos_y
                    self.player_move = True
            else:
                self.image = player_images[orientation_move]
        if orientation_move == 'right':
            if orientation != 'left':
                if pos_x < level_x and level_map[pos_y][pos_x + 1] == '.':
                    self.pos = pos_x + 1, pos_y
                    self.player_move = True
            else:
                self.image = player_images[orientation_move]
        if self.player_move:
            self.image = move_images[orientation_move][self.index]
            self.index = not self.index
            self.rect = self.image.get_rect().move(
                wall_width * self.pos[0] + wall_width // 2 - self.rect.w // 2,
                wall_height * self.pos[1] + wall_height // 2 - self.rect.h // 2)
            self.player_move = False


class Footprints(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, orientation_footprint, index=None):
        super().__init__(footprints_group, all_sprites)
        if index is None:
            self.image = load_image(f'player_footprints/player_footprints_{orientation_footprint}.png')
        else:
            if index:
                self.image = load_image(f'player_footprints_move/player_footprints_{orientation_footprint}_right.png')
            else:
                self.image = load_image(f'player_footprints_move/player_footprints_{orientation_footprint}_left.png')
        self.pos = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            wall_width * pos_x + wall_width // 2 - self.image.get_rect().w // 2,
            wall_height * pos_y + wall_height // 2 - self.image.get_rect().h // 2)


def check_reflections(lst, index_orientation, x_new, y_new):
    collide_x, collide_y, collide = None, None, None
    dist = dis = 1.5
    if index_orientation in {0, 2, 4, 6, 8, 10, 12, 14}:
        collide_y = list(filter(lambda tpl: (tpl[3].x < x_new < tpl[3].x + tpl[3].w) and (
                tpl[3].y + tpl[3].h - dis < y_new < tpl[3].y + tpl[3].h + dist), lst))
        if index_orientation in {0, 4, 8, 12}:
            collide_x = list(filter(
                lambda tpl: (tpl[3].x + tpl[3].w - dis < x_new < tpl[3].x + tpl[3].w + dist) and (
                        tpl[3].y < y_new < tpl[3].y + tpl[3].h), lst))
        else:
            collide_x = list(filter(lambda tpl: (tpl[3].x - dist < x_new < tpl[3].x + dis) and (
                    tpl[3].y < y_new < tpl[3].y + tpl[3].h), lst))
    elif index_orientation in {1, 3, 5, 7, 9, 11, 13, 15}:
        collide_y = list(
            filter(lambda tpl: (tpl[3].x < x_new < tpl[3].x + tpl[3].w) and (tpl[3].y - dis < y_new < tpl[3].y + dist),
                   lst))
        if index_orientation in {1, 5, 9, 13}:
            collide_x = list(filter(
                lambda tpl: (tpl[3].x + tpl[3].w - dis < x_new < tpl[3].x + tpl[3].w + dist) and (
                        tpl[3].y < y_new < tpl[3].y + tpl[3].h), lst))
        else:
            collide_x = list(filter(lambda tpl: (tpl[3].x - dist < x_new < tpl[3].x + dis) and (
                    tpl[3].y < y_new < tpl[3].y + tpl[3].h), lst))
    return collide_x, collide_y


def load_image(name, color=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color is None:
        image.convert_alpha()
    else:
        if color == -1:
            color = image.get_at((0, 0))
        image.set_colorkey(color)
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        map_level = [line.strip() for line in mapFile]
        max_width = max(map(len, map_level))
        return list(map(lambda line: list(line.ljust(max_width, '.')), map_level))


def generate_level(level):
    new_player, x_level, y_level = None, None, None
    for j in range(len(level)):
        for i in range(len(level[j])):
            if level[j][i] == '#':
                Walls('wall', i, j)
            if level[j][i] == '/':
                Angles('left_up', i, j)
            if level[j][i] == '\\':
                Angles('right_up', i, j)
            if level[j][i] == ']':
                Angles('left_down', i, j)
            if level[j][i] == '[':
                Angles('right_down', i, j)
            if level[j][i] == '@':
                new_player = Player(i, j, 'right')
                level[j][i] = '.'
            x_level, y_level = i, j
    return new_player, x_level, y_level


if __name__ == '__main__':
    pygame.init()
    size = width, height = 690, 330
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('echolocation')
    max_level_x, max_level_y = 22, 10

    clock = pygame.time.Clock()

    echo_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    angles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    footprints_group = pygame.sprite.Group()

    player_images = {'up': load_image('player_footprints/player_footprints_up.png'),
                     'down': load_image('player_footprints/player_footprints_down.png'),
                     'left': load_image('player_footprints/player_footprints_left.png'),
                     'right': load_image('player_footprints/player_footprints_right.png')}
    move_images = {'up': [load_image('player_footprints_move/player_footprints_up_right.png'),
                          load_image('player_footprints_move/player_footprints_up_left.png')],
                   'down': [load_image('player_footprints_move/player_footprints_down_right.png'),
                            load_image('player_footprints_move/player_footprints_down_left.png')],
                   'left': [load_image('player_footprints_move/player_footprints_left_right.png'),
                            load_image('player_footprints_move/player_footprints_left_left.png')],
                   'right': [load_image('player_footprints_move/player_footprints_right_right.png'),
                             load_image('player_footprints_move/player_footprints_right_left.png')]}
    angle_images = {'left_up': load_image('angles/left_up.png'),
                    'right_up': load_image('angles/right_up.png'),
                    'left_down': load_image('angles/left_down.png'),
                    'right_down': load_image('angles/right_down.png')}
    wall_images = {'wall_up': load_image('walls/wall_up.png'), 'wall_down': load_image('walls/wall_down.png')}
    wall_width, wall_height = 30, 30
    level_map = load_level('map.txt')
    player, level_x, level_y = generate_level(level_map)
    orientation = 'right'

    EVENT_TYPE_DOWNTIME = pygame.USEREVENT + 1
    EVENT_TYPE_HIDE_WALLS = pygame.USEREVENT + 2
    EVENT_TYPE_HIDE_FOOTPRINTS = pygame.USEREVENT + 3
    EVENT_TYPE_HIDE_ECHO = pygame.USEREVENT + 4
    pygame.time.set_timer(EVENT_TYPE_DOWNTIME, 1300)
    pygame.time.set_timer(EVENT_TYPE_HIDE_WALLS, 120)
    pygame.time.set_timer(EVENT_TYPE_HIDE_FOOTPRINTS, 90)
    pygame.time.set_timer(EVENT_TYPE_HIDE_ECHO, 2000)

    running, move, reflection, stand = True, False, False, True
    lst_collided, number_orientations = [], 20
    score = 0
    coord_x = 0
    coord_y = 0
    while running:
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if score == 1000:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not move:
                        coord_x, coord_y = player.pos
                        for num in range(12):
                            Echo(num, wall_width * coord_x + wall_width // 2, wall_height * coord_y + wall_height // 2)
                if event.key == pygame.K_UP:
                    Player.move(player, 'up')
                    orientation = 'up'
                    move = True
                    stand = False
                if event.key == pygame.K_DOWN:
                    Player.move(player, 'down')
                    orientation = 'down'
                    move = True
                    stand = False
                if event.key == pygame.K_LEFT:
                    Player.move(player, 'left')
                    orientation = 'left'
                    move = True
                    stand = False
                if event.key == pygame.K_RIGHT:
                    Player.move(player, 'right')
                    orientation = 'right'
                    move = True
                    stand = False
            if move:
                if event.type == EVENT_TYPE_DOWNTIME:
                    player.image = player_images[orientation]
                    move = False
                    stand = True
            if event.type == EVENT_TYPE_HIDE_WALLS:
                for wall_collided in lst_collided:
                    for x in range(wall_collided.rect.w):
                        for y in range(wall_collided.rect.h):
                            color_px = wall_collided.image.get_at((x, y))
                            bright = 1.1
                            if color_px[0] >= bright and color_px[1] >= bright and color_px[2] >= bright:
                                wall_collided.image.set_at((x, y),
                                                           (color_px[0] / bright, color_px[1] / bright,
                                                            color_px[2] / bright, color_px[3]))
            if event.type == EVENT_TYPE_HIDE_FOOTPRINTS:
                footprints = list(footprints_group)
                for footprint in footprints:
                    for x in range(footprint.rect.w):
                        for y in range(footprint.rect.h):
                            color_px = footprint.image.get_at((x, y))
                            bright = 1.1
                            if color_px[0] >= bright and color_px[1] >= bright and color_px[2] >= bright:
                                footprint.image.set_at((x, y), (color_px[0] / bright, color_px[1] / bright,
                                                                color_px[2] / bright, color_px[3]))
                if len(footprints) > 60:
                    for f in range(len(footprints) // 2):
                        footprints[f].kill()
            if event.type == EVENT_TYPE_HIDE_ECHO:
                echo = list(echo_group)
                for sprite in echo:
                    if sprite.distance >= 1800:
                        sprite.kill()
        footprints_group.draw(screen)
        walls_group.draw(screen)
        angles_group.draw(screen)
        echo_group.draw(screen)
        player_group.draw(screen)
        echo_group.update(clock.tick(100))
        pygame.display.flip()
    pygame.quit()
