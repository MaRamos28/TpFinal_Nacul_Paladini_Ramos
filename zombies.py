import random as rd
import time

class zombies:
    def __init__(self, x, tipo="normal"):
        self.x = x
        self.y = rd.randint(0,4)
        self.velocidad = 1
        self.daño = 1
        
        tipo = tipo.lower()
        if tipo == "normal":
            self.vida = 10
            self.representacion = "Z"
        elif tipo == "cono":
            self.vida = 20
            self.representacion = "ZC"
        elif tipo == "balde":
            self.vida = 30
            self.representacion = "ZB"
    
    def recibedaño(self):
        self.vida -= 1
        if self.vida == 0:
            return True
        else:
            return False

    def ataque(self):
        self.milis_ataque = time.time()
        if time.time() - self.milis_ataque > 1:
            return True    
    
    def movimiento(self): #Deberia ejecutarse todo el tiempo
        self.milis_mov = time.time()
        if time.time() - self.milis_mov > 6:
            self.x -= self.velocidad
            self.milis_mov = time.time()
