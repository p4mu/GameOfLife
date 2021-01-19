#TODO in mehrere Dateien aufteilen
import pygame
import pyautogui

# TODO infint field/no border
colors = {'alive': (247, 131, 0),  # (0, 0, 0),  # (241, 183, 2),
          'dead': (0, 0, 0),
          'error': (255, 0, 0)}


class GameOfLife:
    __height = 0
    __width = 0
    field = []
    field_copy = []
    __state = 'PAUSE'
    __cells = 0
    __generations = 0
    __fps = 2

    def __init__(self, width_, height_):
        self.__height = height_
        self.__width = width_
        self.field = []
        self.field_copy = []
        self.__state = 'PAUSE'
        self.__cells = 0
        self.__generations = 0

        for x in range(width_):  # create Field
            new_line = []
            for y in range(height_):
                new_line.append(0)
            self.field.append(new_line)

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_state(self):
        return self.__state

    def set_state(self, state_):
        self.__state = state_

    def get_cells(self):
        return self.__cells

    def set_cells(self, cells_):
        self.__cells = cells_

    def inc_cells(self):  # increase cell number
        self.__cells += 1

    def get_generations(self):
        return self.__generations

    def set_generations(self, gens):
        self.__generations = gens

    def inc_generations(self):
        self.__generations += 1

    def get_fps(self):
        return self.__fps

    def set_fps(self, summand):
        self.__fps += summand

    def copy(self):  # copy field TODO shorter?
        self.field_copy = []
        for b in range(self.__width):
            new = []
            for c in range(self.__height):
                new.append(self.field[b][c])
            self.field_copy.append(new)

    def switch_cell_status(self, x, y):
        self.field[x][y] = (self.field[x][y] + 1) % 2

    def check_neighbours(self, x, y):
        if self.field_copy[x][y] == 1:
            neighbours = -1
        else:
            neighbours = 0
        for v in range(-1, 2):
            for w in range(-1, 2):
                if (0 <= (x + v) <= (self.__width - 1)) and (0 <= (y + w) <= (self.__height - 1)):
                    if self.field_copy[x + v][y + w] == 1:
                        neighbours += 1
        return neighbours

    def evolve(self):
        self.inc_generations()
        self.copy()
        for x in range(self.__width):
            for y in range(self.__height):
                neighboursnum = self.check_neighbours(x, y)
                if self.field_copy[x][y] == 1 and (3 < neighboursnum or neighboursnum < 2):
                    self.switch_cell_status(x, y)  # cell dies
                elif self.field_copy[x][y] == 0 and neighboursnum == 3:
                    self.switch_cell_status(x, y)  # cell gets born

    def clear_field(self):
        for r in range(self.__width):
            for s in range(self.__height):
                self.field[r][s] = 0

    @staticmethod
    def locate_mouse(x_coords, y_coords):  # find the cell clicked on in grid
        if left_border <= x_coords <= (left_border + rect_size * x_fields) and top_border <= y_coords <= (
                top_border + rect_size * y_fields):
            x_cell = (x_coords - left_border) // rect_size
            y_cell = (y_coords - top_border) // rect_size
            cell_coords = (x_cell, y_cell)
            return cell_coords
        else:
            return False


class Button:
    __x = 0
    __y = 0
    __size = 30
    __edge_radius = 3
    __sign = ''

    def __init__(self, x=5, y=0):
        self.__x = x
        self.__y = y

    def check_click(self, x_, y_):
        if (self.__x <= x_ <= (self.__x + self.__size)) and (self.__y + top_border) <= y_ <= (
                self.__y + top_border + self.__size):
            return True

    def on_button_click(self):
        if self.__sign == '+':
            game.set_fps(1)
        elif self.__sign == '_' and 0 < game.get_fps() - 1:
            game.set_fps(-1)
        elif self.__sign == '<-' and game.get_state() == 'PAUSE':
            game.clear_field()

    def draw_button(self, top_border_, sign, font_size=41, margin_x=3, margin_y=9):
        pygame.draw.rect(screen,
                         (247, 131, 0),
                         [self.__x, self.__y + top_border_, self.__size, self.__size],
                         0, self.__edge_radius)
        font1 = pygame.font.SysFont('Calibri', font_size, False, False)
        text_button = font1.render(sign, True, (0, 0, 0))
        screen.blit(text_button, [self.__x + margin_x, self.__y + top_border_ - margin_y])
        self.__sign = sign


pygame.init()

screen = pygame.display.set_mode((list(pyautogui.size())[0]-40, list(pyautogui.size())[1]-24))
pygame.display.set_caption("Game of Life")

done = False
clock = pygame.time.Clock()
rect_size = 15
button_size = 30
top_border = 28
bottom_border = 15
left_border = 40
right_border = 15

x_fields = (screen.get_width() - (left_border + right_border)) // rect_size
y_fields = (screen.get_height() - (top_border + bottom_border)) // rect_size

game = GameOfLife(x_fields, y_fields)
button1 = Button()
button2 = Button(5, 35)
button3 = Button(5, 70)

zoom_mode = False


def pause_play():
    if game.get_state() == 'START':
        game.set_state('PAUSE')
    else:
        game.set_state('START')
        game.set_generations(0)


# TODO maybe def zoom():

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # pause or play the evolution
                pause_play()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # left mouse button
            if event.button == 1:
                coordinates = game.locate_mouse(event.pos[0], event.pos[1])
                if coordinates is not False:
                    game.switch_cell_status(coordinates[0], coordinates[1])
                if button1.check_click(event.pos[0], event.pos[1]):
                    button1.on_button_click()
                if button2.check_click(event.pos[0], event.pos[1]):
                    button2.on_button_click()
                if button3.check_click(event.pos[0], event.pos[1]):
                    button3.on_button_click()

            # middle mousebutton
            if event.button == 2:
                zoom_mode = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                zoom_mode = False

    if zoom_mode:
        # zoom() TODO zoom mode
        pass

    if game.get_state() == 'START':
        game.evolve()

    screen.fill(color=(43, 43, 43))

    game.set_cells(0)

    for i in range(game.get_width()):
        for j in range(game.get_height()):
            if game.field[i][j] == 0:  # TODO getter function?
                cell = 'dead'
                just_border = 1
            elif game.field[i][j] == 1:  # TODO getter function?
                cell = 'alive'
                just_border = 0
                game.inc_cells()
            else:
                cell = 'error'
                just_border = 0

            pygame.draw.rect(screen,  # draw every cell
                             colors[cell],
                             [left_border + i * rect_size, top_border + j * rect_size, rect_size, rect_size],
                             just_border)

    font = pygame.font.SysFont('Calibri', 17, False, False)
    text_cells = font.render('Living cells: ' + str(game.get_cells()), True, (0, 0, 0))
    screen.blit(text_cells, [left_border, 6])

    text_generations = font.render('Generation: ' + str(game.get_generations()), True, (0, 0, 0))
    screen.blit(text_generations, [((left_border + x_fields * rect_size) - 117), 6])

    text_state = font.render(game.get_state(), True, (0, 0, 0))
    screen.blit(text_state, [((x_fields * rect_size - 54) // 2) + right_border, 6])

    button1.draw_button(top_border, '+')
    button2.draw_button(top_border, '_', 35, 4, 18)
    button3.draw_button(top_border, '<-', 27, 3, 0)

    text_fps = font.render('gens/sec: ' + str(game.get_fps()), True, (0, 0, 0))
    screen.blit(text_fps, [((left_border + x_fields * rect_size) - 250), 6])

    pygame.display.flip()
    clock.tick(game.get_fps())

pygame.quit()
