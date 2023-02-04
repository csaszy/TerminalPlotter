import os
import math

#--------------------------------|Merge Sort|--------------------------------
def Merge(a,b,m,n,aIndex,bIndex):
    c = []
    indexes = []
    i,j = 0,0
    while i <= m-1 and j <= n-1:
        if a[i] < b[j]:
            c.append(a[i])
            indexes.append(aIndex[i])
            i += 1
        else:
            c.append(b[j])
            indexes.append(bIndex[j])
            j += 1
    for _ in range(i,m):
        c.append(a[i])
        indexes.append(aIndex[i])
        i += 1
    for _ in range(j,n):
        c.append(b[j])
        indexes.append(bIndex[j])
        j += 1
    return c, indexes

def MergeSort(d,indexes):
    if 0 < len(d)-1:
        mid = (0 + len(d)-1)//2
        a,aInd = MergeSort(d[0:mid+1],indexes[0:mid+1])
        b,bInd = MergeSort(d[mid+1:len(d)],indexes[mid+1:len(d)])
        return Merge(a,b,len(a),len(b),aInd,bInd)
    return d,indexes
#--------------------------------|Binary Search|--------------------------------
def BinarySeacrh(a,n,key):
    l,h = 0,n-1
    while l <= h:
        mid = (l+h)//2
        if key == a[mid]:
            return mid
        if key < a[mid]:
            h = mid-1
        else:
            l = mid+1
    return None

#--------------------------------|Plotter class|--------------------------------
class Plotter:
    def __init__(self,sizex,sizey) -> None:
        self.sizex = sizex
        self.sizey = sizey 
        self.mtx = [[0]*sizex for _ in range(sizey)]
        self.scopex = [0,sizex-1]
        self.scopey = [0,sizey-1]

    def DataIn(self,x:list,y:list):
        self.x = x
        self.y = y
        self.sortedY,self.sortedYIndex = MergeSort(self.y,[i for i in range(len(y))])
        self.sortedX,self.sortedXIndex = MergeSort(self.x,[i for i in range(len(x))])

    def CheckNeighbours(self,where,searchlist):
        out = [where]
        i = -1
        try:
            while searchlist[where + i] == searchlist[where] and where + i not in out and where + i >= 0:
                out.append(where+i)
                i -= 1
        except:pass
        i = 1
        try:
            while searchlist[where + i] == searchlist[where] and where + i not in out and where + i <= len(searchlist):
                out.append(where+i)
                i += 1
        except: pass
        return out

    def plot(self):
        #calculating visible points
        yInScope = []
        xInScope = []
        for n in range(self.scopey[0],self.scopey[1]+1):
            indexInSortedY = BinarySeacrh(self.sortedY,len(self.sortedY),n)
            if not indexInSortedY is None:
                matches = self.CheckNeighbours(indexInSortedY,self.sortedY)
                for match in matches:
                    yInScope.append(self.sortedYIndex[match])     #returns the indexes of the y values that are found in scope
        
        for n in range(self.scopex[0],self.scopex[1]+1):
            indexInSortedX = BinarySeacrh(self.sortedX,len(self.sortedX),n)
            if not indexInSortedX is None:
                matches = self.CheckNeighbours(indexInSortedX,self.sortedX)
                for match in matches:
                    xInScope.append(self.sortedXIndex[match])     #returns the indexes of the y values that are found in scope

        #print(self.scopex,self.scopey,xInScope,yInScope)    
        
        visiblePoints = []      #'points that are in scope'
        for i in xInScope:
            if i in yInScope:
                visiblePoints.append([self.x[i],self.y[i]])
        
        #settting up matrix
        for i,row in enumerate(self.mtx):
            for j,el in enumerate(row):
                if el:
                    self.mtx[i][j] = 0

        for point in visiblePoints:
            print(point)
            pOnMtxY = self.scopey[1]-point[1]
            pOnMtxX = point[0]-self.scopex[0]
            #try:
            self.mtx[pOnMtxY][pOnMtxX] = 1
            #except: pass

        self.printMtx()

    def printMtx(self):
        #os.system('cls')
        print()

        #y notation
        yNotation = []
        yNotationf = 5
        yMaxNotLength = 0
        for i in range(self.scopey[0],self.scopey[1]+1):
            if len(str(i)) > yMaxNotLength:
                yMaxNotLength = len(str(i))
        for i in range(self.sizey):
            if (self.scopey[1]-i) % int(math.ceil(self.sizey / yNotationf)) == 0:
                yNotation.append(f'{" "*(yMaxNotLength-len(str(self.scopey[1]-i)))}{self.scopey[1]-i}')
            else:
                yNotation.append(" "*yMaxNotLength)

        #x notation
        xNotationf = 5
        xMaxNotLength = 0
        for i in range(self.scopex[0],self.scopex[1]+1):
            if len(str(i)) > xMaxNotLength:
                xMaxNotLength = len(str(i))
        xNotation = [[" "]*self.sizex for _ in range(xMaxNotLength)]
        for i in range(self.sizex):
            if (self.scopex[0]+i) % int(math.ceil(self.sizex / xNotationf)) == 0:
                for h in range(len(str(self.scopex[0]+i))):
                    xNotation[h][i] = str(self.scopex[0]+i)[h]

        for i,row in enumerate(self.mtx):
            print(f'{yNotation[i]} | ',end=" ")
            for j,el in enumerate(row):
                if el:
                    print("#",end=" ")
                else:
                    print(".",end=" ")
            print()
        print(f'    {" "*yMaxNotLength}',end="")
        print(f'{"- "*self.sizex}')
        for i,row in enumerate(xNotation):
            print(f'    {" "*yMaxNotLength}',end="")
            for j,el in enumerate(row):
                print(el,end=' ')
            print()

    def Move(self,dir):
        print(self.scopex,self.scopey)
        match dir:
            case 'w':
                self.scopey[0] += 1
                self.scopey[1] += 1
            case 's':
                self.scopey[0] -= 1
                self.scopey[1] -= 1
            case 'a':
                self.scopex[0] += 1
                self.scopex[1] += 1
            case 'd':
                self.scopex[0] -= 1
                self.scopex[1] -= 1
        print(self.scopex,self.scopey)

if __name__ == "__main__":
    #datax = [0,0,1,2,3,4,5,6,7,8,9]
    #datay = [-1,0,-5,3,4,5,-6,2,-1,4,7]
    datax = [0,0,0,0,1,2,3,4]
    datay = [0,1,2,3,3,3,3,3]

    p = Plotter(10,8)
    p.DataIn(datax,datay)
    p.plot()
    while True:
        command = input(": ")
        p.Move(command)
        p.plot()
        