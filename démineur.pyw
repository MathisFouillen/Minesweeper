# -*- coding: utf-8 -*-
import pygame, sys
from random import randrange
from pygame.locals import KEYDOWN,  K_BACKSPACE, K_ESCAPE, MOUSEBUTTONDOWN

#init
pygame.init()
screen = pygame.display.set_mode()

#load images and fonts
wall = pygame.image.load("images/wall.png").convert()
bomb = pygame.image.load("images/bomb.jpg").convert()
bomb.set_colorkey((255,255,255))
flag = pygame.image.load("images/flag.png").convert()
flag.set_colorkey((255,255,255))
digged = pygame.image.load("images/digged.png").convert()
font = pygame.font.Font(None, 20)
font2 = pygame.font.Font(None, 50)

#frame setup
pygame.display.set_caption("Démineur")
pygame.display.set_icon(bomb)
FPS = 30
        

def menu():
    
    screen = pygame.display.set_mode((420, 300))
    screen.fill((0,0,0))
    
    #text
    txtGame = font2.render("Démineur",True,(255,255,255))
    screen.blit(txtGame,(125,20))
    
    txt0 = font.render("Débutant",True,(255,255,255))
    screen.blit(txt0,(175,100))
    txt1 = font.render("Moyen",True,(255,255,255))
    screen.blit(txt1,(175,125))
    txt2 = font.render("Avancé",True,(255,255,255))
    screen.blit(txt2,(175,150))
    txt3 = font.render("Expert",True,(255,255,255))
    screen.blit(txt3,(175,175))
    
    #txtRules= font.render("Règles",True,(255,255,255))
    #screen.blit(txtRules,(10,275))
    txtQuit = font.render("Quitter",True,(255,255,255))
    screen.blit(txtQuit,(370,275))
    
    pygame.display.flip()
    
    #mainloop
    loop = 1
    while loop:
        for event in pygame.event.get():

            #quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #left click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                
                if 170<event.pos[0]<235 and 95<event.pos[1]<115:
                    loop = 0
                    game(0)
                    
                if 170<event.pos[0]<220 and 95+25<event.pos[1]<115+25:
                    loop = 0
                    game(1)
                    
                if 170<event.pos[0]<225 and 95+25*2<event.pos[1]<115+25*2:
                    loop = 0
                    game(2)
                
                if 170<event.pos[0]<220 and 95+25*3<event.pos[1]<115+25*3:
                    loop = 0
                    game(3)
                    
                if 10<event.pos[0]<40 and 275<event.pos[1]<390: 
                    pass
                    
                if 365<event.pos[0]<415 and 275<event.pos[1]<390:
                    sys.exit()
                    
                
def game(difficulty):

    #config
    config  = [[8,8,6],[9,9,10],[16,16,30],[30,16,97]]
    WIDTH = config[difficulty][0]
    HEIGHT = config[difficulty][1]
    MINES = config[difficulty][2]

    screen = pygame.display.set_mode((30*WIDTH+120, 30*HEIGHT))

    
    def rightSide():
        #draw right side (flag count)
        screen.blit(flag,(30*WIDTH+50,50))
        txt_flags = font.render(str(MINES - len(flagged)),True,(255,255,255))
        screen.fill((0,0,0), (30*WIDTH+35, 60, 15, 15))
        screen.blit(txt_flags, (30*WIDTH+35, 60))
        pygame.display.update(30*WIDTH+35, 60, 15, 15)
        

    def loose():

        for i in range(len(bombs)):
            screen.blit(bomb, (bombs[i][0]*30, bombs[i][1]*30))

        txt = font2.render("défaite",True,(255,0,0))
        screen.blit(txt, (10*WIDTH,10*HEIGHT))

        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():

                #close game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #restart
                if event.type == pygame.KEYDOWN:
                    menu() 
                    

    def win():
        txt = font2.render("Victoire",True,(255,0,0))
        screen.blit(txt, (10*WIDTH,10*HEIGHT))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():

                #close game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #restart
                if event.type == pygame.KEYDOWN:
                    menu() 
        
        
    def dig(x,y):

        #dig count
        if [x,y] not in digged_list:
            digged_list.append([x,y])

        #draw digged
        screen.blit(digged,(x,y))
        pygame.display.update()

        color = [(0,0,255), (0,255,0), (255,0,0), (0,255,255), (255,0,255), (255,255,0), (175,175,175), (0,0,0)] 

        #digged mine
        if [int(x/30), int(y/30)] in bombs:
            loose()
            return 
        
        #check around
        minesAround = 0
        for k in range(-1,2):
            for l in range(-1,2):
                if([int(x/30+k), int(y/30+l)] in bombs):
                    minesAround += 1
                
        #recursive
        if minesAround == 0:
            l = [[x-30,y-30], [x-30,y], [x-30, y+30], [x,y-30], [x,y+30], [x+30,y-30], [x+30,y], [x+30,y+30]]
            for i in range(len(l)):
                if l[i] not in digged_list and l[i] not in flagged and 0<=l[i][0]<WIDTH*30 and 0<=l[i][1]<HEIGHT*30:
                    dig(l[i][0], l[i][1])

        #draw number           
        else:
            txt_number = font.render(str(minesAround), True, color[minesAround-1])
            screen.blit(txt_number,(x+10, y+10))
    
    
    #game initialization
    bombs = []
    flagged = []
    digged_list = []
    
    #background
    for i in range(WIDTH):
        for j in range(HEIGHT):
            screen.blit(wall, (i*30,j*30))
    
    #draw
    rightSide()
    pygame.display.update()
    
    #put mines
    while len(bombs)<MINES:
        x = randrange(0,WIDTH)
        y = randrange(0,HEIGHT)
        if [x,y] not in bombs:
            bombs.append([x,y])
            
    #mainloop
    while True:
        pygame.time.Clock().tick(FPS)

        for event in pygame.event.get():
            
            #closing game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            #back to menu
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    menu()

            #restart
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    game(difficulty)
                
            #click
            if event.type == MOUSEBUTTONDOWN:
                #only if in window
                if event.pos[0]<WIDTH*30 and event.pos[1]<HEIGHT*30:
                    
                    #left click (dig)
                    if event.button == 1 and [(int(event.pos[0]/30)*30), int(event.pos[1]/30)*30] not in flagged:
                        dig(int(event.pos[0]/30)*30, int(event.pos[1]/30)*30)
                       
                    #right click (flag) 
                    if event.button == 3:
                        if [(int(event.pos[0]/30)*30), int(event.pos[1]/30)*30] not in flagged:
                            if [(int(event.pos[0]/30)*30), int(event.pos[1]/30)*30] not in digged_list: #and len(flagged)<MINES:
                                flagged.append([(int(event.pos[0]/30)*30), int(event.pos[1]/30)*30])
                        else :
                            flagged.remove([(int(event.pos[0]/30)*30), int(event.pos[1]/30)*30])
                            screen.blit(wall, ((int(event.pos[0]/30)*30),(int(event.pos[1]/30)*30)))
                            
                        for i in range(len(flagged)):
                            screen.blit(flag, (flagged[i][0],flagged[i][1]))
                    
                    #draw
                    rightSide()
                    pygame.display.update()
                    
                    #victory check
                    if len(digged_list) == WIDTH*HEIGHT-MINES:
                        win()
                
        
    
menu()