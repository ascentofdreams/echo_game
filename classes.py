class Lines:
    def __init__(self, len_line=70):
        self.lines = []
        self.number_orientations = 16
        self.len_line = len_line

    def spawn_line(self, x_end, y_end, color=(255, 255, 255)):
        if len(self.lines) <= 40:
            for index_orientation in range(13, self.number_orientations, 2):
                count_reflections  = 0
                covered_distance = 0
                self.lines.append(
                    [color, (x_end, y_end, x_end, y_end), index_orientation, covered_distance, count_reflections])

    def render(self):
        lst_lines = self.lines[:]
        distance_max = 750
        for i in range(len(lst_lines)):
            color, x_y, index_orientation, covered_distance, count_reflections = self.lines[i]
            x_end, y_end, x_new, y_new = x_y
            if covered_distance <= distance_max:
                pygame.draw.line(screen, color, (x_end, y_end), (x_new, y_new), 2)
        self.lines = list(filter(lambda l: l[3] <= distance_max, self.lines))
        dist = 8
        for t in walls_group:
            self.lines = list(filter(lambda l: not (t.rect.x + dist <= l[1][2] <= t.rect.x + t.rect.w - dist) or not (
                    t.rect.y + dist <= l[1][3] <= t.rect.y + t.rect.h - dist), self.lines))

    def move(self, pos):
        angle_coefficient, coefficient_visible_line = 2, 8
        if self.lines:
            for i in range(len(self.lines)):
                lst_walls = list(map(lambda t: (t[0], t[1], t[1].image, t[1].rect), enumerate(walls_group)))
                color, x_y, index_orientation, covered_distance, count_reflections = self.lines[i]
                x_end, y_end, x_new, y_new = x_y
                orientation_movement = {0: ['-', '-', pos // 2, pos, 2, 1],
                                        1: ['-', '+', pos // 2, pos, 3, 0],
                                        2: ['+', '-', pos // 2, pos, 0, 3],
                                        3: ['+', '+', pos // 2, pos, 1, 2],

                                        4: ['-', '-', pos, pos // 2, 6, 5],
                                        5: ['-', '+', pos, pos // 2, 7, 4],
                                        6: ['+', '-', pos, pos // 2, 4, 7],
                                        7: ['+', '+', pos, pos // 2, 5, 6],

                                        8: ['-', '-', pos, pos, 10, 9],
                                        9: ['-', '+', pos, pos, 11, 8],
                                        10: ['+', '-', pos, pos, 8, 11],
                                        11: ['+', '+', pos, pos, 9, 10],

                                        12: ['-', '-', pos // 1.3, pos, 14, 13],
                                        13: ['-', '+', pos // 1.3, pos, 15, 12],
                                        14: ['+', '-', pos // 1.3, pos, 12, 15],
                                        15: ['+', '+', pos // 1.3, pos, 13, 14]}
                collide_x, collide_y = check_reflections(lst_walls, index_orientation, x_new, y_new)
                if collide_x or collide_y:
                    count_reflections += 1
                    if count_reflections == 1:
                        if collide_x:
                            Walls.reflection_echo(collide_x[0][1], collide_x, collide_y,
                                                  index_orientation)
                        elif collide_y:
                            Walls.reflection_echo(collide_y[0][1], collide_x, collide_y,
                                                  index_orientation)
                movement = orientation_movement[index_orientation]
                if not (collide_x or collide_y):
                    if sqrt(abs(x_end - x_new) ** 2 + abs(y_end - y_new) ** 2) >= self.len_line:
                        x_end = eval(f'{x_end} {movement[0]} {movement[2]}')
                        y_end = eval(f'{y_end} {movement[1]} {movement[3]}')
                    x_new = eval(f'{x_new} {movement[0]} {movement[2]}')
                    y_new = eval(f'{y_new} {movement[1]} {movement[3]}')
                elif collide_x:
                    if sqrt(abs(x_end - x_new) ** 2 + abs(
                            y_end - y_new) ** 2) >= self.len_line // coefficient_visible_line:
                        x_end = eval(f'{x_end} {movement[0]} {movement[2]}')
                        y_end = eval(f'{y_end} {movement[1]} {movement[3]}')
                    else:
                        index_orientation = movement[4]
                        movement = orientation_movement[index_orientation]
                        x_end, y_end = x_new, y_new
                        if sqrt(abs(x_end - x_new) ** 2 + abs(y_end - y_new) ** 2) >= self.len_line:
                            x_end = eval(f'{x_end} {movement[0]} {movement[2]}')
                            y_end = eval(f'{y_end} {movement[1]} {movement[3]}')
                        x_new = eval(f'{x_new} {movement[0]} {movement[2]}')
                        y_new = eval(f'{y_new} {movement[1]} {movement[3]}')
                elif collide_y:
                    if sqrt(abs(x_end - x_new) ** 2 + abs(
                            y_end - y_new) ** 2) >= self.len_line // coefficient_visible_line:
                        x_end = eval(f'{x_end} {movement[0]} {movement[2]}')
                        y_end = eval(f'{y_end} {movement[1]} {movement[3]}')
                    else:
                        index_orientation = movement[5]
                        movement = orientation_movement[index_orientation]
                        x_end, y_end = x_new, y_new
                        if sqrt(abs(x_end - x_new) ** 2 + abs(y_end - y_new) ** 2) >= self.len_line:
                            x_end = eval(f'{x_end} {movement[0]} {movement[2]}')
                            y_end = eval(f'{y_end} {movement[1]} {movement[3]}')
                        x_new = eval(f'{x_new} {movement[0]} {movement[2]}')
                        y_new = eval(f'{y_new} {movement[1]} {movement[3]}')

                covered_distance += pos
                r, g, b = color
                coefficient_brightness = 3
                if r > pos / coefficient_brightness and g > pos / coefficient_brightness \
                        and b > pos / coefficient_brightness:
                    color = r - pos / coefficient_brightness, g - pos / coefficient_brightness, \
                            b - pos / coefficient_brightness
                self.lines[i] = [color, (x_end, y_end, x_new, y_new), index_orientation, covered_distance,
                                 count_reflections]
