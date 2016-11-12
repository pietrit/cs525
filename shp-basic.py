import matplotlib.pylab as plt

class SH:
    def __init__(self,tourname,graphname):
        self.tname=tourname
        self.gname=graphname
        self.tour=self.readTour()
        (self.graph,self.order)=self.readGraph()
        self.count=len(self.order)
        self.dis=self.countDis()

    def readTour(self):
        f=open(self.tname,'r')
        bList=[]
        for line in f:
            aList=line.split(';')
            for i in range(0,len(aList)):
                aList[i]=aList[i].rstrip('\n')
            bList.append(aList)
        f.close()
        return bList

#return a list of valid path(only one direction recorded)
#and a list of city name
    def readGraph(self):
        f=open(self.gname,'r')
        validroad=[]
        city=f.readline()
        cityorder=city.split(';')
        cityorder[len(cityorder)-1]=cityorder[len(cityorder)-1].rstrip('\n')
        del cityorder[0]
        for line in f:
            bList=[]
            aList=line.split(';')
            for i in range(0,len(aList)):
                aList[i]=aList[i].rstrip('\n')
                if aList[i]=='1':
                    bList.append(i-1)
            validroad.append(bList)
        f.close()
        return (validroad,cityorder)

#get the coordinates of a city, return a list[x,y]
    def coordinates(self,cityNum):
        co=[]
        co.append(int(self.tour[cityNum][1]))
        co.append(int(self.tour[cityNum][2]))
        return co

#get the (order)Number of a city
    def getCityNum(self,city):
        for i in range(0,self.count):
            if city.upper()==self.order[i].upper():
                return i

    def drawRoads(self):
        for i in range(0,len(self.graph)):
            for j in self.graph[i]:
                c1=self.coordinates(i)
                c2=self.coordinates(j)
                plt.plot(c1[0],c1[1],'or')
                plt.plot(c2[0],c2[1],'or')       
                plt.plot((c1[0],c2[0]),(c1[1],c2[1]),'k--')

#draw the shortest path between two cities
    def drawPath(self,start,end,path):
        x=[]
        y=[]
        while end!=start:
            x.append(self.coordinates(end)[0])
            y.append(self.coordinates(end)[1])
            end=path[end]
        x.append(self.coordinates(start)[0])
        y.append(self.coordinates(start)[1])
        plt.plot(x,y,'blue',linewidth=2)

#print the shortest path between two cities             
    def printPath(self,start,end,path):
        p=[]
        d=[]
        s=''
        while end!=start:
            last=path[end]
            d.append(self.dis[end][last])
            p.append(self.order[end])
            end=last
        p.append(self.order[start])
        for i in range(0,len(p)-1):
            s+=p[len(p)-i-1]+'--'+str(d[len(d)-i-1])+'-->'
        s+=p[0]
        print(s)
        
#use dictionary to store valid distance(both direction)
    def countDis(self):
        disAll={}
        for i in range(0,self.count):
            disRow={}
            disAll[i]=disRow
            for j in self.graph[i]:
                c1=self.coordinates(i)
                c2=self.coordinates(j)
                dis=((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)**(1/2)
                disRow[j]=dis
                disAll[j][i]=dis
                disAll[i]=disRow
        return disAll

#parameters: (dictionary)valid distance, starting city,
#number of cities and the not valid distance(just for easier generalization)
    def Dijkstra(self,graph,start,n,notValid=1000):
        Seen=set()
        Unseen=set(range(0,n))
        sh=[notValid]*n#list of shortest distance
        prev=[0]*n#list of previous city
        sh[start]=0#initialize
        prev[start]=start
        Seen.add(start)
        Unseen.remove(start)
        minv=0
        middle=start#take the start point as the middle point
        try:
            while len(Unseen)!=0:
                tmp=notValid
                for i in Unseen:
                    if i in graph[middle].keys():
                        if minv+graph[middle][i]<sh[i]:#update the distances
                            sh[i]=minv+graph[middle][i]
                            prev[i]=middle
                    if sh[i]<tmp:#find the next shortest path
                        tmp=sh[i]
                        k=i
                Seen.add(k)
                Unseen.remove(k)
                middle=k
                minv=tmp
            return[sh,prev]
        except Exception as ex:
            print(ex)

#just for a simple test
    def test(self):
        graph={0:{1:6,2:3},
               1:{0:6,2:2,3:5},
               2:{0:3,1:2,3:3,4:4},
               3:{1:5,2:3,4:2,5:3},
               4:{2:4,3:2,5:5},
               5:{3:3,4:5}}
        result=self.Dijkstra(graph,0,6)

#interactive with user
    def typeIn(self):
        try:
            s=''
            s=input('Start from:')
            while s!='e':
                start=self.getCityNum(s)
                if start!=None:
                    break
                else:
                    s=input('Please type in the prper city name:')
            s=input('To:')
            while s!='e':
                end=self.getCityNum(s)
                if end!=None:
                    return (start,end)
                else:
                    s=input('Please type in the prper city name:')
        except Exception as ex:
            print(ex)

    def main(self):
        notValid=1000
        print(self.order)
        (start,end)=self.typeIn()
        result=self.Dijkstra(self.dis,start,self.count,notValid)
        self.drawRoads()
        if result[0][end]<notValid:
            self.drawPath(start,end,result[1])
            self.printPath(start,end,result[1])
            print('The shortest distance is: ',result[0][end])
        else:
            print('No such path exists.')
        plt.show()
        
     
if __name__ == "__main__":
    sh=SH('tour26.csv','graph26.csv')
    sh.main()



