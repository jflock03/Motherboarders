import sys

class slang(object):
    def __init__(self):
        self.dictionary = {}

    def load(self):
        try:
            file = open('slang.txt', 'r')
        except:
            print('slang file not found.')
            sys.exit(0)
        for line in file:
            line = line.strip()
            pair = line.split(';')
            self.dictionary[pair[0]] = pair[1]
        file.close()

    def get(self, abbr):
        if abbr in self.dictionary:
            return self.dictionary[abbr]
        else:
            return abbr
