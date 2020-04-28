from queue import PriorityQueue
from time import sleep
from .web_scraping import Definition
from words_project.settings import BASE_DIR
import os

#base class, not used in itself
class State(object):
    def __init__(self, value, parent, #for all instances, but first, where it doesn't have children to take these values from. If it is first object, use 0's from below
                 start = 0, goal = 0):

        self.children = [] #all next possible steps
        self.parent = parent
        self.value = value
        self.distance = 0

        #for existing parent- copy it's values
        if parent:
            self.start = parent.start
            self.goal = parent.goal
            self.path = parent.path[:]
            self.path.append(value)
        #if no parents- set starting values
        else:
            self.path   = [value]
            self.start  = start
            self.goal   = goal

    #definitions will be in sub-class
    def Getdistanceance(self):
        pass

    def MakeNewChild(self):
        pass

class State_String(State):
    def __init__(self,value,parent,
                 start = 0,
                 goal = 0):

        super(State_String, self).__init__(value, parent, start, goal)
        self.distance = self.Getdistanceance()

    #How far to the goal
    def Getdistanceance(self):
        if self.value == self.goal:
            return 0
        distance = 0
        for i in range(len(self.goal)):
            letter = self.goal[i]
            try:
                distance += abs(i - self.value.index(letter))
            except:
                distance += abs(i - self.value.find(letter))
        return distance

    #creates all possible steps
    def MakeNewChild(self):
        if not self.children:
            for i in range(len(self.goal)-1):
                val = self.value
                val = val[:i] + val[i+1] + val[i] + val[i+2:]
                child = State_String(val, self)
                self.children.append(child)

class AStar_Solver:
    def __init__(self, start , goal):
        self.path          = []
        self.visitedQueue  = []
        self.priorityQueue = PriorityQueue()
        self.start         = start
        self.goal          = goal

    def Solve(self):
        startState = State_String(self.start, 0, self.start, self.goal)
        count = 0
        self.priorityQueue.put((0,count,startState)) #add next state

        #look for the solution until it's not solved
        while(not self.path and self.priorityQueue.qsize()):
            closestChild = self.priorityQueue.get()[2]
            closestChild.MakeNewChild()
            self.visitedQueue.append(closestChild.value)

            for child in closestChild.children:
                if child.value not in self.visitedQueue:
                    count +=1
                    if not child.distance:
                        self.path = child.path
                        break
                    self.priorityQueue.put((child.distance,count,child))

        return self.path

route = os.path.join(BASE_DIR, 'matrix/static/sowpods.txt')
#Setting all the gears into movement. Going through all words in the dictionary(external)
def a_Loop(entry):
    entry = entry.upper() #Uppercasing all letters given by the user
    all_words = len(open(route).readlines()) #How many words is there in the dictionary
    options = []

    #Go through all the words in the dictionary...
    with open(route, 'r') as f:
        words = f.readlines() #importing dictionary into an array
        #...and going through each one
        for i in range(all_words):
            #Are the letters same in given entry and current word(i)?
            if sorted(words[i].strip()) == sorted(entry):
                #Are the entry letters making the word(same order?)
                if words[i].strip() == entry:
                    options.append(Definition(entry))
                #Main part of the program. Letters are the same, but they are not ordered. A* will find the shortest possible way to mutate our letters into whe word
                else:
                    a = AStar_Solver(entry, words[i].strip())
                    a.Solve()
                    for j in range(len(a.path)): #for all the versions(children) of the word before it becomes the final goal
                        #Set and display current state of the letters(soon to be a word)
                        # print(a.path[j])
                        if j == len(a.path)-1:  #Is it te last stage(word is complete). If so, wait for a little longer, save and display this word
                            options.append(Definition(a.path[j]))


                    entry = a.path[-1] #next word will be calculated from this state and not first entry given by the user
    return options
