#!/usr/bin/python
# -*- coding: latin-1 -*-
#
# MataBicho v1.0
#
# by David G. Maziero (DGM)
# http://www.dgmsoft.rg3.net
#
import cProfile, pstats

import sys, os, math, pygame
from pygame import *
from random import randint
from operator import mod

#
# inicializa pygame
#
pygame.init()
pygame.display.init()
pygame.display.set_caption( "MataBicho v1.0" )
pygame.mixer.init()
counter = pygame.time.Clock()
screen = pygame.display.set_mode( (640,480) )

#
# carrega imagens
#
splash = pygame.image.load( r"data/matabicho.jpg" ).convert()
fundo = pygame.image.load( r"data/fundo.jpg" ).convert()
bugs = pygame.image.load( r"data/bicho.png" ).convert_alpha()
font = pygame.image.load( r"data/fonte.tga" ).convert_alpha()

#
# carrega sfx
#
plof = pygame.mixer.Sound( r"data/plof.wav" )
pygame.mixer.music.load( r"data/musica.mid" )

#
# variáveis globais
#
perdidos = 0
exterminados = 0
bichos = []
acc = 0.0
frametime = 0.0
acao = 0
nivel = 0.0
nivel_contador = 0

#
# Reseta variáveis globais
#
def ResetaTudo():
    global perdidos, exterminados, bichos, acc, acao, nivel, nivel_contador
    perdidos = 0
    exterminados = 0
    bichos = []
    acc = 0.0
    acao = 0
    nivel = 10.0
    nivel_contador = 0
    pygame.mixer.music.play(-1)

#
# Renderiza um texto
#
def Texto( x, y, texto ):
    global screen, font
    for char in texto:
        letra = ord(char)
        if not letra==' ':
            screen.blit( font, [x,y], [32*mod(letra,16),32*(letra/16),28,32] )
        x=x+18

#
# Classe Bicho
#
class Bicho:
    def __init__( self ):
        self.x = randint(60,580)
        self.y = randint(85,395)
        self.comportamento = randint(1,4)
        self.gfx = 0
        self.acc = 0.0
        self.acc2 = 0.0

    def Atualiza( self ):
        global perdidos
        self.acc = self.acc+frametime;
        if self.comportamento==0:
            if self.acc>1:
                return False
        else:
            # animação
            if self.acc>0.125:
                self.acc = 0
                if self.gfx==0: 
                    self.gfx=1 
                else: 
                    self.gfx=0  
            
            # movimentação do bicho          
            if self.comportamento==1:
                self.x = self.x+(160*frametime)
            elif self.comportamento==2:
                self.y = self.y+(160*frametime)
            elif self.comportamento==3:
                self.x = self.x-(160*frametime)
            elif self.comportamento==4:
                self.y = self.y-(160*frametime)

            # se saiu da tela
            if self.x>640 or self.y>480 or self.x<-60 or self.y<-85:
                perdidos = perdidos+1 
                return False                                
            
            # troca de comportamento
            self.acc2 = self.acc2+frametime;
            if self.acc2>0.25:
                self.acc2=0;
                if randint(1,8)==1: self.comportamento=randint(1,4)
                
        return True
        
    def Colide( self, mx, my ):
        global exterminados
        if self.comportamento>0 and mx>=self.x+8 and mx<=self.x+60 and my>=self.y+8 and my<=self.y+72:
            self.comportamento = 0
            self.gfx = 2
            self.acc = 0
            exterminados = exterminados+1
            return True
        else:
            return False

    def Desenha( self, screen ):
        screen.blit( bugs, [self.x,self.y], [0+(self.gfx*65),0,65,80] )

#
# Verificação do teclado
#
def VerificaTeclado():
    global bichos,acao
    for event in pygame.event.get():
        if event.type==KEYDOWN:
            if event.key==27:
                pygame.display.quit()
                sys.exit()
            if event.key==13:
                if acao==0: 
                    acao=1
                    pygame.mixer.music.stop()
                elif acao==2:
                    ResetaTudo()
                    acao=0
                
        if event.type==(MOUSEBUTTONDOWN):
            mx,my = event.pos
            pegou = 0
            for bicho in bichos: pegou = pegou+bicho.Colide( mx, my )
            # pegou um bicho? toca o áudio
            if pegou>0: plof.play()
                
#
# Game loop
#
def GameLoop():
    global screen,counter,font,bichos,acc,mb,lmb,frametime,acao,perdidos,exterminados,nivel,nivel_contador
    
    counter.tick(60)
    frametime = float(counter.get_rawtime())/1000

    VerificaTeclado()
    
    # apresentação
    if acao==0:
        screen.fill( [255,255,255] )
        screen.blit( splash, [79,74] )
        Texto( 170, 384, "Pressione <ENTER>" )
        Texto( 437, 448, "by DGM Soft")
    
    # jogo em si
    elif acao==1:
        
        # adiciona um novo bicho
        acc = acc+frametime
        if acc>(1.2-(nivel/10)):
            acc = 0
            bichos.append( Bicho() )
            nivel_contador = nivel_contador+1
            if nivel_contador==5+(nivel*3):
                nivel_contador = 0
                if nivel<10: nivel = nivel+1
            
        screen.blit( fundo, [0,0] )
        
        # placar
        Texto( 5, 448, "Perdidos: "+str(perdidos) )
        tmp = "Exterminados: "+str(exterminados)
        Texto( 635-(len(tmp)*18), 5, tmp )

        for bicho in bichos:
            if not bicho.Atualiza(): bichos.remove( bicho )
    
        for bicho in bichos:
            bicho.Desenha( screen )

        # condição de derrota        
        if perdidos>=10: acao = 2    
    
    # game over
    elif acao==2:
        screen.blit( fundo, [0,0] )
        for bicho in bichos:
            bicho.Desenha( screen )
        Texto( 239, 224, "GAME OVER" )        
        tmp = "Exterminados: "+str(exterminados)
        Texto( 635-(len(tmp)*18), 5, tmp )

    pygame.display.flip()
    
#
# main
#
ResetaTudo()

def rungame():
    while 1:
        GameLoop()

rungame()
