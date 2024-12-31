
class Entity():
    def __init__(self, name, hp, DMG, stamina):
        self.__name = name
        self.__hp = hp
        self.__DMG = DMG
        self.__stamina = stamina
        self.__guard = False
        self.tiredcount = 0
        self.__max_hp = hp
        self.__max_stamina = stamina
        self.__max_DMG = 150
    def get_name(self):
        return f"{self.__name}"
    def use_energy(self):
        self.__stamina -= 10
    def set_hp(self, amount):
        self.__hp += amount
    def get_hp(self):
        return self.__hp
    def get_DMG(self):
        return self.__DMG
    def set_DMG(self, amount):
        self.__DMG += amount
    def set_stamina(self, amount):
        self.__stamina += amount
    def get_stamina(self):
        return self.__stamina
    def set_guard(self, Boolean):
        self.__guard = Boolean
    def get_guard(self):
        return self.__guard
    def recover(self):
        self.__stamina = 100
    def get_max_hp(self):
        return self.__max_hp
    def get_max_DMG(self):
        return self.__max_DMG
    def get_max_stamina(self):
        return self.__max_stamina
    def normalise_hp(self):
        self.__hp = self.get_max_hp()
    def reset(self):
        self.normalise_hp()
        self.recover()
        self.tiredcount = 0
    def attack(self, entity):
        if self.tiredcount >= 3:
            self.set_stamina(self.get_stamina()*-1)
            self.set_stamina(self.__max_stamina)
        if self.get_stamina()//self.get_max_stamina() >= 0.5:
            entity.set_hp(self.get_DMG()*-1 if not entity.get_guard() else self.get_DMG()*-2)
            self.use_energy()
        else:
            entity.set_hp(self.get_DMG()/-2 if not entity.get_guard() else self.get_DMG()/-4)
            self.tiredcount += 1
            self.use_energy()
            
            
            