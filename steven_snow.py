import pygame
import random


class gen_snow():
    def __init__(self):
        self.snow_cords = []
        for y in range(5):
            for x in range(9):
                self.snow_cords.append([(random.randrange(20, 80) + (x * 200)), random.randrange(10, 90) + (y * 200)])
        for y in range(5):
            for x in range(9):
                self.snow_cords.append(
                    [random.randrange(75, 175, 10) + (x * 200), random.randrange(75, 175, 10) + (y * 200)])

    def draw_snow(self):
        surf = pygame.Surface((1920, 1080), pygame.SRCALPHA, 32)
        for i, coord in enumerate(self.snow_cords):  # Enumerate for update each item of list
            x, y = coord
            pygame.draw.circle(surf, (255, 255, 255), (x, y), 2)
            y += 0.1 * random.randrange(5, 20)
            if y >= 1080:
                self.snow_cords[i] = [x + random.randrange(-50, 50), random.randrange(-50, 50)]
            else:
                self.snow_cords[i] = [x, y]  # Update
        return surf


if __name__ == "__main__":
    screen = pygame.display.set_mode((1920, 1080), vsync=True)
    snow = gen_snow()

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(snow.draw_snow(), (0, 0))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
