class girasoles:
    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.vida = 6
        self.representacion = "G"
        
    def recibedaño(self):
        self.vida -= 1
        if self.vida == 0:
            return True
        else:
            return False

class lanzaguizantes:
    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.vida = 6
        self.representacion = "L"
        self.daño 
        
    def recibedaño(self):
        self.vida -= 1
        if self.vida == 0:
            return True
        else:
            return False

class nuez: 
    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.vida = 60
        self.representacion = "N"
        
    def recibedaño(self):
        self.vida -= 1
        if self.vida == 0:
            return True
        else:
            return False