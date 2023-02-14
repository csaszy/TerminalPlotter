import os
import math


#--------------------------------|Map Func|--------------------------------
def Map(input_start,input_end,output_start,output_end,input):
    return  output_start + ((output_end - output_start) / (input_end - input_start)) * (input - input_start)
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
        #self.scopex = [0,sizex-1]
        #self.scopey = [0,sizey-1]

    def DataIn(self,x:list,y:list):
        self.x = x
        self.y = y
        self.sortedY,self.sortedYIndex = MergeSort(self.y,[i for i in range(len(y))])
        self.sortedX,self.sortedXIndex = MergeSort(self.x,[i for i in range(len(x))])
        self.scopex = [self.sortedX[0],self.sortedX[-1]]
        self.scopey = [self.sortedY[0],self.sortedY[-1]]

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
            #print(point)
            #print(Map(self.scopex[0],self.scopex[1],0,self.sizex-1,point[0]),Map(self.scopey[0],self.scopey[1],0,self.sizey-1,point[1]),point)
            pOnMtxY = round(Map(self.scopey[1],self.scopey[0],0,self.sizey-1,point[1]))
            pOnMtxX = round(Map(self.scopex[0],self.scopex[1],0,self.sizex-1,point[0]))
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
        for i in range(self.sizey):
            if i % int(math.ceil(self.sizey / yNotationf)) == 0:
                yNotation.append(round(Map(0,self.sizey-1,self.scopey[1],self.scopey[0],i),2))
                if len(str(yNotation[-1])) > yMaxNotLength:
                    yMaxNotLength = len(str(yNotation[-1]))
            else:
                yNotation.append('x')
        for i,el in enumerate(yNotation):
            if el == 'x':
                yNotation[i] = " "*yMaxNotLength
            else:
                yNotation[i] = f'{" "*(yMaxNotLength-len(str(el)))}{str(el)}'
        
        #print(yNotation)

        #x notation
        xNotationf = 5
        xMaxNotLength = 0
        rawxNotation = []
        for i in range(self.sizex):
            if i % int(math.ceil(self.sizex / xNotationf)) == 0:
                rawxNotation.append(round(Map(0,self.sizex-1,self.scopex[0],self.scopex[1],i),2))
                if len(str(rawxNotation[-1])) > xMaxNotLength:
                    xMaxNotLength = len(str(rawxNotation[-1]))
            else:
                rawxNotation.append('x')
        xNotation = [[" "]*self.sizex for _ in range(xMaxNotLength)]
        for i,el in enumerate(rawxNotation):
            for h,d in enumerate(str(el)):
                if el == 'x':
                    xNotation[h][i] = " "
                else:
                    xNotation[h][i] = d

        #slieders
        ySlider = ["|"]*self.sizey
        startPoint = Map(self.sortedY[0],self.sortedY[-1],0,self.sizey,self.scopey[0])
        endPoint = Map(self.sortedY[0],self.sortedY[-1],0,self.sizey,self.scopey[1])
        for i in range(round(startPoint),round(endPoint)):
            if i >= 0:
                try:
                    ySlider[i] = "&"
                except: pass

        xSlider = ["-"]*self.sizex
        startPoint = Map(self.sortedX[0],self.sortedX[-1],0,self.sizex,self.scopex[0])
        endPoint = Map(self.sortedX[0],self.sortedX[-1],0,self.sizex,self.scopex[1])
        for i in range(round(startPoint),round(endPoint)):
            if i >= 0:
                try:
                    xSlider[i] = "&"
                except: pass
        
        #displaying
        print(len(self.mtx),len(self.mtx[0]))
        print(self.sizey,self.sizex)
        print(self.scopex,self.scopey)
        print(f'    {" "*yMaxNotLength}',end="")
        for i in xSlider:
            print(f'{i} ',end="")
        print()
        for i,row in enumerate(self.mtx):
            print(f'{yNotation[i]} | ',end=" ")
            for j,el in enumerate(row):
                if el:
                    print("#",end=" ")
                else:
                    print(".",end=" ")
            print(f' {ySlider[i]}')
        print(f'    {" "*yMaxNotLength}',end="")
        print(f'{"- "*self.sizex}')
        for i,row in enumerate(xNotation):
            print(f'    {" "*yMaxNotLength}',end="")
            for j,el in enumerate(row):
                print(el,end=' ')
            print()

    def Move(self,dir):
        print(self.scopex,self.scopey)
        moveMultiplier = 1
        movexAmount = int(math.floor((self.scopex[1] - self.scopex[0] +1 ) / (self.sizex -1)))
        moveyAmount = int(math.floor((self.scopey[1] - self.scopey[0] +1 ) / (self.sizey -1)))
        match dir:
            case 'w':
                self.scopey[0] += moveyAmount*moveMultiplier
                self.scopey[1] += moveyAmount*moveMultiplier
            case 's':
                self.scopey[0] -= moveyAmount*moveMultiplier
                self.scopey[1] -= moveyAmount*moveMultiplier
            case 'd':
                self.scopex[0] += movexAmount*moveMultiplier
                self.scopex[1] += movexAmount*moveMultiplier
            case 'a':
                self.scopex[0] -= movexAmount*moveMultiplier
                self.scopex[1] -= movexAmount*moveMultiplier
        print(self.scopex,self.scopey)
    
    def Size(self,dir):
        print("sizeing")
        zoomMultiplier = 1
        zoomyAmount = int(((self.scopey[1] - self.scopey[0] +1 ) / (self.sizey -1))//2)     #doesnt work :(
        print(self.scopex,self.scopey)
        match dir:
            case 't':
                prevScope = [self.scopey[i] for i in range(2)]      #it is necessary to 'copy' the list this way
                self.scopey[0] += zoomyAmount*zoomMultiplier
                self.scopey[1] -= zoomyAmount*zoomMultiplier
                scopeWidth = self.scopey[1] - self.scopey[0]
                if scopeWidth < self.sizey:                         #if not allowed ==> snapping scope to screen
                    self.scopey[0] = prevScope[0]
                    self.scopey[1] = prevScope[0] + self.sizey-1
                    print('[LOG] max Y zoom reached')
            case 'g':
                self.scopey[0] -= 1*zoomMultiplier
                self.scopey[1] += 1*zoomMultiplier                
                #if self.scopey[1] - self.scopey[0] > self.sortedY[-1] - self.sortedY[0]:
                #    self.scopey[0] += 1*zoomMultiplier
                #    self.scopey[1] -= 1*zoomMultiplier 
                #    print('[LOG] min Y zoom reached')
            case 'h':
                self.scopex[0] += 1*zoomMultiplier
                self.scopex[1] -= 1*zoomMultiplier
                if self.scopex[0] >= self.scopex[1]:
                    self.scopex[0] -= 1*zoomMultiplier
                    self.scopex[1] += 1*zoomMultiplier
                    print('[LOG] max X zoom reached')
            case 'f':
                self.scopex[0] -= 1*zoomMultiplier
                self.scopex[1] += 1*zoomMultiplier
                if self.scopex[1] - self.scopex[0] > self.sortedX[-1] - self.sortedX[0]:
                    self.scopex[0] += 1*zoomMultiplier
                    self.scopex[1] -= 1*zoomMultiplier
                    print('[LOG] min X zoom reached')
            #case 'g':
            #    
            #case 't':
                
        print(self.scopex,self.scopey)

if __name__ == "__main__":
    #datax = [0,0,1,2,3,4,5,6,7,8,9]
    #datay = [-1,0,-5,3,4,5,-6,2,-1,4,7]
    #datax = [0,0,0,0,1,2,3,4,4,4,4,4]
    #datay = [0,1,2,3,3,3,3,3,2,1,0,-1]

    datax = [17, 18, 19, 20, 21, 22, 23, 24, 25, 15, 16, 17, 25, 26, 27, 28, 14, 15, 28, 29, 30, 31, 32, 14, 32, 33, 34, 13, 14, 34, 35, 36, 12, 13, 36, 37, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 11, 12, 37, 38, 157, 158, 159, 170, 171, 172, 173, 10, 11, 39, 155, 156, 157, 173, 174, 9, 10, 40, 154, 155, 174, 175, 8, 9, 40, 41, 153, 154, 175, 176, 7, 8, 41, 42, 152, 153, 176, 7, 42, 151, 152, 177, 196, 197, 198, 199, 6, 7, 42, 43, 151, 177, 178, 196, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 6, 43, 150, 151, 178, 196, 208, 5, 6, 43, 44, 150, 179, 196, 208, 5, 44, 149, 150, 179, 195, 196, 208, 4, 5, 44, 45, 149, 179, 180, 195, 208, 4, 45, 148, 149, 180, 195, 208, 3, 4, 45, 148, 180, 181, 195, 208, 2, 3, 46, 147, 148, 181, 195, 208, 2, 46, 147, 181, 195, 208, 209, 1, 2, 46, 47, 146, 147, 181, 182, 195, 209, 1, 47, 146, 182, 195, 209, 0, 1, 47, 145, 146, 182, 183, 195, 209, 0, 47, 48, 145, 183, 195, 209, 0, 48, 145, 183, 195, 209, 48, 145, 184, 195, 209, 48, 49, 144, 145, 184, 195, 49, 144, 185, 195, 49, 50, 144, 185, 186, 195, 50, 143, 144, 186, 195, 196, 50, 51, 95, 96, 97, 98, 99, 100, 101, 102, 103, 143, 186, 187, 196, 51, 92, 93, 94, 95, 103, 104, 105, 106, 143, 187, 196, 51, 90, 91, 92, 106, 107, 108, 142, 143, 187, 188, 196, 51, 52, 89, 90, 109, 110, 141, 142, 188, 196, 52, 88, 89, 110, 111, 112, 141, 189, 196, 52, 53, 86, 87, 88, 112, 113, 114, 140, 141, 189, 190, 196, 53, 84, 85, 86, 114, 115, 116, 139, 140, 190, 191, 196, 53, 54, 82, 83, 84, 116, 117, 118, 119, 137, 138, 139, 191, 192, 196, 54, 55, 81, 82, 119, 120, 121, 122, 123, 124, 135, 136, 137, 192, 193, 196, 55, 79, 80, 81, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 193, 194, 195, 196, 55, 56, 78, 79, 194, 195, 56, 57, 76, 77, 78, 57, 58, 74, 75, 76, 58, 59, 71, 72, 73, 74, 59, 60, 61, 68, 69, 70, 71, 61, 62, 63, 64, 65, 66, 67, 68]
    datay = [49, 49, 49, 49, 49, 49, 49, 49, 49, 48, 48, 48, 48, 48, 48, 48, 47, 47, 47, 47, 47, 47, 47, 46, 46, 46, 46, 45, 45, 45, 45, 45, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 42, 42, 42, 42, 42, 42, 42, 42, 41, 41, 41, 41, 41, 41, 41, 40, 40, 40, 40, 40, 40, 40, 40, 39, 39, 39, 39, 39, 39, 39, 38, 38, 38, 38, 38, 38, 38, 38, 38, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 36, 36, 36, 36, 36, 36, 36, 35, 35, 35, 35, 35, 35, 35, 35, 34, 34, 34, 34, 34, 34, 34, 34, 33, 33, 33, 33, 33, 33, 33, 33, 33, 32, 32, 32, 32, 32, 32, 32, 31, 31, 31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 30, 30, 30, 29, 29, 29, 29, 29, 29, 29, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 27, 27, 27, 27, 27, 27, 26, 26, 26, 26, 26, 26, 26, 26, 26, 25, 25, 25, 25, 25, 25, 25, 24, 24, 24, 24, 24, 24, 23, 23, 23, 23, 23, 22, 22, 22, 22, 22, 22, 21, 21, 21, 21, 20, 20, 20, 20, 20, 20, 19, 19, 19, 19, 19, 19, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3]

    p = Plotter(11,11)
    p.DataIn(datax,datay)
    p.plot()
    while True:
        command = input(": ")
        p.Move(command)
        p.Size(command)
        p.plot()
        