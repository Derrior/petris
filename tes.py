import curses
import sys
import os
from time import sleep

curses.initscr()
'''
for i in range(22):

    a = (sys.stdin.read(1))
    curses.flushinp()
    sys.stdout.write(str((ord(a))) + '\n' + '\b\b\b\b\b\b')
    sys.stdout.write('\n\n\n\n\n\n\n')
    sys.stdout.flush()
'''

while True:
    curses.beep()
    sleep(0.2) 
    curses.beep()
    sleep(1.2)
    curses.beep()
    sleep(0.2)
    curses.beep()
    sleep(1.2)
    curses.beep()
    sleep(0.2)
    curses.beep()
    sleep(1.2)
