import numpy as np
import sys
import termios
import contextlib
from pprint import pprint
from gridworld import initGrid,makeMove,getReward,dispGrid

# state = initGrid()
# arr = dispGrid(state)
# pprint(arr)
# state = makeMove(state, 1)
# arr = dispGrid(state)
# pprint(arr)
# print(getReward(state))
# state = makeMove(state, 1)
# print('Reward: %s' % (getReward(state),))
# dispGrid(state)
#!/usr/bin/env python

@contextlib.contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)


def main():
    print 'exit with ^C or ^D'
    with raw_mode(sys.stdin):
        try:
            while True:
                ch = sys.stdin.read(1)
                if not ch or ch == chr(4):
                    break
                print '%02x' % ord(ch),
        except (KeyboardInterrupt, EOFError):
            pass


if __name__ == '__main__':
    main()
