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
        self.scopex = [0,sizex]
        self.scopey = [0,sizey]

    def DataIn(self,x:list,y:list):
        self.x = x
        self.y = y
        self.sortedY,self.sortedYIndex = MergeSort(self.y,[i for i in range(len(y))])
        self.sortedX,self.sortedXIndex = MergeSort(self.x,[i for i in range(len(x))])

    def plot(self):
        #calculating visible points
        yInScope = []
        xInScope = []
        for n in range(self.scopey[0],self.scopey[1]):
            indexInSortedY = BinarySeacrh(self.sortedY,len(self.sortedY),n)
            if not indexInSortedY is None:
                yInScope.append(self.sortedYIndex[indexInSortedY])     #returns the indexes of the y values that are found in scope
        
        for n in range(self.scopex[0],self.scopex[1]):
            indexInSortedX = BinarySeacrh(self.sortedX,len(self.sortedX),n)
            if not indexInSortedX is None:
                xInScope.append(self.sortedXIndex[indexInSortedX])     #returns the indexes of the x values that are found in scope

        #print(self.scopex,self.scopey,xInScope,yInScope)    
        
        visiblePoints = []      #'points that are in scope'
        for i in xInScope:
            if i in yInScope:
                visiblePoints.append([self.x[i],self.y[i]])
        
        #settting up matrix
        #for point in visiblePoints:
        #    print(point)
        #    mtx[point[0]-self.scopey[0]]

        self.printMtx()

    def printMtx(self):
        for i,row in enumerate(self.mtx):
            for j,el in enumerate(row):
                print(el,end=" ")
            print()

if __name__ == "__main__":
    datax = [0,1,2,3,4,5,6,7,8,9]
    datay = [-1,-5,3,4,5,-6,2,-1,4,7]

    p = Plotter(40,8)
    p.DataIn(datax,datay)
    p.plot()