import pygame, time

from sudoku import (
    get_playable_sudoku,
    _get_playable_sudoku,
    solve_sudoku,
    get_range,
    get_same_number,
    is_filled,
    print_sudoku,
)

# initialize pygame idk
pygame.init()

# empty value for the sudoku
EMPTY = None

# screen and sudoku size
WIDTH = 1200
HEIGHT = 800
SUDOKU_DIMENSION = 650

# size of each square of the sudoku
BOX_SIZE = SUDOKU_DIMENSION / 9

# blue for the font
QUITE_BLUE = (59, 89, 169)

# gray for the backound of the buttons
GRAY_BTN = (235, 238, 243)

# button background (Blue)
BLUE_BUTTON = (97, 122, 187)
# top-left corner
SUDOKU_X_POSITION = 100
SUDOKU_Y_POSITION = 100

# line stuff
LINE_WIDTH = 2
BACKGROUND_LINE_COLOR = (235, 237, 242)
BACKGROUND_LINE_COLOR_STRONG = (102, 114, 132)

# hardcoded xddd
FONT_SIZE = SUDOKU_DIMENSION // 16

# initialice variables
running = True
playing = True
result = None
selected_number = None
colored_range = None

# error counter
error_counter = 0

# start in normal difficulty
level = 1
minutes = 0

# start without overlay
current_overlay = None
relatives = None

# create a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# set the background color
background = pygame.Rect(0, 0, WIDTH, HEIGHT)


# an auxiliar function
def draw_button(rect, font):
    pygame.draw.rect(screen, GRAY_BTN, rect)
    screen.blit(font, (rect.x + 20, rect.y + 5))


# main font
font = pygame.font.SysFont("Comic Sans MS", FONT_SIZE)

# a liittler one
little_font = pygame.font.SysFont("Comic Sans MS", int(FONT_SIZE // 1.5))


# buttons colors
easy_color = (235, 238, 243)
normal_color = (235, 238, 243)
hard_color = (235, 238, 243)
colors = [easy_color, normal_color, hard_color]


# create button
generate_button = pygame.Rect(875, 165, 250, 80)
generate = font.render("Create", True, QUITE_BLUE)

# solve botton
AI_button = pygame.Rect(875, 265, 250, 80)
ai = font.render("Solve", True, QUITE_BLUE)

# eraser
erase_button = pygame.Rect(875, 635, 250, 70)
erase = font.render("Eraser", True, QUITE_BLUE)

# mistakes counter
rect_mistake = pygame.Rect(
    SUDOKU_Y_POSITION + SUDOKU_DIMENSION - 210,
    SUDOKU_X_POSITION - BOX_SIZE / 2,
    BOX_SIZE * 1.666,
    BOX_SIZE / 2,
)
mistakes = font.render(f"mistakes {error_counter} / 3", True, (255, 255, 255))

# number panel
buttons = []
for i in range(3):
    for j in range(3):
        rect_temp = pygame.Rect(875 + 90 * j, 365 + 90 * i, 70, 70)
        value_temp = font.render(str(j + 1 + i * 3), True, QUITE_BLUE)
        buttons.append((rect_temp, value_temp, j + 1 + i * 3))

# easy button
rect_easy = pygame.Rect(
    SUDOKU_Y_POSITION,
    SUDOKU_X_POSITION - BOX_SIZE / 2,
    BOX_SIZE * 1.666,
    BOX_SIZE / 2,
)
easy_text = little_font.render("Easy", True, QUITE_BLUE)

# normal button
rect_normal = pygame.Rect(
    SUDOKU_Y_POSITION + (BOX_SIZE * 1.666),
    SUDOKU_X_POSITION - BOX_SIZE / 2,
    BOX_SIZE * 1.666,
    BOX_SIZE / 2,
)
normal_text = little_font.render("Normal", True, QUITE_BLUE)

# hard button
rect_hard = pygame.Rect(
    SUDOKU_Y_POSITION + (BOX_SIZE * 1.666 * 2),
    SUDOKU_X_POSITION - BOX_SIZE / 2,
    BOX_SIZE * 1.666,
    BOX_SIZE / 2,
)
hard_text = little_font.render("Hard", True, QUITE_BLUE)

# the states the board have (if have more than one then is an animation)
states = [get_playable_sudoku(0)]

_, solved_state, _ = solve_sudoku(states[0])

# clock stuff
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
timer = pygame.Rect(875, 65, 250, 80)

# selected square relatives
overlay = pygame.Surface((BOX_SIZE, BOX_SIZE), pygame.SRCALPHA)
overlay_relatives = pygame.Surface((BOX_SIZE, BOX_SIZE), pygame.SRCALPHA)
overlay.fill((85, 159, 235, 50))
overlay_relatives.fill((59, 111, 164, 50))

# ----------------------------------- Game Loop ------------------------------------ #
while running:
    # event detector
    for event in pygame.event.get():
        # stop the game with the red button xd
        if event.type == pygame.QUIT:
            running = False
        # whenever the mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            # position of the mouse when clicked
            mouse_x, mouse_y = event.pos
            # if the mouse was on the sudoku board and
            if (
                SUDOKU_Y_POSITION < mouse_x < SUDOKU_DIMENSION + SUDOKU_Y_POSITION
                and SUDOKU_X_POSITION < mouse_y < SUDOKU_DIMENSION + SUDOKU_X_POSITION
                and error_counter < 3
            ):
                # deteminate the square positon the mouse was on
                row = int((mouse_x - SUDOKU_Y_POSITION) // BOX_SIZE)
                column = int((mouse_y - SUDOKU_X_POSITION) // BOX_SIZE)

                # if a number was selected before from the number panel
                if selected_number:

                    # when the eraser was selected
                    if selected_number == "#":
                        states[0][column][row] = None
                    # when an actual number was selected
                    else:
                        states[0][column][row] = selected_number

                        # if the number is wrong, update the error counter
                        if states[0][column][row] != solved_state[column][row]:
                            error_counter += 1
                # get the squares that need to be overlayed
                colored_range = list(get_range((column, row)))
                current_overlay = (column, row)
                relatives = None

                # if the square has a number then get the other postions of the same number
                if states[0][column][row]:
                    relatives = get_same_number((column, row), states[0])
            # if the create button is clicked
            elif generate_button.collidepoint(event.pos):
                # since is a new game set the playing mode to True
                playing = True

                # eliminate the overlay on the squares
                relatives = None
                colored_range = list()

                # reset the minutes and error counter
                minutes, error_counter = 0, 0

                # get the record of how the new sudoku has been created
                # set the states to the record of the creation
                _, states = _get_playable_sudoku(level)

                # solve the new sudoku and store it
                _, solved_state, _ = solve_sudoku(states[-1])

                # reset the clock to the current time
                start_time = pygame.time.get_ticks()

            elif AI_button.collidepoint(event.pos):

                # eliminate the overlay on the squares
                colored_range = list()

                # get the solution and the record
                _, _, record = solve_sudoku(states[0])

                # if exist a record, then set the states to the record
                if record:
                    states = record

            elif rect_easy.collidepoint(event.pos):

                # reset this values because is a new game
                playing = True
                relatives = None
                minutes, error_counter, level = 0, 0, 0

                # set the new sudoku in the screen
                states = [get_playable_sudoku(level)]

                # get the solution and store it
                _, solved_state, _ = solve_sudoku(states[0])

                # restart the clock
                start_time = pygame.time.get_ticks()
                colored_range = list()

            elif rect_normal.collidepoint(event.pos):

                # reset this values because is a new game
                playing = True
                relatives = None
                minutes, error_counter = 0, 0

                # set the new level of the game
                level = 1

                # set the new sudoku in the screen
                states = [get_playable_sudoku(level)]

                # get the solution and store it
                _, solved_state, _ = solve_sudoku(states[0])

                # restart the clock
                start_time = pygame.time.get_ticks()
                colored_range = list()

            elif rect_hard.collidepoint(event.pos):

                # reset this values because is a new game
                minues, error_counter = 0, 0
                relatives = None
                playing = True

                # set the new level of the game
                level = 2

                # set the new sudoku in the screen
                states = [get_playable_sudoku(level)]

                # get the solution and store it
                _, solved_state, _ = solve_sudoku(states[0])
                # restart the clock
                start_time = pygame.time.get_ticks()
                colored_range = list()

            elif erase_button.collidepoint(event.pos):
                # use the '#' because idk
                selected_number = "#"

            # if the click wasn't on the buttons of before then check the
            # numbers panel
            else:

                changed = False
                # iterates over every button
                for i in buttons:
                    rect, _, value = i
                    # if the button was clicked set the selected number to the current value
                    if rect.collidepoint(event.pos):
                        changed = True
                        selected_number = value

                # if the click wasnt on the panel set the values to None
                if not changed:
                    selected_number = None
                    current_overlay = None

    # time
    seconds = (pygame.time.get_ticks() - start_time) / 1000

    # convert seconds to minutes
    if seconds >= 59:
        seconds = seconds
        minutes += 1
        start_time = pygame.time.get_ticks()

    # if a game is being solved
    if playing:

        # show always two digits numbers
        if seconds <= 9.5 and playing:
            text = f"{minutes}:0{seconds:.0f} "
        else:
            text = f"{minutes}:{seconds:.0f} "
        if minutes < 10:
            text = "0" + text

    # if a game is not being solve then set the result
    else:
        text = f"{result}"

    # select the color of the buttons difficult
    for i in range(3):
        if i == level:
            colors[i] = (199, 214, 232)
        else:
            colors[i] = GRAY_BTN
    # ---------------------------------- Draw -------------------------------

    # draw the background
    pygame.draw.rect(screen, (255, 255, 255), background)

    # draw the clock
    clock_text = font.render(text, True, (255, 255, 255))
    pygame.draw.rect(screen, BLUE_BUTTON, timer)
    screen.blit(clock_text, (940, 75))

    # draw the background lines of the board of the sudoku
    for i in range(10):

        # set vertical lines
        line = pygame.Rect(
            SUDOKU_Y_POSITION + i * BOX_SIZE,
            SUDOKU_X_POSITION,
            LINE_WIDTH,
            SUDOKU_DIMENSION,
        )
        # set horizontal lines
        pygame.draw.rect(screen, BACKGROUND_LINE_COLOR, line)
        line = pygame.Rect(
            SUDOKU_Y_POSITION,
            SUDOKU_X_POSITION + i * BOX_SIZE,
            SUDOKU_DIMENSION,
            LINE_WIDTH,
        )

        # draw the line
        pygame.draw.rect(screen, BACKGROUND_LINE_COLOR, line)

    # draw the strong lines of the board
    for i in range(4):

        # set the vertical lines
        line = pygame.Rect(
            SUDOKU_Y_POSITION + i * BOX_SIZE * 3,
            SUDOKU_X_POSITION,
            LINE_WIDTH,
            SUDOKU_DIMENSION,
        )
        # set the horizontal lines
        pygame.draw.rect(screen, BACKGROUND_LINE_COLOR_STRONG, line)
        line = pygame.Rect(
            SUDOKU_Y_POSITION,
            SUDOKU_X_POSITION + i * BOX_SIZE * 3,
            SUDOKU_DIMENSION,
            LINE_WIDTH,
        )
        # draw the lines
        pygame.draw.rect(screen, BACKGROUND_LINE_COLOR_STRONG, line)

    # use the first value of the states
    current = states[0]

    # iterate over each element on the matrix
    for row in range(len(current)):
        for column in range(len(current)):

            # if the value is a number then draw the number on the board
            if current[row][column] != None:
                text_surface = font.render(str(current[row][column]), True, (0, 0, 0))
                screen.blit(
                    text_surface,
                    (
                        SUDOKU_Y_POSITION
                        + column * BOX_SIZE
                        + BOX_SIZE // 2
                        - FONT_SIZE / 2
                        + 8,
                        SUDOKU_X_POSITION
                        + row * BOX_SIZE
                        + BOX_SIZE // 2
                        - FONT_SIZE / 2
                        - 8,
                    ),
                )

    # draw the generate button
    pygame.draw.rect(screen, GRAY_BTN, generate_button)
    screen.blit(generate, (generate_button.x + 60, generate_button.y + 5))

    # draw the solve button
    pygame.draw.rect(screen, GRAY_BTN, AI_button)
    screen.blit(ai, (AI_button.x + 70, AI_button.y + 5))

    # if the selected number is a number draw the number
    if isinstance(selected_number, int):
        pygame.draw.rect(screen, GRAY_BTN, erase_button)
        screen.blit(erase, (erase_button.x + 60, erase_button.y + 5))

    # if is the eraser then draw Eraser xddddd
    else:
        pygame.draw.rect(screen, BLUE_BUTTON, erase_button)
        erase1 = font.render("Eraser", True, (255, 255, 255))
        screen.blit(erase1, (erase_button.x + 60, erase_button.y + 5))

    # draw the counter of mistakes
    mistakes = little_font.render(f"Mistakes: {error_counter} / 3", True, (0, 0, 0))
    screen.blit(mistakes, (rect_mistake.x + (BOX_SIZE * 1.666) / 4, rect_mistake.y + 1))

    # draw the button of difficultt easy
    pygame.draw.rect(screen, colors[0], rect_easy)
    screen.blit(easy_text, (rect_easy.x + (BOX_SIZE * 1.666) / 4, rect_easy.y + 1))

    # draw the button of difficultt normal
    pygame.draw.rect(screen, colors[1], rect_normal)
    screen.blit(
        normal_text, (rect_normal.x + (BOX_SIZE * 1.666) / 4 - 20, rect_normal.y + 1)
    )

    # draw the button of difficultt hard
    pygame.draw.rect(screen, colors[2], rect_hard)
    screen.blit(hard_text, (rect_hard.x + (BOX_SIZE * 1.666) / 4, rect_hard.y + 1))

    # draw the panel with the numbers
    for i in range(1, len(buttons) + 1):

        # if the number is selected draw it with a different color
        if i == selected_number:
            pygame.draw.rect(screen, BLUE_BUTTON, buttons[i - 1][0])
            value_temp = font.render(str(i), True, (255, 255, 255))
            screen.blit(value_temp, (buttons[i - 1][0].x + 15, buttons[i - 1][0].y + 5))

        # draw the deffault color
        else:
            draw_button(buttons[i - 1][0], buttons[i - 1][1])

    # colorate the range of the selected number
    if colored_range:
        for i in colored_range:
            row, column = i
            screen.blit(
                overlay,
                (
                    column * BOX_SIZE + SUDOKU_Y_POSITION,
                    SUDOKU_X_POSITION + row * BOX_SIZE,
                ),
            )

    # colorate the same numbers as the selected one
    if relatives:
        for i in relatives:
            row, column = i
            screen.blit(
                overlay_relatives,
                (
                    column * BOX_SIZE + SUDOKU_Y_POSITION,
                    SUDOKU_X_POSITION + row * BOX_SIZE,
                ),
            )

    # colorate the square selectionated
    if current_overlay:
        row, column = current_overlay
        screen.blit(
            overlay,
            (column * BOX_SIZE + SUDOKU_Y_POSITION, SUDOKU_X_POSITION + row * BOX_SIZE),
        )

    # if the len of states is higher than one then
    # is in animation mode so we need to eliminate the current frame
    if len(states) > 1:

        states.pop(0)

    # if the user reach 3 mistakes, then the playing mode stop
    if error_counter >= 3:
        playing = False
        # the text the clock shows
        result = "Failed"

    # if is there a sudoku being solve and theres only one element on
    # states and the unique element theres on states is filled
    # then the sudoku is solved xddd
    if playing and len(states) == 1 and is_filled(states[0]):
        playing = False
        result = "Solved"

    # im not sure what this does xdddd
    clock.tick(60)

    # update the changes on the screen
    pygame.display.update()
