import random, colorsys, sys, time
from Tkinter import *
class Game:
        def __init__(self, size):
                if size > 12 or size < 2:
                        print "Size out of range: closing.",
                        time.sleep(1)
                        print ".",
                        time.sleep(1)
                        print ".",
                        time.sleep(1)
                        print "."
                        sys.exit(0)
                self.size = size
                self.grid = [[Tile() for i in range(size)] for j in range(size)]
                self.addRandomTile()
                self.addRandomTile()
        
        def __str__(self):
                ret = ''
                iS = {}
                for j in self.grid:
                        for i in range(len(j)):
                                iS[i] = max(iS.get(i), len(str(j[i])))
                for j in self.grid:
                        for i in range(len(j)):
                                ret = ret + str(j[i]) + ' ' + ' '*(iS[i]-len(str(j[i])))
                        ret = ret + '\n'
                return ret.replace(' 0', '  ').replace('0 ', '  ')
                return '\n'.join([' '.join([str(i) for i in j]) for j in self.grid]).replace(' 0', '  ').replace('0 ', '  ')

        def addRandomTile(self):
                availableTiles = self.getAvailableTiles()
                findTiles = self.findTile(random.choice(availableTiles))
                self.grid[findTiles[0]][findTiles[1]] = Tile(2)
        
        def getAvailableTiles(self):
                tiles = []
                for i in self.grid:
                        for j in i:
                                if j.value == 0:
                                        tiles.append(j)
                                                
                return tiles
                                 
        def findTile(self, tile):
                for i in range(len(self.grid)):
                        for j in range(len(self.grid[i])):
                                if self.grid[i][j] == tile:
                                        return i,j
           
        def move(self, direction):
                merged = []
                moved = False
                lines = rotate(self.grid, direction+1)
                for line in lines:
                        while len(line) and line[-1].value == 0:
                                line.pop(-1)
                        i = len(line) - 1
                        while i >= 0:
                                if line[i].value == 0:
                                        moved = True
                                        line.pop(i)
                                i -= 1
                        i = 0
                        while i < len(line)-1:
                                if line[i].value == line[i+1].value and not (line[i] in merged or line[i+1] in merged):
                                        moved = True
                                        line[i] = Tile(line[i].value*2)
                                        line.pop(i+1)
                                        merged.append(line[i])
                                else:
                                        i+=1
                                        
                        while len(line) < len(self.grid):
                                line.append(Tile())
                for line in lines:
                        if not len(lines):
                                line = [Tile() for i in self.grid]


                self.grid = rotate(lines, 0-(direction + 1))
                if moved:
                        self.addRandomTile()
                        

                
                

        def lost(self):
                result = True
                length = len(self.grid) - 1
                for i in range(len(self.grid)):
                        for j in range(len(self.grid[i])):
                                val = self.grid[i][j].value
                                if val == 0:
                                        result = False

                                if i > 0 and self.grid[i-1][j].value == val:
                                        result = False
                                if j > 0 and self.grid[i][j-1].value == val:
                                        result = False
                                if i < length and self.grid[i+1][j].value == val:
                                        result = False
                                if j < length and self.grid[i][j+1].value == val:
                                        result = False
                return result

        def makeCopy(self, grid):
                
                for i in range(len(self.grid)):
                        for j in range(len(self.grid[i])):
                                grid[i][j] = self.grid[i][j]
                
                
                                
        def automate(self):
                temp = 0
                maxRatio = 0
                direction = 0
                moveTest = [[None for i in j] for j in self.grid]
                self.makeCopy(moveTest)
                for i in range(0,4):
                        
                        self.makeCopy(moveTest)
                        temp = testMove(moveTest, i)
                        if temp > maxRatio:
                                maxRatio = temp
                                direction = i
                
                self.move(direction)
                        
                        

        def getValues(self):
                result = []
                for i in self.grid:
                        for j in i:
                                result.append(j)
                return result
        
def testMove(grid, direction):
                merged = []
                moved = False
                lines = rotate(grid, direction+1)
                for line in lines:
                        while len(line) and line[-1].value == 0:
                                line.pop(-1)
                        i = len(line) - 1
                        while i >= 0:
                                if line[i].value == 0:
                                        moved = True
                                        line.pop(i)
                                i -= 1
                        i = 0
                        while i < len(line)-1:
                                if line[i].value == line[i+1].value and not (line[i] in merged or line[i+1] in merged):
                                        moved = True
                                        line[i] = Tile(line[i].value*2)
                                        line.pop(i+1)
                                        merged.append(line[i])
                                else:
                                        i+=1
                                        
                        while len(line) < len(grid):
                                line.append(Tile())
                for line in lines:
                        if not len(lines):
                                line = [Tile() for i in grid]


                grid = rotate(lines, 0-(direction + 1))
                if moved:
                        return calculateRatio(grid)
                else:
                        return 0
           

def calculateRatio(grid):
        count = 1
        total = 2
        for i in grid:
                for j in i:
                        if j.value > 0:
                                count += 1
                                total += j.value
        return total/count
def equal(grid1, grid2):
        for i in range(len(grid1)):
                for j in range(len(grid1[i])):
                        if not grid1[i][j].value == grid2[i][j].value:
                                return False
        return True



        
                                
        
def onKeyPress(event):
        global g
        global b

        for i in b:
                for j in i:
                        j.destroy()
        if event.keycode == 37:
                g.move(3)
                
        elif event.keycode == 38:
                g.move(2)
               
        elif event.keycode == 39:
                g.move(1)
                
        elif event.keycode == 40:
                g.move(0)
                
        elif event.keycode == 32:
                g.automate()
                
        makeButtons(g)
                
                
                

        if g.lost():
                for i in range(len(b)):
                        for j in range(len(b[i])):
                                if b[i][j].config('text')[-1] != str(g.grid[i][j]):
                                                b[i][j].destroy()
                                                b[i][j] = None
                try:
                        g.q.destroy()
                except Exception as e:
                        pass
                g.q = Button(root, text="You Lost")
                g.q.pack()

def makeButtons(g):
        global b
        for i in range(len(g.grid)):
                for j in range(len(g.grid[i])):
                        if g.grid[i][j].value:
                                b[i][j] = Button(root, text=str(g.grid[i][j].value), bg=findColors(g.grid[i][j].value)[0], fg=findColors(g.grid[i][j].value)[1])
                        else:
                                b[i][j] = Button(root, text='')
                        
                        b[i][j].config(width=100/g.size, height=45/g.size)
                        
                        b[i][j].grid(row=i, column=j)
                                
def findColors(num):
        if (num != 0 and ((num & (num - 1)) == 0)):
                bi = bin(num)
                po = len(bi)
                hue = 30.0 * po
                rgb = colorsys.hls_to_rgb(hue/256.0, 0.5, 0.5)
                rgb = [str(hex(int(256*x)))[2:3] for x in rgb]
                return "#" + str(rgb[0]) + str(rgb[1]) + str(rgb[2]), "#FFFFFF"
        else:
                return "#000000", "#FFFFFF"                        

def rotate(grid, num):
        grid2 = []
        s = len(grid)-1
        num = num%4
        if num == 0: #right
                grid2 = grid
                
        elif num == 1: #down
                grid2 = [[None for i in j] for j in grid]
                for y in range(len(grid)):
                         for x in range(len(grid[y])):
                                 grid2[x][s-y] = grid[y][x]
        elif num == 2: #left
                grid2 = grid
                grid2.reverse()
                for i in grid:
                         i.reverse()
        elif num == 3:
                grid2 = [[None for i in j] for j in grid]
                for y in range(len(grid)):
                         for x in range(len(grid[y])):

                                 grid2[y][x] = grid[x][s-y]



        return grid2
                
                
class Tile:
        def __init__(self, value=0):
                self.value = value
                 
        def __str__(self):
                return str(self.value)       

g = Game(5)

b = [[None for i in j] for j in g.grid]

root = Tk()
root.bind('<KeyPress>', onKeyPress)

makeButtons(g)

root.mainloop()


