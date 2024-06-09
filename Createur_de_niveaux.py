import sys

import pygame

from gestion_image import chargeur_images
from terrain import Terrain

taille_affichage = 2.0

class editeur():
    n=0
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('créateur de niveau')
        self.screen = pygame.display.set_mode((1200,800))
        self.display = pygame.Surface((600,400))
        self.clock = pygame.time.Clock()

        self.assets = {




        }

        self.mouvement = [False,False,False,False]

        self.terrain = Terrain(self,taille_block =16)

        try:
            self.terrain.charger('carte.json')
        except FileNotFoundError:
            pass

        self.scroll = [0,0]

        self.list_block = list(self.assets)
        self.group_block = 0
        self.variante_block = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.sur_grille = True
    
    def run(self):
        while True:
            self.display.fill((0 ,0 , 0))

            self.scroll[0] += (self.mouvement[1]-self.mouvement[0]) * 2
            self.scroll[1] += (self.mouvement[3]-self.mouvement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.terrain.render(self.display,decalage= render_scroll)

            image_block_choisie = self.assets[self.list_block[self.group_block]][self.variante_block].copy()
            image_block_choisie.set_alpha(100)

            pos_souris = pygame.mouse.get_pos()
            pos_souris = (pos_souris[0]/taille_affichage,pos_souris[1]/taille_affichage)
            pos_block = (int((pos_souris[0]+self.scroll[0])//self.terrain.taille_block), int ((pos_souris[1]+ self.scroll[1])//self.terrain.taille_block))

            if self.sur_grille :
                self.display.blit(image_block_choisie,(pos_block[0] * self.terrain.taille_block - self.scroll[0],pos_block[1] * self.terrain.taille_block - self.scroll[1]))
            else:
                self.display.blit(image_block_choisie,pos_souris)
            
            if self.clicking and self.sur_grille:
                self.terrain.blockmap[str(pos_block[0])+ ';' + str(pos_block[1])] ={'type': self.list_block[self.group_block],'variant': self.variante_block, 'pos':pos_block}
            if self.right_clicking:
                loc_block = str(pos_block[0])+ ';' + str(pos_block[1])
                if loc_block in self.terrain.blockmap:
                    del self.terrain.blockmap[loc_block]
                for block in self.terrain.hors_grille_block.copy():
                    image_block = self.assets[block['type']][block['variante']]
                    image_re = pygame.Rect(block['pos'][0]- self.scroll[0],block['pos'][1]-self.scroll[1],image_block.get_width(),image_block.get_height())
                    if image_re.collidepoint(pos_souris):
                        self.terrain.hors_grille_block.remove(block)
            
            self.display.blit(image_block_choisie, (5,5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.sur_grille:
                            self.terrain.hors_grille_block.append({'type':self.list_block[self.group_block],'variante': self.variante_block,'pos':(pos_souris[0],self.scroll[0],pos_souris[1]+self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.variante_block = (self.variante_block - 1) % len(self.assets[self.list_block[self.group_block]])
                        if event.button == 5:
                            self.variante_block =(self.variante_block + 1) % len(self.assets[self.list_block[self.group_block]])
                    else:
                        if event.button == 4 :
                            self.group_block = (self.group_block - 1) % len(self.list_block)
                            self.variante_block = 0
                        if event.button == 5 :
                            self.group_block = (self.group_block + 1) % len(self.list_block)
                            self.variante_block = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.mouvement[0] = True
                    if event.key == pygame.K_d:
                        self.mouvement[1] = True
                    if event.key == pygame.K_z:
                        self.mouvement[2] = True
                    if event.key == pygame.K_s:
                        self.mouvement[3] = True
                    if event.key == pygame.K_TAB:
                        self.sur_grille = not self.sur_grille
                    if event.key == pygame.K_LCTRL and pygame.K_s:
                        n+=1
                        self.terrain.sauvegarder('carte'+n+'.json')
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        self.mouvement[0] = False
                    if event.key == pygame.K_d:
                        self.mouvement[1] = False
                    if event.key == pygame.K_z:
                        self.mouvement[2] = False
                    if event.key == pygame.K_s:
                        self.mouvement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
                
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

editeur().run()






