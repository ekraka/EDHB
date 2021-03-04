import sys
import hb_connections as hb
import os

def get_ids(path,suffix='_ah'):
        f=open(path,'r')
        lines=f.readlines()
        f.close()
        i=-1
        i2=0
        ref=0
        lm={}
        length=0
        kr_st=None
        for line in lines:
                i+=1
                if ref==5:
                        break
                if ref==1 and not kr_st:
                    kr=line.strip().split()
                    if kr[0]!='DonarSymbol':
                        kr_st=(43,67)
                    else:
                        kr_st=(11,36)
                if 'File format' in line:
                        ref+=1
                if len(line.strip().split())==0 and ref>0:
                        ref+=1
                if ref==2:
                        lines[i-1]=' '.join(lines[i-1].strip().split())+', IntramolecularRing(size) \n'
                if ref==2 or ref==3:
                        ref+=1
                if ref==4:
                        s,e=kr_st # 10,28
                        #print line[s:e]
                        l=line[s:e].split(',')
                        st=l 
                        lm[str(i2+1)+'.']=st
                        #lines[i]=lines[i].strip()+' '+lmodes[i2]+'\n'
                        i2+=1
        return lm

def addRing(path,p_id):
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
                        lines[i-1]=' '.join(lines[i-1].strip().split())+', IntramolecularRing(size) \n'
                if ref==2 or ref==3:
                        ref+=1
                if ref==4:
                        if i2==0:
                                if length<len(line):
                                        length=len(line)
                        lm[str(i2+1)+'.']=p_id[str(i2+1)+'.']
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

def job(path):
        dic=get_ids(path,suffix='_ah')
        
        p_id={}
        con=hb.connections(path[:-4]+'.xyz')
        for i in dic:
            a,b,c=dic[i]
            #print a,b,c
            refe_lis=con.bfs(int(a)-1,int(c)-1)
            if len(refe_lis)==0:
                p_id[i]='None'
            elif 0 and len(refe_lis)==4:
                # for writing dihedral in bracket for 5 memberd rings
                p_id[i]='I('+str(len(refe_lis)+1)+')'+'('+str(con.dihedral(refe_lis))+')'
            else:
                p_id[i]='I('+str(len(refe_lis)+1)+')'
            

        
        return addRing(path,p_id)

def make_input_pucker(lis,d,count):
    st0 = ''
    for i in lis:
        st0+='    '.join(list(map(str,d[i][1:])))+'\n'

    f = open('P'+str(d[lis[0]][0])+'-'+str(d[lis[0]][0])+'_'+str(count)+'.dat','w')
    f.write(st0)
    f.close()


def test(path):

        def lmode_id(path):
            f=open(path,'r')
            lines=f.readlines()
            f.close()
            i=-1
            i2=0
            ref=0
            lm={}
            length=0
            kr_st=None
            for line in lines:
                    i+=1
                    if ref==5:
                            break
                    if ref==1 and not kr_st:
                        kr=line.strip().split()
                        if kr[0]!='DonarSymbol':
                            kr_st=(43,67)
                        else:
                            kr_st=(11,36)
                    if 'File format' in line:
                            ref+=1
                    if len(line.strip().split())==0 and ref>0:
                            ref+=1
                    if ref==2:
                            lines[i-1]=' '.join(lines[i-1].strip().split())+', IntramolecularRing(size)(dihedral for C5 type) \n'
                    if ref==2 or ref==3:
                            ref+=1
                    if ref==4:
                            s,e=kr_st
                            #print line[s:e]
                            l=line.strip().split()
                            st=l[-3]
                            lm[str(i2+1)+'.']=st
                            #lines[i]=lines[i].strip()+' '+lmodes[i2]+'\n'
                            i2+=1
            return lm


        dic=get_ids(path,suffix='_ah')
        l_d=lmode_id(path)
        #print l_d
        p_id={}
        con=hb.connections(path[:-4]+'.xyz')
        st_d = {}
        count = 0
        for i in dic:
            a,b,c=dic[i]
            #print a,b,c
            a,b,c = list(map(int,[a,b,c]))
            refe_lis=con.bfs(int(a)-1,int(c)-1)
            
            dist=con.distance(int(a),int(c))
            hbl = con.distance(int(b),int(c))
            if len(refe_lis)==0:
                p_id[i]='None'
            elif len(refe_lis)==4:

                make_input_pucker(refe_lis+[b],con.d,count)
                count+=1

                p_id[i]='I('+str(len(refe_lis)+1)+')'+'('+str(con.dihedral(refe_lis))+')'
                bond = con.atom_name(int(a))+'-'+con.atom_name(int(c))
                if bond in st_d:
                    st_d[bond]+=bond+' '+str(dist)+' '+str(con.dihedral(refe_lis))+' '+l_d[i]+' '+str(hbl)+' '+str(a)+' '+str(b)+' '+str(c)+'\n'
                else:
                    st_d[bond] = bond+' '+str(dist)+' '+str(con.dihedral(refe_lis))+' '+l_d[i]+' '+str(hbl)+' '+str(a)+' '+str(b)+' '+str(c)+'\n'
            else:
                p_id[i]='I('+str(len(refe_lis)+1)+')'
            

        
        return st_d


if __name__=='__main__':

    d_c = {}
    for i in os.listdir('.'):
        if i[-4:]=='.txt':
            print (i) 
            d = test(i)
            #print d
            for i in d:
                if i in d_c:
                    d_c[i]+=d[i]
                else:
                    d_c[i]=d[i]
    for i in d_c:
        print (d_c[i]+'\n\n')
    






