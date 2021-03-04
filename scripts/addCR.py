import numpy as np
import scipy.spatial as spatial
import time
import math
from math import log10, floor
from scipy import interpolate
import os
import sys
#import xlrd
#from xlutils.copy import copy as xl_copy

def distance(a,b):
    a = list(map(float, a))
    b = list(map(float, b))
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)

def round_sig(x, sig=5):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def chain(r,st):
    l=len(r)
    l_=st[l:]
    if len(l_)==0 or l_.isdigit() or l_ == 'A':
        chain='backbone'
    else:
        chain='side_chain' 
    return chain

def get_backbone(d):
    li = []
    for i in d:
        if d[i][3] == 'backbone':# and self.d[i][2]!='H':
            li.append(i)
    #print li
    return li

def cartoon(point, li0, d, n = 2):
    #print self.get_backbone()
    if d[point][3] != 'backbone':
        return -2 
    
    ind = li0.index(point)
    fli = []

    count = 0
    c1, c2 = 0, 0
    while len(fli) < n+1:
        if d[li0[ind+count]][2] == 'C':
            fli.append(li0[ind+count])
        count += 1
        if ind+count >= len(li0): 
            break
    c1 = count

    count = 1
    while len(fli) < 2*n+1:
        d[li0[ind-count]][2]
        if d[li0[ind-count]][2] == 'C':
            fli.append(li0[ind-count])
        count+=1
        if ind-count <= 0:
            c2 = 2*n+1 - len(fli)
            break

    if c2:
        count = c1
        while len(fli) < 2*n+1:
            if d[li0[ind+count]][2] == 'C':
                fli.append(li0[ind+count])
            count += 1
            if ind+count >= len(li0):
                break

    fli.sort()
    #print fli
    coord = [list(map(float,d[i][-3:])) for i in fli]
    coord = np.array(coord)
    x,y,z = coord[:,0],coord[:,1],coord[:,2]
    try:
        tck, u = interpolate.splprep([x,y,z], s=3)
    except ValueError:
        return None
    x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
    u_fine = np.linspace(0,1,len(coord)*10)

    x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

    coord_fine = []

    for i in range (len(x_fine)):
        coord_fine.append([x_fine[i],y_fine[i],z_fine[i]])

    coord_fine = np.array(coord_fine)

    dis = 0
    for i in range (1,len(coord_fine)-1):
        #print self.d[fli[i]][-3:],self.d[fli[i-1]][-3:]
        dis += distance(coord_fine[i],coord_fine[i-1])

    #print dis, distance(d[fli[0]][-3:], d[fli[-1]][-3:])

    res = dis/distance(d[fli[0]][-3:], d[fli[-1]][-3:])

    return res

def read_pdb(filename):
    f = open(filename+'.pdb', 'r')
    list1 = f.readlines()
    f.close()

    f = open(filename+'.xyz', 'r')
    list2 = f.readlines()[2:]
    f.close()

    count = 0
    d = {}
    for line in list1:
        if "ENDMDL" in line.split()[0]:
            break
        if line.split()[0] in ['ATOM', 'HETATM']:
            #print line
            id,at,rt,_,_0,x,y,z=line.strip().split()[1:9]
            s=line.strip().split()[-1]
            try:
                float(s)
                if at[:2] in ['Cl', 'Br', 'Li', 'Be', 'Si']:
                    s = at[:2]
                else:
                    s = at[0]
            except ValueError:
                pass
            x,y,z = list2[count].strip().split()[1:]
            d[count]=[at,rt,s,chain(s,at),_0, x, y, z]
            count+=1
    return d 

def func(filename,d,p_id):
        
        file =open(filename+'.xyz','r')
        lines=file.readlines()
        file.close()

        coord_xyz = []
        for li in lines[2:]:
            if len(li.strip().split()) < 4:
                break
            coord_xyz.append(list(map(float,li.strip().split()[1:])))

        ref=0
        lis=[]
        index=0
        pdb_d = read_pdb(filename) 
        li0 = get_backbone(pdb_d)

        coord = [pdb_d[i][-3:] for i in range (len(pdb_d))]
        point_tree = spatial.cKDTree(coord)

        #print len(coord), len(coord_xyz)

        for id in p_id:
                #print lis[id],id
                a,b,c = list(map(int,p_id[id]))
                #closest_point_in_pdb = (point_tree.query_ball_point(coord_xyz[a-1], 5))
                #print coord[closest_point_in_pdb[163]]
                #li = [[distance(coord_xyz[a-1], coord[i]), i] for i in closest_point_in_pdb]
                #li.sort()
                point = a-1#li[0][1]
                #print 'Distance for', a,'is:', distance(coord_xyz[a-1], coord[point])
                ra = cartoon(point, li0, pdb_d)
                
                #closest_point_in_pdb = (point_tree.query_ball_point(coord_xyz[c-1], 5))
                #print coord[closest_point_in_pdb[163]]
                #li = [[distance(coord_xyz[c-1], coord[i]), i] for i in closest_point_in_pdb]
                #li.sort()
                point = c-1#li[0][1]
                #print 'Distance for', c,'is:', distance(coord_xyz[c-1], coord[point])
                rd = cartoon(point, li0, pdb_d)

                if ra is None:
                    ra = -1
                if rd is None:
                    rd = -1

                ra = str(round_sig(ra, 3))
                rd = str(round_sig(rd, 3))

                #print angle(data[a-1],data[b-1],data[c-1])
                d[str(id)]= "{:>6} {:>6}".format(*[ra ,rd])

def get_ids(path,suffix='_ah'):
        f=open(path,'r')
        lines=f.readlines()
        f.close()
        i=-1
        i2=0
        ref=0
        lm={}
        length=0
        for line in lines:
                i+=1
                if ref==5:
                        break
                if 'File format' in line:
                        ref+=1
                if len(line.strip().split())==0 and ref>0:
                        ref+=1
                if ref==2:
                        lines[i-1]=' '.join(lines[i-1].strip().split())+', HB Angle \n'
                if ref==2 or ref==3:
                        ref+=1
                if ref==4:
                        s,e=line.index('('),line.index(')')
                        n1=line.strip().split()[line.strip().split().index('(')-1]
                        l=line[s+1:e].split(',')
                        k = line.strip().split()[2]
                        try:
                            int(k)
                        except ValueError:
                            k = line[44:51].strip()
                        st=[l[0].strip(),l[1].strip(),k]
                        #print st
                        if i2==0:
                                length=len(line)
                        lm[str(i2+1)+'.']=st
                        #lines[i]=lines[i].strip()+' '+lmodes[i2]+'\n'
                        i2+=1
        return lm

def addCR(path,p_id):
        f=open(path,'r')
        lines=f.readlines()
        f.close()
        i=-1
        i2=0
        ref=0
        lm={}
        length=0
        for line in lines:
                i+=1
                if ref==5:
                        break
                if 'File format' in line:
                        ref+=1
                if len(line.strip().split())==0 and ref>0:
                        ref+=1
                if ref==2:
                        lines[i-1]=' '.join(lines[i-1].strip().split())+', AcceptorCurvatureRatio, DonarCurvatureRatio \n'
                if ref==2 or ref==3:
                        ref+=1
                if ref==4:
                        if i2==0:
                                if length<len(line):
                                        length=len(line)
                        st0 = p_id[str(i2+1)+'.']
                        if len(st0) < 6:
                            st0 = st0 + (6-len(st0))*'0'
                        lm[str(i2+1)+'.']=st0
                        i2+=1
        j=0
        length+=1
        for line in lines:
                if len(line.strip().split())==0:
                        j+=1
                        continue
                if line.strip().split()[0] in lm:
                        string=lm[line.strip().split()[0]]
                        lines[j]=lines[j][:-1]+' '*(length-len(lines[j])+2)+string+'\n' 
                j+=1
        g=open(path,'w')
        g.write(''.join(lines))
        g.close()
        return lm 

def job(path): # give xyz
        ref=0
        d={}
        n=0
        
        filename=path.split('/')[-1].split('.')[0]
        
        p_id=get_ids(filename+'.txt','_ah')  
        #print p_id   
        func(filename,d,p_id)    
        
        return addCR(filename+'.txt',d)

if __name__=='__main__':
        job(sys.argv[1])






