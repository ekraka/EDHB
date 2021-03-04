import numpy as np
import scipy.spatial as spatial
import time
import math
from math import log10, floor
import os
import sys
from math import log10, floor

class connections:

    def __init__(self,file):
            self.d=self.data_extraction(file)
            

            self.arr=[self.d[i][1:] for i in self.d]
            self.point_tree = spatial.cKDTree(self.arr)

            ref=0
            atom_d={}
            for i in self.d:
                    atom_d[ref]=self.d[i][0]
                    ref+=1

            self.atom_d=atom_d

    def data_extraction(self,path1):
        d={}
        f=open(path1,'r')
        lines=f.readlines()
        f.close()
        ref=1
        for i in lines[2:]:
            if len(i.strip().split())==1:
                            break
            if len(i.strip().split())==0:
                continue
            a,x,y,z=i.strip().split()
            d[ref]=[a]+list(map(float,[x,y,z]))
            ref+=1

        return d

    class Queue:
        def __init__(self):
            self.list = []
        def push(self,item):
            self.list.insert(0,item)
        def pop(self):
            return self.list.pop()
        def isEmpty(self):
            return len(self.list) == 0

    class Stack:
         def __init__(self):
             self.items = []

         def isEmpty(self):
             return self.items == []

         def push(self, item):
             self.items.append(item)

         def pop(self):
             return self.items.pop()

         def peek(self):
             return self.items[len(self.items)-1]

         def size(self):
             return len(self.items)

    def next_state(self,cstate):
            ma = 1.6
            li1=(self.point_tree.query_ball_point(self.d[cstate+1][1:], ma))
            return li1 

    def bfs(self,cstate,goal):
        path=[]
        item=[cstate,path]
        vs=set()
        f=self.Queue()
        ref=0
        vs.add(cstate)
        while True:
            #print cstate
            [cstate,path]=item
            nstate=self.next_state(cstate)
            #print nstate
            for i in nstate:
                    if cstate==goal and len(path) > 2:
                            return list(map(lambda x: x+1,path+[cstate]))
                    f.push([i,path+[cstate]])
            while True:
                if f.isEmpty():
                    return []
                item=f.pop()
                if item[0] not in vs:
                    break
            cstate=item[0]
            vs.add(item[0])
            ref+=1
            #print path,cstate
        return []

    def round_sig(self,x, sig=3):
            if x == 0.0:
                    return 0.0
            return round(x, sig-int(floor(log10(abs(x))))-1)

    def dihedral(self,lis):
        """formula from Wikipedia article on "Dihedral angle"; formula was removed
        from the most recent version of article (no idea why, the article is a
        mess at the moment) but the formula can be found in at this permalink to
        an old version of the article:
        https://en.wikipedia.org/w/index.php?title=Dihedral_angle&oldid=689165217#Angle_between_three_vectors
        uses 1 sqrt, 3 cross products"""
        p=np.array([self.d[i][1:] for i in lis])

        p0 = p[0]
        p1 = p[1]
        p2 = p[2]
        p3 = p[3]

        b0 = -1.0*(p1 - p0)
        b1 = p2 - p1
        b2 = p3 - p2

        b0xb1 = np.cross(b0, b1)
        b1xb2 = np.cross(b2, b1)
        
        b0xb1_x_b1xb2 = np.cross(b0xb1, b1xb2)
        

        y = np.dot(b0xb1_x_b1xb2, b1)*(1.0/np.linalg.norm(b1))
        x = np.dot(b0xb1, b1xb2)
        return self.round_sig(np.degrees(np.arctan2(y, x)))

    def distance(self,a,b):
            x1,y1,z1=self.d[a][1:]
            x2,y2,z2=self.d[b][1:]
            return self.round_sig(math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2),4)

    def atom_name(self,a):
            return self.d[a][0]


if __name__=='__main__':
	con=connections(sys.argv[1])

	lis = con.bfs(3,29)
	print (lis)
	#print con.dihedral(lis) 

















