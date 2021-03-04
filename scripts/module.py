import os
import sys
import subprocess

def pdb_xyz(file):
    f=open(file,'r')
    list1=f.readlines()
    f.close()
    d={}
    id=0
    for line in list1:
        if len(line.strip().split())==0:
            continue
        if "TER" in line.split()[0]:
            break
        if 'ATOM' in line.split()[0]: #use HETATM only when required
            #print line
            x,y,z=line.strip().split()[6:9]
            s=line.strip().split()[-1]
            d[id]=[s,x,y,z]
            id+=1
    g=open(file.split('.')[0]+'.xyz','w')
    for i in range (len(d)):
        g.write('  '.join(d[i])+'\n')
    g.close()

def make_fchk(path,sym):
    f=open(path,'r')
    lines=f.readlines()
    f.close()
    s,cord=[],[]
    ref=0
    for line in lines:
        if 'Number of symbols in /Mol/' in line:
            break
        if len(line.strip().split())==0:
            continue
        if 'Nuclear charges' in line:
            ref=1
        if ref==1 or ref==2:
            ref+=1
        if ref==3:
            lis=[i.split('.')[0] for i in line.strip().split()]
            s+=lis 
        if 'Current cartesian coordinates' in line:
            ref+=1
        if ref==4 or ref==5:
            ref+=1
        if ref==6:
            lis=[str((float(i.split('E')[0])*(10**int(i.split('E')[1])))*0.529177) for i in line.strip().split()]
            cord+=lis
        
    cords=[]
    i,ref=0,0
    g=open(path[:-5]+'.xyz','w')
    while i < (len(cord)):
        g.write(sym[s[ref]]+' '+' '.join(cord[i:i+3])+'\n')
        i+=3
        ref+=1
    g.close()

def make_out(path,sym):
    data = subprocess.check_output('gcartesian '+path, shell=True)
    g=open(path[:-4]+'.xyz','w')
    ref=0
    for i in data.split('\n'):
        if ref==1 and len(i.strip().split())==4:
            li=i.strip().split()
            try:
                int(li[0])
                g.write(sym[li[0]]+' '+' '.join(li[1:])+'\n')
            except KeyError:
                g.write(' '.join(li)+'\n')
        try:
            if len(i.strip().split())>0:
                int(i.strip().split()[0])
                if len(i.strip().split())==2:
                    ref=1
        except ValueError:
            pass
        #g.write(data)
    g.close()

def filter_xyz(path,suf):
    path=path[:-suf]+'.xyz'
    f=open(path,'r')
    lines=f.readlines()
    f.close()

    g=open(path,'w')
    index=0
    for line in lines:
        if len(line.strip().split())==4:
            index+=1

    g.write(str(index)+'\n')
    g.write('comment\n')
    g.write(''.join(lines))
    g.close()

def get_inp():
    tp = open(os.path.join(os.path.split(sys.argv[0])[0], 'main_input'))
    lines = tp.readlines()
    tp.close()

    dic={}
    for line in lines:
        if '#' in line or len(line.strip().split())==0:
            continue
        a,b=line.strip().split()
        dic[a]=b 
    return dic

def make_xyz(path):
    inp_d = get_inp()
    if os.system(inp_d['babel_path']+' '+path+' '+path.split('.')[0]+'.xyz')==0:
        return 0
    sym={'15':'P','14':'Si','1':'H','7':'N','8':'O','6':'C','53':'I','36':'Kr','9':'F','16':'S'}
    if path.split('.')[-1]=='fchk':
        make_fchk(path,sym)
        filter_xyz(path,5)
        return 2
    elif path.split('.')[-1]=='out':
        make_out(path,sym)
        filter_xyz(path,4)
        return 3
    elif path.split('.')[-1]=='pdb':
        pdb_xyz(path)
        filter_xyz(path,4)
        return 4
    elif path.split('.')[-1]=='xyz':
        return 5
    else:
        raise Exception('File extension unknown!')
    return 1

def get_ids(path):
    f=open(path,'r')
    lines=f.readlines()
    f.close()
    ref=0
    st=''
    for line in lines:
        if ref==5:
            break
        if 'File format' in line:
            ref=1
        if len(line.strip().split())==0 and ref>0:
            ref+=1
        if ref==2 or ref==3:
            ref+=1
        if ref==4:
            s,e=line.index('('),line.index(')')
            l=line[s+1:e].split(',')
            st+=l[0].strip()+' '+l[1].strip()+' 0 0 : '+line[e+1:].split()[0]+'\n'
    return st


def make_lmode(path):
    #print 'performing step 1 ...'
    ids=get_ids('output.txt')
    filename=path.split('/')[-1].split('.')[0]
    s1="""
 $Contrl QCProg="gaussian"
   iprint=0
   isymm = 1
 $end

$qcdata
 """
    s2='fchk="'+filename+'.fchk"'
    s3="""$end

$LocMod $End
"""
    s4=ids
    f=open(filename+'.alm','w')
    f.write(filename+'\n')
    f.write(s1)
    f.write(' '+s2+'\n')
    f.write(s3)
    f.write(s4+'\n')
    f.close()

    os.system("/Users/47510753/Downloads/LocalMode-2016/lmodes.exe -b "+'< '+filename+'.alm' +' >'+' '+filename+'.out')



            


