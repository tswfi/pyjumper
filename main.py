"""
Simple jumper game
"""
import os
import sys
import pygame
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([5,5])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = random.randrange(10, 200), random.randrange(5, 50)

        self.inair = 1
        self.dy = 5
        self.dx = 0
        self.size = self.image.get_size()

    def handle_keys(self):
        # move left and right and jump
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and not self.inair:
            self.dy = -10
        if key[pygame.K_RIGHT]:
            self.dx += 1
        elif key[pygame.K_LEFT]:
            self.dx -= 1

    def update(self, walls):
        # apply gravity
        self.rect.y += self.dy

        # apply movement
        self.rect.x += self.dx

        # adjust our gravity
        if self.dy < 5:
            self.dy += 1

        # adjust movement
        if self.dx > 0:
            self.dx -= 1
        if self.dx < 0:
            self.dx += 1

        # if we are clipping stand on the thing
        hitlist = pygame.sprite.spritecollide(self, walls, False)
        if len(hitlist):
            self.rect.y = hitlist[0].rect.y - self.size[1]
            self.inair = 0
        else:
            self.inair = 1

        # check if we died
        w, h = pygame.display.get_surface().get_size()
        if self.rect.y > h:
            print("Ded")
            pygame.quit()

class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # random size from screen
        w, h = pygame.display.get_surface().get_size()
        self.image = pygame.Surface([
                random.randrange(w/20,w/10),
                random.randrange(h/20,h/10)
        ])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

        self.rect.topleft = random.randrange(0, w), random.randrange(0, h)


def main():
    # initialize pygame
    pygame.init()

    # initialize our screen
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption('PyJumper')
    pygame.mouse.set_visible(0)

    # and clock
    clock = pygame.time.Clock()


    # background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    # render background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # hold all sprites here
    allsprites = pygame.sprite.Group()

    # create our walls
    walls = pygame.sprite.Group()
    while len(walls) < 20:
        w = Wall()
        walls.add(w)
        allsprites.add(w)

    # create our player
    player = Player()
    allsprites.add(player)

    # and go
    running = True
    while running:
        clock.tick(60)

        # handle events
        for event in pygame.event.get():
            # quit with esc or hitting close button
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # update player
        player.update(walls)

        # check keypresses for player
        player.handle_keys()

        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()

    print("Quit")
    pygame.quit()

if __name__ == '__main__':
    main()