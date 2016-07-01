import pygame
from pygame.locals import *
import random

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    ## Init, asioiden valmistelu ja tiedostojen lataus
    clock = pygame.time.Clock()
    width = 1920
    height = 1080
    image_size = 150
    screen = pygame.display.set_mode((width, height))

    time = 0;
    speed = [2,5, 2,5]
    ball = pygame.transform.scale(pygame.image.load("pinkviini.png"), (image_size, image_size))
    ballrect = ball.get_rect()

    box = pygame.image.load("laatikkko.png")
    boxlist = []
    boxmaara = 12
    for i in range(0,boxmaara):
        boxrect = box.get_rect()
        for _ in range(10): # lets try ten times, and then give up
            boxrect.center = (random.randint(image_size,width-image_size),random.randint(image_size,height-image_size))
            collides = False
            for other_box in boxlist:
                if boxrect.colliderect(other_box):
                    collides = True
                    break
            if not collides:
                break
        boxlist.append(boxrect)

    #bling = pygame.mixer.Sound("peruna.wav")
    font = pygame.font.Font(None, 50)
    text = font.render("The PenguinBoxGame. The goal is to put the penguin inside any of the boxes. Press t if you get stuck.", 1, (255, 255, 255))
    teksti = font.render("If you somehow manage to put the penguin in a box, restart and repeat.", 1, (255, 255, 255))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    tekstipos = teksti.get_rect()
    tekstipos.centerx = screen.get_rect().centerx
    tekstipos.centery = 100

    running = True
    # Mainloop, ohjelman varsinainen logiikka
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ballrect.center = event.pos
                #bling.play()


        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            ballrect = ballrect.move([20,0])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ballrect = ballrect.move([-20,0])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            ballrect = ballrect.move([0,-20])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            ballrect = ballrect.move([0,20])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_t]:
            ballrect.center = (random.randint(50,1900),random.randint(50,1050))

        if ballrect.left < 0:
            ballrect.left = 0
        if ballrect.right > width:
            ballrect.right = width
        if ballrect.bottom > height:
            ballrect.bottom = height
        if ballrect.top < 0:
            ballrect.top = 0

        for boxrect in boxlist:
            if boxrect.left < ballrect.right and boxrect.left > ballrect.left:
                if boxrect.top < ballrect.bottom and boxrect.top > ballrect.top:
                    ballrect.top = boxrect.bottom
                    ballrect.left = boxrect.right
                if boxrect.bottom > ballrect.top and boxrect.bottom < ballrect.bottom:
                    ballrect.bottom = boxrect.top
                    ballrect.left = boxrect.right
            if boxrect.right > ballrect.left and boxrect.right < ballrect.right:
                if boxrect.top < ballrect.bottom and boxrect.top > ballrect.top:
                    ballrect.top = boxrect.bottom
                    ballrect.right = boxrect.left
                if boxrect.bottom > ballrect.top and boxrect.bottom < ballrect.bottom:
                    ballrect.bottom = boxrect.top
                    ballrect.right = boxrect.left


        screen.fill((0, 0, (time/10) % 256))
        screen.blit(ball, ballrect)
        screen.blit(text, textpos)
        screen.blit(teksti, tekstipos)
        for boxrect in boxlist:
            screen.blit(box, boxrect)
        pygame.display.flip()

        time += clock.tick(60) # rajoitetaan mainloop 60 kierrokseen sekunnissa
