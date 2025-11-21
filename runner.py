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

pygame.init()

WIDTH = 1200
HEIGHT = 800
SUDOKU_DIMENSION = 650

BOX_SIZE = SUDOKU_DIMENSION / 9
BTN_FONT_COLOR = (59, 89, 169)
SUDOKU_X_POSITION = 100
SUDOKU_Y_POSITION = 100
LINE_WIDTH = 2
BACKGROUND_LINE_COLOR = (235, 237, 242)
BACKGROUND_LINE_COLOR_STRONG = (102, 114, 132)
FONT_SIZE = SUDOKU_DIMENSION // 16
result = None
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
running = True


def draw_button(rect, font):
    pygame.draw.rect(screen, button_color, rect)
    screen.blit(font, (rect.x + 15, rect.y + 5))


# fuente
font = pygame.font.SysFont("Comic Sans MS", FONT_SIZE)
little_font = pygame.font.SysFont("Comic Sans MS", int(FONT_SIZE // 1.5))


background = pygame.Rect(0, 0, 1200, 800)
# buttons
button_color = (235, 238, 243)
easy_color = (235, 238, 243)
normal_color = (235, 238, 243)
hard_color = (235, 238, 243)
colors = [easy_color, normal_color, hard_color]

generate_button = pygame.Rect(875, 165, 250, 80)
generate = font.render("NEW", True, BTN_FONT_COLOR)

AI_button = pygame.Rect(875, 265, 250, 80)
ai = font.render("AI", True, BTN_FONT_COLOR)

erase_button = pygame.Rect(875, 635, 250, 70)
erase = font.render("Eraser", True, BTN_FONT_COLOR)

rect_mistake = pygame.Rect(
    SUDOKU_Y_POSITION + SUDOKU_DIMENSION - 210,
    SUDOKU_X_POSITION - BOX_SIZE / 2,
    BOX_SIZE * 1.666,
    BOX_SIZE / 2,
)

# numbers


buttons = []
for i in range(3):
    for j in range(3):
        rect_temp = pygame.Rect(875 + 90 * j, 365 + 90 * i, 70, 70)
        value_temp = font.render(str(j + 1 + i * 3), True, BTN_FONT_COLOR)
        buttons.append((rect_temp, value_temp, j + 1 + i * 3))


# difficulty
rect_easy = pygame.Rect(
    SUDOKU_Y_POSITION,
    SUDOKU_X_POSITION - BOX_SIZE / 2,
    BOX_SIZE * 1.666,
    BOX_SIZE / 2,
)
easy_text = little_font.render("Easy", True, BTN_FONT_COLOR)

rect_normal = pygame.Rect(
    SUDOKU_Y_POSITION + (BOX_SIZE * 1.666),
    SUDOKU_X_POSITION - BOX_SIZE / 2,
    BOX_SIZE * 1.666,
    BOX_SIZE / 2,
)
normal_text = little_font.render("Normal", True, BTN_FONT_COLOR)
timer_color = (97, 122, 187)
rect_hard = pygame.Rect(
    SUDOKU_Y_POSITION + (BOX_SIZE * 1.666 * 2),
    SUDOKU_X_POSITION - BOX_SIZE / 2,
    BOX_SIZE * 1.666,
    BOX_SIZE / 2,
)
hard_text = little_font.render("Hard", True, BTN_FONT_COLOR)
# errors
errors = 0
mistakes = font.render(f"mistakes {errors} / 3", True, (255, 255, 255))

selected = None
EMPTY = None

states = [get_playable_sudoku(0)]
_, solved, _ = solve_sudoku(states[0])
# clock
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
timer = pygame.Rect(875, 65, 250, 80)

(194, 221, 248)
# selected color
selected_overlay = None
overlay = pygame.Surface((BOX_SIZE, BOX_SIZE), pygame.SRCALPHA)
overlay_relatives = pygame.Surface((BOX_SIZE, BOX_SIZE), pygame.SRCALPHA)
overlay.fill((85, 159, 235, 50))  # R, G, B, A  → A = transparencia (0-255)
overlay_relatives.fill((59, 111, 164, 50))  # R, G, B, A  → A = transparencia (0-255)
# current
current_overlay = None
level = 1
minutes = 0
playing = True
relatives = None
while running:
    # event detector
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (
                SUDOKU_Y_POSITION < mouse_x < SUDOKU_DIMENSION + SUDOKU_Y_POSITION
                and SUDOKU_X_POSITION < mouse_y < SUDOKU_DIMENSION + SUDOKU_X_POSITION
                and errors < 3
            ):
                x = int((mouse_x - SUDOKU_Y_POSITION) // BOX_SIZE)
                y = int((mouse_y - SUDOKU_X_POSITION) // BOX_SIZE)
                if selected:
                    if selected == "#":
                        states[0][y][x] = None
                    else:
                        states[0][y][x] = selected
                    if states[0][y][x] != solved[y][x]:
                        errors += 1

                selected_overlay = list(get_range((y, x)))
                current_overlay = (y, x)
                relatives = None
                if states[0][y][x]:
                    relatives = get_same_number((y, x), states[0])

            elif generate_button.collidepoint(event.pos):
                # factorizar
                playing = True
                relatives = None
                minutes, errors = 0, 0
                _, record = _get_playable_sudoku(level)
                if record:
                    states = record
                _, solved, _ = solve_sudoku(states[-1])
                start_time = pygame.time.get_ticks()
                selected_overlay = list()
            elif AI_button.collidepoint(event.pos):

                selected_overlay = list()
                _, solution, record = solve_sudoku(states[0])

                if record:
                    states = record

            elif rect_easy.collidepoint(event.pos):
                # factorizar
                playing = True
                relatives = None
                minutes, errors, level = 0, 0, 0
                states = [get_playable_sudoku(level)]
                _, solved, _ = solve_sudoku(states[0])
                start_time = pygame.time.get_ticks()
                selected_overlay = list()
            elif rect_normal.collidepoint(event.pos):
                # factoriaz
                level = 1
                minutes, errors = 0, 0
                playing = True
                relatives = None
                states = [get_playable_sudoku(level)]
                _, solved, _ = solve_sudoku(states[0])
                start_time = pygame.time.get_ticks()
                selected_overlay = list()

            elif rect_hard.collidepoint(event.pos):
                # factorizar
                level = 2
                minues, errors = 0, 0
                playing = True
                relatives = None
                states = [get_playable_sudoku(level)]
                _, solved, _ = solve_sudoku(states[0])
                start_time = pygame.time.get_ticks()
                selected_overlay = list()
            elif erase_button.collidepoint(event.pos):
                selected = "#"
            else:

                changed = False
                for i in buttons:
                    rect, _, value = i
                    if rect.collidepoint(event.pos):
                        changed = True
                        selected = value
                if not changed:
                    selected = None
                    current_overlay = None
    

    # background
    pygame.draw.rect(screen, (255, 255, 255), background)
    # time
    elapsed = (pygame.time.get_ticks() - start_time) / 1000
    seconds = elapsed
    if elapsed >= 59:
        elapsed = elapsed
        minutes += 1
        start_time = pygame.time.get_ticks()
    if playing:
        if elapsed <= 9.5 and playing:
            text = f"{minutes}:0{elapsed:.0f} "
        else:
            text = f"{minutes}:{elapsed:.0f} "
        if minutes < 10:
            text = "0" + text
    else:
        text = f"{result}"

    clock_text = font.render(text, True, (255, 255, 255))
    pygame.draw.rect(screen, timer_color, timer)
    screen.blit(clock_text, (940, 75))
    for i in range(10):
        line = pygame.Rect(
            SUDOKU_Y_POSITION + i * BOX_SIZE,
            SUDOKU_X_POSITION,
            LINE_WIDTH,
            SUDOKU_DIMENSION,
        )
        pygame.draw.rect(screen, BACKGROUND_LINE_COLOR, line)
        line = pygame.Rect(
            SUDOKU_Y_POSITION,
            SUDOKU_X_POSITION + i * BOX_SIZE,
            SUDOKU_DIMENSION,
            LINE_WIDTH,
        )
        pygame.draw.rect(screen, BACKGROUND_LINE_COLOR, line)
    for i in range(4):
        line = pygame.Rect(
            SUDOKU_Y_POSITION + i * BOX_SIZE * 3,
            SUDOKU_X_POSITION,
            LINE_WIDTH,
            SUDOKU_DIMENSION,
        )
        pygame.draw.rect(screen, BACKGROUND_LINE_COLOR_STRONG, line)
        line = pygame.Rect(
            SUDOKU_Y_POSITION,
            SUDOKU_X_POSITION + i * BOX_SIZE * 3,
            SUDOKU_DIMENSION,
            LINE_WIDTH,
        )
        pygame.draw.rect(screen, BACKGROUND_LINE_COLOR_STRONG, line)

    current = states[0]
    for i in range(len(current)):
        for k in range(len(current)):
            if current[i][k] != None:
                text_surface = font.render(str(current[i][k]), True, (0, 0, 0))
                screen.blit(
                    text_surface,
                    (
                        SUDOKU_Y_POSITION
                        + k * BOX_SIZE
                        + BOX_SIZE // 2
                        - FONT_SIZE / 2,
                        SUDOKU_X_POSITION
                        + i * BOX_SIZE
                        + BOX_SIZE // 2
                        - FONT_SIZE / 2,
                    ),
                )

    pygame.draw.rect(screen, button_color, generate_button)
    screen.blit(generate, (generate_button.x + 60, generate_button.y + 5))

    pygame.draw.rect(screen, button_color, AI_button)
    screen.blit(ai, (AI_button.x + 90, AI_button.y + 5))
    if not selected == "#":
        pygame.draw.rect(screen, button_color, erase_button)
        screen.blit(erase, (erase_button.x + 60, erase_button.y + 5))
    else:
        pygame.draw.rect(screen, timer_color, erase_button)
        erase1 = font.render("Eraser", True, (255, 255, 255))
        screen.blit(erase1, (erase_button.x + 60, erase_button.y + 5))

    mistakes = little_font.render(f"Mistakes: {errors} / 3", True, (0, 0, 0))
    screen.blit(mistakes, (rect_mistake.x + (BOX_SIZE * 1.666) / 4, rect_mistake.y + 1))
    # select the current dificulty color
    for i in range(3):
        if i == level:
            colors[i] = (199, 214, 232)
        else:
            colors[i] = button_color
    # draw easy btn
    pygame.draw.rect(screen, colors[0], rect_easy)
    screen.blit(easy_text, (rect_easy.x + (BOX_SIZE * 1.666) / 4, rect_easy.y + 1))

    # draw normal btn
    pygame.draw.rect(screen, colors[1], rect_normal)
    screen.blit(
        normal_text, (rect_normal.x + (BOX_SIZE * 1.666) / 4 - 20, rect_normal.y + 1)
    )

    # draw hard btn
    pygame.draw.rect(screen, colors[2], rect_hard)
    screen.blit(hard_text, (rect_hard.x + (BOX_SIZE * 1.666) / 4, rect_hard.y + 1))
    # draw the panel with the numbers
    for i in range(1, len(buttons) + 1):
        if i == selected:
            pygame.draw.rect(screen, timer_color, buttons[i - 1][0])
            value_temp = font.render(str(i), True, (255, 255, 255))
            screen.blit(value_temp, (buttons[i - 1][0].x + 15, buttons[i - 1][0].y + 5))

        else:
            draw_button(buttons[i - 1][0], buttons[i - 1][1])
    # coloreate the selected numbers and their relatives
    if selected_overlay:
        for i in selected_overlay:
            x, y = i
            screen.blit(
                overlay,
                (y * BOX_SIZE + SUDOKU_Y_POSITION, SUDOKU_X_POSITION + x * BOX_SIZE),
            )
    if relatives:
        for i in relatives:
            x, y = i
            screen.blit(
                overlay_relatives,
                (y * BOX_SIZE + SUDOKU_Y_POSITION, SUDOKU_X_POSITION + x * BOX_SIZE),
            )
    if current_overlay:
        x, y = current_overlay
        screen.blit(
            overlay,
            (y * BOX_SIZE + SUDOKU_Y_POSITION, SUDOKU_X_POSITION + x * BOX_SIZE),
        )
    if len(states) > 1:
        
        states.pop(0)


    if errors >= 3:
        playing = False
        result = "Failed"

    if playing and is_filled(states[0]):
        playing = False
        result = "Solved"

    clock.tick(60)
    pygame.display.update()
