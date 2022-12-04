import pygame
from glob import glob


class menu():
    def __init__(self):
        self.background = pygame.image.load("sprites/menu/background.jpg").convert()
        self.Chadwick = pygame.image.load("sprites/menu/characters_scaled/1.png").convert_alpha()
        self.Gallo = pygame.image.load("sprites/menu/characters_scaled/2.png").convert_alpha()
        self.Mazewafer = pygame.image.load("sprites/menu/characters_scaled/3.png").convert_alpha()
        self.Chadward = pygame.image.load("sprites/menu/characters_scaled/4.png").convert_alpha()
        self.level_text = []

        file_list = glob("sprites/menu/buttons/*.png")
        for file in file_list:
            self.level_text.append(pygame.image.load(file).convert_alpha())

        self.starting_coord = [420, 850]
        self.level = 1  # starts at 1, do not change unless for testing, if level > 4, = free play mode

        x, y = self.starting_coord
        # list comprehension explained and created by brian
        self.button_coord = [[[x + i * 300, y], [x + 200 + i * 300, y + 100]] for i in range(4)]

    def update_level(self):
        if self.level < 1:  # cap the max level to 4, if player achieves that then it means they had full playability
            self.level += 1

    def check_button(self):
        # for event in pygame_event.copy():
        if pygame.mouse.get_pressed()[0]:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            for button, coord in enumerate(self.button_coord):
                starting_coord, ending_coord = coord
                start_x, start_y = starting_coord
                end_x, end_y = ending_coord

                if (start_x <= mouse_x <= end_x) and (start_y <= mouse_y <= end_y):
                    # print(True)
                    # print(starting_coord,ending_coord)
                    # print(button)
                    return button + 1
        return None

    def draw_menu(self, pygame_event):
        surf = pygame.Surface((1920, 1080))
        surf.blit(self.background, (0, 0))
        # draw everything u need and get input
        for start_coord, _ in self.button_coord:
            pygame.draw.rect(surf, [255, 255, 255], (start_coord, (200, 100)))

        # getting input
        chosen_level = self.check_button(pygame_event)
        if chosen_level != None and chosen_level > self.level:  # check if the chosen level is not valid
            chosen_level = None

        # make sure that self.level is smaller or equal to selected level
        x, y = self.starting_coord
        for i, current_text in enumerate(self.level_text):
            surf.blit(current_text, [x + (i * 300), y])
        # surf.blit(self.leve2_text, [x + 300, y])
        # if selected menu then:
        surf.blit(self.Chadwick, (420, 500))
        surf.blit(self.Gallo, (680, 500))
        surf.blit(self.Mazewafer, (960, 500))
        surf.blit(self.Chadward, (1330, 500))

        return surf, chosen_level


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), vsync=1)

    screen_menu = menu()

    running = 1
    while running:
        pygame_event = pygame.event.get()
        menu, chosen_level = screen_menu.draw_menu(pygame_event)
        if chosen_level != None:
            print(chosen_level)

        screen.blit(menu, (0, 0))
        pygame.display.update()

        for event in pygame_event:
            if event.type == pygame.QUIT:
                running = False
