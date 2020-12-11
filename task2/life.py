'''
Logic:
0-1: alive -> dead
2: no change
3: dead -> alive
4+: alive -> dead

each cell is a boolean value; 1 = alive, 0 = dead;

alive = green, dead = white


'''

import copy

class Life:

    field = [] #game field; an array of boolean values, where 0 is a dead cell, 1 is an alive cell

    settings = {'field_length': 0,
                'field_width': 0,
                'looping': False} #not implemented
            #game settings dictionary, field_length and field_width are self-explanatory; if looping is activated, the cells at the edges of the field will be considered adjacent
    
    def set_length(self, n):
        self.settings['field_length'] = n

    def length(self):
        return self.settings['field_length']

    def set_width(self, n):
        self.settings['field_width'] = n

    def width(self):
        return self.settings['field_width']

    def toggle_looping(self):
        self.settings['looping'] = not self.settings['looping']

    def looping(self):
        return self.settings['looping']

    def kill_cell(self, x, y):
        self.field[x][y] = False

    def enliven_cell(self, x, y):
        self.field[x][y] = True

    def cell_is_alive(self, x, y):
        return self.field[x][y]
    
    def clear_field(self):
        for i in range(self.length()):
            for j in range(self.width()):
                self.field[i][j] = False
                
    def generate_field(self): #generate an entirely new field using current field_length and field_width
        self.field = []
        for i in range(self.length()):
            self.field.append([])
            for j in range(self.width()):
                self.field[i].append(False)

    def debug_show_field(self):
        for i in range(self.length()):
            for j in range(self.width()):
                if self.field[i][j]:
                    print('1', end = ' ')
                else:
                    print('0', end = ' ')
            print('')
    
    def __init__(self, x, y, l):

        self.set_length(x)
        self.set_width(y)
        if l:
            self.toggle_looping()
        self.generate_field()

    def check_surrounding(self, x, y): #maybe rewrite
        if (x == 0):
            if (y == 0):
                return self.field[x+1][y]+self.field[x+1][y+1]+self.field[x][y+1]
            elif (y == self.width()-1):
                return self.field[x+1][y]+self.field[x+1][y-1]+self.field[x][y-1]
            else:
                return self.field[x][y-1]+self.field[x+1][y-1]+self.field[x+1][y]+self.field[x+1][y+1]+self.field[x][y+1]
        elif (x == self.length()-1):
            if (y == 0):
                return self.field[x-1][y]+self.field[x-1][y+1]+self.field[x][y+1]
            elif (y == self.width()-1):
                return self.field[x-1][y]+self.field[x-1][y-1]+self.field[x][y-1]
            else:
                return self.field[x][y-1]+self.field[x-1][y-1]+self.field[x-1][y]+self.field[x-1][y+1]+self.field[x][y+1]
        elif (y == 0):
            return self.field[x-1][y]+self.field[x-1][y+1]+self.field[x][y+1]+self.field[x+1][y+1]+self.field[x+1][y]
        elif (y == self.width()-1):
            return self.field[x-1][y]+self.field[x-1][y-1]+self.field[x][y-1]+self.field[x+1][y-1]+self.field[x+1][y]
        else:
            return self.field[x-1][y]+self.field[x-1][y-1]+self.field[x][y-1]+self.field[x+1][y-1]+self.field[x+1][y]+self.field[x+1][y+1]+self.field[x][y+1]+self.field[x-1][y+1]
    
    def step(self):

        newfield = copy.deepcopy(self.field)
        changed = False
        for x in range(self.length()):
            for y in range(self.width()):
                check = self.check_surrounding(x, y)
                if (check < 2 and self.field[x][y] == True):
                    newfield[x][y] = False
                    changed = True
                elif (check == 3 and self.field[x][y] == False):
                    newfield[x][y] = True
                    changed = True
                elif (check > 3 and self.field[x][y] == True):
                    newfield[x][y] = False
                    changed = True
                
        self.field = copy.deepcopy(newfield)
        return changed

