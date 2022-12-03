import pygame
import random


class background_conveyer():
    def __init__(self, input_speed, max_gifts):
        self.crate_image = pygame.image.load(
            "sprites/gift.png").convert_alpha()  # convert with alpha for more perforemance
        self.speed = input_speed

        # written by Brian, everything below in this function
        # sort from lowest to highest
        # remove duplicates
        self.box = [[random.randrange(-100 * max_gifts, 100, 150), 100] for _ in
                    range(random.randrange(2, max_gifts))]  # generate
        self.box = list(dict.fromkeys([tuple(coord) for coord in sorted(self.box, key=lambda k: [
            k[0]])]))  # lambda is an anonymous function, convert to tuple to remove duplicates
        # [k[0]] is the the first element of the first element (x-coord) of the list
        # depending of the x-coord sort the list
        self.box = [list(coord) for coord in self.box]  # convert each tuple element back into a list

    def reset(self):
        # written by brian
        try:
            last_box_x, last_box_y = self.box[0]
        except:
            last_box_x, last_box_y = [-100, 100]
        if last_box_x > 100:  # add 100 to 0 so that there isn't any clipping
            new_loc = [random.randrange(-100, 0), 100]  # which is the start
        else:
            new_loc = [random.randrange(-300, -150, 50) + last_box_x,
                       100]  # reset 1 singular box, y always stays the same
        return new_loc

    def draw_box(self, input_coord):
        x, y = input_coord
        self.surf.blit((self.crate_image), (x, y))

    def draw_conveyor(self):
        self.surf = pygame.Surface((1200, 300), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.surf, (150, 150, 150), ((0, 200), (1200, 100)))

        for index, coord in enumerate(self.box):
            x, y = coord
            self.draw_box((x, y))

            if x > 1200:
                # written by brian
                # moves the box from the end to the start with random position
                self.box.pop(-1)  # remove the box if it is past the end, aslo known as the last one
                self.box.insert(0,
                                self.reset())  # add another box to the start, insert at index 0 or the starting point
            else:
                self.box[index] = [x + self.speed, y]
        return self.surf


if __name__ == "__main__":
    screen = pygame.display.set_mode((1920, 1080), vsync=True)
    convayor1 = background_conveyer(1, 20)  # called the class and __init__ runs once
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit((convayor1.draw_conveyor()), (0, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
