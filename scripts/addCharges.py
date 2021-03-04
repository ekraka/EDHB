#!/usr/bin/python
import xlwt
import module
import sys
#import xlrd
#from xlutils.copy import copy as xl_copy

#metals=['Co','Rh','Ni','Pd','Pt','Ir','I']

def func(filename,d):
        
        file =open(filename,'r')
        lines=file.readlines()
        file.close()
        ref=0
        lis=[]
        for line in lines:

                if ref==1: 
                        if len(line.strip().split())==0:
                                break
                        try:
                                float(line.strip().split()[0])
                        except ValueError:
                                break
                if ref==1:
                        lis+=line.strip().split()
                if 'Mulliken Charges' in line:
                        ref=1
        for id in range (len(lis)):
                d[str(id+1)]=str(float(lis[id]))

def get_ids(path,suffix,d):
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
                        lines[i-1]=' '.join(lines[i-1].strip().split())+', DensityCriticalPointAcceptor \n'
                if ref==2 or ref==3:
                        ref+=1
                if ref==4:
                        s,e=line.index('('),line.index(')')
                        n1=line.strip().split()[line.strip().split().index('(')-1]
                        l=line[s+1:e].split(',')
                        st=[d[l[0].strip()],d[l[1].strip()]]

                        if i2==0:
                                length=len(line)
                        lm[str(i2+1)+'.']=st
                        #lines[i]=lines[i].strip()+' '+lmodes[i2]+'\n'
                        i2+=1
        return lm 

def addC(path,p_id):
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
                        lines[i-1]=' '.join(lines[i-1].strip().split())+', AcceptorCharge, H_Charge \n'
                if ref==2 or ref==3:
                        ref+=1
                if ref==4:
                        if i2==0:
                                if length<len(line):
                                        length=len(line)
                        try:
                                float(p_id[str(i2+1)+'.'][0])
                                lm[str(i2+1)+'.']="{:>15} {:>15}".format(*p_id[str(i2+1)+'.'])
                        except ValueError:
                                lm[str(i2+1)+'.']='None'
                        #lines[i]=lines[i].strip()+' '+lmodes[i2]+'\n'
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


def job(path): # give fchk 
        ref=0
        d={}
        n=0
        
        filename=path.split('/')[-1].split('.')[0]
        func(path,d)
        p_id=get_ids(filename+'.txt','_ah',d)     
        #print p_id	
        return addC(filename+'.txt',p_id)

if __name__=='__main__':
        job(sys.argv[1])






