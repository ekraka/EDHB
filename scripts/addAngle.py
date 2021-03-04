#!/usr/bin/python
import xlwt
import module
import sys
import numpy as np
from math import log10, floor
#import xlrd
#from xlutils.copy import copy as xl_copy

#metals=['Co','Rh','Ni','Pd','Pt','Ir','I']

def angle(a,b,c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        if round_sig(cosine_angle, 6) in [-1.0, 1.0]:
            cosine_angle = 0.99 * np.sign(cosine_angle)
        #print cosine_angle
        angle = np.arccos(cosine_angle)

        return round_sig(np.degrees(angle))

def round_sig(x, sig=5):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def func(filename,d,p_id):
        
        file =open(filename,'r')
        lines=file.readlines()
        file.close()
        ref=0
        lis=[]
        index=0
        data = []
        for i in range (2,len(lines)):
                data+=[list(map(float,lines[i].strip().split()[1:]))]

        
        for id in p_id:
                #print lis[id],id
                a,b,c = list(map(int,p_id[id]))
                #print angle(data[a-1],data[b-1],data[c-1])
                d[str(id)]=str(angle(data[a-1],data[b-1],data[c-1]))

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

def addAngle(path,p_id):
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
                        if i2==0:
                                if length<len(line):
                                        length=len(line)
                        st0 = str(float(p_id[str(i2+1)+'.']))
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
        func(path,d,p_id)    
        
        return addAngle(filename+'.txt',d)

if __name__=='__main__':
        print (job(sys.argv[1]))






