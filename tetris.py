#!/usr/bin/python3

from random import randrange, randint, choice, random

from copy import deepcopy

import os, sys, threading

import curses, colored

from time import clock, sleep, time

from figure import figure

monitor = curses.initscr()

        
    
wight = 9
height = 23
invisible = 4
figures = [figure() for i in range(7)]
figures[0].make([[0, 0], [0, 1], [0, 2], [0, 3]])
figures[1].make(([[0, 0], [0, 1], [0, 2], [1, 2]]))
figures[2].make(([[0, 0], [0, 1], [0, 2], [1, 1]]))
figures[3].make(([[0, 0], [0, 1], [1, 2], [1, 1]]))
figures[4].make(([[0, 2], [0, 1], [1, 0], [1, 1]]))
figures[5].make([[0, 0], [0, 1], [1, 1], [1, 0]])
figures[6].make(([[0, 0], [0, 1], [0, 2], [-1, 2]]))
log = open('log.txt' , 'w')
color = {}
color[figures[0]] = 'light_yellow'
color[figures[1]] = 'purpur'
color[figures[2]] = 'dark_blue'
color[figures[3]] = 'light_blue'
color[figures[4]] = 'green'
color[figures[5]] = 'red'
color[figures[6]] = 'yellow'
scores = [1000, 3000, 6000, 10000, 15000, 21000, 28000]
killed = [10, 30, 50, 80, 120, 160, 200]
#Amounts = 
T = 40

dir_map = {'right': 0, 'left': 1, 'down': 2, 'up': 3}
#         R   L   D   U
dx_map = [0,  0, -1,  1]
dy_map = [1, -1,  0,  0]
class Screen:
    def __init__(self, amount = 1):
        self.screen = [[' '] * ( wight) for i in range(height)]
        self.active = False
        self.is_hard = False
        if amount >= 2:
            if amount > 2:
                self.is_hard = True
            self.active = True
            self.curr2 = figure()
            self.curr_color2 = 0
            self.level2 = 0
            self.killed2 = 0
            self.scores2 = 0
            self.screen2 = [[' '] * wight for i in range(height)]
            self.delete2 = []
        self.scores = 0
        self.level = 0
        self.killed = 0
        self.curr = figure()
        self.curr_color = 0
        self.delete = []
    def new(self, screen = 1):
        new_figure = (figures[randrange(0, 7)])
        self.screen[-invisible][wight // 2] = ('#', color[new_figure])
        self.curr_color = color[new_figure]
#        print("NEW")
        for i in range(len(new_figure.coords)):
            x = height - invisible + new_figure.coords[i][0]
            y = wight // 2 + new_figure.coords[i][1]
            self.screen[x][y] = ('#', self.curr_color)
            self.curr.append([x, y])
     
    def move(self, direction, screen = 1):
        if screen == 2:
            self.swap()
        dir_idx = dir_map[direction]
        dx = dx_map[dir_idx]
        dy = dy_map[dir_idx]
        for i in range(len(self.curr.coords)):
            x, y = self.curr.coords[i]
            if x + dx < 0 or x + dx >= height or y + dy < 0 or y + dy >= wight or (self.screen[x + dx][y + dy] != ' '\
                                             and [x + dx, y + dy] not in self.curr.coords):
                if direction == 'down':
                    self.curr.clear()
                    if screen == 2:
                        self.swap()
                    
                    return True
                if screen == 2:
                    self.swap()
                return False

        for i in range(len(self.curr.coords)):
            x, y = self.curr.coords[i]
            self.screen[x][y] = ' '
            self.curr.coords[i][0] += dx
            self.curr.coords[i][1] += dy
        for i in range(len(self.curr.coords)):      
            x, y = self.curr.coords[i]
            self.screen[x][y] = ('#', self.curr_color)
        if screen == 2:
            self.swap()
        return True

    def rotate(self, arg, screen = 1):
        #arg = {left, right}
        #a = sum(x) in current figure
        #b = sum(x) in new figure
        #c = sum(y) in current figure
        #d = sum(y) in new figure
        if screen == 2:
            self.swap()
        new_figure = figure()
        new_figure.coords = self.curr.coords
        a, b, c, d = 0, 0, 0, 0
        #a, b, c, d = eval("new_figure." + arg + '()')
        a, b, c, d = getattr(new_figure, arg)() 

        while a < b:
            new_figure.move('up')
            b -= 4
        while a > b:
            new_figure.move('down')
            a -= 4
        while c < d:
            new_figure.move('left')
            d -= 4
        while c > d:
            new_figure.move('right')
            c -= 4

        for i in range(len(new_figure.coords)):
            x, y = new_figure.coords[i]
            if x >= height or x < 0 or y >= wight or y < 0 or (self.screen[x][y] != ' ' and [x, y] not in self.curr.coords):
                del new_figure
                if screen == 2:
                    self.swap()
#                print(1, end = '')
                return False
        for i in range(len(new_figure.coords)):
            self.screen[self.curr.coords[i][0]][self.curr.coords[i][1]] = ' '
        for i in range(len(new_figure.coords)):
            self.screen[new_figure.coords[i][0]][new_figure.coords[i][1]] = ('#', self.curr_color)
        del self.curr
        self.curr = new_figure
        if screen == 2:
            self.swap()
        return True

    def swap(self):
        
        self.curr2, self.curr = self.curr, self.curr2
        self.curr_color2, self.curr_color = self.curr_color, self.curr_color2
        self.level2, self.level = self.level, self.level2
        self.killed2, self.killed = self.killed, self.killed2
        self.scores2, self.scores = self.scores, self.scores2
        self.screen2, self.screen = self.screen, self.screen2
        self.delete, self.delete2 = self.delete2, self.delete

    def turn(self, arg, screen = 1):

        if screen == 2:
            self.swap()
        if self.is_hard and random() < 0.01:
            self.swap()
        if self.curr.empty():

#Make new figure
            for i in range(wight):
                if self.screen[-invisible + 1][i] != ' ':
                    print("Game Over")
                    if screen == 2:
                        self.swap()
                    return False
# Remove filled lines
            for i in range(height): 
                F = True
                for j in range(wight):
                    if self.screen[i][j] == ' ':
                        F = False
#                        if i == 0:
#                            print(i, j, file=log)
#                if i == 0:
#                    print(i, F, file=log)

#                log.flush()
                if F:
                     for j in range(wight):
                        self.screen[i][j] = ('@', 'dark_blue')
                     self.delete.append(i)
            self.new(screen) 
            if screen == 2:
                self.swap()
            return True
        else:
            if arg[0] == 't':

                if screen == 2:
                    self.swap()
                return self.rotate(arg, screen)
            else:

                if screen == 2:
                    self.swap()
                return self.move(arg, screen)


    def Print(self):
        to_write = []
        os.system("clear")
        for i in range(height - invisible - 1, -1, -1):
            for k in range(2):
                for j in range(wight):
                    to_write.append('|')
                    if self.screen[i][j] == ' ':
                        to_write.append(' ')
                        to_write.append(' ')

                    else:
                        to_write.append(colored.Print(self.screen[i][j]))
                        to_write.append(colored.Print(self.screen[i][j]))
                to_write.append(('|'))
            #sys.stdout.write(a)
                to_write.append('\\    /')
                if self.active:
                    for j in range(wight):
                        to_write.append('|')
                        if self.screen2[i][j] == ' ':
                            to_write.append(' ')
                            to_write.append(' ')

                        else:
                            to_write.append(colored.Print(self.screen2[i][j]))
                            to_write.append(colored.Print(self.screen2[i][j]))
                    to_write.append('|')    
                to_write.append(('\n'))
                to_write.append(('\r'))
        for i in range(3 * (wight) + 1):
            to_write.append(('%'))
        if self.active:
            to_write.append('      ' + '%' * (3 * wight + 1))
        to_write.append(('\n'))
        to_write.append(('\r'))
        to_write.append(('Level: ' + str(self.level).rjust(10, ' ')))
        if self.active:
            to_write.append('                   ')
            to_write.append('Level: ' + str(self.level2).rjust(10, ' '))
        to_write.append(('\n\r'))
        to_write.append('Scores:' + str(self.scores).rjust(10, ' '))  
        if self.active:
            to_write.append('                  ')
            to_write.append('Scores: ' + str(self.scores2).rjust(10, ' '))
        to_write.append('\n\r')
#        print(self.delete)
        if len(self.delete):
            i = 0
            j = 0
            down = 0
            ans = []
            for i in range(height - invisible):
                if j < len(self.delete) and i == self.delete[j]:
                    j += 1
                else:
                    ans.append(i)
            for i in range(len(ans)):
                if i != ans[i]:
                    self.screen[i] = deepcopy(self.screen[ans[i]])
            for i in range(len(ans), height - invisible):
                self.screen[i] = [' ' for i in range(wight)]
            self.scores += count(len(self.delete))
            self.killed += len(self.delete)
            if self.scores >= scores[self.level] and self.killed >= killed[self.level]:
                global T
                self.level += 1
                T -= 8
                T = max(T, 16 - self.level)

            self.delete = []
        if self.active and len(self.delete2):
            self.swap()
            i = 0
            j = 0
            down = 0
            ans = []
            for i in range(height - invisible):
                if j < len(self.delete) and i == self.delete[j]:
                    j += 1
                else:
                    ans.append(i)
            for i in range(len(ans)):
                if i != ans[i]:
                    self.screen[i] = deepcopy(self.screen[ans[i]])
            for i in range(len(ans), height - invisible):
                self.screen[i] = [' ' for i in range(wight)]
            self.scores += count(len(self.delete))
            self.killed += len(self.delete)
            if self.scores >= scores[self.level] and self.killed >= killed[self.level]:
                global T
                self.level += 1
                T -= 8
                T = max(T, 16 - self.level)

            self.delete = []
            self.swap()
        sys.stdout.write(''.join(to_write))

            

def count(amount):
    return int((179 * 80 / T * amount * (amount + 1) / 2) ** (3 / 4))
   
#    return Amounts[amount - 1]

def input_function():  
    for i in range(179179179):
        global command
        command = (sys.stdin.read(1))
        curses.flushinp()
    
"""
print(count(1))
print(count(2))
print(count(3))
print(count(4))
"""
amount_of_screens = 2

INPUT = threading.Thread(target = input_function, daemon=True)
INPUT.start()
A = Screen(amount_of_screens)
clock()
t = 0
t_start = time()
p = True
command = ''
print('press "Enter" to start')
print('\b' * 179)
#a = sys.stdin.read(1)
##curses.flushinp()
A.Print()
Input = False
#curses.ungetch('/')
while p:
#    print(1)
    for i in range(T):
#        sleep(0.01)
        INPUT.join(0.01)

#INPUT. 
#        command = choice(['a', 'd', 's', '/', ' '])
#        print(command)
        if command == 'a':
            Input = True
            screen = 1
            command = 'left'
        elif command == 'd':
            Input = True
            command = 'right'
            screen = 1
        elif command == ' ':
            Input = True
            screen = 1
            command = 'turn_left'
        elif command == 's':
            Input = True
            command = 'down'
            screen = 1
        elif command == 'w':
            Input = True
            screen = 1
            command = 'turn_right'
        elif command == 'p':
            os.system('clear')
            sys.stdout.write('\r')
            a = sys.stdin.read(1)
            curses.flushinp()
            A.Print()
        elif command == ',':
            screen = 2
            command = 'left'
            Input = True
        elif command == '.':
            screen = 2
            command = 'down'
            Input = True
        elif command == "/":
            screen = 2
            command = 'right'
            Input = True
        elif command == ';':
            screen = 2
            command = 'turn_right'
            Input = True
        else:
            command = '\\'
        if Input:
            p = A.turn(command, screen)
            if p:
                A.Print()
            Input = False
        command = '\\'
    
    A.Print()
    p = A.turn('down', 1)
    if (amount_of_screens == 2):
        p = A.turn('down', 2)
    command = ''
    (A.Print())
    if not p:
        print("Game Over")
        print('\r')

        t = time() - t_start
        print("Your time is", t)
        print('\r')
        print('Type nothing to exit')
        print('\r')
        INPUT.join(3)
        #a = sys.stdin.readline().rstrip()
        #while a != "q":
        #    a = sys.stdin.readline().rstrip()
        
#        INPUT.join()
        if command:
            t_start = time()
            p = True
            del A
            A = Screen(amount_of_screens)
#        else:
#            INPUT.

os.system("clear")
del monitor
curses.endwin()
