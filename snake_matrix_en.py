import random
import numpy

"""Snake World matrix module
    The array contains data about the cells in the playing field: wall = 4, tail = 1, empty cell= 0, head = 7, apple= 2
   
    - generates an apple
    - calculates the sensor value
    - doing following move and analyzes its consequences
   """

class Mir:

    def __init__(self, size):
        self.size = size + 2
        self.arr = numpy.zeros((self.size, self.size), dtype=int)
        for k in range (0, self.size):
            self.arr[k,0], self.arr[k,self.size-1], self.arr[0,k], self.arr[self.size-1, k]= 4,4,4,4
        self.score = 0
        self.count_moves = 0
        self.count_all_moves = 0
        self.snake_sensors = []
        self.sens_lib = {}
        self.head =[]
        self.tail =[]
        self.life = True                # the snake is alive = True

    # apple generator
    def eat(self):
        self.count_moves = 0
        flag = True
        while flag:
            i = random.randint(0, self.size-1)
            j = random.randint(0, self.size-1)
            if self.arr[i, j] == 0:
                self.apple_pos = [i,j]
                self.arr[i, j] = 2
                flag = False

    # creating new game matrix
    def new(self):
        self.life = True
        self.score = 0
        self.count_all_moves = 0
        self.arr = numpy.zeros((self.size, self.size), dtype=int)
        for k in range (0, self.size):
            self.arr[k,0], self.arr[k,self.size-1], self.arr[0,k], self.arr[self.size-1, k]= 4,4,4,4
        self.arr[self.size//2-1, self.size//2] = 7
        self.arr[self.size//2, self.size//2] = 1

        self.tail = []
        self.tail.append([self.size//2-1, self.size//2])
        self.tail.append([self.size//2, self.size//2])
        self.eat()

    # next move function
    def move(self, way):

        new_i = self.tail[0][0]-way[0]+way[1]
        new_j = self.tail[0][1]-way[2]+way[3]

        self.count_moves += 1
        self.count_all_moves += 1

        if self.arr[new_i,new_j] == 4 or self.arr[new_i,new_j] ==1 :    # snake moved to the wall or tail
            self.life = False   # the snake died

        else:
            self.arr[new_i,new_j] = 7                           # new valid cell become the head
            self.arr[self.tail[0][0],self.tail[0][1]] = 1       # the head become the tail
            self.tail.insert(0,[new_i,new_j])

            if [new_i,new_j] == self.apple_pos:                 # snake eat the apple
                self.score += 1
                self.eat()
            else:
                self.arr[self.tail[-1][0],self.tail[-1][1]] = 0     # the last tail cell become empty
                self.tail.pop()

            self.sensors()

        return self.life

    # calculating the sensors data
    def sensors(self):
        """Coordinates [i,j] - i- vertical, j- horizontal, [0,0] - upper left cell:
         Snake sensors:
         1. Straight distance to the walls - 4 pcs.
         2. Straight distance to the apple - 4 pcs.
         3. Straight distance to the tail - 4 pcs.
         4. Sector where the apple is: below/above/left/right - 4 pieces, values 0/1
         5. Diagonal distance to walls, food, tail - 12 pcs.
         6. Distance from the head to the apple, calculation using the hypotenuse """

        i, j = self.tail[0][0], self.tail[0][1]      # Head coordinates
        i_apl = self.apple_pos[0]                    # Apple coordinates
        j_apl = self.apple_pos[1]

        """ 1. Sensors head-wall"""
        sens_up, sens_down, sens_left,sens_right = 0,0,0,0
        """ 2,3. Sensors head-apple, head-tail """
        sens_apl_up, sens_apl_down, sens_apl_left, sens_apl_right = 0,0,0,0
        sens_tail_up, sens_tail_down, sens_tail_left, sens_tail_right = 0,0,0,0

        k = 1
        for iter_i in range (i, 0, -1):
            if self.arr[iter_i-1,j] == 2:
                sens_apl_up = k
                break
            if self.arr[iter_i-1,j] == 1:
                sens_tail_up = k
                break
            if self.arr[iter_i-1,j] == 4:
                sens_up = k
                break
            k = k + 1

        k = 1
        for iter_i in range (i, self.size-1):
            if self.arr[iter_i+1,j] == 2:
                sens_apl_down = k
                break
            if self.arr[iter_i+1,j] == 1:
                sens_tail_down = k
                break
            if self.arr[iter_i+1,j] == 4:
                sens_down = k
                break
            k = k+1

        k = 1
        for iter_j in range (j, 0, -1):
            if self.arr[i, iter_j-1] == 2:
                sens_apl_left = k
                break
            if self.arr[i, iter_j-1] == 1:
                sens_tail_left = k
                break
            if self.arr[i, iter_j-1] == 4:
                sens_left = k
                break
            k = k+1

        k = 1
        for iter_j in range (j, self.size-1):
            if self.arr[i, iter_j+1] == 2:
                sens_apl_right = k
                break
            if self.arr[i, iter_j+1] == 1:
                sens_tail_right = k
                break
            if self.arr[i, iter_j+1] == 4:
                sens_right = k
                break
            k = k+1

        """ 4. Sensors: sector with apple """
        sens_sekt_up, sens_sekt_down, sens_sekt_left, sens_sekt_right = 0,0,0,0
        if i_apl < i : sens_sekt_up = 1
        if i_apl > i : sens_sekt_down = 1
        if j_apl < j : sens_sekt_left = 1
        if j_apl > j : sens_sekt_right = 1

        """ 5. Shortest distance from head to apple, 4 sensors """
        sens_apl_up_left, sens_apl_up_right, sens_apl_down_left, sens_apl_down_right = 0,0,0,0
        if i_apl < i and j_apl < j :  sens_apl_up_left = ((i-i_apl)**2 + (j - j_apl)**2 ) ** (0.5)
        if i_apl > i and j_apl < j :  sens_apl_down_left = ((i-i_apl)**2 + (j - j_apl)**2 ) ** (0.5)
        if i_apl < i and j_apl > j :  sens_apl_up_right = ((i-i_apl)**2 + (j - j_apl)**2 ) ** (0.5)
        if i_apl > i and j_apl > j :  sens_apl_down_right = ((i-i_apl)**2 + (j - j_apl)**2 ) ** (0.5)

        """ 6. Diagonal distance sensors from head to objects """
        sens_45_up_left, sens_45_up_right, sens_45_down_left, sens_45_down_right = 0,0,0,0
        sens_45_apl_up_left, sens_45_apl_up_right, sens_45_apl_down_left, sens_45_apl_down_right = 0,0,0,0
        sens_45_tail_up_left, sens_45_tail_up_right, sens_45_tail_down_left, sens_45_tail_down_right = 0,0,0,0


        for iter in range(1, self.size+1):
            if self.arr[i-iter, j-iter] == 2:
                sens_45_apl_up_left = iter
                break
            if self.arr[i-iter, j-iter] == 1:
                sens_45_tail_up_left = iter
                break
            if self.arr[i-iter, j-iter] == 4:
                sens_45_up_left = iter
                break

        for iter in range(1, self.size + 1):
            if self.arr[i + iter, j - iter] == 2:
                sens_45_apl_down_left = iter
                break
            if self.arr[i + iter, j - iter] == 1:
                sens_45_tail_down_left = iter
                break
            if self.arr[i + iter, j - iter] == 4:
                sens_45_down_left = iter
                break

        for iter in range(1, self.size + 1):
            if self.arr[i-iter, j+iter] == 2:
                sens_45_apl_up_right = iter
                break
            if self.arr[i-iter, j+iter] == 1:
                sens_45_tail_up_right = iter
                break
            if self.arr[i-iter, j+iter] == 4:
                sens_45_up_right = iter
                break

        for iter in range(1, self.size + 1):
            if self.arr[i+iter, j+iter] == 2:
                sens_45_apl_down_right = iter
                break
            if self.arr[i+iter, j+iter] == 1:
                sens_45_tail_down_right = iter
                break
            if self.arr[i+iter, j+iter] == 4:
                sens_45_down_right = iter
                break


        sens = [['wall ↑' , sens_up], ['wall ↓' , sens_down], ['wall ←' , sens_left], ['wall →' , sens_right]]
        sens_apl = [['appla ↑' , sens_apl_up], ['appla ↓' , sens_apl_down], ['appla ←' , sens_apl_left], ['appla →' , sens_apl_right]]
        sens_apl_sq = [['appla ↑ ←' , sens_apl_up_left], ['appla ↑ →' , sens_apl_up_right], ['appla ↓ ←' , sens_apl_down_left], ['appla ↓ →' , sens_apl_down_right]]
        sens_tail = [['tail ↑' , sens_tail_up], ['tail ↓' , sens_tail_down], ['tail ←' , sens_tail_left], ['tail →' , sens_tail_right]]
        sens_sekt = [['sector ↑' , sens_sekt_up], ['sector ↓' , sens_sekt_down], ['sector ←' , sens_sekt_left], ['sector →' , sens_sekt_right]]
        sens_45 = [['w45 ↑ ←', sens_45_up_left] ,['w45 ↑ →', sens_45_up_right],['w45 ↓ ←', sens_45_down_left],['w45 ↓ →', sens_45_down_right]]
        sens_45_apl = [['a45 ↑ ←', sens_45_apl_up_left] ,['a45 ↑ →', sens_45_apl_up_right],['a45 ↓ ←', sens_45_apl_down_left],['a45 ↓ →', sens_45_apl_down_right]]
        sens_45_tail = [['t45 ↑ ←', sens_45_tail_up_left] ,['t45 ↑ →', sens_45_tail_up_right],['t45 ↓ ←', sens_45_tail_down_left],['t45 ↓ →', sens_45_tail_down_right]]



        lib = {'sens':sens, 'sens_apl':sens_apl, 'sens_apl_sq':sens_apl_sq,
                    'sens_tail':sens_tail, 'sens_sekt':sens_sekt, 'sens_45':sens_45,
                    'sens_45_apl':sens_45_apl, 'sens_45_tail':sens_45_tail}

        """Normalization for sensors values"""
        def norm_sens(lib):
            for i in range(0,4):
                if lib['sens'][i][1] !=0 : lib['sens'][i][1] = 1 / (lib['sens'][i][1])
                if lib['sens_apl'][i][1] !=0 : lib['sens_apl'][i][1] = 1 / (lib['sens_apl'][i][1])
                if lib['sens_45'][i][1] !=0 : lib['sens_45'][i][1] = 1 / (lib['sens_45'][i][1])
                if lib['sens_45_apl'][i][1] !=0 : lib['sens_45_apl'][i][1] = 1 / (lib['sens_45_apl'][i][1])
                if lib['sens_45_tail'][i][1] !=0 : lib['sens_45_tail'][i][1] = 1 / (lib['sens_45_tail'][i][1])
                if lib['sens_tail'][i][1] !=0 : lib['sens_tail'][i][1] = 1 / (lib['sens_tail'][i][1])
                if lib['sens_apl_sq'][i][1] !=0 : lib['sens_apl_sq'][i][1] = 1 / (lib['sens_apl_sq'][i][1])

            return lib

        self.sens_lib = norm_sens(lib)
        self.snake_sensors = []
        for s in self.sens_lib:
            for i in range (0,4):
                self.snake_sensors.append(self.sens_lib[s][i][1])

        return self.sens_lib
