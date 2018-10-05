#!/usr/bin/python3.6
#-*- conding: utf-8 -*-

import pygame
from pygame.locals import *

name = input("Le nom de ton fichier 'niveau 1.txt' par exemple : ")
image = input("le nom de ton image de fichier niveau 'niveau1.png' par example, en 1200 par 675 :")

screen_l = 1200
screen_h = 675

pygame.init()
screen = pygame.display.set_mode((screen_l,screen_h))
pygame.display.set_caption("Schizophrenia éditeur")
pygame.display.flip()


fond = pygame.image.load(image).convert()

screen.blit(fond,(0,0))
pygame.display.flip()

run = True


try :
	fichier = open(name,"r")
except:
	pass
else:
	fichier = open(name,"a")
	fichier.write("\n")
	fichier.close()


fichier = open(name,"a")

def get_touches():
	#no parameters
	#gives a "quit" if the player presses Alt+F4, otherwise gives the pressed keys
	pygame.event.pump()

	keys_name = ["0","1","2","3","4","5","U","L","D","R","Enter","ENTER","esc"]
	keys_nb = [48,49,50,51,52,53,273,276,274,275,13,271,27]
	keys_input = []

	all_keys = pygame.key.get_pressed()
	if all_keys[pygame.K_F4] and (all_keys[pygame.K_LALT] or all_keys[pygame.K_RALT]): 
		return("quit")

	for event in pygame.event.get():
		if event.type == KEYDOWN:
			
			for x in range(0,len(keys_nb)):
				
				
				if event.key == keys_nb[x] and not(keys_name[x] in keys_input):
					keys_input.append(keys_name[x])
		if event.type == pygame.QUIT:
			return("quit")
	return keys_input


state=1

tmp = 0

first = 1

print("coin superieur gauche")

while run:
	pressed =get_touches()

	if pressed == "quit":
		run=False

	if pygame.mouse.get_pressed()[0]==0:
		tmp = 0

	if pygame.mouse.get_pressed()[0]==1 and tmp == 0 and (state == 1 or state ==2):
		pos = pygame.mouse.get_pos()
		tmp=1

		if state == 1:
			if first == 1:
				first = 0
			else:
				fichier.write("\n")

			fichier.write(str(pos[0])+","+str(pos[1])+",")
			print("coin inferieur droit")
			state = 2

		elif state == 2:
			fichier.write(str(pos[0])+","+str(pos[1])+",")
			print("type de ta plate_forme")
			state = 3

	if state == 3:
		if "0" in pressed:
			fichier.write("0")
			state = 1 
			print("coin superieur gauche")
		elif "1" in pressed:
			fichier.write("1")
			state = 1 
			print("coin superieur gauche")
		elif "2" in pressed:
			fichier.write("2")
			state = 1 
			print("coin superieur gauche")
		elif "3" in pressed:
			fichier.write("3")
			state = 1 
			print("coin superieur gauche")
		elif "4" in pressed:
			fichier.write("4")
			state = 1 
			print("coin superieur gauche")
		elif "5" in pressed:
			fichier.write("5")
			state = 1 
			print("coin superieur gauche")


fichier.close()










