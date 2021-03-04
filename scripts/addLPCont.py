import sys

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
                        lines[i-1]=' '.join(lines[i-1].strip().split())+', LonePairDonationToHydrogen \n'
                if ref==2 or ref==3:
                        ref+=1
                if ref==4:
                        s,e=line.index('('),line.index(')')
                        n1=line.strip().split()[line.strip().split().index('(')-1]
                        l=line[s+1:e].split(',')
                        k = line.strip().split()[2]
                        if ']' in k:
                            k = line[44:51].strip()
                        st=[l[0].strip(),l[1].strip(),k]
                        #print st
                        if i2==0:
                                length=len(line)
                        lm[str(i2+1)+'.']=st
                        #lines[i]=lines[i].strip()+' '+lmodes[i2]+'\n'
                        i2+=1
        return lm

def addLP_BD(path,p_id):
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
                        lines[i-1]=' '.join(lines[i-1].strip().split())+', LonePairToHydrogenBondEnergy \n'
                if ref==2 or ref==3:
                        ref+=1
                if ref==4:
                        if i2==0:
                                if length<len(line):
                                        length=len(line)
                        try:
                                float(p_id[str(i2+1)+'.'])
                                lm[str(i2+1)+'.']=str(float(p_id[str(i2+1)+'.']))
                        except KeyError:
                                lm[str(i2+1)+'.']=0.0
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

def job(path, filename):
        dic=get_ids(filename,suffix='_ah')
        file=path#.split('/')[-1].split('.')[0]+'.g09.out'
        f=open(file,'r')
        lines=f.readlines()
        f.close()

        ref=0
        d={}
        p_id={}
        for i in dic:
                a,b,c=dic[i]
                d[(i,a,b,c)]=0
        #print (path)#d={(200,10,9):0}#, '17.': ['182', '184', '183']
        for line in lines:
                #print line[16:20].strip()
                lis=line.strip().split()
                if len(lis)<2:
                        continue
                if 'NATURAL BOND ORBITALS' in line:
                        break
                if ref==1 and 'LP'==lis[1] and 'BD*' in line:
                        #print line,line[16:20].strip(),line[44:47].strip(),line[50:53].strip()
                        for h,i,j,k in d:
                                #print h,i,j,k
                                li=list(map(int,[i,j,k]))
                                li.sort()
                                t_li=list(map(int,[line[16:20].strip(),line[44:47].strip(),line[50:53].strip()]))
                                ac=t_li[0]
                                t_li.sort()
                                #print i,ac
                                if li==t_li and int(i)==ac:
                                        #print line,line[16:20].strip(),line[44:47].strip(),line[50:53].strip()
                                        d[(h,i,j,k)]+=float(lis[-3])

                if 'SECOND ORDER PERTURBATION THEORY ANALYSIS' in line:
                        ref=1
        if ref==0:
                raise Exception("No SECOND ORDER PERTURBATION THEORY ANALYSIS found !!")
        for tu in d:
                h=tu[0]
                p_id[h]=d[tu]
        #print p_id
        return addLP_BD(filename,p_id)


if __name__=='__main__':
    job(sys.argv[1])

