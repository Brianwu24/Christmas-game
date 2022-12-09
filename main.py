# ALL WRITTEN BY BRIAN WU
# 2022-12-02
# finished -

# main canvas imports
import random
import pygame
import numpy as np
from pygame import *
from glob import glob

from derek_menu import menu
from brian_canvas import canvas_pixels, get_canvas_coord
from steven_conveyor import background_conveyer
from steven_snow import gen_snow
from andrew_background import create_background
# image processing, evaluation, and comparison
# Convolutional Neural Network import
# import numpy as np

from CNN import AI_Judges
from image_compare import compare_images, check_image_copy

# for text color and or frame
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]


# IMPORTANT
# ALWAYS USE ALT + F4 to CLOSE THE PYGAME WINDOWN
# or else tensorflow will bug out
# IMPORTANT

class canvas():
    def __init__(self, input_starting_coord, input_pixel_size):
        self.starting_coord = input_starting_coord.copy()
        self.canvas_size = 13
        self.pixel_size = input_pixel_size

        # load images
        self.canvas_frame = pygame.image.load("sprites/christmas_pattern.jpg").convert()

        self.is_click = False
        self.saturate = 0  # -1 for darken, 0 for no change, 1 is for lighten

        self.pixels = canvas_pixels(self.canvas_size, self.pixel_size)
        self.font = pygame.font.Font('freesansbold.ttf', 55)
        self.key_list_num = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.key_list = ["q", "w", "e"]
        self.special_key_list = ["s", "d"]

        self.get_canvas_coord = get_canvas_coord(self.canvas_size, self.pixel_size,
                                                 self.starting_coord)  # init the range/domain of coords that are in the canvas

        self.color = [255, 0, 0]  # changed to change the color of the brush, black is the starting color
        # black,white,red,orange,yellow,green,blue,cyan,purple,pink,grey,brown
        self.canvas_colors_1 = [[0, 0, 0], [255, 255, 255], [255, 0, 0], [200, 140, 0], [255, 255, 0],
                                [0, 0, 255], [0, 255, 0], [34, 139, 34], [0, 255, 255], [255, 0, 255], [255, 183, 197],
                                [255, 255, 255]]

        self.canvas_colors_2 = [[0, 0, 0], [80, 80, 80], [150, 75, 0], [255, 255, 255], [255, 255, 255],
                                [255, 255, 255],
                                [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
                                [255, 255, 255]]  # White are empty colors in case customization is added

        self.redo_cache = np.array([])

    def reset_redo_cache(self):
        self.redo_cache = np.array([])

    def reset_canvas(self):
        self.pixels.reset()

    def draw_canvas(self, pygame_event, input_starting_coord, input_pixel_size, is_palette, is_draw):
        global undo_cache
        global redo_cache

        self.is_palette = is_palette
        self.pixel_size = input_pixel_size
        self.starting_coord = input_starting_coord
        self.pygame_event = pygame_event.copy()

        for event in self.pygame_event:
            self.coord = self.get_canvas_coord.find_coord(
                pygame.mouse.get_pos())  # cursor coord -> canvas coord, make sure to copy it
            keys = pygame.key.get_pressed()
            if self.coord is not None and is_draw:
                if event.type == pygame.MOUSEBUTTONDOWN and keys[
                    pygame.K_LSHIFT]:  # fill the entire canvas with color by pressing shift mouse click
                    if pygame.mouse.get_pressed()[0] and self.saturate != 0:  # if we are desaturating/saturating
                        if self.saturate == -1:
                            self.pixels.fill_saturate(-1)
                        else:
                            self.pixels.fill_saturate(1)
                    elif pygame.mouse.get_pressed()[0]:
                        self.pixels.fill_color(self.color)
                    elif pygame.mouse.get_pressed()[2]:
                        self.pixels.fill_color([255, 255, 255])  # reset canvas by setting all pixels to white
                        self.pixels.fill_color([255, 255, 255])  # reset canvas by setting all pixels to white

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.is_click = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.is_click = False
                if self.is_click and self.saturate == 0 and pygame.mouse.get_pressed()[
                    0]:  # painting selected color by holding or clicking left click
                    self.pixels.put_color(self.coord, self.color)
                elif self.is_click and self.saturate != 0 and pygame.mouse.get_pressed()[
                    0] and not keys[pygame.K_LSHIFT]:  # if we are lighetning/darkening
                    if self.saturate == 1:  # if darkening
                        self.pixels.saturate(1, self.coord)
                    else:
                        self.pixels.saturate(-1, self.coord)

                elif self.is_click and pygame.mouse.get_pressed()[2]:  # eraser by holding right-clicking
                    self.pixels.put_color(self.coord, [255, 255, 255])

                if event.type == pygame.KEYDOWN:
                    # saturation,s for more lighting, d for darker pixel, if any 0 <= color channel <= 255 then can't
                    # be changed
                    if keys[pygame.K_s]:
                        self.saturate = 1
                    elif keys[pygame.K_d]:
                        self.saturate = -1

                    if keys[pygame.K_1]:
                        self.color = self.canvas_colors_1[2]
                        self.saturate = 0
                        # print("Red")
                    elif keys[pygame.K_2]:
                        self.color = self.canvas_colors_1[3]
                        self.saturate = 0
                        # print("Orange")
                    elif keys[pygame.K_3]:
                        self.color = self.canvas_colors_1[4]
                        self.saturate = 0
                        # print("Yellow")
                    elif keys[pygame.K_4]:
                        self.color = self.canvas_colors_1[5]
                        self.saturate = 0
                        # print("Green")
                    elif keys[pygame.K_5]:
                        self.color = self.canvas_colors_1[6]
                        self.saturate = 0
                        # print("Dark Green")
                    elif keys[pygame.K_6]:
                        self.color = self.canvas_colors_1[7]
                        self.saturate = 0
                        # print("Blue")
                    elif keys[pygame.K_7]:
                        self.color = self.canvas_colors_1[8]
                        self.saturate = 0
                        # print("Cyan")
                    elif keys[pygame.K_8]:
                        self.color = self.canvas_colors_1[9]
                        self.saturate = 0
                        # print("Purple")
                    elif keys[pygame.K_9]:
                        self.color = self.canvas_colors_1[10]
                        self.saturate = 0
                        # print("Pink")
                    elif keys[pygame.K_BACKSPACE]:
                        self.color = self.canvas_colors_1[1]
                        self.saturate = 0
                        # print("White")
                    elif keys[pygame.K_q]:
                        self.color = self.canvas_colors_2[0]
                        self.saturate = 0
                        # print("Black")
                    elif keys[pygame.K_w]:
                        self.color = self.canvas_colors_2[1]
                        self.saturate = 0
                        # print("Gray")
                    elif keys[pygame.K_e]:
                        self.color = self.canvas_colors_2[2]
                        self.saturate = 0
                        # print("Brown")
                    # flip and transpose
                    elif keys[pygame.K_LEFT]:
                        self.pixels.flip(2)
                    elif keys[pygame.K_RIGHT]:
                        self.pixels.flip(1)
                    elif (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and keys[pygame.K_t]:
                        # BEST FEATURE I HAVE ADDED
                        self.pixels.transpose()

        keys = pygame.key.get_pressed()
        if is_draw:
            if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and (
                    keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and keys[pygame.K_z]:
                if len(redo_cache) != 0:
                    cache = redo_cache.pop(-1)
                    undo_cache.append(cache)
                    self.pixels.canvas = cache.tolist()
            elif (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and keys[pygame.K_z] and self.pixels.canvas != [[[255, 255, 255] for _ in range(self.canvas_size)] for __ in range(self.canvas_size)]:
                cache = undo_cache.pop(-1)
                redo_cache.append(cache)
                if len(undo_cache) != 0:
                    self.pixels.canvas = undo_cache[-1].tolist()


        starting_x, starting_y = self.starting_coord
        screen.blit(self.canvas_frame, (starting_x - 25, starting_y - 25))
        screen.blit(self.pixels.draw_pixels(), self.starting_coord)  # draw the canvas

        # separate color switch from palette show because of a bug, where palette doesn't show
        if is_palette == 1:
            x, y = starting_coord
            render_palette_text = self.font.render("Palette", True, BLACK)
            screen.blit(render_palette_text, (x + 120, y - 210))

            for index, text in enumerate(self.key_list_num):  # for the top row
                render_text = self.font.render(text, True, WHITE, self.canvas_colors_1[index + 2])
                screen.blit(render_text, (x + (index * 50), y - 150))

            for index, text in enumerate(self.key_list):
                render_text = self.font.render(text, True, WHITE, self.canvas_colors_2[index])
                screen.blit(render_text, (x + (index * 50), y - 90))
            render_lighten = self.font.render(self.special_key_list[0], True, [0, 0, 0], [255, 255, 255])
            screen.blit(render_lighten, (x + 200, y - 90))
            render_darken = self.font.render(self.special_key_list[1], True, [255, 255, 255], [0, 0, 0])
            screen.blit(render_darken, (x + 250, y - 90))
        # pygame.display.update()  # don't update can cause artifacts sometimes(if in for loop, must be outside of
        # for loop)


# load the judges
CNN_judges = AI_Judges()
map_judges = {  # level: judge
    1: "Chadwick",
    2: "Gallo",
    3: "Mazewafer",
    4: "Chadward"
}
# IMPORTANT
# ALWAYS USE ALT + F4 to CLOSE
# IMPORTANT

pygame.init()  # has to be before class as setting self.font requires it
# always the same can be reused for every level

# load music, may or not be copy righted, not for commercial use
pygame.mixer.init()

music_file_list = glob("music/*.mp3")


def load_music():
    choice = random.choice(music_file_list)
    pygame.mixer.music.load(choice)
    mixer.music.set_volume(.5)


def unload_music():
    pygame.mixer.music.unload()


load_music()
pygame.mixer.music.play()

screen = pygame.display.set_mode((1920, 1080), flags=pygame.DOUBLEBUF | pygame.HWSURFACE, vsync=True)
pygame.display.set_caption('Christmas Chadward')

canvas_size = 13
pixel_size = 40
starting_coord = [300, 355]

pygame.mouse.set_visible(False)  # turn cursor into invisible
cursor = pygame.image.load("sprites/cursor.png").convert_alpha()

screen_menu = menu()

# load images, and define functions to control

# load the hearts image and create function
hearts = pygame.image.load("sprites/heart.png").convert_alpha()


def draw_health(coord, hp):
    x, y = coord
    for i in range(hp):
        screen.blit(hearts, (x + i * 90, y))


# load the green checks and create function
check = pygame.image.load("sprites/greencheck.png").convert_alpha()


def draw_points(coord, points):
    x, y = coord
    for i in range(points):
        screen.blit(check, (x + i * 55, y))


positive_dialogue = []
positive_files = glob("sprites/dialogue/positive/*.png")
for positive_file in positive_files:
    positive_dialogue.append(pygame.image.load(positive_file).convert_alpha())
del positive_files  # save memory

negative_dialogue = []
negative_files = glob("sprites/dialogue/negative/*.png")
for negative_file in negative_files:
    negative_dialogue.append(pygame.image.load(negative_file).convert_alpha())
del negative_files  # save memory


def move_canvas():  # animation always stays the same speed
    global starting_coord
    x, y = starting_coord.copy()  # make sure to copy, y always stays the same
    starting_coord = [x + 3, y]


screen_background = create_background()
background = screen_background.draw_background()

# if reusing the screen canvas make sure to reset it using screen_canvas.reset()
screen_canvas = canvas(starting_coord, pixel_size)

# creating the conveyors
conveyors = [background_conveyer(1, 5) for _ in range(3)]


def update_conveyors(level):  # level starts at 1 but is updated from 1 to 2 thus starting at 2
    if level == 2:
        conveyors = [background_conveyer(3, 10) for _ in range(3)]
    elif level == 3:
        conveyors = [background_conveyer(5, 15) for _ in range(3)]
    elif level == 4:
        conveyors = [background_conveyer(10, 30) for _ in range(3)]
    else:
        conveyors = [background_conveyer(3, 10) for _ in range(3)]
    return conveyors


# load all images
gift_chair = pygame.image.load("sprites/gift_chair.png").convert_alpha()

# creating and loading all the images for the characters
character_list = glob("sprites/characters/*.png")
characters = []
for i, character in enumerate(character_list):
    characters.append(pygame.image.load(character).convert_alpha())  # append the characters into a dict


def draw_character(level, input_coord):
    screen.blit((characters[level - 1]), input_coord)


snow = gen_snow()

undo_steps = 0  # skips the amount of undo updates
undo_cache = []  # empty list
# undo_cache.append(screen_canvas.pixels.get_canvas_array())

redo_cache = []

# keep track of game states, and other variables
game_state = [1, True]  # 0 < level <= 4, is draw menu
game = [5, 0]  # health/points
# lose when health reaches 0
# win if points reach 5
game_images = []  # use this to check for duplicates

is_show_palette = 1  # 0 is False 1 is True 2 is unable to change state from False unless resetting the canvas
is_move_canvas = False
is_draw = True

has_pressed_enter = 0  # False, 1 True 2 = pressed 2 times

has_eval = False  # 0 = False, 1 = True, if the NN has evaluated the image
is_pass = [None, False]  # pass or fail, has checked for similarity
is_dialogue, has_chosen_dialogue = False, False

running = True
while running:
    change = check_image_copy(screen_canvas.pixels.get_canvas_array(), undo_cache)
    if change:
        undo_cache.append(screen_canvas.pixels.get_canvas_array())
        if not screen_canvas.pixels.get_canvas_array().all():
            redo_cache = []

    if not pygame.mixer.music.get_busy():
        unload_music()
        load_music()
        pygame.mixer.music.play()

    pygame_event = pygame.event.get()

    if game_state[1]:
        menu_surf, chosen_level = screen_menu.draw_menu(pygame_event)
        if chosen_level is not None:
            game_state = [chosen_level, False]  # chosen a level, thus no longer in menu

        conveyors = update_conveyors(game_state[0])
        screen.blit(menu_surf, (0, 0))
        screen.blit(snow.draw_snow(), (0, 0))
        # draw and get returned value and set is menu false
    else:
        # draw background
        screen.blit(background, (0, 0))
        screen.blit(gift_chair, (1200, 322))

        # draw mid ground
        for i, conveyor in enumerate(conveyors):  # drawing conveyors
            screen.blit(conveyor.draw_conveyor(), (0, 300 + (i * 200)))
        # screen.blit(conveyors[0].draw_conveyor(), (0, 300))

        # draw foreground
        screen_canvas.draw_canvas(pygame_event, starting_coord, 25, is_show_palette, is_draw)
        draw_character(game_state[0], (1200, 400))

        # after drawing then do logic
        keys = pygame.key.get_pressed()
        starting_x, starting_y = starting_coord.copy()
        for event in pygame_event:
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_RETURN] and not is_move_canvas:
                    has_pressed_enter = 1
                if keys[pygame.K_RETURN] and starting_x >= 700:
                    has_pressed_enter = 2

                if has_pressed_enter == 1 and is_show_palette != 2:
                    is_show_palette = 2  # stop showing palette
                    is_move_canvas = True  # now able to move the canvas
                    is_draw = False
                    # run tensorflow here
                elif has_pressed_enter == 2 and is_show_palette == 2:
                    has_pressed_enter = 0
                    # check if we should reset the menu
                    if game[1] >= 5:
                        game = [5, 0]  # reset the health and points
                        game_state[1] = True
                        screen_menu.update_level()  # update the level
                    elif game[0] == 0:
                        game = [5, 0]  # reset the health and points
                        game_state[1] = True

                    # reset everything, absolutly everything
                    is_show_palette = 1
                    is_draw = True
                    starting_coord = [300, 355]
                    screen_canvas.reset_canvas()
                    has_chosen_dialogue = False
                    is_dialogue = False
                    is_pass = [None, False]  # reset to no pass/fail, and has not checked for similarity

                    # update conveyor speed

                    # update the evaluation state
                    has_eval = False

                if keys[pygame.K_SPACE] and is_show_palette != 2:
                    if is_show_palette == 1:
                        is_show_palette = 0
                    else:
                        is_show_palette = 1
        starting_x, starting_y = starting_coord.copy()  # update it incase starting_coord was reset to [300, 355]
        if (starting_x < 700) and is_move_canvas:  # if it has not reached the end then continue moving it
            move_canvas()
        elif starting_x >= 700:
            is_move_canvas = False
            is_dialogue = True

        if (starting_x >= 700) and not is_move_canvas and not has_eval:
            is_similar = compare_images(screen_canvas.pixels.canvas, game_images)

            # added after the video simple idea if all the pixels are the same color then don't add it to the list of
            # picures because it can disrupt the originality check
            if not np.allclose(screen_canvas.pixels.get_canvas_array(),
                               screen_canvas.pixels.get_canvas_array()[0][0]) and (
                    screen_canvas.pixels.canvas.copy() not in game_images.copy()):
                game_images.append(screen_canvas.pixels.canvas.copy())
            # is_pass = [None, False] # is the image as pass or fail, has checked for similarity
            if is_similar and not is_pass[1]:  # if they are similar subtract health
                print("IMAGE TOO SIMILAR")
                is_pass = [False, True]
            elif not has_eval and not is_similar:  # else if they are not similar evaluate them with the CNN
                eval = CNN_judges.judge(map_judges[game_state[0]], screen_canvas.pixels.canvas)
                # round, remove negative numbers
                # abs is good enough as the negatives are very close to 0
                print(f"The computer rates the image as: {eval}")
                if eval < 0.75:  # if fail you lose 1 health, 0.75 is the passing grade
                    is_pass[0] = False
                elif 0.75 < eval <= 1:  # CNN will never go past 1.1 but in case it does that means the human tricked
                    # the AI
                    game[1] += 1
                    is_pass[0] = True
                elif eval > 1.1:  # good luck even trying, the AI isn't trained to give higher than 1 eval
                    game[1] += 1  # add a point

                    if game[0] < 5:  # capped at 5 health
                        game[0] += 1  # extra life
                    is_pass[0] = True
            has_eval = True

            if not is_pass[0]:
                game[0] -= 1

        if is_dialogue:
            # draw dialogue
            if is_pass[0]:
                if not has_chosen_dialogue:
                    positive_text = random.choice(positive_dialogue)
                    has_chosen_dialogue = True
                screen.blit(positive_text, (1050, 300))
            elif not is_pass[0]:
                if not has_chosen_dialogue:
                    negative_text = random.choice(negative_dialogue)
                    has_chosen_dialogue = True
                screen.blit(negative_text, (1050, 300))

        draw_health((730, 100), game[0])
        draw_points((1350, 110), game[1])
        screen.blit(snow.draw_snow(), (0, 0))

    cursor_x, cursor_y = pygame.mouse.get_pos()
    screen.blit(cursor, (cursor_x - 20, cursor_y - 20))

    pygame.display.flip()
    for event in pygame_event:
        if event.type == pygame.QUIT:
            running = False

# IMPORTANT
# ALWAYS USE ALT + F4 to CLOSE
# IMPORTANT
