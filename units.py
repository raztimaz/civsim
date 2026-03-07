import random

class UnitGroup:
    def __init__(self,units,x,y,world):
        self.x=x
        self.y=y
        
        for unit in units:
            if not self._is_valid_unit(unit):
                raise ValueError("Invalid unit")
        if len(units)==0:
            raise ValueError("Group can't be empty")
        
        self.units=units[:]
        self.main_unit=units[0]
        self.world=world

        for unit in units:
            unit.group=self
    def _is_valid_unit(self,unit):
        if unit.x!=self.x or unit.y!=self.y or unit.group is not None:
            return False
        return True
    def update(self,world):
        for unit in self.units:
            unit.update(world)
    def add_unit(self,unit):
        if not self._is_valid_unit(unit):
            raise ValueError("Invalid unit")
        self.units.append(unit)
        unit.group=self
    def remove_unit(self,unit):
        self.units.remove(unit)
        unit.group=None
        if len(self.units)==0:
            self.world.unit_groups[self.x][self.y]=None
            return
        if unit is self.main_unit:
            self.main_unit=self.units[0]

class Unit:
    def __init__(self,unit_type,world,x,y):
        self.type=unit_type
        self.world=world
        self.x=x
        self.y=y
        self.group=None
    def update(self,world):
        if random.random()<0.05:
            self.move(random.randint(-1,1),
                      random.randint(-1,1))
    def move(self,dx,dy):
        self.group.remove_unit(self)
        self.x+=dx
        self.y+=dy
        group=self.world.unit_groups[self.x][self.y]
        
        if group is not None:
            group.add_unit(self)
        else:
            self.world.unit_groups[self.x][self.y]=UnitGroup([self],self.x,self.y,self.world)
