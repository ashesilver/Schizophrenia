#!/usr/bin/python3.7
#-*- coding: utf-8 -*-
#crédits : Thibault Tersinet et Sylvain Leclerc 

import pygame, time
from pygame.locals import *

from random import randint
from math import *

from ennemies import *
from player import *

def initialize(screen_l = 1200,screen_h = 675):
	#returns pygame object (weird stuff)
	pygame.init()
	screen = pygame.display.set_mode((screen_l,screen_h))
	pygame.display.set_caption("Schizophrenia")
	pygame.display.set_icon(pygame.image.load('images/Stickman.png'))
	pygame.display.flip()
	return screen

def get_data(classe,i=0,sort=None):
	"""get the data of something;
	i must be an int ; sort must be a str ; classe must be an existing object"""
	obj = classe
	obj.number = i
	obj.kind = sort
	return obj.output_data()

def get_touches():
	#no parameters
	#gives a "quit" if the player presses Alt+F4, otherwise gives the pressed keys
	pygame.event.pump()

	keys_name = ["1","2","3","4","U","L","D","R","Enter","ENTER","esc"]
	keys_nb = [49,50,51,52,273,276,274,275,13,271,27]
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

def sq(nb):
	#prend en entrée un nombre
	#retourne son carré
	return nb*nb



class Plate_forme():
	"""créé, affiche et supprime des plate_forme"""
	def __init__(self,x=0, y=0, x2=10, y2=10, kind=0, screen=""):
		self.screen = screen
		self.position = [[x,y],[x2,y2]]
		self.angles = [[x,y],[x,y2],[x2,y2],[x2,y]]
		self.kind=kind

		self.color=(50,50,50)


		if kind==0:
			self.color=(25,36,237) # bleu
		elif kind==1:
			self.color=(255,137,10) # orange
		elif kind==2:
			self.color=(255,11,0) # rouge
		elif kind==3: 
			self.color=(55,255,0) # vert
		elif kind==4:
			self.color=(255,35,49) # ne sert pas
		else :
			self.color=(0,0,0) # noir


	def set(self): 
		"""place le polygon de la plate forme à sa place"""
		pygame.draw.polygon(self.screen,self.color,self.angles,0)

class Niveau():
	"""gère les fichiers niveaux et place les plates_formes"""
	def __init__(self, surface, nb):
		self.nb = nb
		self.plates_formes = []
		self.plates_formes_obj = []
		self.fond_file = "niveaux/"+str(nb)+".background.png"
		self.fond_obj = pygame.image.load(self.fond_file).convert()
		self.screen = surface
		

	def get(self):
		"""recupère le niveau depuis un fichier texte et stock les coordonées des plates-formes dans self.plates_formes"""
		fichier_nom = "niveaux/"+str(self.nb)+".txt"
		fichier=open(fichier_nom,"r")

		for x in fichier:
			tmp=""
			tmp2=[]
			for y in x:
				if y !=",":
					tmp+=y
				else:
					tmp2.append(int(tmp))
					tmp=""
			tmp2.append(int(tmp))
			tmp=""
			self.plates_formes.append(tmp2)

		fichier.close()

	def set(self):
		"""affiche le fond et toutes les platesformes"""
		self.screen.blit(self.fond_obj,(0,0))

		for x in self.plates_formes:
			self.plates_formes_obj.append(Plate_forme(x[0],x[1],x[2],x[3],x[4],self.screen))
		for x in self.plates_formes_obj:
			x.set()


class Joueur():			
	"""classe du joueur"""

	def __init__(self,screen,main_obj):
		self.screen=screen
		self.temp = None
		self.__obj__ = main_obj


		self.platform = []
		self.var = player[self.__obj__.current_lvl]["base_suit"]

		self.position = [player[self.__obj__.current_lvl]["base_pos"]["x"],player[self.__obj__.current_lvl]["base_pos"]["y"]]
		self.last_position = player[self.__obj__.current_lvl]["base_pos"]["y"]
		self.vecteur_vitesse = [0,0]
		self.vecteur_acceleration = [0,(-1)]


		self.sol = False
		self.limit_left = True
		self.limit_right = True
		self.roof = False
		self.grab_platform = True
		self.grinding = False

		#les stats de chaque personalité
		self.perso_vitesse = suits[self.var]['speed']
		self.perso_hauteur_saut = suits[self.var]['jump_height']
		self.perso_degat_chutte = suits[self.var]['fall_dmg']
		self.temp_color = suits[self.var]['temp_color']

		self.input = [] #contient les touches pressées au moment oú elles sont pressées
		self.Quit = False

	def death(self):
		#no parameters
		#kill the player : return to the same level (little animation tho)
		perdu = pygame.image.load("images/perdu.png").convert()
		perdu_son = pygame.mixer.Sound("sons/perdu.wav")
		perdu_son.play()

		end = time.time()+0.5

		self.screen.blit(perdu,(int((1200/2)-(357/2)),int((675/2)-(166/2))))

		pygame.display.flip()

		while end > time.time():
			get_touches()

		self.__obj__.within_level_loop()

	def win(self):
		#no parameters
		#wins the game : return to main menu
		self.position,self.vecteur_acceleration,self.vecteur_vitesse =[0,0],[0,0],[0,0]
		self.Quit = True
		print("yes")

		
	def detect_platform(self):
		#no parameters
		"""detect if the player will enter a platform next tick or is walking on a platform"""
		for x in self.platform :
			
			if (x[1] <= (self.vecteur_vitesse[1] + self.position[1]) or self.position[1] + 1 == x[1]) and self.position[1] <= x[1]:
				if self.position[0] >= x[0] and self.position[0] <= x[2] :
					self.position[1] = x[1] - 1    # -1 pour rester sur la plateforme
					self.sol = True
					try:
						if self.position[1]-self.last_position+self.perso_hauteur_saut >= self.perso_degat_chutte:
							self.death()
					except:
						pass
					finally :
						self.last_position = self.position[1]
						if x[4] == 2 :
							self.death()
							pass
						if x[4] == 5 :
							self.win()
							pass
						elif x[4] == 3 and self.var == "flee":
							self.perso_hauteur_saut = self.perso_hauteur_saut*2
			elif (x[3] >= (self.position[1] + self.vecteur_vitesse[1])) and self.position[1] >= x[3]:
				if self.position[0] >= x[0] and self.position[0] <= x[2] :
					self.position[1] = x[3] + 4    # +2 pour l'affichage
					self.vecteur_vitesse[1] = 0
					if x[4] == 2 :
						self.death()
						pass
					if x[4] == 5 :
						self.win()
					elif x[4] == 1 and self.var == "strong":
						self.roof = True
						self.grabbed_platform = x
			
			if ((self.position[0] - self.perso_vitesse) <= x[2] ) and self.position[0] > x[2]:
				if x[1] <= self.position[1] and self.position[1] <= x[3] + 1 :
					self.limit_left = False
					self.grinding = True
					if x[4] == 2 :
						self.death()
						pass
					if x[4] == 5 :
						self.win()
					if self.var == "strong" :
						self.vecteur_vitesse[1] = -1
					else :
						self.vecteur_vitesse[1] = 0
					self.position[0] = x[2] + 2  #pygame est très soupe au lait... du coup j'ai ajusté...
			if ((self.perso_vitesse + self.position[0]) >= x[0] ) and self.position[0] < x[0]:
				if x[1] <= self.position[1] and self.position[1] <= x[3] + 1 :
					self.limit_right = False
					self.grinding = True
					if x[4] == 2 :
						self.death()
						pass
					if x[4] == 5 :
						self.win()
					if self.var == "strong" :
						self.vecteur_vitesse[1] = -1
					else :
						self.vecteur_vitesse[1] = 0				
					self.position[0] = x[0] - 1 #pygame est très soupe au lait... du coup j'ai ajusté...
		
		if self.roof :
			if self.position[0] < self.grabbed_platform[0] or self.position[0] > self.grabbed_platform[2] :
				self.roof = False
		if self.position[1] >= 674 :
			self.sol = True
		elif self.position[1] <= 1 :
			self.vecteur_vitesse[1] = 0
		if self.position[0] <= 1 :
			self.limit_left = False
		elif self.position[0] >= 1199 :
			self.limit_right = False

	def update(self):
		#no parameters
		"""modifie l'acceleration, la vitesse et la position en fonction des touches pressés et des valeurs précédentes"""
		self.change()
		self.detect_platform()
		if self.grab_platform and self.roof:
			self.vecteur_acceleration[1] = 0
		else :
			if self.sol and self.grinding :
				self.grinding = False
			elif self.sol :
				self.vecteur_acceleration[1] = 0
				self.vecteur_vitesse[1] = 0
			else :
				self.vecteur_acceleration[1] = (-1)
		self.vecteur_vitesse[0] = 0
		if "U" in self.input and self.sol:
			self.vecteur_vitesse[1] = -1 * self.perso_hauteur_saut
			self.sol = False
		elif "D" in self.input and self.roof:
			self.roof = False
			self.vecteur_acceleration[1] = -1
		elif "D" in self.input and self.sol:
			self.vecteur_vitesse[1] = 0
		if "U" in self.input and self.grinding and self.var == "strong" :
			self.vecteur_acceleration[1] = 1
		if "L" in self.input and self.limit_left:
			self.vecteur_vitesse[0] = (-1) * (self.perso_vitesse)
		elif "R" in self.input and self.limit_right:
			self.vecteur_vitesse[0] = self.perso_vitesse

		#reset limits
		self.sol = False
		self.limit_right = True
		self.limit_left = True
		self.grinding = False
		self.next()

		return self.Quit

	def next(self):
		#update graphics and positions

		pygame.draw.circle(self.screen,[255,255,255],[self.position[0],self.position[1]-1],1,0)

		self.vecteur_vitesse[1]  -= self.vecteur_acceleration[1]
		# max fall speed settings to avoid bugs
		if self.vecteur_vitesse[1] == (10) :
			self.vecteur_vitesse[1] = (9)
		self.position[0] += self.vecteur_vitesse[0]
		self.position[1]  += self.vecteur_vitesse[1]

		pygame.draw.circle(self.screen,self.temp_color,[self.position[0],self.position[1]-1],1,0)

	def change(self):
		#no parameters
		"""prend la nouvelle personalite et change les stats en fonction"""
		try:
			if "1" in self.input:
				self.var = "normal"
			elif "2" in self.input:
				self.var = "strong"
			elif "3" in self.input:
				self.var = "flee"
			elif "4" in self.input:
				pass
		finally:
			if self.roof:
				self.var = "strong"
			self.perso_vitesse = suits[self.var]['speed']
			self.perso_hauteur_saut = suits[self.var]['jump_height']
			self.perso_degat_chutte = suits[self.var]['fall_dmg']
			self.temp_color = suits[self.var]['temp_color']


	def get_touches(self):
		#no parameters
		#get pressed keys, and gives a "quit" if the player presses Alt+F4
		pygame.event.pump()

		keys_name = ["1","2","3","4","U","L","D","R"]
		keys_nb = [49,50,51,52,273,276,274,275]

		all_keys = pygame.key.get_pressed()
		if all_keys[pygame.K_F4] and (all_keys[pygame.K_LALT] or all_keys[pygame.K_RALT]): 
			pygame.quit()
			quit()

		for event in pygame.event.get():
			if event.type == KEYUP:
				for x in range(0,len(keys_nb)):
					if event.key == keys_nb[x] and keys_name[x] in self.input:
						self.input.remove(keys_name[x])
			if event.type == KEYDOWN:
				for x in range(0,len(keys_nb)):
					if event.key == keys_nb[x] and not(keys_name[x] in self.input):
						self.input.append(keys_name[x])
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

	def output_data(self):
		#no parameters
		#get the data of the player
		return {
		"state" : self.var, 
		"position":{'x':self.position[0],'y':self.position[1]},
		"is_hanging" : self.roof}

class Ennemies():
	"""Ennemies gesture"""
	def __init__(self, current_lvl,screen):
		#data : the current lvl which is played.
		#Set everything up for the object when the class is called.
		self.screen = screen
		self.xpos = 0
		self.ypos = 0
		self.xmin = 0
		self.xmax = 0
		self.temp_color = [0,0,0]
		self.tot_number = 0
		self.list_kinds = ["goomba","koopa","donkey_kong_jr"]
		self.counter = 0
		self.number = 0
		self.new_ennemy = {}
		self.all_ennemies = []
		self.all_ennemies_fake = []
		self.speed = 0
		self.direction = True
		self.overwrite_mode = False
		self.size = 0
		self.current_lvl = current_lvl

	def get(self):
		#no parameters
		""" the "spy"... this method looks' in other files to import the wanted informations"""
		self.xpos = self.var[self.current_lvl][str("n_"+str(letter_number_list[(self.counter+1)]))]["base_pos"]["xpos"]
		self.ypos = self.var[self.current_lvl][str("n_"+str(letter_number_list[(self.counter+1)]))]["base_pos"]["ypos"]
		self.xmin = self.var[self.current_lvl][str("n_"+str(letter_number_list[(self.counter+1)]))]["max_coords"]["xmin"]
		self.xmax = self.var[self.current_lvl][str("n_"+str(letter_number_list[(self.counter+1)]))]["max_coords"]["xmax"]
		self.temp_color = self.var[self.current_lvl][str("n_"+str(letter_number_list[(self.counter+1)]))]["temp_color"]
		self.speed = self.var["stats"]["ms"]
		self.size = self.var["stats"]["hitbox"][0]

	def draw(self):
		#no parameters
		"""load on screen visual informations on ennemies"""
		
		if self.direction:
			pygame.draw.circle(self.screen,[255,255,255],[self.xpos-self.speed,self.ypos],self.size,0)
		else :
			pygame.draw.circle(self.screen,[255,255,255],[self.xpos+self.speed,self.ypos],self.size,0)
		pygame.draw.circle(self.screen,self.temp_color,[self.xpos,self.ypos],self.size,0)

		pass
	
	def encode(self):
		#no parameters
		""" encode each ennemy in a dictionnary, in a list of dictionnaries """
		self.new_ennemy = {
		"xpos":self.xpos,
		"ypos":self.ypos,
		"max_coords":[self.xmin,self.xmax],
		"temp_color":self.temp_color,
		"speed":self.speed,
		"direction":self.direction,
		"kind":self.kind,
		"size":self.size
		}
		if self.overwrite_mode :
			self.all_ennemies_fake.append(self.new_ennemy)
		else :
			self.all_ennemies.append(self.new_ennemy)

	def set(self):
		#no parameters
		"""initialize everything"""
		for x in self.list_kinds :
			self.kind = x
			if self.kind == "goomba":
				self.var = goomba
			elif self.kind == "koopa":
				self.var = koopa
			elif self.kind == "donkey_kong_jr":
				self.var = donkey_kong_jr
			self.tot_number = self.var[self.current_lvl]["tot_number"][0]
			for self.counter in range(self.tot_number):
				self.get()
				self.draw()
				self.encode()
			self.counter = 0
		self.overwrite_mode = True

	def update(self):
		#no parameters
		"""updates graphical aspects, and hitboxes of ennemies (per frame)"""
		for i in range(len(self.all_ennemies)):
			self.direction = self.all_ennemies[i]["direction"]
			if self.all_ennemies[i]["xpos"]-self.all_ennemies[i]["speed"] < self.all_ennemies[i]["max_coords"][0]:
				self.direction = True
			elif self.all_ennemies[i]["xpos"]+self.all_ennemies[i]["speed"] > self.all_ennemies[i]["max_coords"][1]:
				self.direction = False
			self.xpos = self.all_ennemies[i]["xpos"]
			if self.direction :
				self.xpos += self.all_ennemies[i]["speed"]
			else :
				self.xpos -= self.all_ennemies[i]["speed"]			
			self.ypos = self.all_ennemies[i]["ypos"]
			self.temp_color = self.all_ennemies[i]["temp_color"]
			self.xmin = self.all_ennemies[i]["max_coords"][0]
			self.xmax = self.all_ennemies[i]["max_coords"][1]
			self.kind = self.all_ennemies[i]["kind"]
			self.speed = self.all_ennemies[i]["speed"]
			self.size = self.all_ennemies[i]["size"]
			self.draw()
			self.encode()
		self.all_ennemies = self.all_ennemies_fake
		self.all_ennemies_fake = []

	def output_data(self):
		#no parameters
		"""returns the informations needed on a specific ennemy"""
		if self.kind == None:
			return self.all_ennemies
		specific_kind_ennemies = []
		for x in self.all_ennemies :
			if self.kind == x['kind']:
				specific_kind_ennemies.append(x)
		if self.number==0:
			return specific_kind_ennemies
		return specific_kind_ennemies[self.number-1]

class __Core__():
	"""classe prinicpale gérant toutes les autres"""

	def __init__(self, FPS_limit=60):
		#whole pygame support
		self.screen = initialize()
		self.clock = pygame.time.Clock()
		#var
		self.lvl_tag = 0
		self.current_lvl = ""
		self.is_level_running = False
		self.FPS_limit = FPS_limit
		self.input = get_touches()

		self.save = "save.txt"

		self.max_lvl = 1


		try :
			fichier = open(self.save,"r")
		except:
			fichier = open(self.save,"w")
			fichier.write("1")
			fichier.close()
		else:
			self.max_lvl = int(fichier.read())
			fichier.close()

	def loading (self):
		#affiche un écran de chargement ne chargant rien du tout, purement décoratif 
		fond = pygame.image.load("images/loading.png")
		barre = pygame.image.load("images/loading barre.png")

		self.screen.blit(fond,(0,0))

		pygame.display.flip()

		for x in range(0,200):
			self.screen.blit(barre,(297+x*3,352))
			pygame.display.flip()
			if randint(0,10) == 7:
				time.sleep(1/20)

	def update_max_lvl(self):
		#change dans le fichier de sauvegarde le niveau maximal atteint par self.lvl_tag si self.lvl_tag > self.max_lvl

		if self.lvl_tag > self.max_lvl:
			fichier = open(self.save,"w")
			fichier.write(str(self.lvl_tag))
			fichier.close()

	def collisions_player_ennemies(self):
		"""test si le joueur est en contact avec les enemies, si c'est le cas lance la methode death() de joueur"""
		DA_MAN = get_data(self.player)
		DA_BEACHIZ = get_data(self.ennemies,0,None)
		
		for x in DA_BEACHIZ:
			no_mans_land = [[0,0],[0,0]]
			if x["kind"] == "goomba":
				hitbox = goomba['stats']['hitbox'][0]
			elif x["kind"] == "donkey_kong_jr":
				hitbox = donkey_kong_jr['stats']['hitbox'][0]
			elif x["kind"] == "koopa":
				hitbox = koopa['stats']['hitbox'][0]
			no_mans_land = [[x['xpos']-hitbox,x['ypos']-hitbox],[x['xpos']+hitbox,x['ypos']+hitbox]]
			if (DA_MAN['position']['x'] > no_mans_land[0][0] and DA_MAN['position']['x'] < no_mans_land[1][0] ) and (DA_MAN['position']['y'] > no_mans_land[0][1] and DA_MAN['position']['y'] < no_mans_land[1][1]):
				self.player.death()

	def within_level_loop(self):
		"""methode creant tous les objet necessaires pour lancer un niveau et qui appelle ensuite les methodes adéquates """
		self.level = Niveau(self.screen,self.lvl_tag)
		self.level.get()
		self.level.set()
		self.player = Joueur(self.screen,self)
		self.player.platform = self.level.plates_formes
		self.ennemies = Ennemies(self.current_lvl,self.screen)
		self.ennemies.set()
		self.Quit = False
		self.is_level_running = True

		while not self.Quit:
			#pygame.display.update()
			if self.player.get_touches() == "quit":
				self.Quit = True
			self.clock.tick(self.FPS_limit)
			self.ennemies.update()
			self.collisions_player_ennemies()
			self.Quit = self.player.update()
			pygame.display.flip()

		self.is_level_running = False

	def run(self):
		"""cette methode gere tout le jeu ainsi que les menus, c'est celle a appeller pour lancer le jeu"""
		centres = [[179, 311], [251, 357], [251, 436], [325, 394], [397, 436], [468, 395], [468, 479], [542, 436], [612, 397], [687, 439], [758, 397], [758, 482], [761, 564], [829, 522], [906, 481], [906, 399], [906, 317], [974, 275], [1050, 317], [1050, 408]]
		self.lvl_tag = 1

		run = True

		menu = True
		selection_niveaux = False
		a_propos = False
		play = False

		set_locked_lvl = True

		mouse_btn_pos = 0 # sur quel bouton est la souris

		btn1 = pygame.image.load("images/btn1.png").convert()
		btn2 = pygame.image.load("images/btn2.png").convert()
		btn3 = pygame.image.load("images/btn3.png").convert()
		btn4 = pygame.image.load("images/btn4.png").convert()

		fond_main = pygame.image.load("images/fond_menu.png").convert()
		fond_select = pygame.image.load("images/selection.png").convert()
		fond_a_propos = pygame.image.load("images/a propos.png").convert()

		point = pygame.image.load("images/point.png").convert()
		pas_point = pygame.image.load("images/pas point.png").convert()
		cerrure = pygame.image.load("images/cerrure.png").convert()


		bouton_son = pygame.mixer.Sound("sons/bouton.wav")
		niveau_son = pygame.mixer.Sound("sons/niveau.wav")


		while run: # boucle du jeu

			self.input = get_touches()
			
			if menu: #boucle du menu principale
				self.clock.tick(self.FPS_limit)

				pos = pygame.mouse.get_pos()

				#detecte si la souris est sur l'un des boutons du menu

				if (362<pos[0]<830 and 226<pos[1]<285) :
					if (mouse_btn_pos != 1 ):
						mouse_btn_pos = 1
						bouton_son.play()
						self.screen.blit(fond_main, (0,0))
						self.screen.blit(btn1, (309,225))
						pygame.display.flip()
						


				elif (362<pos[0]<830 and 330<pos[1]<385) :
					if (mouse_btn_pos != 2 ):
						mouse_btn_pos = 2
						bouton_son.play()
						self.screen.blit(fond_main, (0,0))
						self.screen.blit(btn2, (309,325))
						pygame.display.flip()



				elif (362<pos[0]<830 and 430<pos[1]<485) :
					if (mouse_btn_pos != 3 ):
						mouse_btn_pos = 3
						bouton_son.play()
						self.screen.blit(fond_main, (0,0))
						self.screen.blit(btn3, (309,425))
						pygame.display.flip()



				elif (362<pos[0]<830 and 530<pos[1]<585) :
					if (mouse_btn_pos != 4 ):
						mouse_btn_pos = 4
						bouton_son.play()
						self.screen.blit(fond_main, (0,0))
						self.screen.blit(btn4, (309,525))
						pygame.display.flip()

				else:
					self.screen.blit(fond_main, (0,0))
					pygame.display.flip()
					mouse_btn_pos = 0



				#detecte si l'utilisateur clique sur l'un des boutons

				if (pygame.mouse.get_pressed()[0]==1 and mouse_btn_pos==1) or "1" in self.input:
					self.lvl_tag = 1

					play = True
					menu = False

				if (pygame.mouse.get_pressed()[0]==1 and mouse_btn_pos==2 ) or "2" in self.input:
					self.lvl_tag = self.max_lvl

					play = True
					menu = False

				if (pygame.mouse.get_pressed()[0]==1 and mouse_btn_pos==3)or "3" in self.input:

					set_locked_lvl = True
					selection_niveaux = True
					menu = False
					self.loading()

				if (pygame.mouse.get_pressed()[0]==1 and mouse_btn_pos==4) or "4" in self.input:
					a_propos = True
					menu = False

			if selection_niveaux: # boucle du menu selection des niveaux
				
				

				if set_locked_lvl:
					self.screen.blit(fond_select, (0,0))
					for x in range(0,len(centres)):
						if x+1 > self.max_lvl:
							self.screen.blit(cerrure,(centres[x][0]-5,centres[x][1]-35))
					pygame.display.flip()
					set_locked_lvl = False


				
				pos = pygame.mouse.get_pos()

				for x in range(0,len(centres)):

					if sqrt(sq(pos[0]-centres[x][0])+sq(pos[1]-centres[x][1])) < 45:
						#niveau_son.play()
						self.screen.blit(point,(centres[x][0]+15,centres[x][1]+24))
						pygame.display.flip()

						if pygame.mouse.get_pressed()[0]==1 and x < self.max_lvl:
							self.lvl_tag = x+1
							set_locked_lvl = True
							play = True
							selection_niveaux = False
					else:
						self.screen.blit(pas_point,(centres[x][0]+15,centres[x][1]+24))
						pygame.display.flip()

			if a_propos: # boucle du menu a propos
				self.screen.blit(fond_a_propos,(0,0))
				pygame.display.flip()

			if play: # boucle du niveau en cours
				self.current_lvl = "lvl"+str(self.lvl_tag)

				try:
					self.within_level_loop()
				except:
					try:
						self.level.get()
					except:
						#raise
						pass
					else:
						run = False
					finally:
						self.lvl_tag = 1
						menu = True
						play = False
					#raise
				else:
					self.lvl_tag += 1
					self.update_max_lvl()
				

			if "esc" in self.input:

				menu = True
				selection_niveaux = False
				a_propos = False

			if self.input =="quit":
				run = False
				menu = False
				selection_niveaux = False
				a_propos = False
				play = False
						
		
__main__ = __Core__(60)
__main__.loading()
__main__.run()
pygame.quit()
quit()
