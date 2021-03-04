#!/usr/bin/python
import xlwt
import module
import sys
import numpy as np
from math import log10, floor
#import xlrd
#from xlutils.copy import copy as xl_copy

#metals=['Co','Rh','Ni','Pd','Pt','Ir','I']


def func(filename,d,p_id):

        li = np.array([list(map(int, p_id[i])) for i in p_id])
        a, h, do = li[:,0], li[:,1], li[:,2]
        
        d_a = dict(zip(*np.unique(a, return_counts=True)))
        d_h = dict(zip(*np.unique(h, return_counts=True)))

        #print d_a, d_h, d_do
        
        for id in p_id:
                #print p_id[id],id
                a1,b1,c1 = list(map(int,p_id[id]))
                
                #print angle(data[a-1],data[b-1],data[c-1])
                if c1 in d_a:
                    #print a1, b1, c1, d_a[a1], d_h[b1], d_a[c1]
                    d[str(id)]=str(d_a[a1]-1)+'-'+str(d_h[b1]-1)+'-'+str(d_a[c1])
                else:
                    #print a1, b1, c1, d_a[a1], d_h[b1]
                    d[str(id)]=str(d_a[a1]-1)+'-'+str(d_h[b1]-1)+'-0'

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

def addBifr(path,p_id):
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
                        lines[i-1]=' '.join(lines[i-1].strip().split())+', HB Bifr \n'
                if ref==2 or ref==3:
                        ref+=1
                if ref==4:
                        if i2==0:
                                if length<len(line):
                                        length=len(line)
                        st0 = p_id[str(i2+1)+'.']
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
        
        return addBifr(filename+'.txt',d)

if __name__=='__main__':
        print (job(sys.argv[1]))







