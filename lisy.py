#!/usr/bin/python
# coding: utf-8

import numpy as np
from random import randint, random, choice
from display import Display

class Harefox(object):
    
    def __init__(self, size, ids, colors, params):
        self.size = size
        self.ids = ids
        self.params = params
        self.__generateMap()
        self.display = Display(self.map, sorted(self.ids.values()), colors, self.updateMap)

    def __generateMap(self):
        self.map = np.zeros(size, dtype = np.int8)
        self.foxes = randint(0.5*self.size[0], self.size[0])
        self.hares = randint(self.size[0]*5, 6*self.size[0])
        self.__placeAnimals(self.foxes, self.ids['fox'])
        self.__placeAnimals(self.hares, self.ids['hare'])

    def __placeAnimals(self, startNr, animal):
        for i in xrange(startNr): # for number of animals
            i = size[0] * size[1]
            while i: # searching for a place for a new animal
                pos = (randint(0, size[0]-1), randint(0, size[1]-1))
                if self.map[pos] == self.ids['grass']:
                    break
                i -= 1
            self.map[pos] = animal

    def __searchAdjacent(self, obj, pos, dis):
        ''' returns list of found objects in the desired area '''
        fields = []
        for x in xrange(pos[0] - dis, pos[0] + dis + 1):
            for y in xrange(pos[1] - dis, pos[1] + dis + 1):
                x %= self.size[0]
                y %= self.size[1]
                if self.map[x, y] == obj:
                    fields.append((x, y)) 
        return fields

    def __move(self, pos):
        dis = 2 if random() <= self.params['2sqChance'] else 1
        emptyFields = self.__searchAdjacent(self.ids['grass'], pos, dis)
        newPos = pos
        try:
            newPos = choice(emptyFields)
            #teleportation of the animal
            self.map[newPos] = self.map[pos]
            self.map[pos] = self.ids['grass']
        except:
            pass

        return newPos

    def updateMap(self):
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                
                if self.map[x, y] == self.ids['fox']:
                    newPos = self.__move((x, y))
                    #Eating
                    snacks = self.__searchAdjacent(self.ids['hare'], newPos, 2)
                    try:
                        snackPos = choice(snacks)
                        self.map[snackPos] = self.ids['grass']
                        if random() <= self.params['foxSpawnChance']:
                            #Spawning
                            kindergarden = self.__searchAdjacent(self.ids['grass'], newPos, 1)
                            try:
                                newPos = choice(kindergarden)
                                self.map[newPos] = self.ids['fox']
                            except:
                                pass
                    except IndexError, e:
                        if random() <= self.params['dieChance']:
                            #Die hard!
                            self.map[newPos] = self.ids['grass']

                elif self.map[x, y] == self.ids['hare']:
                    self.__move((x, y))
                    if random() <= self.params['hareSpawnChance']:
                        #Spawning
                        kindergarden = self.__searchAdjacent(self.ids['grass'], (x, y), 1)
                        try:
                            newPos = choice(kindergarden)
                            self.map[newPos] = self.ids['hare']
                        except:
                            pass
        return self.map


if __name__ == '__main__':
    size = (50, 50)
    ids = { 'grass': 0,
            'fox':   1,
            'hare':  2
    }
    colors = ['green', 'red', 'white']
    params = { 'dieChance':         0.5,
               'hareSpawnChance':   0.1,
               'foxSpawnChance':    0.2,
               '2sqChance':         0.3,
               'turns':             5000
    }
    sim = Harefox(size, ids, colors, params)
    