import module
import sys
import numpy as np

def get_backbone(d):
    li = []
    for i in d:
        if d[i][3] == 'backbone':# and self.d[i][2]!='H':
            li.append(i)
    return li 

def cartoon(d, point, n = 2):
    #print self.get_backbone()
    if d[point][3] != 'backbone':
        return None 
    
    li0 = get_backbone()
    ind = li0.index(point)
    fli = []

    count = 0
    while len(fli) < n+1:
        if d[li0[ind+count]][2] == 'C':
            fli.append(li0[ind+count])
        count += 1
        if ind+count > len(li0):
            break

    count = 1
    while len(fli) < 2*n+1:
        if d[li0[ind-count]][2] == 'C':
            fli.append(li0[ind-count])
        count+=1
        if ind-count == 0:
            break

    fli.sort()
    coord = [map(float,d[i][-3:]) for i in fli]
    coord = np.array(coord)
    x,y,z = coord[:,0],coord[:,1],coord[:,2]
    tck, u = interpolate.splprep([x,y,z], s=3)
    x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
    u_fine = np.linspace(0,1,len(coord)*10)

    x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

    coord_fine = []

    for i in range (len(x_fine)):
        coord_fine.append([x_fine[i],y_fine[i],z_fine[i]])

    coord_fine = np.array(coord_fine)

    '''
    fig2 = plt.figure(2)
    ax3d = fig2.add_subplot(111, projection='3d')
    ax3d.plot(x, y, z, 'r*')
    #ax3d.plot(x_knots, y_knots, z_knots, 'go')
    ax3d.plot(x_fine, y_fine, z_fine, 'g-')

    fig2.show()
    plt.show()
    '''

    #print fli
    #self.check_cartoon(fli)

    dis = 0
    for i in range (1,len(coord_fine)-1):
        #print self.d[fli[i]][-3:],self.d[fli[i-1]][-3:]
        dis += distance(coord_fine[i],coord_fine[i-1])

    print dis, distance(d[fli[0]][-3:], d[fli[-1]][-3:])

    res = dis/distance(d[fli[0]][-3:], d[fli[-1]][-3:])

    return res

def chain(r,st):
    l=len(r)
    l_=st[l:]
    if len(l_)==0 or l_.isdigit() or l_ == 'A':
        chain='backbone'
    else:
        chain='side_chain' 
    return chain


def read_pdb(filename):

        file1=open(filename+'.pdb','r')
        list1=file1.readlines()
        file1.close()

        for line in list1:
            if "TER" in line.split()[0]:
                break
            if line.split()[0] in ['ATOM']:
                #print line
                id,at,rt,_,_0,x,y,z=line.strip().split()[1:9]
                s=line.strip().split()[-1]
                d[int(id)]=[at,rt,s,chain(s,at),_0,x,y,z]
        return d 

def check_cartoon(point):
    res1 = cartoon(point)
    res2 = cartoon(point, 5)

    print res1, res2

    if res1 < 1.18 and res2 < 1.2:
        return 'Beta'
    elif res1 < 1.18 and res2 > 1.2:
        return 'Coil' 
    elif res1 < 2.0 and res2 < 2.5:
        return 'Alpha'
    elif res2 > 2.5:
        return 'Sharp Turn' 

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
                        st=[l[0].strip(),l[1].strip(),line.strip().split()[2]]
                
                        if i2==0:
                                length=len(line)
                        lm[str(i2+1)+'.']=st
                        #lines[i]=lines[i].strip()+' '+lmodes[i2]+'\n'
                        i2+=1
        return lm

def addHBtype(path,p_id):
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
                        lines[i-1]=' '.join(lines[i-1].strip().split())+', HB type \n'
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

def func(filename,d,p_id):
        
        file =open(filename,'r')
        lines=file.readlines()
        file.close()
        ref=0
        lis=[]
        index=0
        data = []
        for i in range (2,len(lines)):
                data+=[map(float,lines[i].strip().split()[1:])]

        
        for id in p_id:
                #print lis[id],id
                a,b,c = map(int,p_id[id])
                #print angle(data[a-1],data[b-1],data[c-1])
                d[str(id)]=str(angle(data[a-1],data[b-1],data[c-1]))

def job(path): # give xyz
        ref=0
        d={}
        n=0
        
        filename=path.split('/')[-1].split('.')[0]
        
        p_id=get_ids(filename+'.txt','_ah')  
        #print p_id   
        func(path,d,p_id)    
        
        return addHBtype(filename+'.txt',d)

if __name__=='__main__':
        print job(sys.argv[1])





