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

    def plot(self):
        for i in range(self.scopey[0],self.scopey[1]):
            for j,n in enumerate(self.y):
                if i == n:
                    self.mtx[i][j]
             
        self.printMtx()

    def printMtx(self):
        for i,row in enumerate(self.mtx):
            for j,el in enumerate(row):
                print(el,end=" ")
            print()

if __name__ == "__main__":
    datax = [0,1,2,3,4,5,6,7,8,9]
    datay = [0,1,3,4,5,6,2,1,4,7]

    p = Plotter(40,8)
    p.DataIn(datax,datay)
    p.plot()