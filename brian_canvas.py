import pygame
import numpy as np

class get_canvas_coord():
    def __init__(self, canvas_size, pixel_size, starting_coord=None):
        self.coord_list = []
        if starting_coord == None:
            starting_pos = [0, 0]
        else:
            starting_pos = starting_coord.copy()

        for i in range(canvas_size):
            temp_list = []
            y = i * pixel_size + starting_pos[1]
            for o in range(canvas_size):
                x = o * pixel_size + starting_pos[0]
                temp_list.append([x, y, x + pixel_size, y + pixel_size])
            self.coord_list.append(temp_list)

    def __repr__(self):
        #for testing
        return str(self.coord_list)  # print the range for each canvas pixel coords that the cursor can hover over

    def find_coord(self, position):  # pixel coord to canvas coord
        # starts from (0,0) to (canvas_size - 1, canvas_size - 1)
        cursor_x, cursor_y = position
        for y in self.coord_list:
            for x in y:
                start_x, start_y, end_x, end_y = x
                if start_y <= cursor_y <= end_y and start_x <= cursor_x <= end_x:
                    x_move = y.index(x)
                    y_move = self.coord_list.index(y)
                    return x_move, y_move


class canvas_pixels():
    def __init__(self, input_canvas_size, input_pixel_size):
        self.canvas_size = input_canvas_size
        self.pixel_size = input_pixel_size
        self.canvas = [[[255, 255, 255] for _ in range(self.canvas_size)] for __ in range(self.canvas_size)]

        self.is_transpose = False

    def __repr__(self):
        string = ''
        for y in range(self.canvas_size):
            for x in range(self.canvas_size):
                string += str(self.canvas.copy()[y][x])
            string += '\n'
        return string

    def get_canvas_array(self):
        return np.array(self.canvas.copy(), np.int16)

    def flip(self, side):  # left = 1, right = 2
        np_canvas = self.get_canvas_array()
        if side == 1:
            self.canvas = np.rot90(np_canvas, k=1).tolist()
        elif side == 2:
            self.canvas = np.rot90(np_canvas, k=-1).tolist()

    def transpose(self):  # transpose
        #make sure that it is hard to use, so that there will be no mistake
        #BEST FEATURE I HAVE EVER CREATED
        self.canvas = np.transpose(self.get_canvas_array()).reshape(13, 13, 3).tolist() #BIG T = transpose, make sure to reshape in order to keep the array the same shape

    def put_color(self, coord, color):
        x, y = list(coord).copy()
        r, g, b = list(color).copy()

        self.canvas[y][x] = [r, g, b]

    def fill_color(self, color):
        self.canvas = [[color.copy() for _ in range(self.canvas_size)] for __ in range(self.canvas_size)]

    def fill_saturate(self, saturation):  # -1 for darken, 1 for lighten
        for y, y_color in enumerate(self.canvas):
            for x, x_color in enumerate(y_color):
                r, g, b = x_color
                if saturation == -1:  # ineffiecient, kinda ugly
                    if r >= 10:
                        r -= 10
                    if g >= 10:
                        g -= 10
                    if b >= 10:
                        b -= 10
                elif saturation == 1:
                    if r <= 245:
                        r += 10
                    if g <= 245:
                        g += 10
                    if b <= 245:
                        b += 10
                # else:
                #     break #hopefull save computation, if no change then do nothing
                self.canvas[y][x] = [r, g, b]

    def saturate(self, saturation, coord):
        x, y = list(coord).copy()
        color = self.canvas[y][x]
        r, g, b = color
        if saturation == -1:  # ineffiecient, kinda ugly
            if r >= 10:
                r -= 10
            if g >= 10:
                g -= 10
            if b >= 10:
                b -= 10
        elif saturation == 1:
            if r <= 245:
                r += 10
            if g <= 245:
                g += 10
            if b <= 245:
                b += 10
        self.canvas[y][x] = [r, g, b]

    def reset(self):
        self.canvas = [[[255, 255, 255] for _ in range(self.canvas_size)] for __ in range(self.canvas_size)]

    def draw_pixels(self):
        surf = pygame.Surface((self.canvas_size * self.pixel_size, self.canvas_size * self.pixel_size))
        for y, y_pixels in enumerate(self.canvas.copy()):
            for x, x_pixels in enumerate(y_pixels):
                r, g, b = x_pixels
                pygame.draw.rect(surf, (r, g, b),
                                 ((x * self.pixel_size, y * self.pixel_size), (self.pixel_size, self.pixel_size)))
        return surf


if __name__ == "__main__":
    pygame.init()

    import os
    from glob import glob
    import numpy as np

    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    RED = [255, 0, 0]
    GRAY = [120, 120, 120]


    # for drawing my itself only, not for importing, because I have to create a new surface
    class canvas():
        def __init__(self, input_starting_coord, input_pixel_size):
            self.starting_coord = input_starting_coord.copy()
            self.canvas_size = 13
            self.pixel_size = input_pixel_size
            self.canvas_frame = pygame.image.load("sprites/christmas_pattern.jpg")

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
                                    [0, 0, 255], [0, 255, 0], [34, 139, 34], [0, 255, 255], [255, 0, 255],
                                    [255, 183, 197],
                                    [255, 255, 255]]

            self.canvas_colors_2 = [[0, 0, 0], [80, 80, 80], [150, 75, 0], [255, 255, 255], [255, 255, 255],
                                    [255, 255, 255],
                                    [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
                                    [255, 255, 255]]  # White are empty colors in case customization is added

        def reset_canvas(self):
            self.pixels.reset()

        def draw_canvas(self, pygame_event, input_starting_coord, input_pixel_size, is_palette, is_draw):
            self.is_palette = is_palette
            self.pixel_size = input_pixel_size
            self.starting_coord = input_starting_coord
            self.pygame_event = pygame_event.copy()

            for event in self.pygame_event:
                self.coord = self.get_canvas_coord.find_coord(
                    pygame.mouse.get_pos())  # cursor coord -> canvas coord, make sure to copy it
                keys = pygame.key.get_pressed()
                if self.coord != None and is_draw:
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

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.is_click = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.is_click = False

                    if self.is_click and self.saturate == 0 and pygame.mouse.get_pressed()[
                        0]:  # painting selected color by holding or clicking left click
                        self.pixels.put_color(self.coord, self.color)
                    elif self.is_click and self.saturate != 0 and pygame.mouse.get_pressed()[
                        0] and not keys[pygame.K_LSHIFT]:  # if we are lightning/darkening
                        if self.saturate == 1:  # if darkening
                            self.pixels.saturate(1, self.coord)
                        else:
                            self.pixels.saturate(-1, self.coord)

                    elif self.is_click and pygame.mouse.get_pressed()[2]:  # eraser by holding right-clicking
                        self.pixels.put_color(self.coord, [255, 255, 255])

                    if event.type == pygame.KEYDOWN:
                        # saturation,s for more lighting, d for darker pixel, if any 0 <= color channel <= 255 then can't be changed
                        if keys[pygame.K_s]:
                            self.saturate = 1
                        elif keys[pygame.K_d]:
                            self.saturate = -1

                        if keys[pygame.K_1]:
                            self.color = self.canvas_colors_1[2]
                            self.saturate = 0
                            print("Red")
                        elif keys[pygame.K_2]:
                            self.color = self.canvas_colors_1[3]
                            self.saturate = 0
                            print("Orange")
                        elif keys[pygame.K_3]:
                            self.color = self.canvas_colors_1[4]
                            self.saturate = 0
                            print("Yellow")
                        elif keys[pygame.K_4]:
                            self.color = self.canvas_colors_1[5]
                            self.saturate = 0
                            print("Green")
                        elif keys[pygame.K_5]:
                            self.color = self.canvas_colors_1[6]
                            self.saturate = 0
                            print("Dark Green")
                        elif keys[pygame.K_6]:
                            self.color = self.canvas_colors_1[7]
                            self.saturate = 0
                            print("Blue")
                        elif keys[pygame.K_7]:
                            self.color = self.canvas_colors_1[8]
                            self.saturate = 0
                            print("Cyan")
                        elif keys[pygame.K_8]:
                            self.color = self.canvas_colors_1[9]
                            self.saturate = 0
                            print("Purple")
                        elif keys[pygame.K_9]:
                            self.color = self.canvas_colors_1[10]
                            self.saturate = 0
                            print("Pink")
                        elif keys[pygame.K_BACKSPACE]:
                            self.color = self.canvas_colors_1[1]
                            self.saturate = 0
                            print("White")
                        elif keys[pygame.K_q]:
                            self.color = self.canvas_colors_2[0]
                            self.saturate = 0
                            print("Black")
                        elif keys[pygame.K_w]:
                            self.color = self.canvas_colors_2[1]
                            self.saturate = 0
                            print("Gray")
                        elif keys[pygame.K_e]:
                            self.color = self.canvas_colors_2[2]
                            self.saturate = 0
                            print("Brown")
                        # flip and transpose
                        elif keys[pygame.K_LEFT]:
                            self.pixels.flip(2)
                        elif keys[pygame.K_RIGHT]:
                            self.pixels.flip(1)
                if keys[pygame.K_t] and keys[pygame.K_LCTRL]:
                    # BEST FEATURE I HAVE ADDED
                    self.pixels.transpose()

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


    # for drawing dataset to train the CNN

    starting_coord = [500, 400]
    canvas_size = 13  # size in a square, for each side if 2 then it would dictate a 2 by 2 square = 4 draw_pixels
    pixel_size = 40

    # screen_size = [canvas_size * pixel_size, canvas_size * pixel_size]
    screen_size = [1920, 1080]
    screen = pygame.display.set_mode(screen_size, vsync=True)

    # getting the canvas coord from the mouse/pixel coord
    # used to change colors
    screen_canvas = canvas(starting_coord, pixel_size)
    # canvas_coord = get_canvas_coord(canvas_size, pixel_size)

    running = True
    # starting color
    color = [0, 0, 0]  # color starts as back, can be changed to white but what ever, or any other color
    # change this to 0 for the start, or the number + 1 where you left off

    is_click = False
    while running:
        pygame_event = pygame.event.get()
        screen_canvas.draw_canvas(pygame_event, starting_coord, 25, 1, True)
        keys = pygame.key.get_pressed()
        for event in pygame_event:
            if event.type == pygame.KEYDOWN and keys[pygame.K_RETURN]:
                output_path = "CNN/Dataset/Required"
                data_name = len(glob(f"{output_path}/*.npz"))
                image = np.array(screen_canvas.pixels.canvas.copy(), np.int16)

                # make sure the human doesn't give an absured evalution
                valid = False
                while not valid:
                    value = float(input("Eval?"))
                    if 0 <= value <= 10:
                        valid = True
                        value = [value / 10]
                        output_eval = np.array(value.copy(), np.float16)
                    else:
                        print("Try again")
                print(f"Saving {data_name}.npz")
                np.savez_compressed(f"{output_path}/REQUIRED{data_name}.npz", inputs=image, outputs=output_eval)
                screen_canvas.pixels.reset()

        pygame.display.flip()

        for event in pygame_event:
            if event.type == pygame.QUIT:
                running = False
