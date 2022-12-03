import pygame
import math
import random

# colours and xy positions
BACKGROUND_COLOUR = (255, 213, 128)
SKY_BLUE = (135, 206, 235)
BROWN = (94, 74, 58)
GREEN = (78, 143, 56)
CANDY_CANE_RED = (215, 0, 12)
SHADED_RED = (183, 0, 10)
WHITE = (255, 250, 250)
SHADED_WHITE = (217, 213, 213)
WREATH_GREEN = (0, 128, 128)
WINDOW_FRAME_COLOUR = (211, 211, 211)
WINDOW_FRAME_COLOUR2 = (169, 169, 169)
WINDOW_FRAME_COLOUR3 = (215, 215, 190)
WINDOW_FRAME_COLOUR4 = (50, 50, 50)
LAMP_COLOUR = (14, 9, 5)
# 805,205 - 370 wide
# 1980,1080
window_x = 150
window_y = 205
candy_cane_x = 550
candy_cane_y = 0


# randomizes the colour, coordinates and size of the ornaments
class create_background():
    def __init__(self):

        # this chooses the randomized points that are in the wreath putting it into a list and returns it to the variable points
        def get_midpoints():
            n = 100
            r = 57
            return [(math.cos(2 * math.pi / n * x) * r, math.sin(2 * math.pi / n * x) * r) for x in range(0, n + 1)]

        # recieves the random points from the function get_midpoints
        self.points = random.choices(get_midpoints().copy(), k=random.randrange(10, 20))
        # chooses random colours for the ornaments
        self.colours_list = [random.choice([CANDY_CANE_RED, WHITE]) for _ in range(10 + len(self.points))]
        # chooses random sizes for the ornaments
        self.size_list = [random.randrange(7, 10) for _ in range(10 + len(self.points))]

        self.surf = pygame.Surface((1920, 1080))

    def reset_surf(self):
        self.surf = pygame.Surface((1920, 1080))

    # drawing the wreath
    def draw_wreath(self, position):
        x, y = position
        pygame.draw.circle(self.surf, WREATH_GREEN, (x, y), 75, 37)
        pygame.draw.rect(self.surf, LAMP_COLOUR, ((x - 2, y - 275), (4, 200)))
        # draws 10 ornaments on the wreath, that takes the information from the three lists above
        for i in range(10):
            pygame.draw.circle(self.surf, self.colours_list[i], (x + self.points[i][0], y + self.points[i][1]),
                               self.size_list[i])

    # drawing the candy canes
    def draw_candy_cane(self, position1, position2):
        x, y = position1
        x2, y2 = position2

        # left candy cane
        pygame.draw.rect(self.surf, WHITE, pygame.Rect((x, y), (50, 1080)))
        pygame.draw.rect(self.surf, SHADED_WHITE, pygame.Rect((x + 35, y), (15, 1080)))
        for i in range(12):
            pygame.draw.polygon(self.surf, CANDY_CANE_RED, (
                (x + 50, y + 55 + i * 75), (x, y + 75 + i * 75), (x, y + 35 + i * 75), (x + 50, y + 15 + i * 75)))
            pygame.draw.polygon(self.surf, SHADED_RED, (
                (x + 50, y + 55 + i * 75), (x + 35, y + 61.5 + i * 75), (x + 35, y + 21.5 + i * 75),
                (x + 50, y + 15 + i * 75)))

        # right candy cane
        pygame.draw.rect(self.surf, WHITE, pygame.Rect((x2, y2), (50, 1080)))
        pygame.draw.rect(self.surf, SHADED_WHITE, pygame.Rect((x2, y2), (15, 1080)))
        for i in range(12):
            pygame.draw.polygon(self.surf, CANDY_CANE_RED, (
                (x2 + 50, y2 + 55 + i * 75), (x2, y2 + 75 + i * 75), (x2, y2 + 35 + i * 75),
                (x2 + 50, y2 + 15 + i * 75)))
            pygame.draw.polygon(self.surf, SHADED_RED, (
                (x2 + 15, y2 + 68.25 + i * 75), (x2, y2 + 74.75 + i * 75), (x2, y2 + 34.75 + i * 75),
                (x2 + 15, y2 + 28.25 + i * 75)))

    # drawing the window
    def draw_window(self, position):
        x, y = position
        # draws 3 windows
        for i in range(3):
            # window frame
            pygame.draw.rect(self.surf, WINDOW_FRAME_COLOUR, ((x, y), (312, 403)))
            pygame.draw.rect(self.surf, WINDOW_FRAME_COLOUR2, ((x + 10, y + 10), (292, 383)))
            pygame.draw.rect(self.surf, WINDOW_FRAME_COLOUR3, ((x + 20, y + 20), (272, 363)))
            pygame.draw.rect(self.surf, WINDOW_FRAME_COLOUR4, ((x + 40, y + 40), (232, 323)))

            # background of window
            for i in range(4):
                pygame.draw.rect(self.surf, SKY_BLUE, ((x + 50 + i * 54, y + 50), (50, 99)))
                pygame.draw.rect(self.surf, SKY_BLUE, ((x + 50 + i * 54, y + 153), (50, 69)))
                pygame.draw.rect(self.surf, WHITE, ((x + 50 + i * 54, y + 190), (50, 62)))
                pygame.draw.rect(self.surf, WHITE, ((x + 50 + i * 54, y + 256), (50, 99)))

            # draw clouds
            for i in range(7):
                pygame.draw.circle(self.surf, WHITE, (x + 60 + i * 5, y + 70), 5)
                pygame.draw.circle(self.surf, WHITE, (x + 65 + i * 3, y + 63), 5)
                pygame.draw.circle(self.surf, WHITE, (x + 65 + i * 4, y + 73), 3)
                pygame.draw.circle(self.surf, WHITE, (x + 114 + i * 5, y + 90), 5)
                pygame.draw.circle(self.surf, WHITE, (x + 119 + i * 3, y + 83), 5)
                pygame.draw.circle(self.surf, WHITE, (x + 119 + i * 4, y + 93), 3)
                pygame.draw.circle(self.surf, WHITE, (x + 164 + i * 5, y + 130), 5)
                pygame.draw.circle(self.surf, WHITE, (x + 170 + i * 3, y + 123), 5)
                pygame.draw.circle(self.surf, WHITE, (x + 169 + i * 4, y + 133), 3)
                pygame.draw.circle(self.surf, WHITE, (x + 224 + i * 5, y + 90), 5)
                pygame.draw.circle(self.surf, WHITE, (x + 229 + i * 3, y + 83), 5)
                pygame.draw.circle(self.surf, WHITE, (x + 229 + i * 4, y + 93), 3)

            # draw tree
            for i in range(6):
                pygame.draw.rect(self.surf, BROWN, ((x + 117 + i * 15, y + 180), (3, 10)))
                for i2 in range(3):
                    pygame.draw.polygon(self.surf, GREEN, (
                        (x + 114 + i * 15, y + 186 - i2 * 3), (x + 122 + i * 15, y + 186 - i2 * 3),
                        (x + 118 + i * 15, y + 182 - i2 * 3)))
            x += 654

    # function that draws everything
    def draw_background(self):
        self.surf.fill((BACKGROUND_COLOUR))
        self.draw_window((window_x, window_y))
        self.draw_wreath((960, 275))
        self.draw_candy_cane((candy_cane_x, candy_cane_y), (candy_cane_x + 765, candy_cane_y))
        # save resources
        return self.surf  # run once to generate everything, store as a pygame image then blit that when needed


# protects the code when being imported
if __name__ == "__main__":
    pygame.init()

    WIDTH = 1920
    HEIGHT = 1080
    size = (WIDTH, HEIGHT)

    screen = pygame.display.set_mode(size, flags=pygame.DOUBLEBUF | pygame.HWSURFACE, vsync=True)

    screen_background = create_background()
    image = screen_background.draw_background()

    running = True
    while running:
        screen.blit(image, (0, 0))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()

    pygame.quit()

