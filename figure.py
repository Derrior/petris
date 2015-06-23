from copy import deepcopy

Xses = {"right":0, "left": 0, "up": -1, "down": 1}
Yses = {"right":1, "left": -1, "up": 0, "down": 0}
class figure:
    def __init__(self):
        self.coords = []
        self.angle = 0

    def make(self, c):
        min_x = 100
        ind = 0
        for i in range(len(c)):
            if c[i][0] < min_x:
                min_x = c[i][0]
                ind = i
        for i in range(len(c)):
            self.coords.append([c[i][0] - c[ind][0], c[i][1] - c[ind][1]])
        self.coords.sort()
        return self

    def append(self, elem):
        self.coords.append(elem)

    def clear(self):
        self.coords = []

    def empty(self):
        return len(self.coords) == 0
    
##rotate figure

    def turn_left(self):    
        new_coords = []
        last_y = 0
        curr_y = 0
        last_x = 0
        curr_x = 0
        for i in range(len(self.coords)):

            last_y += self.coords[i][1]
            last_x += self.coords[i][0]
            x, y = ([self.coords[0][1] - self.coords[i][1] + self.coords[0][0], self.coords[i][0] - self.coords[0][0] + self.coords[0][1]])
            curr_y += y
            curr_x += x
            new_coords.append([x, y])      
        self.coords = deepcopy(new_coords)
        self.coords.sort()
        return last_x, curr_x, last_y, curr_y


    def turn_right(self):
        new_coords = []
        last_y = 0
        curr_y = 0
        last_x = 0
        curr_x = 0
        for i in range(len(self.coords)):
            x, y = self.coords[i]
            last_y += y
            last_x += x
            x, y = ([-self.coords[0][1] + y + self.coords[0][0], -x + self.coords[0][0] + self.coords[0][1]])
            curr_y += y
            curr_x += x
            new_coords.append([x, y])      
        self.coords = deepcopy(new_coords)
        self.coords.sort()
        return last_x, curr_x, last_y, curr_y

    def move(self, direct):
        dx = Xses[direct]
        dy = Yses[direct]

        new_coords = []
        last_y = 0
        curr_y = 0
        last_x = 0
        curr_x = 0
        for i in range(len(self.coords)):
            x, y = self.coords[i]
            last_y += y
            last_x += x
            x, y = x + dx, y + dy
            curr_y += y
            curr_x += x
            new_coords.append([x, y])      
        self.coords = deepcopy(new_coords)
        self.coords.sort()


        
