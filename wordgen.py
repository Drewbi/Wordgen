import sys
import termios
import contextlib
import os.path
import random

wordarray = {}

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

def open_file(filename):
    if os.path.isfile(filename):
        infile = open(filename, 'r', encoding='utf-8')
        return infile
    else:
        print()
        raise SystemExit("Cannot locate file {0}\nExiting...".format(filename))

def loadwords():
    for i in range(26):
        wordarray[chr(i+97)] = []
    file = "words.txt"
    f = open_file(file)
    for word in f:
        if(ord(word[0].lower()) > 96 and ord(word[0].lower()) < 123):
            wordarray[word[0].lower()].append(word.strip())
    #print(wordarray)

def choose_word(ch):
    length = len(wordarray[ch])
    return wordarray[ch][int(length*random.random())]

def main():
    print ('exit with ^C or ^D')
    loadwords()
    with raw_mode(sys.stdin):
        try:
            while True:
                ch = sys.stdin.read(1).lower()
                if not ch or ch == chr(4):
                    break
                if ord(ch) > 96 and ord(ch) < 123:
                    print(choose_word(ch).capitalize(), end=" ")
                    sys.stdout.flush()
        except (KeyboardInterrupt, EOFError):
            pass


if __name__ == '__main__':
    main()
